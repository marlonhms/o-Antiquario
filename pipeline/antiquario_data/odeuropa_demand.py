from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
import json
from pathlib import Path
import secrets
from typing import Any

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json
from .odeuropa_retrieval import expand_odeuropa_query, load_latest_odeuropa_retrieval_index


FORBIDDEN_EVENT_FIELDS = {
    "query",
    "normalized_query",
    "user_id",
    "session_id",
    "ip",
    "ip_address",
    "email",
    "device_id",
    "user_agent",
}


@dataclass(frozen=True)
class DemandEventResult:
    recorded: bool
    event_id: str | None
    matched_targets: int
    events_path: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "recorded": self.recorded,
            "event_id": self.event_id,
            "matched_targets": self.matched_targets,
            "events_path": self.events_path.as_posix(),
            "raw_query_stored": False,
            "personal_identifiers_stored": False,
        }


@dataclass(frozen=True)
class DemandGateResult:
    gate_id: str
    p4_items: int
    research_ready: int
    watchlist: int
    dormant: int
    output_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "p4_items": self.p4_items,
            "research_ready": self.research_ready,
            "watchlist": self.watchlist,
            "dormant": self.dormant,
            "output_directory": self.output_directory.as_posix(),
            "documents_created": 0,
            "facts_generated": False,
        }


def _load_jsonl(path: Path, *, missing_ok: bool = False) -> list[dict[str, Any]]:
    if not path.is_file():
        if missing_ok:
            return []
        raise FileNotFoundError(path)
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: JSON inválido") from error
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: registro precisa ser objeto")
            records.append(record)
    return records


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ModuleNotFoundError as error:
        raise RuntimeError("Biblioteca 'pyyaml' ausente no ambiente Python.") from error
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: raiz YAML precisa ser objeto")
    return payload


def _resolve_retrieval_directory(data_directory: Path, retrieval_directory: Path | None) -> Path:
    data_root = data_directory.resolve()
    if retrieval_directory is not None:
        resolved = retrieval_directory.resolve()
    else:
        latest = load_json(data_root / "staging" / "odeuropa" / "latest.json")
        relative = latest.get("staging_directory")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError("latest.json ODEUROPA inválido")
        resolved = (data_root / relative / "equivalence" / "retrieval").resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError("diretório de recuperação precisa permanecer dentro de data")
    return resolved


def _validate_event(event: dict[str, Any]) -> None:
    forbidden = FORBIDDEN_EVENT_FIELDS & set(event)
    if forbidden:
        raise ValueError(f"evento de demanda contém campos privados proibidos: {', '.join(sorted(forbidden))}")
    if event.get("schema_version") != 1:
        raise ValueError("evento de demanda possui schema inválido")
    event_id = event.get("event_id")
    occurred_on = event.get("occurred_on")
    language = event.get("language")
    targets = event.get("matched_target_ids")
    privacy = event.get("privacy")
    if not isinstance(event_id, str) or not event_id or not isinstance(occurred_on, str):
        raise ValueError("evento de demanda não possui identidade ou data")
    try:
        date.fromisoformat(occurred_on)
    except ValueError as error:
        raise ValueError("evento de demanda possui data inválida") from error
    if language not in {"de", "en", "fr", "it", "pt-BR"}:
        raise ValueError("evento de demanda possui idioma inválido")
    if event.get("source") != "local_companion":
        raise ValueError("evento de demanda possui origem não autorizada")
    if not isinstance(targets, list) or not targets or any(not isinstance(value, str) for value in targets):
        raise ValueError("evento de demanda não possui destinos canônicos")
    if len(set(targets)) != len(targets):
        raise ValueError("evento de demanda contém destinos duplicados")
    if not isinstance(privacy, dict) or privacy.get("raw_query_stored") is not False:
        raise ValueError("evento de demanda não comprova descarte da consulta bruta")
    if privacy.get("personal_identifiers_stored") is not False:
        raise ValueError("evento de demanda permite identificadores pessoais")


