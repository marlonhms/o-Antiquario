from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json
from .odeuropa import ATTRIBUTION, LICENSE_ID, SOURCE_ID, normalize_search_key


TARGET_TYPE_BY_COLLECTION = {
    "families": "olfactory-family",
    "accords": "accord",
    "notes": "olfactory-note",
}
FORBIDDEN_PREDICATES = (
    "has-note",
    "has-top-note",
    "has-heart-note",
    "has-base-note",
    "declares-*",
)


@dataclass(frozen=True)
class CanonicalTarget:
    collection: str
    canonical_id: str
    entity_type: str
    label_pt: str
    label_en: str
    source_ids: tuple[str, ...]

    @property
    def global_id(self) -> str:
        return f"antiquario:{self.entity_type}:{self.canonical_id}"

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.global_id,
            "type": self.entity_type,
            "canonical_id": self.canonical_id,
            "collection": self.collection,
            "label_pt": self.label_pt,
            "label_en": self.label_en,
            "source_ids": list(self.source_ids),
        }


@dataclass(frozen=True)
class CanonicalHit:
    target: CanonicalTarget
    field: str
    label: str


@dataclass(frozen=True)
class OdeuropaEquivalenceResult:
    snapshot_id: str
    resolved_bridges: int
    candidates: int
    ambiguities: int
    unresolved: int
    output_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "snapshot_id": self.snapshot_id,
            "resolved_bridges": self.resolved_bridges,
            "candidates": self.candidates,
            "ambiguities": self.ambiguities,
            "unresolved": self.unresolved,
            "output_directory": self.output_directory.as_posix(),
            "scope": "retrieval_only",
            "semantic_identity": "unverified",
            "promotion_status": "blocked",
        }


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256("\0".join(parts).encode("utf-8")).hexdigest()[:20]
    return f"odeuropa:{prefix}:{digest}"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
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


