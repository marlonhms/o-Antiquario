from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json


STRUCTURAL_PREDICATES = {
    "has-top-note",
    "has-heart-note",
    "has-base-note",
    "has-note",
    "has-accord",
    "includes-note",
    "expressed-by",
}


@dataclass(frozen=True)
class OdeuropaBacklogBuildResult:
    backlog_id: str
    items: int
    identity_items: int
    content_items: int
    priority_counts: dict[str, int]
    output_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "backlog_id": self.backlog_id,
            "items": self.items,
            "identity_items": self.identity_items,
            "content_items": self.content_items,
            "priority_counts": self.priority_counts,
            "output_directory": self.output_directory.as_posix(),
            "knowledge_core_mutated": False,
            "facts_generated": False,
        }


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
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
        latest_path = data_root / "staging" / "odeuropa" / "latest.json"
        latest = load_json(latest_path)
        relative = latest.get("staging_directory")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError("latest.json ODEUROPA inválido")
        resolved = (data_root / relative / "equivalence" / "retrieval").resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError("diretório de recuperação precisa permanecer dentro de data")
    return resolved


def _gold_signals(gold: dict[str, Any]) -> tuple[Counter[str], Counter[str], dict[str, set[str]]]:
    cases = gold.get("cases")
    if gold.get("schema_version") != 1 or not isinstance(cases, list):
        raise ValueError("conjunto ouro ODEUROPA inválido")
    expected: Counter[str] = Counter()
    forbidden: Counter[str] = Counter()
    case_ids: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise ValueError("caso ouro ODEUROPA inválido")
        for key, counter in (("expected_target_ids", expected), ("forbidden_target_ids", forbidden)):
            values = case.get(key, [])
            if not isinstance(values, list):
                raise ValueError(f"caso ouro {case['id']} possui {key} inválido")
            for value in values:
                target_id = str(value)
                counter[target_id] += 1
                case_ids[target_id].add(str(case["id"]))
    return expected, forbidden, case_ids


def _catalog_signals(catalog: dict[str, Any]) -> tuple[Counter[str], dict[str, set[str]], dict[str, Counter[str]]]:
    fragrances = catalog.get("fragrances")
    if not isinstance(fragrances, list):
        raise ValueError("catálogo de recomendação não contém fragrances")
    occurrences: Counter[str] = Counter()
    fragrance_ids: dict[str, set[str]] = defaultdict(set)
    positions: dict[str, Counter[str]] = defaultdict(Counter)
    fields = {
        "topNotes": "top",
        "heartNotes": "heart",
        "baseNotes": "base",
    }
    for fragrance in fragrances:
        if not isinstance(fragrance, dict) or not isinstance(fragrance.get("id"), str):
            raise ValueError("catálogo contém fragrância inválida")
        fragrance_id = str(fragrance["id"])
        for field, position in fields.items():
            values = fragrance.get(field, [])
            if not isinstance(values, list):
                raise ValueError(f"fragrância {fragrance_id} possui {field} inválido")
            for value in values:
                if not isinstance(value, str):
                    raise ValueError(f"fragrância {fragrance_id} possui nota inválida")
                occurrences[value] += 1
                fragrance_ids[value].add(fragrance_id)
                positions[value][position] += 1
        accords = fragrance.get("accords", [])
        if not isinstance(accords, list):
            raise ValueError(f"fragrância {fragrance_id} possui accords inválido")
        for value in accords:
            accord_id = value.get("id") if isinstance(value, dict) else value
            if not isinstance(accord_id, str):
                raise ValueError(f"fragrância {fragrance_id} possui acorde inválido")
            occurrences[accord_id] += 1
            fragrance_ids[accord_id].add(fragrance_id)
            positions[accord_id]["accord"] += 1
    return occurrences, fragrance_ids, positions