def record_anonymized_query_demand(
    data_directory: Path,
    query: str,
    *,
    language: str,
    events_path: Path | None = None,
    index_path: Path | None = None,
    occurred_on: str | None = None,
    event_id: str | None = None,
) -> DemandEventResult:
    data_directory = data_directory.resolve()
    resolved_events = (events_path or data_directory / "private" / "demand" / "olfactory-query-events.jsonl").resolve()
    if not resolved_events.is_relative_to(data_directory):
        raise ValueError("eventos de demanda precisam permanecer dentro de data")
    index = load_json(index_path.resolve()) if index_path else load_latest_odeuropa_retrieval_index(data_directory)
    expansion = expand_odeuropa_query(index, query, language=language)
    target_ids = sorted({str(target["id"]) for target in expansion["canonical_targets"]})
    if not target_ids:
        return DemandEventResult(False, None, 0, resolved_events)
    event_date = occurred_on or date.today().isoformat()
    identifier = event_id or f"demand:{sha256(f'{event_date}\0{secrets.token_hex(16)}'.encode('utf-8')).hexdigest()[:24]}"
    event = {
        "schema_version": 1,
        "event_id": identifier,
        "occurred_on": event_date,
        "language": language,
        "matched_target_ids": target_ids,
        "source": "local_companion",
        "privacy": {
            "raw_query_stored": False,
            "personal_identifiers_stored": False,
            "timestamp_precision": "day",
        },
    }
    _validate_event(event)
    existing = _load_jsonl(resolved_events, missing_ok=True)
    for item in existing:
        _validate_event(item)
        if item["event_id"] == identifier:
            if canonical_json(item) != canonical_json(event):
                raise ValueError(f"event_id duplicado com conteúdo divergente: {identifier}")
            return DemandEventResult(False, identifier, len(target_ids), resolved_events)
    write_dicts_jsonl(resolved_events, [*existing, event])
    return DemandEventResult(True, identifier, len(target_ids), resolved_events)


def _catalog_signals(catalog: dict[str, Any]) -> tuple[Counter[str], dict[str, set[str]]]:
    fragrances = catalog.get("fragrances")
    if not isinstance(fragrances, list):
        raise ValueError("catálogo de recomendação não contém fragrances")
    occurrences: Counter[str] = Counter()
    fragrances_by_term: dict[str, set[str]] = defaultdict(set)
    for fragrance in fragrances:
        if not isinstance(fragrance, dict) or not isinstance(fragrance.get("id"), str):
            raise ValueError("catálogo contém fragrância inválida")
        values: list[str] = []
        for field in ("topNotes", "heartNotes", "baseNotes"):
            raw_values = fragrance.get(field, [])
            if not isinstance(raw_values, list) or any(not isinstance(value, str) for value in raw_values):
                raise ValueError(f"fragrância {fragrance['id']} possui {field} inválido")
            values.extend(raw_values)
        accords = fragrance.get("accords", [])
        if not isinstance(accords, list):
            raise ValueError(f"fragrância {fragrance['id']} possui accords inválido")
        for accord in accords:
            value = accord.get("id") if isinstance(accord, dict) else accord
            if not isinstance(value, str):
                raise ValueError(f"fragrância {fragrance['id']} possui acorde inválido")
            values.append(value)
        for value in values:
            occurrences[value] += 1
            fragrances_by_term[value].add(str(fragrance["id"]))
    return occurrences, fragrances_by_term


def _load_policy(path: Path) -> tuple[dict[str, int], dict[str, dict[str, str]]]:
    payload = _load_yaml(path)
    policy = payload.get("policy")
    priorities = payload.get("priorities", [])
    if payload.get("schema_version") != 1 or not isinstance(policy, dict) or not isinstance(priorities, list):
        raise ValueError("política de demanda P4 inválida")
    values = {
        "window_days": int(policy.get("window_days", 90)),
        "min_query_events": int(policy.get("min_query_events", 3)),
        "min_active_days": int(policy.get("min_active_days", 2)),
        "min_catalog_fragrances": int(policy.get("min_catalog_fragrances", 1)),
    }
    if any(value <= 0 for value in values.values()):
        raise ValueError("limiares da política P4 precisam ser positivos")
    editorial: dict[str, dict[str, str]] = {}
    for item in priorities:
        if not isinstance(item, dict):
            raise ValueError("prioridade editorial P4 inválida")
        target_id = item.get("target_id")
        priority = item.get("priority")
        rationale = item.get("rationale")
        if not isinstance(target_id, str) or priority not in {"high", "medium", "low"}:
            raise ValueError("prioridade editorial P4 possui destino ou nível inválido")
        if not isinstance(rationale, str) or len(rationale.strip()) < 12:
            raise ValueError("prioridade editorial P4 exige justificativa")
        if target_id in editorial:
            raise ValueError(f"prioridade editorial duplicada: {target_id}")
        editorial[target_id] = {"priority": priority, "rationale": rationale.strip()}
    return values, editorial


