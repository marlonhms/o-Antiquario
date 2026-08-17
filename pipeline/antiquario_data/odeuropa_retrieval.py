from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json
from .odeuropa import ATTRIBUTION, LICENSE_ID, SOURCE_ID, normalize_search_key


SUPPORTED_QUERY_LANGUAGES = {"de", "en", "fr", "it", "pt-BR"}


@dataclass(frozen=True)
class OdeuropaRetrievalBuildResult:
    index_id: str
    entries: int
    query_keys: int
    targets: int
    source_bridges: int
    retrieval_ready_targets: int
    evaluation_passed: bool | None
    output_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "index_id": self.index_id,
            "entries": self.entries,
            "query_keys": self.query_keys,
            "targets": self.targets,
            "source_bridges": self.source_bridges,
            "retrieval_ready_targets": self.retrieval_ready_targets,
            "evaluation_passed": self.evaluation_passed,
            "output_directory": self.output_directory.as_posix(),
            "scope": "retrieval_only",
            "candidate_bridges_included": 0,
        }


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


def _resolve_equivalence_directory(data_directory: Path, equivalence_directory: Path | None) -> Path:
    data_root = data_directory.resolve()
    if equivalence_directory is not None:
        resolved = equivalence_directory.resolve()
    else:
        latest_path = data_root / "staging" / "odeuropa" / "latest.json"
        if not latest_path.is_file():
            raise FileNotFoundError("staging ODEUROPA ausente; execute sync e resolve primeiro")
        latest = load_json(latest_path)
        relative = latest.get("staging_directory")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError("latest.json ODEUROPA inválido")
        resolved = (data_root / relative / "equivalence").resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError("diretório de equivalências precisa permanecer dentro de data")
    return resolved