def _graph_signals(graph: dict[str, Any], document_ids: set[str]) -> dict[str, object]:
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("grafo compilado inválido")
    document_nodes = {
        str(node["id"])
        for node in nodes
        if isinstance(node, dict) and node.get("kind") == "document" and isinstance(node.get("id"), str)
    }
    structural_edges: set[tuple[str, str, str]] = set()
    connected_documents: set[str] = set()
    predicates: Counter[str] = Counter()
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("grafo compilado contém aresta inválida")
        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        predicate = str(edge.get("predicate", ""))
        if predicate not in STRUCTURAL_PREDICATES or not ({source, target} & document_ids):
            continue
        signature = (source, target, predicate)
        structural_edges.add(signature)
        counterpart = target if source in document_ids else source
        if counterpart in document_nodes and counterpart not in document_ids:
            connected_documents.add(counterpart)
        predicates[predicate] += 1
    return {
        "structural_edges": len(structural_edges),
        "connected_documents": len(connected_documents),
        "predicate_counts": dict(sorted(predicates.items())),
    }


def _priority_for(
    route_status: str,
    *,
    gold_expected: int,
    catalog_fragrances: int,
) -> tuple[str, str, str, str]:
    if route_status == "ambiguous_document_match":
        return (
            "P0",
            "identity_resolution",
            "reconcile_canonical_identity",
            "blocked_identity_review",
        )
    if gold_expected:
        return (
            "P1",
            "content_coverage",
            "enrich_existing_document" if route_status == "document_without_chunks" else "create_canonical_document",
            "evidence_and_content_required",
        )
    if catalog_fragrances:
        return (
            "P2",
            "content_coverage",
            "enrich_existing_document" if route_status == "document_without_chunks" else "create_canonical_document",
            "evidence_and_content_required",
        )
    if route_status == "document_without_chunks":
        return ("P3", "content_coverage", "enrich_existing_document", "evidence_and_content_required")
    return ("P4", "content_coverage", "create_canonical_document", "evidence_and_content_required")


def _priority_sort_key(item: dict[str, Any]) -> tuple[object, ...]:
    tier_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    signals = item["priority"]["signals"]
    route_status = str(item["gap"]["route_status"])
    readiness = 0 if route_status == "document_without_chunks" else 1
    return (
        tier_order[str(item["priority"]["tier"])],
        -int(signals["gold_expected_occurrences"]),
        -int(signals["catalog_distinct_fragrances"]),
        readiness,
        -int(signals["graph_connected_documents"]),
        str(item["target"]["id"]),
    )