def _load_taxonomy(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ModuleNotFoundError as error:
        raise RuntimeError("Biblioteca 'pyyaml' ausente no ambiente Python.") from error
    if not path.is_file():
        raise FileNotFoundError(f"taxonomia canônica ausente: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError("taxonomia canônica precisa ser um objeto YAML")
    return payload


def _build_canonical_indexes(
    taxonomy: dict[str, Any],
) -> tuple[dict[str, list[CanonicalHit]], dict[str, list[CanonicalHit]], dict[str, list[CanonicalHit]]]:
    english: dict[str, list[CanonicalHit]] = {}
    aliases: dict[str, list[CanonicalHit]] = {}
    all_labels: dict[str, list[CanonicalHit]] = {}

    def add(index: dict[str, list[CanonicalHit]], key: str, hit: CanonicalHit) -> None:
        if key:
            index.setdefault(key, []).append(hit)

    for collection, entity_type in TARGET_TYPE_BY_COLLECTION.items():
        entries = taxonomy.get(collection, [])
        if not isinstance(entries, list):
            raise ValueError(f"taxonomia.{collection} precisa ser uma lista")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"taxonomia.{collection} contém entrada inválida")
            canonical_id = str(entry.get("id", "")).strip()
            label_pt = str(entry.get("pt", "")).strip()
            label_en = str(entry.get("en", "")).strip()
            source_ids_raw = entry.get("source_ids", [])
            if not canonical_id or not label_pt or not label_en or not isinstance(source_ids_raw, list):
                raise ValueError(f"taxonomia.{collection} contém campos obrigatórios inválidos")
            target = CanonicalTarget(
                collection=collection,
                canonical_id=canonical_id,
                entity_type=entity_type,
                label_pt=label_pt,
                label_en=label_en,
                source_ids=tuple(sorted(str(value) for value in source_ids_raw)),
            )
            for field, label in (("id", canonical_id), ("pt", label_pt), ("en", label_en)):
                hit = CanonicalHit(target=target, field=field, label=label)
                key = normalize_search_key(label)
                add(all_labels, key, hit)
                if field == "en":
                    add(english, key, hit)
            aliases_raw = entry.get("aliases", [])
            if aliases_raw is None:
                aliases_raw = []
            if not isinstance(aliases_raw, list):
                raise ValueError(f"taxonomia.{collection}.{canonical_id}.aliases precisa ser uma lista")
            for alias in aliases_raw:
                label = str(alias).strip()
                hit = CanonicalHit(target=target, field="alias", label=label)
                key = normalize_search_key(label)
                add(aliases, key, hit)
                add(all_labels, key, hit)

    for index in (english, aliases, all_labels):
        for key, hits in index.items():
            index[key] = sorted(hits, key=lambda hit: (hit.target.global_id, hit.field, hit.label))
    return english, aliases, all_labels


def _unique_targets(hits: list[CanonicalHit]) -> list[CanonicalTarget]:
    targets = {hit.target.global_id: hit.target for hit in hits}
    return [targets[key] for key in sorted(targets)]


def _source_term(term: dict[str, Any]) -> dict[str, object]:
    return {
        "id": str(term["id"]),
        "type": str(term.get("entity_type_candidate") or "unknown"),
        "label_original": str(term["term_original"]),
        "entry_original": str(term["entry_original"]),
        "language": str(term["language"]),
        "part_of_speech": str(term["part_of_speech"]),
        "search_key": str(term["search_key"]),
        "wordnet_synsets": sorted(str(value) for value in term.get("wordnet_synsets", [])),
    }


def _evidence(term: dict[str, Any], method: str, claim_scope: str) -> dict[str, object]:
    return {
        "source_id": SOURCE_ID,
        "locator": str(term["source_locator"]),
        "license": LICENSE_ID,
        "attribution": ATTRIBUTION,
        "claim_scope": claim_scope,
        "confidence": "high" if method == "exact_english_label" else "medium",
        "claim_nature": "inferred",
        "method": method,
        "original_label": str(term["term_original"]),
        "original_language": str(term["language"]),
    }


def _bridge_record(
    term: dict[str, Any],
    target: CanonicalTarget,
    *,
    method: str,
    status: str,
    matched_label: str | None = None,
    matched_field: str | None = None,
    matched_synsets: list[str] | None = None,
    anchor_term_ids: list[str] | None = None,
) -> dict[str, object]:
    bridge_id = _stable_id("retrieval-bridge", str(term["id"]), target.global_id, method)
    return {
        "schema_version": 1,
        "bridge_id": bridge_id,
        "source_term": _source_term(term),
        "target": target.as_dict(),
        "link_kind": "lexical-retrieval-bridge",
        "scope": "retrieval_only",
        "semantic_identity": "unverified",
        "type_compatibility": "cross_ontology",
        "match": {
            "method": method,
            "normalized_key": str(term["search_key"]),
            "matched_label": matched_label,
            "matched_field": matched_field,
            "matched_synsets": matched_synsets or [],
            "anchor_term_ids": anchor_term_ids or [],
        },
        "claim_nature": "inferred",
        "confidence": "high" if method == "exact_english_label" else "medium",
        "status": status,
        "promotion_status": "blocked",
        "commercial_claims_generated": False,
        "evidence": _evidence(
            term,
            method,
            "ponte lexical entre termo ODEUROPA e conceito canônico, válida somente para recuperação",
        ),
    }


def _ambiguity_record(
    term: dict[str, Any],
    *,
    reason: str,
    targets: list[CanonicalTarget],
    method: str,
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    target_ids = [target.global_id for target in targets]
    return {
        "schema_version": 1,
        "ambiguity_id": _stable_id("equivalence-ambiguity", str(term["id"]), reason, *target_ids),
        "source_term": _source_term(term),
        "candidate_targets": [target.as_dict() for target in targets],
        "reason": reason,
        "method": method,
        "details": details or {},
        "status": "quarantined",
        "scope": "retrieval_only",
        "semantic_identity": "unverified",
        "promotion_status": "blocked",
        "evidence": _evidence(
            term,
            method,
            "ambiguidade na resolução lexical ODEUROPA para a taxonomia canônica",
        ),
    }


def _unresolved_record(term: dict[str, Any], reason: str) -> dict[str, object]:
    return {
        "schema_version": 1,
        "source_term": _source_term(term),
        "reason": reason,
        "status": "unresolved",
        "scope": "retrieval_only",
        "promotion_status": "blocked",
        "provenance": {
            "source_id": SOURCE_ID,
            "locator": str(term["source_locator"]),
            "license": LICENSE_ID,
            "attribution": ATTRIBUTION,
        },
    }


def _resolve_staging_directory(data_directory: Path, staging_directory: Path | None) -> Path:
    data_root = data_directory.resolve()
    if staging_directory is not None:
        resolved = staging_directory.resolve()
    else:
        latest_path = data_root / "staging" / "odeuropa" / "latest.json"
        if not latest_path.is_file():
            raise FileNotFoundError("staging ODEUROPA ausente; execute sync odeuropa primeiro")
        latest = load_json(latest_path)
        relative = latest.get("staging_directory")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError("latest.json ODEUROPA não contém staging_directory válido")
        resolved = (data_root / relative).resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError("diretório de staging ODEUROPA precisa permanecer dentro de data")
    return resolved


def _count_by(records: list[dict[str, object]], value_getter: Callable[[dict[str, object]], object]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(value_getter(record))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _audit_resolution_outputs(
    source_terms: list[dict[str, Any]],
    bridges: list[dict[str, object]],
    candidates: list[dict[str, object]],
    ambiguities: list[dict[str, object]],
    unresolved: list[dict[str, object]],
) -> None:
    source_ids = [str(term.get("id", "")) for term in source_terms]
    if any(not identifier for identifier in source_ids) or len(set(source_ids)) != len(source_ids):
        raise ValueError("staging ODEUROPA contém IDs de termo vazios ou duplicados")

    output_records = bridges + candidates + ambiguities + unresolved
    allocated_ids = [str(record["source_term"]["id"]) for record in output_records]
    if sorted(allocated_ids) != sorted(source_ids):
        raise RuntimeError("cada termo ODEUROPA precisa aparecer exatamente uma vez na resolução")

    bridge_ids = [str(record["bridge_id"]) for record in bridges + candidates]
    if len(set(bridge_ids)) != len(bridge_ids):
        raise RuntimeError("resolvedor ODEUROPA gerou bridge_id duplicado")

    for record in bridges + candidates:
        if "predicate" in record:
            raise RuntimeError("pontes de recuperação não podem declarar predicados do grafo")
        if record.get("scope") != "retrieval_only" or record.get("semantic_identity") != "unverified":
            raise RuntimeError("ponte ODEUROPA violou o escopo seguro de recuperação")
        target = record.get("target")
        if not isinstance(target, dict) or target.get("type") == "fragrance":
            raise RuntimeError("ponte ODEUROPA contém destino inválido")


def resolve_odeuropa_equivalences(
    data_directory: Path,
    *,
    taxonomy_path: Path | None = None,
    staging_directory: Path | None = None,
) -> OdeuropaEquivalenceResult:
    data_directory = data_directory.resolve()
    staging = _resolve_staging_directory(data_directory, staging_directory)
    terms_path = staging / "terms.jsonl"
    report_path = staging / "report.json"
    if not terms_path.is_file() or not report_path.is_file():
        raise FileNotFoundError(f"snapshot ODEUROPA incompleto em {staging}")
    source_report = load_json(report_path)
    snapshot_id = source_report.get("snapshot_id")
    if not isinstance(snapshot_id, str) or len(snapshot_id) != 64:
        raise ValueError("report.json ODEUROPA não contém snapshot_id válido")

    taxonomy_file = (taxonomy_path or data_directory / "taxonomy" / "taxonomy.yml").resolve()
    taxonomy_bytes = taxonomy_file.read_bytes() if taxonomy_file.is_file() else b""
    taxonomy_hash = sha256(taxonomy_bytes).hexdigest()
    taxonomy = _load_taxonomy(taxonomy_file)
    english_index, alias_index, all_labels_index = _build_canonical_indexes(taxonomy)
    terms = _load_jsonl(terms_path)

    direct_resolution: dict[str, CanonicalTarget] = {}
    direct_hits: dict[str, CanonicalHit] = {}
    synset_anchors: dict[str, dict[str, dict[str, object]]] = {}
    for term in terms:
        if term.get("status") != "candidate" or term.get("language") != "en":
            continue
        hits = english_index.get(str(term.get("search_key", "")), [])
        targets = _unique_targets(hits)
        if len(targets) != 1:
            continue
        target = targets[0]
        term_id = str(term["id"])
        direct_resolution[term_id] = target
        direct_hits[term_id] = next(hit for hit in hits if hit.target.global_id == target.global_id)
        for synset in sorted(str(value) for value in term.get("wordnet_synsets", [])):
            target_map = synset_anchors.setdefault(synset, {})
            anchor = target_map.setdefault(
                target.global_id,
                {"target": target, "term_ids": [], "source_types": set()},
            )
            anchor["term_ids"].append(term_id)
            anchor["source_types"].add(str(term.get("entity_type_candidate") or "unknown"))

    bridges: list[dict[str, object]] = []
    candidates: list[dict[str, object]] = []
    ambiguities: list[dict[str, object]] = []
    unresolved: list[dict[str, object]] = []

    for term in terms:
        term_id = str(term["id"])
        language = str(term.get("language", ""))
        search_key = str(term.get("search_key", ""))
        if term.get("status") != "candidate":
            unresolved.append(_unresolved_record(term, "source_term_quarantined"))
            continue

        if term_id in direct_resolution:
            hit = direct_hits[term_id]
            bridges.append(_bridge_record(
                term,
                direct_resolution[term_id],
                method="exact_english_label",
                status="resolved_for_retrieval",
                matched_label=hit.label,
                matched_field=hit.field,
            ))
            continue

        if language == "en":
            english_hits = english_index.get(search_key, [])
            english_targets = _unique_targets(english_hits)
            if len(english_targets) > 1:
                ambiguities.append(_ambiguity_record(
                    term,
                    reason="canonical_english_label_collision",
                    targets=english_targets,
                    method="exact_english_label",
                ))
                continue
            alias_hits = alias_index.get(search_key, [])
            alias_targets = _unique_targets(alias_hits)
            if len(alias_targets) == 1:
                hit = alias_hits[0]
                candidates.append(_bridge_record(
                    term,
                    alias_targets[0],
                    method="exact_alias_unknown_language",
                    status="candidate",
                    matched_label=hit.label,
                    matched_field=hit.field,
                ))
                continue
            if len(alias_targets) > 1:
                ambiguities.append(_ambiguity_record(
                    term,
                    reason="canonical_alias_collision",
                    targets=alias_targets,
                    method="exact_alias_unknown_language",
                ))
                continue

        synset_target_map: dict[str, dict[str, object]] = {}
        matched_synsets: dict[str, list[str]] = {}
        for synset in sorted(str(value) for value in term.get("wordnet_synsets", [])):
            for target_id, anchor in synset_anchors.get(synset, {}).items():
                synset_target_map[target_id] = anchor
                matched_synsets.setdefault(target_id, []).append(synset)
        if len(synset_target_map) == 1:
            target_id, anchor = next(iter(sorted(synset_target_map.items())))
            source_type = str(term.get("entity_type_candidate") or "unknown")
            anchor_types = set(anchor["source_types"])
            target = anchor["target"]
            if source_type not in anchor_types:
                ambiguities.append(_ambiguity_record(
                    term,
                    reason="synset_crosses_odeuropa_types",
                    targets=[target],
                    method="shared_wordnet_synset",
                    details={
                        "matched_synsets": matched_synsets[target_id],
                        "source_type": source_type,
                        "anchor_source_types": sorted(anchor_types),
                    },
                ))
            else:
                candidates.append(_bridge_record(
                    term,
                    target,
                    method="shared_wordnet_synset",
                    status="candidate",
                    matched_synsets=matched_synsets[target_id],
                    anchor_term_ids=sorted(str(value) for value in anchor["term_ids"]),
                ))
            continue
        if len(synset_target_map) > 1:
            targets = [synset_target_map[key]["target"] for key in sorted(synset_target_map)]
            ambiguities.append(_ambiguity_record(
                term,
                reason="synset_maps_to_multiple_canonical_targets",
                targets=targets,
                method="shared_wordnet_synset",
                details={"matched_synsets_by_target": matched_synsets},
            ))
            continue

        cross_language_hits = all_labels_index.get(search_key, []) if language != "en" else []
        cross_language_targets = _unique_targets(cross_language_hits)
        if cross_language_targets:
            ambiguities.append(_ambiguity_record(
                term,
                reason="cross_language_homograph",
                targets=cross_language_targets,
                method="exact_cross_language_label",
                details={"language": language},
            ))
            continue

        unresolved.append(_unresolved_record(term, "no_supported_equivalence_evidence"))

    bridges.sort(key=lambda record: str(record["bridge_id"]))
    candidates.sort(key=lambda record: str(record["bridge_id"]))
    ambiguities.sort(key=lambda record: str(record["ambiguity_id"]))
    unresolved.sort(key=lambda record: (str(record["source_term"]["language"]), str(record["source_term"]["id"])))

    _audit_resolution_outputs(terms, bridges, candidates, ambiguities, unresolved)

    output_directory = staging / "equivalence"
    write_dicts_jsonl(output_directory / "resolved-retrieval-bridges.jsonl", bridges)
    write_dicts_jsonl(output_directory / "equivalence-candidates.jsonl", candidates)
    write_dicts_jsonl(output_directory / "ambiguities.jsonl", ambiguities)
    write_dicts_jsonl(output_directory / "unresolved.jsonl", unresolved)
    eligible_source_terms = sum(1 for term in terms if term.get("status") == "candidate")
    covered_terms = len(bridges) + len(candidates)
    try:
        taxonomy_locator = taxonomy_file.relative_to(data_directory).as_posix()
    except ValueError:
        taxonomy_locator = taxonomy_file.as_posix()
    report = {
        "schema_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": snapshot_id,
        "taxonomy_path": taxonomy_locator,
        "taxonomy_sha256": taxonomy_hash,
        "counts": {
            "source_terms": len(terms),
            "resolved_retrieval_bridges": len(bridges),
            "equivalence_candidates": len(candidates),
            "ambiguities": len(ambiguities),
            "unresolved": len(unresolved),
            "eligible_source_terms": eligible_source_terms,
            "source_terms_already_quarantined": len(terms) - eligible_source_terms,
            "covered_terms": covered_terms,
            "retrieval_coverage_percent": round(covered_terms * 100 / eligible_source_terms, 2) if eligible_source_terms else 0.0,
            "resolved_by_method": _count_by(bridges, lambda record: record["match"]["method"]),
            "candidates_by_method": _count_by(candidates, lambda record: record["match"]["method"]),
            "ambiguities_by_reason": _count_by(ambiguities, lambda record: record["reason"]),
            "covered_by_source_language": _count_by(
                bridges + candidates,
                lambda record: record["source_term"]["language"],
            ),
            "covered_by_target_type": _count_by(
                bridges + candidates,
                lambda record: record["target"]["type"],
            ),
        },
        "contract": {
            "scope": "retrieval_only",
            "semantic_identity": "unverified",
            "claim_nature": "inferred",
            "promotion_status": "blocked",
            "commercial_claims_generated": False,
            "forbidden_predicates": list(FORBIDDEN_PREDICATES),
            "automatic_resolution_rule": "unique exact English canonical label",
            "candidate_rules": ["exact alias with unknown language", "shared WordNet synset from a unique English anchor"],
            "ambiguity_rules": [
                "multiple canonical targets",
                "cross-language homograph without synset evidence",
                "shared synset crossing ODEUROPA entity types",
            ],
        },
        "files": {
            "resolved_retrieval_bridges": "resolved-retrieval-bridges.jsonl",
            "equivalence_candidates": "equivalence-candidates.jsonl",
            "ambiguities": "ambiguities.jsonl",
            "unresolved": "unresolved.jsonl",
        },
    }
    atomic_write_text(output_directory / "report.json", f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    atomic_write_text(
        output_directory / "manifest.json",
        f"{json.dumps({
            'schema_version': 1,
            'snapshot_id': snapshot_id,
            'taxonomy_sha256': taxonomy_hash,
            'resolution_id': sha256(canonical_json(report).encode('utf-8')).hexdigest(),
            'report': 'report.json',
        }, ensure_ascii=False, sort_keys=True, indent=2)}\n",
    )

    return OdeuropaEquivalenceResult(
        snapshot_id=snapshot_id,
        resolved_bridges=len(bridges),
        candidates=len(candidates),
        ambiguities=len(ambiguities),
        unresolved=len(unresolved),
        output_directory=output_directory,
    )