def _compile_entries(bridges: list[dict[str, Any]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    targets_by_language_key: dict[tuple[str, str], set[str]] = {}
    for bridge in bridges:
        if bridge.get("status") != "resolved_for_retrieval":
            raise ValueError("índice aceita somente bridges com status resolved_for_retrieval")
        if bridge.get("scope") != "retrieval_only" or bridge.get("semantic_identity") != "unverified":
            raise ValueError("bridge fora do contrato seguro de recuperação")
        if bridge.get("promotion_status") != "blocked" or bridge.get("commercial_claims_generated") is not False:
            raise ValueError("bridge permite promoção ou claims comerciais")
        if "predicate" in bridge:
            raise ValueError("bridge de recuperação não pode conter predicado do grafo")

        source = bridge.get("source_term")
        target = bridge.get("target")
        evidence = bridge.get("evidence")
        match = bridge.get("match")
        if not all(isinstance(value, dict) for value in (source, target, evidence, match)):
            raise ValueError("bridge contém estrutura incompleta")
        language = str(source.get("language", ""))
        key = normalize_search_key(str(source.get("label_original", "")))
        target_id = str(target.get("id", ""))
        if language not in SUPPORTED_QUERY_LANGUAGES or not key or not target_id:
            raise ValueError("bridge contém idioma, termo ou destino inválido")
        targets_by_language_key.setdefault((language, key), set()).add(target_id)

        group_key = (language, key, target_id)
        group = grouped.setdefault(group_key, {
            "language": language,
            "key": key,
            "source_labels": set(),
            "source_term_ids": set(),
            "source_locators": set(),
            "bridge_ids": set(),
            "methods": set(),
            "target": target,
        })
        group["source_labels"].add(str(source["label_original"]))
        group["source_term_ids"].add(str(source["id"]))
        group["source_locators"].add(str(evidence["locator"]))
        group["bridge_ids"].add(str(bridge["bridge_id"]))
        group["methods"].add(str(match["method"]))

    collisions = {
        f"{language}:{key}": sorted(targets)
        for (language, key), targets in targets_by_language_key.items()
        if len(targets) > 1
    }
    if collisions:
        raise ValueError(f"índice contém chaves com múltiplos destinos: {canonical_json(collisions)}")

    entries: list[dict[str, object]] = []
    for (language, key, target_id), group in sorted(grouped.items()):
        target = group["target"]
        label_pt = str(target.get("label_pt", ""))
        label_en = str(target.get("label_en", ""))
        canonical_id = str(target.get("canonical_id", ""))
        expansions = [
            {"value": label_pt, "language": "pt-BR", "role": "canonical_label"},
            {"value": label_en, "language": "en", "role": "canonical_label"},
            {"value": canonical_id.replace("-", " "), "language": "und", "role": "canonical_id"},
        ]
        unique_expansions: dict[tuple[str, str], dict[str, str]] = {}
        for expansion in expansions:
            normalized = normalize_search_key(expansion["value"])
            if normalized:
                unique_expansions[(expansion["language"], normalized)] = expansion
        entries.append({
            "entry_id": f"odeuropa:retrieval-entry:{sha256(f'{language}\0{key}\0{target_id}'.encode('utf-8')).hexdigest()[:20]}",
            "language": language,
            "key": key,
            "token_count": len(key.split()),
            "source_labels": sorted(group["source_labels"], key=lambda value: (normalize_search_key(value), value)),
            "target": target,
            "expansions": [unique_expansions[item] for item in sorted(unique_expansions)],
            "scope": "retrieval_only",
            "semantic_identity": "unverified",
            "claim_nature": "inferred",
            "status": "active",
            "provenance": {
                "source_id": SOURCE_ID,
                "license": LICENSE_ID,
                "attribution": ATTRIBUTION,
                "bridge_ids": sorted(group["bridge_ids"]),
                "source_term_ids": sorted(group["source_term_ids"]),
                "locators": sorted(group["source_locators"]),
                "methods": sorted(group["methods"]),
            },
        })
    return entries


def _attach_knowledge_routes(
    entries: list[dict[str, object]],
    knowledge_directory: Path,
) -> dict[str, object]:
    documents_path = knowledge_directory / "documents.json"
    chunks_path = knowledge_directory / "chunks.json"
    manifest_path = knowledge_directory / "knowledge-manifest.json"
    if not documents_path.is_file() or not chunks_path.is_file() or not manifest_path.is_file():
        raise FileNotFoundError(f"Knowledge Core compilado incompleto em {knowledge_directory}")
    documents = load_json(documents_path)
    chunks = load_json(chunks_path)
    manifest = load_json(manifest_path)
    if not isinstance(documents, list) or not isinstance(chunks, list) or not isinstance(manifest, dict):
        raise ValueError("artefatos compilados do Knowledge Core possuem formato inválido")
    document_ids = {
        str(document["id"])
        for document in documents
        if isinstance(document, dict) and isinstance(document.get("id"), str)
    }
    chunks_by_document: dict[str, list[str]] = {}
    document_label_index: dict[tuple[str, str], set[str]] = {}
    for document in documents:
        if not isinstance(document, dict):
            continue
        document_id = document.get("id")
        document_type = document.get("type")
        title = document.get("title")
        aliases = document.get("aliases", [])
        if not isinstance(document_id, str) or not isinstance(document_type, str) or not isinstance(title, str):
            continue
        if not isinstance(aliases, list):
            raise ValueError(f"documento {document_id} contém aliases inválidos")
        labels = [document_id.rsplit(":", 1)[-1], title, *(str(alias) for alias in aliases)]
        for label in labels:
            normalized = normalize_search_key(label)
            if normalized:
                document_label_index.setdefault((document_type, normalized), set()).add(document_id)
    for chunk in chunks:
        if not isinstance(chunk, dict) or not isinstance(chunk.get("id"), str) or not isinstance(chunk.get("documentId"), str):
            raise ValueError("Knowledge Core contém chunk inválido")
        chunks_by_document.setdefault(str(chunk["documentId"]), []).append(str(chunk["id"]))

    routed_targets: set[str] = set()
    routed_chunks: set[str] = set()
    route_status_counts: dict[str, int] = {}
    for entry in entries:
        target = entry["target"]
        target_id = str(target["id"])
        target_type = str(target["type"])
        candidate_document_ids: set[str] = set()
        matched_labels: set[str] = set()
        route_method = "none"
        if target_id in document_ids:
            candidate_document_ids.add(target_id)
            resolved_document_id = target_id
            chunk_ids = sorted(chunks_by_document.get(target_id, []))
            route_status = "direct" if chunk_ids else "document_without_chunks"
            route_method = "direct_id"
        else:
            for label in (target.get("canonical_id"), target.get("label_pt"), target.get("label_en")):
                normalized = normalize_search_key(str(label or ""))
                matches = document_label_index.get((target_type, normalized), set())
                if matches:
                    matched_labels.add(str(label))
                    candidate_document_ids.update(matches)
            if len(candidate_document_ids) == 1:
                resolved_document_id = next(iter(candidate_document_ids))
                chunk_ids = sorted(chunks_by_document.get(resolved_document_id, []))
                route_status = "reconciled" if chunk_ids else "document_without_chunks"
                route_method = "exact_same_type_label"
            elif len(candidate_document_ids) > 1:
                resolved_document_id = None
                chunk_ids = []
                route_status = "ambiguous_document_match"
                route_method = "exact_same_type_label"
            else:
                resolved_document_id = None
                chunk_ids = []
                route_status = "missing_document"
        ready = bool(chunk_ids)
        if ready:
            routed_targets.add(target_id)
            routed_chunks.update(chunk_ids)
        route_status_counts[route_status] = route_status_counts.get(route_status, 0) + 1
        entry["retrieval"] = {
            "knowledge_document_available": bool(candidate_document_ids),
            "retrieval_ready": ready,
            "route_status": route_status,
            "route_method": route_method,
            "document_id": resolved_document_id,
            "candidate_document_ids": sorted(candidate_document_ids),
            "matched_canonical_labels": sorted(matched_labels, key=lambda value: (normalize_search_key(value), value)),
            "chunk_ids": chunk_ids,
        }
    return {
        "knowledge_release_id": manifest.get("releaseId"),
        "knowledge_content_hash": manifest.get("contentHash"),
        "targets_with_documents_and_chunks": len(routed_targets),
        "routed_chunks": len(routed_chunks),
        "route_status_counts": dict(sorted(route_status_counts.items())),
    }


def _compile_query_keys(
    entries: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    proposals: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}

    def add(entry: dict[str, object], language: str, value: str, origin: str) -> None:
        key = normalize_search_key(value)
        if not key:
            return
        target = entry["target"]
        target_id = str(target["id"])
        target_map = proposals.setdefault((language, key), {})
        proposal = target_map.setdefault(target_id, {
            "target": target,
            "entry_ids": set(),
            "origins": set(),
            "source_values": set(),
            "expansions": entry["expansions"],
            "retrieval": entry["retrieval"],
        })
        proposal["entry_ids"].add(str(entry["entry_id"]))
        proposal["origins"].add(origin)
        proposal["source_values"].add(value)

    for entry in entries:
        add(entry, str(entry["language"]), str(entry["key"]), "odeuropa_resolved_bridge")
        target = entry["target"]
        add(entry, "pt-BR", str(target["label_pt"]), "canonical_taxonomy_label")
        add(entry, "en", str(target["label_en"]), "canonical_taxonomy_label")

    query_keys: list[dict[str, object]] = []
    collisions: list[dict[str, object]] = []
    for (language, key), target_map in sorted(proposals.items()):
        if len(target_map) > 1:
            collisions.append({
                "language": language,
                "key": key,
                "target_ids": sorted(target_map),
                "reason": "canonical_query_key_maps_to_multiple_targets",
                "status": "blocked",
            })
            continue
        target_id, proposal = next(iter(target_map.items()))
        origins = sorted(proposal["origins"])
        query_keys.append({
            "query_key_id": f"odeuropa:query-key:{sha256(f'{language}\0{key}\0{target_id}'.encode('utf-8')).hexdigest()[:20]}",
            "language": language,
            "key": key,
            "token_count": len(key.split()),
            "target": proposal["target"],
            "expansions": proposal["expansions"],
            "entry_ids": sorted(proposal["entry_ids"]),
            "origins": origins,
            "source_values": sorted(proposal["source_values"], key=lambda value: (normalize_search_key(value), value)),
            "scope": "retrieval_only",
            "semantic_identity": "canonical" if "canonical_taxonomy_label" in origins else "unverified",
            "retrieval": proposal["retrieval"],
            "status": "active",
        })
    return query_keys, collisions


def _validate_index(index: dict[str, Any]) -> list[dict[str, Any]]:
    if index.get("schema_version") != 1 or index.get("scope") != "retrieval_only":
        raise ValueError("índice ODEUROPA possui schema ou escopo inválido")
    entries = index.get("entries")
    query_keys = index.get("query_keys")
    if not isinstance(entries, list) or not isinstance(query_keys, list):
        raise ValueError("índice ODEUROPA não contém entries")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("entrada do índice precisa ser objeto")
        language = str(entry.get("language", ""))
        key = str(entry.get("key", ""))
        if language not in SUPPORTED_QUERY_LANGUAGES or not key:
            raise ValueError("entrada do índice contém idioma ou chave inválida")
        if entry.get("scope") != "retrieval_only" or entry.get("semantic_identity") != "unverified":
            raise ValueError("entrada do índice viola contrato semântico")
        target = entry.get("target")
        if not isinstance(target, dict) or target.get("type") == "fragrance":
            raise ValueError("entrada do índice possui destino inválido")
        retrieval = entry.get("retrieval")
        if not isinstance(retrieval, dict) or not isinstance(retrieval.get("chunk_ids"), list):
            raise ValueError("entrada do índice não contém rota de recuperação válida")
        if retrieval.get("retrieval_ready") != bool(retrieval["chunk_ids"]):
            raise ValueError("estado retrieval_ready diverge dos chunks disponíveis")
    seen: set[tuple[str, str]] = set()
    validated: list[dict[str, Any]] = []
    for query_key in query_keys:
        if not isinstance(query_key, dict):
            raise ValueError("query key precisa ser objeto")
        language = str(query_key.get("language", ""))
        key = str(query_key.get("key", ""))
        signature = (language, key)
        if language not in SUPPORTED_QUERY_LANGUAGES or not key or signature in seen:
            raise ValueError(f"query key inválida ou duplicada: {language}:{key}")
        seen.add(signature)
        if query_key.get("scope") != "retrieval_only" or query_key.get("semantic_identity") not in {"canonical", "unverified"}:
            raise ValueError("query key viola contrato semântico")
        target = query_key.get("target")
        retrieval = query_key.get("retrieval")
        if not isinstance(target, dict) or target.get("type") == "fragrance" or not isinstance(retrieval, dict):
            raise ValueError("query key contém destino ou rota inválida")
        validated.append(query_key)
    return validated


def expand_odeuropa_query(index: dict[str, Any], query: str, *, language: str) -> dict[str, object]:
    if language not in SUPPORTED_QUERY_LANGUAGES:
        raise ValueError(f"idioma de consulta não suportado: {language}")
    query_keys = _validate_index(index)
    normalized_query = normalize_search_key(query)
    tokens = normalized_query.split()
    by_key = {
        str(entry["key"]): entry
        for entry in query_keys
        if entry["language"] == language
    }
    max_tokens = max((int(entry["token_count"]) for entry in by_key.values()), default=0)
    matches: list[dict[str, object]] = []
    position = 0
    while position < len(tokens):
        matched_entry: dict[str, Any] | None = None
        matched_length = 0
        for length in range(min(max_tokens, len(tokens) - position), 0, -1):
            phrase = " ".join(tokens[position:position + length])
            entry = by_key.get(phrase)
            if entry is not None:
                matched_entry = entry
                matched_length = length
                break
        if matched_entry is None:
            position += 1
            continue
        matches.append({
            "query_term": matched_entry["key"],
            "token_start": position,
            "token_end": position + matched_length,
            "query_key_id": matched_entry["query_key_id"],
            "origins": matched_entry["origins"],
            "target": matched_entry["target"],
            "expansions": matched_entry["expansions"],
            "scope": "retrieval_only",
        })
        position += matched_length

    targets: dict[str, dict[str, object]] = {}
    routes: dict[str, dict[str, object]] = {}
    expansion_terms: set[str] = set()
    for match in matches:
        target = match["target"]
        target_id = str(target["id"])
        targets[target_id] = target
        entry = by_key[str(match["query_term"])]
        retrieval = entry["retrieval"]
        if retrieval["retrieval_ready"]:
            routes[target_id] = {
                "target_id": target_id,
                "document_id": retrieval["document_id"],
                "chunk_ids": retrieval["chunk_ids"],
            }
        for expansion in match["expansions"]:
            normalized = normalize_search_key(str(expansion["value"]))
            if normalized:
                expansion_terms.add(normalized)
    return {
        "query": query,
        "normalized_query": normalized_query,
        "query_language": language,
        "matches": matches,
        "canonical_targets": [targets[key] for key in sorted(targets)],
        "retrieval_routes": [routes[key] for key in sorted(routes)],
        "unroutable_target_ids": sorted(set(targets) - set(routes)),
        "expanded_terms": sorted(expansion_terms),
        "scope": "retrieval_only",
        "facts_generated": False,
    }


def evaluate_odeuropa_retrieval(index: dict[str, Any], gold_path: Path) -> dict[str, object]:
    gold = _load_yaml(gold_path)
    if gold.get("schema_version") != 1 or not isinstance(gold.get("cases"), list):
        raise ValueError("conjunto ouro ODEUROPA inválido")
    thresholds = gold.get("thresholds", {})
    if not isinstance(thresholds, dict):
        raise ValueError("thresholds do conjunto ouro precisam ser objeto")

    results: list[dict[str, object]] = []
    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0
    safety_violations = 0
    expected_target_occurrences = 0
    routed_expected_occurrences = 0
    seen_case_ids: set[str] = set()
    for case in gold["cases"]:
        if not isinstance(case, dict):
            raise ValueError("caso ouro precisa ser objeto")
        case_id = str(case.get("id", ""))
        query = str(case.get("query", ""))
        language = str(case.get("language", ""))
        expected_raw = case.get("expected_target_ids", [])
        forbidden_raw = case.get("forbidden_target_ids", [])
        if not case_id or case_id in seen_case_ids or not query:
            raise ValueError("caso ouro contém ID vazio/duplicado ou consulta vazia")
        if not isinstance(expected_raw, list) or not isinstance(forbidden_raw, list):
            raise ValueError(f"caso ouro {case_id} possui listas de destino inválidas")
        seen_case_ids.add(case_id)
        expected = {str(value) for value in expected_raw}
        forbidden = {str(value) for value in forbidden_raw}
        expansion = expand_odeuropa_query(index, query, language=language)
        predicted = {str(target["id"]) for target in expansion["canonical_targets"]}
        true_positive = predicted & expected
        false_positive = predicted - expected
        false_negative = expected - predicted
        forbidden_hits = predicted & forbidden
        routed = {str(route["target_id"]) for route in expansion["retrieval_routes"]}
        total_true_positive += len(true_positive)
        total_false_positive += len(false_positive)
        total_false_negative += len(false_negative)
        safety_violations += len(forbidden_hits)
        expected_target_occurrences += len(expected)
        routed_expected_occurrences += len(expected & routed)
        results.append({
            "id": case_id,
            "query": query,
            "language": language,
            "expected_target_ids": sorted(expected),
            "predicted_target_ids": sorted(predicted),
            "false_positive_ids": sorted(false_positive),
            "false_negative_ids": sorted(false_negative),
            "forbidden_hits": sorted(forbidden_hits),
            "routed_expected_target_ids": sorted(expected & routed),
            "unroutable_expected_target_ids": sorted(expected - routed),
            "exact_match": predicted == expected,
        })

    precision = (
        total_true_positive / (total_true_positive + total_false_positive)
        if total_true_positive + total_false_positive
        else 1.0
    )
    recall = (
        total_true_positive / (total_true_positive + total_false_negative)
        if total_true_positive + total_false_negative
        else 1.0
    )
    exact_accuracy = sum(1 for result in results if result["exact_match"]) / len(results) if results else 0.0
    route_coverage = routed_expected_occurrences / expected_target_occurrences if expected_target_occurrences else 1.0
    precision_min = float(thresholds.get("precision_min", 1.0))
    recall_min = float(thresholds.get("recall_min", 1.0))
    exact_min = float(thresholds.get("exact_match_accuracy_min", 1.0))
    max_safety = int(thresholds.get("max_safety_violations", 0))
    route_coverage_min = float(thresholds.get("route_coverage_min", 0.0))
    passed = (
        precision >= precision_min
        and recall >= recall_min
        and exact_accuracy >= exact_min
        and safety_violations <= max_safety
        and route_coverage >= route_coverage_min
    )
    return {
        "schema_version": 1,
        "gold_set": gold_path.as_posix(),
        "cases": len(results),
        "metrics": {
            "micro_precision": round(precision, 6),
            "micro_recall": round(recall, 6),
            "exact_match_accuracy": round(exact_accuracy, 6),
            "safety_violations": safety_violations,
            "knowledge_route_coverage": round(route_coverage, 6),
        },
        "thresholds": {
            "precision_min": precision_min,
            "recall_min": recall_min,
            "exact_match_accuracy_min": exact_min,
            "max_safety_violations": max_safety,
            "route_coverage_min": route_coverage_min,
        },
        "passed": passed,
        "results": results,
    }


def build_odeuropa_retrieval_index(
    data_directory: Path,
    *,
    equivalence_directory: Path | None = None,
    gold_path: Path | None = None,
    knowledge_directory: Path | None = None,
) -> OdeuropaRetrievalBuildResult:
    data_directory = data_directory.resolve()
    equivalence = _resolve_equivalence_directory(data_directory, equivalence_directory)
    bridge_path = equivalence / "resolved-retrieval-bridges.jsonl"
    equivalence_manifest_path = equivalence / "manifest.json"
    equivalence_report_path = equivalence / "report.json"
    if not bridge_path.is_file() or not equivalence_manifest_path.is_file() or not equivalence_report_path.is_file():
        raise FileNotFoundError("equivalências ODEUROPA incompletas; execute odeuropa-resolve primeiro")
    bridges = _load_jsonl(bridge_path)
    equivalence_manifest = load_json(equivalence_manifest_path)
    equivalence_report = load_json(equivalence_report_path)
    if equivalence_report.get("counts", {}).get("equivalence_candidates", 0) < 0:
        raise ValueError("relatório de equivalências inválido")
    entries = _compile_entries(bridges)
    resolved_knowledge_directory = (
        knowledge_directory.resolve()
        if knowledge_directory is not None
        else (data_directory.parent / "knowledge" / "compiled").resolve()
    )
    knowledge_routes = _attach_knowledge_routes(entries, resolved_knowledge_directory)
    query_keys, query_key_collisions = _compile_query_keys(entries)
    entry_hash = sha256(canonical_json({"entries": entries, "query_keys": query_keys}).encode("utf-8")).hexdigest()
    index_id = f"odeuropa-retrieval-v1-{entry_hash[:12]}"
    index = {
        "schema_version": 1,
        "index_id": index_id,
        "source_id": SOURCE_ID,
        "source_snapshot_id": equivalence_manifest.get("snapshot_id"),
        "resolution_id": equivalence_manifest.get("resolution_id"),
        "taxonomy_sha256": equivalence_manifest.get("taxonomy_sha256"),
        "knowledge_release_id": knowledge_routes["knowledge_release_id"],
        "knowledge_content_hash": knowledge_routes["knowledge_content_hash"],
        "scope": "retrieval_only",
        "semantic_identity": "unverified",
        "candidate_bridges_included": 0,
        "counts": {
            "source_bridges": len(bridges),
            "entries": len(entries),
            "query_keys": len(query_keys),
            "query_key_collisions": len(query_key_collisions),
            "targets": len({str(entry["target"]["id"]) for entry in entries}),
            "source_languages": len({str(entry["language"]) for entry in entries}),
            "query_languages": len({str(query_key["language"]) for query_key in query_keys}),
            "retrieval_ready_targets": knowledge_routes["targets_with_documents_and_chunks"],
            "routed_chunks": knowledge_routes["routed_chunks"],
            "route_status": knowledge_routes["route_status_counts"],
        },
        "entries": entries,
        "query_keys": query_keys,
        "query_key_collisions": query_key_collisions,
    }
    _validate_index(index)

    output_directory = equivalence / "retrieval"
    atomic_write_text(output_directory / "index.json", f"{json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    routing_gaps = [
        {
            "target": entry["target"],
            "retrieval": entry["retrieval"],
            "source_entry_id": entry["entry_id"],
            "status": "blocked_until_retrievable_content",
        }
        for entry in entries
        if not entry["retrieval"]["retrieval_ready"]
    ]
    write_dicts_jsonl(output_directory / "routing-gaps.jsonl", routing_gaps)
    resolved_gold = gold_path.resolve() if gold_path else None
    evaluation: dict[str, object] | None = None
    if resolved_gold is not None:
        evaluation = evaluate_odeuropa_retrieval(index, resolved_gold)
        atomic_write_text(
            output_directory / "evaluation.json",
            f"{json.dumps(evaluation, ensure_ascii=False, sort_keys=True, indent=2)}\n",
        )
    manifest = {
        "schema_version": 1,
        "index_id": index_id,
        "content_sha256": sha256(canonical_json(index).encode("utf-8")).hexdigest(),
        "source_snapshot_id": index["source_snapshot_id"],
        "resolution_id": index["resolution_id"],
        "taxonomy_sha256": index["taxonomy_sha256"],
        "knowledge_release_id": index["knowledge_release_id"],
        "knowledge_content_hash": index["knowledge_content_hash"],
        "scope": "retrieval_only",
        "candidate_bridges_included": 0,
        "evaluation_passed": evaluation["passed"] if evaluation is not None else None,
        "files": {
            "index": "index.json",
            "evaluation": "evaluation.json" if evaluation is not None else None,
            "routing_gaps": "routing-gaps.jsonl",
        },
    }
    atomic_write_text(output_directory / "manifest.json", f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return OdeuropaRetrievalBuildResult(
        index_id=index_id,
        entries=len(entries),
        query_keys=len(query_keys),
        targets=int(index["counts"]["targets"]),
        source_bridges=len(bridges),
        retrieval_ready_targets=int(index["counts"]["retrieval_ready_targets"]),
        evaluation_passed=bool(evaluation["passed"]) if evaluation is not None else None,
        output_directory=output_directory,
    )


def load_latest_odeuropa_retrieval_index(data_directory: Path) -> dict[str, Any]:
    equivalence = _resolve_equivalence_directory(data_directory.resolve(), None)
    index_path = equivalence / "retrieval" / "index.json"
    if not index_path.is_file():
        raise FileNotFoundError("índice de recuperação ODEUROPA ausente; execute odeuropa-index primeiro")
    index = load_json(index_path)
    _validate_index(index)
    return index