def build_odeuropa_routing_backlog(
    data_directory: Path,
    *,
    retrieval_directory: Path | None = None,
    gold_path: Path | None = None,
    knowledge_directory: Path | None = None,
    catalog_path: Path | None = None,
) -> OdeuropaBacklogBuildResult:
    data_directory = data_directory.resolve()
    retrieval = _resolve_retrieval_directory(data_directory, retrieval_directory)
    gaps_path = retrieval / "routing-gaps.jsonl"
    retrieval_manifest_path = retrieval / "manifest.json"
    gaps = _load_jsonl(gaps_path)
    retrieval_manifest = load_json(retrieval_manifest_path)

    resolved_gold = (gold_path or data_directory / "evaluation" / "odeuropa-retrieval-gold.yml").resolve()
    resolved_knowledge = (knowledge_directory or data_directory.parent / "knowledge" / "compiled").resolve()
    resolved_catalog = (catalog_path or data_directory.parent / "apps" / "web" / "public" / "catalog" / "recommendation-catalog.json").resolve()
    gold = _load_yaml(resolved_gold)
    graph = load_json(resolved_knowledge / "graph.json")
    catalog = load_json(resolved_catalog)
    if not isinstance(graph, dict) or not isinstance(catalog, dict):
        raise ValueError("fontes de priorização inválidas")

    gold_expected, gold_forbidden, gold_case_ids = _gold_signals(gold)
    catalog_occurrences, catalog_fragrances, catalog_positions = _catalog_signals(catalog)

    grouped: dict[str, dict[str, Any]] = {}
    source_entry_ids: dict[str, set[str]] = defaultdict(set)
    for gap in gaps:
        target = gap.get("target")
        route = gap.get("retrieval")
        if not isinstance(target, dict) or not isinstance(route, dict):
            raise ValueError("lacuna ODEUROPA inválida")
        target_id = str(target.get("id", ""))
        route_status = str(route.get("route_status", ""))
        if not target_id or route_status not in {
            "missing_document",
            "document_without_chunks",
            "ambiguous_document_match",
        }:
            raise ValueError("lacuna ODEUROPA possui destino ou estado inválido")
        signature = canonical_json({"target": target, "retrieval": route})
        previous = grouped.get(target_id)
        if previous is not None and previous["signature"] != signature:
            raise ValueError(f"rotas inconsistentes para {target_id}")
        grouped[target_id] = {"target": target, "retrieval": route, "signature": signature}
        source_entry_id = gap.get("source_entry_id")
        if isinstance(source_entry_id, str) and source_entry_id:
            source_entry_ids[target_id].add(source_entry_id)

    items: list[dict[str, Any]] = []
    for target_id, group in grouped.items():
        target = group["target"]
        route = group["retrieval"]
        canonical_id = str(target.get("canonical_id", ""))
        raw_candidate_ids = route.get("candidate_document_ids", [])
        if not isinstance(raw_candidate_ids, list):
            raise ValueError(f"lacuna {target_id} possui candidatos documentais inválidos")
        candidate_ids = {
            str(value)
            for value in raw_candidate_ids
            if isinstance(value, str)
        }
        if isinstance(route.get("document_id"), str):
            candidate_ids.add(str(route["document_id"]))
        candidate_ids.add(target_id)
        graph_signals = _graph_signals(graph, candidate_ids)
        tier, lane, action, safety_lane = _priority_for(
            str(route["route_status"]),
            gold_expected=gold_expected[target_id],
            catalog_fragrances=len(catalog_fragrances[canonical_id]),
        )
        reasons: list[str] = []
        if tier == "P0":
            reasons.append("multiple_same_type_documents_match_the_canonical_label")
        if gold_expected[target_id]:
            reasons.append("target_expected_by_retrieval_gold_set")
        if catalog_fragrances[canonical_id]:
            reasons.append("target_used_by_active_recommendation_catalog")
        if route["route_status"] == "document_without_chunks":
            reasons.append("existing_document_has_no_retrievable_chunks")
        elif route["route_status"] == "missing_document":
            reasons.append("canonical_document_is_missing")
        item = {
            "schema_version": 1,
            "backlog_item_id": f"odeuropa:routing-backlog:{sha256(target_id.encode('utf-8')).hexdigest()[:20]}",
            "target": target,
            "gap": {
                "route_status": route["route_status"],
                "route_method": route.get("route_method"),
                "document_id": route.get("document_id"),
                "candidate_document_ids": sorted(str(value) for value in raw_candidate_ids if isinstance(value, str)),
                "source_entry_ids": sorted(source_entry_ids[target_id]),
            },
            "remediation": {
                "action": action,
                "safety_lane": safety_lane,
                "automatic_knowledge_mutation_allowed": False,
                "promotion_status": "blocked",
                "required_evidence_scope": "allowed_core_or_independent_curated_evidence",
            },
            "priority": {
                "tier": tier,
                "lane": lane,
                "signals": {
                    "gold_expected_occurrences": gold_expected[target_id],
                    "gold_forbidden_occurrences": gold_forbidden[target_id],
                    "gold_case_ids": sorted(gold_case_ids[target_id]),
                    "catalog_occurrences": catalog_occurrences[canonical_id],
                    "catalog_distinct_fragrances": len(catalog_fragrances[canonical_id]),
                    "catalog_pyramid_positions": dict(sorted(catalog_positions[canonical_id].items())),
                    "graph_structural_edges": graph_signals["structural_edges"],
                    "graph_connected_documents": graph_signals["connected_documents"],
                    "graph_predicate_counts": graph_signals["predicate_counts"],
                },
                "reasons": reasons,
                "meaning": "operational_priority_not_semantic_confidence",
            },
            "governance": {
                "odeuropa_scope": "retrieval_and_discovery_only",
                "odeuropa_may_supply_document_facts": False,
                "facts_generated": False,
                "semantic_identity_verified": False,
            },
        }
        items.append(item)

    items.sort(key=_priority_sort_key)
    lane_ranks: Counter[str] = Counter()
    for rank, item in enumerate(items, start=1):
        lane = str(item["priority"]["lane"])
        lane_ranks[lane] += 1
        item["rank"] = rank
        item["lane_rank"] = lane_ranks[lane]

    content_hash = sha256(canonical_json(items).encode("utf-8")).hexdigest()
    backlog_id = f"odeuropa-routing-backlog-v1-{content_hash[:12]}"
    priority_counts = dict(sorted(Counter(str(item["priority"]["tier"]) for item in items).items()))
    lane_counts = dict(sorted(Counter(str(item["priority"]["lane"]) for item in items).items()))
    action_counts = dict(sorted(Counter(str(item["remediation"]["action"]) for item in items).items()))
    report = {
        "schema_version": 1,
        "backlog_id": backlog_id,
        "retrieval_index_id": retrieval_manifest.get("index_id"),
        "knowledge_release_id": retrieval_manifest.get("knowledge_release_id"),
        "catalog_release_id": catalog.get("releaseId"),
        "counts": {
            "items": len(items),
            "priority_tiers": priority_counts,
            "lanes": lane_counts,
            "actions": action_counts,
        },
        "ranking_policy": [
            "P0: ambiguous canonical identity; isolated in the identity-resolution lane",
            "P1: unroutable target expected by the retrieval gold set",
            "P2: unroutable target used by the active recommendation catalog",
            "P3: existing canonical document without retrievable chunks",
            "P4: missing canonical document without observed gold/catalog demand",
        ],
        "safety": {
            "knowledge_core_mutated": False,
            "facts_generated": False,
            "semantic_confidence_changed": False,
            "protected_relations_generated": False,
        },
        "top_items": [
            {
                "rank": item["rank"],
                "target_id": item["target"]["id"],
                "label_pt": item["target"].get("label_pt"),
                "tier": item["priority"]["tier"],
                "lane": item["priority"]["lane"],
                "action": item["remediation"]["action"],
                "reasons": item["priority"]["reasons"],
            }
            for item in items[:10]
        ],
    }
    manifest = {
        "schema_version": 1,
        "backlog_id": backlog_id,
        "content_sha256": content_hash,
        "inputs": {
            "routing_gaps": gaps_path.as_posix(),
            "retrieval_manifest": retrieval_manifest_path.as_posix(),
            "gold_set": resolved_gold.as_posix(),
            "knowledge_graph": (resolved_knowledge / "graph.json").as_posix(),
            "recommendation_catalog": resolved_catalog.as_posix(),
        },
        "files": {
            "items": "routing-backlog.jsonl",
            "report": "backlog-report.json",
        },
    }
    write_dicts_jsonl(retrieval / "routing-backlog.jsonl", items)
    atomic_write_text(retrieval / "backlog-report.json", f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    atomic_write_text(retrieval / "backlog-manifest.json", f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return OdeuropaBacklogBuildResult(
        backlog_id=backlog_id,
        items=len(items),
        identity_items=lane_counts.get("identity_resolution", 0),
        content_items=lane_counts.get("content_coverage", 0),
        priority_counts=priority_counts,
        output_directory=retrieval,
    )