def build_p4_demand_gate(
    data_directory: Path,
    *,
    retrieval_directory: Path | None = None,
    events_path: Path | None = None,
    catalog_path: Path | None = None,
    policy_path: Path | None = None,
    as_of: str | None = None,
) -> DemandGateResult:
    data_directory = data_directory.resolve()
    retrieval = _resolve_retrieval_directory(data_directory, retrieval_directory)
    resolved_events = (events_path or data_directory / "private" / "demand" / "olfactory-query-events.jsonl").resolve()
    if not resolved_events.is_relative_to(data_directory):
        raise ValueError("eventos de demanda precisam permanecer dentro de data")
    resolved_catalog = (catalog_path or data_directory.parent / "apps" / "web" / "public" / "catalog" / "recommendation-catalog.json").resolve()
    resolved_policy = (policy_path or data_directory / "evaluation" / "odeuropa-p4-demand.yml").resolve()
    policy, editorial = _load_policy(resolved_policy)
    reference_date = date.fromisoformat(as_of or date.today().isoformat())
    first_date = reference_date - timedelta(days=policy["window_days"] - 1)

    backlog = _load_jsonl(retrieval / "routing-backlog.jsonl")
    p4_items = [item for item in backlog if item.get("priority", {}).get("tier") == "P4"]
    if len(p4_items) != len(backlog):
        raise ValueError("gate P4 exige backlog contendo somente itens P4")
    target_ids = {str(item.get("target", {}).get("id", "")) for item in p4_items}
    unknown_editorial = set(editorial) - target_ids
    if unknown_editorial:
        raise ValueError(f"prioridades editoriais não pertencem ao backlog P4: {', '.join(sorted(unknown_editorial))}")

    event_counts: Counter[str] = Counter()
    event_days: dict[str, set[str]] = defaultdict(set)
    seen_events: set[str] = set()
    events = _load_jsonl(resolved_events, missing_ok=True)
    for event in events:
        _validate_event(event)
        identifier = str(event["event_id"])
        if identifier in seen_events:
            raise ValueError(f"evento de demanda duplicado: {identifier}")
        seen_events.add(identifier)
        occurred = date.fromisoformat(str(event["occurred_on"]))
        if occurred < first_date or occurred > reference_date:
            continue
        for target_id in event["matched_target_ids"]:
            if target_id in target_ids:
                event_counts[target_id] += 1
                event_days[target_id].add(str(event["occurred_on"]))

    catalog = load_json(resolved_catalog)
    if not isinstance(catalog, dict):
        raise ValueError("catálogo de recomendação inválido")
    catalog_occurrences, catalog_fragrances = _catalog_signals(catalog)

    gate_items: list[dict[str, Any]] = []
    for backlog_item in p4_items:
        target = backlog_item["target"]
        target_id = str(target["id"])
        canonical_id = str(target.get("canonical_id", ""))
        query_ready = (
            event_counts[target_id] >= policy["min_query_events"]
            and len(event_days[target_id]) >= policy["min_active_days"]
        )
        catalog_ready = len(catalog_fragrances[canonical_id]) >= policy["min_catalog_fragrances"]
        editorial_item = editorial.get(target_id)
        editorial_ready = editorial_item is not None and editorial_item["priority"] == "high"
        reasons: list[str] = []
        if query_ready:
            reasons.append("recurring_anonymized_query_demand")
        if catalog_ready:
            reasons.append("declared_in_approved_catalog")
        if editorial_ready:
            reasons.append("high_editorial_priority_with_rationale")
        if reasons:
            gate_status = "research_ready"
        elif event_counts[target_id] or editorial_item is not None:
            gate_status = "watchlist"
        else:
            gate_status = "dormant"
        gate_items.append({
            "schema_version": 1,
            "gate_item_id": f"odeuropa:p4-demand:{sha256(target_id.encode('utf-8')).hexdigest()[:20]}",
            "target": target,
            "backlog_item_id": backlog_item.get("backlog_item_id"),
            "gate_status": gate_status,
            "signals": {
                "anonymized_query_events": event_counts[target_id],
                "active_query_days": len(event_days[target_id]),
                "catalog_occurrences": catalog_occurrences[canonical_id],
                "catalog_distinct_fragrances": len(catalog_fragrances[canonical_id]),
                "editorial_priority": editorial_item["priority"] if editorial_item else None,
                "editorial_rationale": editorial_item["rationale"] if editorial_item else None,
            },
            "gate": {
                "research_authorized": gate_status == "research_ready",
                "document_creation_allowed": False,
                "core_promotion_allowed": False,
                "independent_evidence_required": True,
                "reasons": reasons,
            },
            "governance": {
                "demand_is_not_evidence": True,
                "facts_generated": False,
                "relations_generated": False,
                "odeuropa_scope": "retrieval_and_discovery_only",
            },
        })

    status_order = {"research_ready": 0, "watchlist": 1, "dormant": 2}
    gate_items.sort(key=lambda item: (
        status_order[str(item["gate_status"])],
        -int(item["signals"]["catalog_distinct_fragrances"]),
        -int(item["signals"]["anonymized_query_events"]),
        str(item["target"]["id"]),
    ))
    for rank, item in enumerate(gate_items, start=1):
        item["rank"] = rank

    catalog_release_id = catalog.get("releaseId")
    if catalog_release_id is not None and not isinstance(catalog_release_id, str):
        raise ValueError("catálogo de recomendação possui releaseId inválido")
    identity_payload = {
        "items": gate_items,
        "as_of": reference_date.isoformat(),
        "window": {"from": first_date.isoformat(), "to": reference_date.isoformat()},
        "policy": policy,
        "catalog_release_id": catalog_release_id,
    }
    content_hash = sha256(canonical_json(identity_payload).encode("utf-8")).hexdigest()
    gate_id = f"odeuropa-p4-demand-v1-{content_hash[:12]}"
    counts = Counter(str(item["gate_status"]) for item in gate_items)
    output_directory = retrieval / "demand-gate"
    write_dicts_jsonl(output_directory / "items.jsonl", gate_items)
    report = {
        "schema_version": 1,
        "gate_id": gate_id,
        "as_of": reference_date.isoformat(),
        "window": {"from": first_date.isoformat(), "to": reference_date.isoformat()},
        "policy": policy,
        "catalog_release_id": catalog_release_id,
        "counts": {
            "p4_items": len(gate_items),
            "research_ready": counts["research_ready"],
            "watchlist": counts["watchlist"],
            "dormant": counts["dormant"],
            "events_read": len(events),
            "documents_created": 0,
        },
        "privacy": {
            "raw_queries_read_by_gate": False,
            "raw_queries_stored": False,
            "personal_identifiers_stored": False,
            "event_precision": "day",
        },
        "safety": {
            "demand_is_not_evidence": True,
            "research_ready_does_not_allow_document_creation": True,
            "facts_generated": False,
            "relations_generated": False,
        },
        "research_queue": [
            {
                "rank": item["rank"],
                "target_id": item["target"]["id"],
                "label_pt": item["target"].get("label_pt"),
                "reasons": item["gate"]["reasons"],
                "signals": item["signals"],
            }
            for item in gate_items
            if item["gate_status"] == "research_ready"
        ],
    }
    atomic_write_text(output_directory / "report.json", f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    manifest = {
        "schema_version": 1,
        "gate_id": gate_id,
        "content_sha256": content_hash,
        "inputs": {
            "backlog": (retrieval / "routing-backlog.jsonl").as_posix(),
            "events": resolved_events.as_posix(),
            "catalog": resolved_catalog.as_posix(),
            "policy": resolved_policy.as_posix(),
        },
        "files": {"items": "items.jsonl", "report": "report.json"},
    }
    atomic_write_text(output_directory / "manifest.json", f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return DemandGateResult(
        gate_id=gate_id,
        p4_items=len(gate_items),
        research_ready=counts["research_ready"],
        watchlist=counts["watchlist"],
        dormant=counts["dormant"],
        output_directory=output_directory,
    )
