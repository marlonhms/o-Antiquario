from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json


DECLARED_NOTE_PREDICATES = {
    "has-top-note": "saída",
    "has-heart-note": "coração",
    "has-base-note": "fundo",
    "has-note": "sem camada",
}
SECTION_MARKER = "<!-- antiquario:auto-factual-coverage:v1 -->"


@dataclass(frozen=True)
class EnrichmentPlanResult:
    plan_id: str
    candidates: int
    eligible: int
    blocked: int
    output_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "candidates": self.candidates,
            "eligible": self.eligible,
            "blocked": self.blocked,
            "output_directory": self.output_directory.as_posix(),
            "knowledge_core_mutated": False,
            "relations_generated": 0,
            "sensory_claims_generated": False,
        }


@dataclass(frozen=True)
class EnrichmentPromotionResult:
    plan_id: str
    promoted: int
    skipped: int
    blocked: int
    report_path: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "promoted": self.promoted,
            "skipped": self.skipped,
            "blocked": self.blocked,
            "report_path": self.report_path.as_posix(),
            "relations_generated": 0,
            "sensory_claims_generated": False,
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
        latest = load_json(data_root / "staging" / "odeuropa" / "latest.json")
        relative = latest.get("staging_directory")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError("latest.json ODEUROPA inválido")
        resolved = (data_root / relative / "equivalence" / "retrieval").resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError("diretório de recuperação precisa permanecer dentro de data")
    return resolved


def _allowed_core_sources(source_manifest: dict[str, Any]) -> set[str]:
    sources = source_manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifesto de fontes inválido")
    return {
        str(source["id"])
        for source in sources
        if isinstance(source, dict)
        and source.get("classification") == "allowed_core"
        and isinstance(source.get("id"), str)
    }


def _source_evidence(document: dict[str, Any]) -> list[dict[str, object]]:
    evidence = document.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError(f"documento {document.get('id')} não possui evidência")
    result: list[dict[str, object]] = []
    for item in evidence:
        if not isinstance(item, dict) or not isinstance(item.get("source_id"), str):
            raise ValueError(f"documento {document.get('id')} possui evidência inválida")
        result.append({
            "source_id": item["source_id"],
            "license": item.get("license"),
            "confidence": item.get("confidence"),
            "claim_scope": item.get("claim_scope"),
            "locator": item.get("locator") or f"knowledge/vault/{document['path']}#relations",
        })
    return result


def _build_section(
    document: dict[str, Any],
    declarations: list[dict[str, Any]],
    knowledge_release_id: str,
) -> str:
    position_counts = Counter(DECLARED_NOTE_PREDICATES[item["predicate"]] for item in declarations)
    ordered_positions = ["saída", "coração", "fundo", "sem camada"]
    position_lines = [
        f"- {position}: {position_counts[position]}"
        for position in ordered_positions
        if position_counts[position]
    ]
    examples = sorted(
        declarations,
        key=lambda item: (str(item["fragrance"]["title"]), str(item["fragrance"]["id"]), str(item["predicate"])),
    )[:5]
    example_lines = [
        f"- [[{Path(str(item['fragrance']['path'])).stem}|{item['fragrance']['title']}]] — "
        f"{DECLARED_NOTE_PREDICATES[item['predicate']]}"
        for item in examples
    ]
    title = str(document["title"])
    return "\n".join([
        SECTION_MARKER,
        "## Cobertura factual no grafo",
        "",
        f"No release `{knowledge_release_id}`, **{title}** aparece em "
        f"{len({item['fragrance']['id'] for item in declarations})} fragrância(s) com declaração de pirâmide "
        "proveniente de fonte já aprovada pelo projeto.",
        "",
        *position_lines,
        "",
        "### Exemplos rastreáveis",
        "",
        *example_lines,
        "",
        "### Limite da automação",
        "",
        "Esta seção resume relações que já existiam no grafo. Ela não cria notas, não comprova ingrediente físico "
        "e não estima cheiro, concentração, intensidade, fixação, projeção ou evolução temporal.",
    ])


def audit_enrichment_candidates(
    candidates: list[dict[str, Any]],
    *,
    allowed_core_sources: set[str] | None = None,
) -> dict[str, object]:
    issues: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        if not candidate_id or candidate_id in seen_ids:
            issues.append({"candidate_id": candidate_id, "code": "duplicate_or_empty_candidate_id"})
        seen_ids.add(candidate_id)
        if candidate.get("schema_version") != 1 or candidate.get("status") != "candidate":
            issues.append({"candidate_id": candidate_id, "code": "invalid_candidate_contract"})
        target = candidate.get("target_document")
        proposal = candidate.get("proposal")
        provenance = candidate.get("provenance")
        safety = candidate.get("safety")
        if not all(isinstance(value, dict) for value in (target, proposal, provenance, safety)):
            issues.append({"candidate_id": candidate_id, "code": "incomplete_candidate_structure"})
            continue
        if target.get("type") != "olfactory-note" or candidate.get("backlog_tier") != "P3":
            issues.append({"candidate_id": candidate_id, "code": "unsupported_target_or_tier"})
        if proposal.get("relations_to_add") != []:
            issues.append({"candidate_id": candidate_id, "code": "relations_must_remain_empty"})
        section = proposal.get("markdown_section")
        if not isinstance(section, str) or not section.startswith(SECTION_MARKER):
            issues.append({"candidate_id": candidate_id, "code": "invalid_markdown_section"})
        declarations = provenance.get("declared_relations")
        if not isinstance(declarations, list) or not declarations:
            issues.append({"candidate_id": candidate_id, "code": "missing_declared_relations"})
        else:
            for declaration in declarations:
                if not isinstance(declaration, dict):
                    issues.append({"candidate_id": candidate_id, "code": "invalid_declaration"})
                    continue
                if declaration.get("predicate") not in DECLARED_NOTE_PREDICATES:
                    issues.append({"candidate_id": candidate_id, "code": "unsupported_predicate"})
                if declaration.get("origin") != "frontmatter" or declaration.get("claim_nature") != "declared":
                    issues.append({"candidate_id": candidate_id, "code": "non_declared_relation"})
                evidence = declaration.get("evidence")
                if not isinstance(evidence, list) or not evidence:
                    issues.append({"candidate_id": candidate_id, "code": "missing_declaration_evidence"})
                elif allowed_core_sources is not None:
                    source_ids = {str(item.get("source_id")) for item in evidence if isinstance(item, dict)}
                    if not source_ids or not source_ids <= allowed_core_sources:
                        issues.append({"candidate_id": candidate_id, "code": "source_not_allowed_core"})
        expected_false = (
            "relations_generated",
            "sensory_claims_generated",
            "performance_claims_generated",
            "chemical_identity_generated",
            "odeuropa_used_as_factual_evidence",
        )
        if any(safety.get(key) is not False for key in expected_false):
            issues.append({"candidate_id": candidate_id, "code": "unsafe_generation_flag"})
        raw_hash = target.get("raw_file_sha256")
        if not isinstance(raw_hash, str) or re.fullmatch(r"[a-f0-9]{64}", raw_hash) is None:
            issues.append({"candidate_id": candidate_id, "code": "invalid_precondition_hash"})
    return {
        "schema_version": 1,
        "candidates": len(candidates),
        "issues": issues,
        "passed": not issues,
    }


def build_knowledge_enrichment_plan(
    data_directory: Path,
    *,
    retrieval_directory: Path | None = None,
    knowledge_directory: Path | None = None,
    vault_directory: Path | None = None,
    source_manifest_path: Path | None = None,
) -> EnrichmentPlanResult:
    data_directory = data_directory.resolve()
    retrieval = _resolve_retrieval_directory(data_directory, retrieval_directory)
    knowledge = (knowledge_directory or data_directory.parent / "knowledge" / "compiled").resolve()
    vault = (vault_directory or data_directory.parent / "knowledge" / "vault").resolve()
    source_manifest = (source_manifest_path or data_directory / "sources.yml").resolve()
    allowed_sources = _allowed_core_sources(_load_yaml(source_manifest))

    backlog = _load_jsonl(retrieval / "routing-backlog.jsonl")
    documents_raw = load_json(knowledge / "documents.json")
    graph = load_json(knowledge / "graph.json")
    knowledge_manifest = load_json(knowledge / "knowledge-manifest.json")
    if not isinstance(documents_raw, list) or not isinstance(graph, dict) or not isinstance(knowledge_manifest, dict):
        raise ValueError("Knowledge Core compilado inválido")
    documents = {
        str(document["id"]): document
        for document in documents_raw
        if isinstance(document, dict) and isinstance(document.get("id"), str)
    }
    edges = graph.get("edges")
    if not isinstance(edges, list):
        raise ValueError("grafo compilado não contém edges")

    candidates: list[dict[str, Any]] = []
    for backlog_item in sorted(backlog, key=lambda item: int(item.get("rank", 0))):
        if backlog_item.get("priority", {}).get("tier") != "P3":
            continue
        gap = backlog_item.get("gap")
        if not isinstance(gap, dict) or gap.get("route_status") != "document_without_chunks":
            raise ValueError("item P3 fora do contrato document_without_chunks")
        document_id = gap.get("document_id")
        if not isinstance(document_id, str) or document_id not in documents:
            raise ValueError("item P3 não possui documento compilado")
        document = documents[document_id]
        if document.get("type") != "olfactory-note":
            raise ValueError(f"automação P3 não suporta o tipo {document.get('type')}")
        document_sources = {str(value) for value in document.get("source_ids", [])}
        if not document_sources or not document_sources <= allowed_sources:
            raise ValueError(f"documento {document_id} usa fonte fora de allowed_core")
        raw_path = (vault / str(document["path"])).resolve()
        if not raw_path.is_relative_to(vault) or not raw_path.is_file():
            raise ValueError(f"caminho de vault inválido para {document_id}")
        raw_bytes = raw_path.read_bytes()
        raw_text = raw_bytes.decode("utf-8")
        if SECTION_MARKER in raw_text:
            raise ValueError(f"documento {document_id} já contém cobertura factual automatizada")

        declarations: list[dict[str, Any]] = []
        for edge in edges:
            if not isinstance(edge, dict):
                raise ValueError("grafo contém aresta inválida")
            if edge.get("target") != document_id or edge.get("predicate") not in DECLARED_NOTE_PREDICATES:
                continue
            if edge.get("origin") != "frontmatter":
                continue
            fragrance_id = edge.get("source")
            fragrance = documents.get(str(fragrance_id))
            if fragrance is None or fragrance.get("type") != "fragrance":
                raise ValueError(f"declaração de {document_id} não parte de uma fragrância")
            fragrance_sources = {str(value) for value in fragrance.get("source_ids", [])}
            if not fragrance_sources or not fragrance_sources <= allowed_sources:
                raise ValueError(f"fragrância {fragrance_id} usa fonte fora de allowed_core")
            declarations.append({
                "claim_id": f"knowledge:declared-relation:{sha256(canonical_json(edge).encode('utf-8')).hexdigest()[:20]}",
                "claim_nature": "declared",
                "origin": "frontmatter",
                "predicate": edge["predicate"],
                "target_document_id": document_id,
                "fragrance": {
                    "id": fragrance["id"],
                    "title": fragrance["title"],
                    "path": fragrance["path"],
                },
                "evidence": _source_evidence(fragrance),
            })
        declarations.sort(key=lambda item: (str(item["fragrance"]["id"]), str(item["predicate"])))
        if not declarations:
            raise ValueError(f"documento {document_id} não possui declarações aprovadas")

        section = _build_section(document, declarations, str(knowledge_manifest.get("releaseId")))
        candidate_id = f"antiquario:enrichment-candidate:{sha256(f'{document_id}\0{section}'.encode('utf-8')).hexdigest()[:20]}"
        candidates.append({
            "schema_version": 1,
            "candidate_id": candidate_id,
            "status": "candidate",
            "backlog_item_id": backlog_item.get("backlog_item_id"),
            "backlog_tier": "P3",
            "target_document": {
                "id": document_id,
                "type": document["type"],
                "title": document["title"],
                "path": document["path"],
                "content_hash": document.get("contentHash"),
                "raw_file_sha256": sha256(raw_bytes).hexdigest(),
            },
            "proposal": {
                "operation": "append_factual_coverage_section",
                "markdown_section": section,
                "relations_to_add": [],
                "updated_at_required": True,
            },
            "provenance": {
                "knowledge_release_id": knowledge_manifest.get("releaseId"),
                "declared_relations": declarations,
                "method": "deterministic_aggregation_of_approved_frontmatter_relations",
            },
            "safety": {
                "relations_generated": False,
                "sensory_claims_generated": False,
                "performance_claims_generated": False,
                "chemical_identity_generated": False,
                "odeuropa_used_as_factual_evidence": False,
            },
            "promotion": {
                "status": "eligible_after_audit",
                "requires_matching_raw_file_sha256": True,
                "requires_allowed_core_sources": True,
            },
        })

    audit = audit_enrichment_candidates(candidates, allowed_core_sources=allowed_sources)
    audit_issues_by_candidate = Counter(str(issue["candidate_id"]) for issue in audit["issues"])
    for candidate in candidates:
        candidate["audit"] = {
            "status": "passed" if not audit_issues_by_candidate[candidate["candidate_id"]] else "blocked",
            "issue_count": audit_issues_by_candidate[candidate["candidate_id"]],
        }
    content_hash = sha256(canonical_json(candidates).encode("utf-8")).hexdigest()
    plan_id = f"knowledge-enrichment-v1-{content_hash[:12]}"
    output_directory = retrieval / "enrichment"
    write_dicts_jsonl(output_directory / "candidates.jsonl", candidates)
    atomic_write_text(output_directory / "audit.json", f"{json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    report = {
        "schema_version": 1,
        "plan_id": plan_id,
        "knowledge_release_id": knowledge_manifest.get("releaseId"),
        "counts": {
            "candidates": len(candidates),
            "eligible": sum(1 for candidate in candidates if candidate["audit"]["status"] == "passed"),
            "blocked": sum(1 for candidate in candidates if candidate["audit"]["status"] == "blocked"),
            "declared_relations_reused": sum(len(candidate["provenance"]["declared_relations"]) for candidate in candidates),
            "relations_generated": 0,
        },
        "safety": {
            "knowledge_core_mutated": False,
            "odeuropa_used_as_factual_evidence": False,
            "sensory_claims_generated": False,
            "performance_claims_generated": False,
        },
        "items": [
            {
                "candidate_id": candidate["candidate_id"],
                "document_id": candidate["target_document"]["id"],
                "title": candidate["target_document"]["title"],
                "path": candidate["target_document"]["path"],
                "declared_relations": len(candidate["provenance"]["declared_relations"]),
                "audit_status": candidate["audit"]["status"],
            }
            for candidate in candidates
        ],
    }
    atomic_write_text(output_directory / "report.json", f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    manifest = {
        "schema_version": 1,
        "plan_id": plan_id,
        "content_sha256": content_hash,
        "knowledge_release_id": knowledge_manifest.get("releaseId"),
        "files": {"candidates": "candidates.jsonl", "audit": "audit.json", "report": "report.json"},
    }
    atomic_write_text(output_directory / "manifest.json", f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return EnrichmentPlanResult(
        plan_id=plan_id,
        candidates=len(candidates),
        eligible=int(report["counts"]["eligible"]),
        blocked=int(report["counts"]["blocked"]),
        output_directory=output_directory,
    )


def promote_knowledge_enrichment_plan(
    data_directory: Path,
    *,
    retrieval_directory: Path | None = None,
    vault_directory: Path | None = None,
    source_manifest_path: Path | None = None,
    updated_at: str | None = None,
) -> EnrichmentPromotionResult:
    data_directory = data_directory.resolve()
    retrieval = _resolve_retrieval_directory(data_directory, retrieval_directory)
    output_directory = retrieval / "enrichment"
    manifest = load_json(output_directory / "manifest.json")
    candidates = _load_jsonl(output_directory / "candidates.jsonl")
    audit = load_json(output_directory / "audit.json")
    if not isinstance(manifest, dict) or not isinstance(audit, dict) or audit.get("passed") is not True:
        raise ValueError("plano de enriquecimento não passou na auditoria")
    if sha256(canonical_json(candidates).encode("utf-8")).hexdigest() != manifest.get("content_sha256"):
        raise ValueError("hash do plano de enriquecimento diverge dos candidatos")
    source_manifest = (source_manifest_path or data_directory / "sources.yml").resolve()
    live_audit = audit_enrichment_candidates(
        candidates,
        allowed_core_sources=_allowed_core_sources(_load_yaml(source_manifest)),
    )
    if live_audit["passed"] is not True:
        raise ValueError("candidatos não passaram na reauditoria da promoção")
    vault = (vault_directory or data_directory.parent / "knowledge" / "vault").resolve()
    promotion_date = updated_at or date.today().isoformat()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", promotion_date) is None:
        raise ValueError("updated_at precisa usar YYYY-MM-DD")

    results: list[dict[str, str]] = []
    promoted = 0
    skipped = 0
    blocked = 0
    for candidate in candidates:
        target = candidate["target_document"]
        proposal = candidate["proposal"]
        path = (vault / str(target["path"])).resolve()
        result = {"candidate_id": str(candidate["candidate_id"]), "path": path.as_posix(), "status": "blocked"}
        if not path.is_relative_to(vault) or not path.is_file():
            result["reason"] = "invalid_or_missing_vault_path"
            blocked += 1
            results.append(result)
            continue
        raw_bytes = path.read_bytes()
        text = raw_bytes.decode("utf-8")
        if SECTION_MARKER in text:
            result["status"] = "skipped"
            result["reason"] = "section_already_present"
            skipped += 1
            results.append(result)
            continue
        if sha256(raw_bytes).hexdigest() != target["raw_file_sha256"]:
            result["reason"] = "raw_file_changed_after_plan"
            blocked += 1
            results.append(result)
            continue
        if candidate.get("audit", {}).get("status") != "passed":
            result["reason"] = "candidate_audit_not_passed"
            blocked += 1
            results.append(result)
            continue
        updated_text, substitutions = re.subn(
            r"(?m)^updated_at:\s*\d{4}-\d{2}-\d{2}\s*$",
            f"updated_at: {promotion_date}",
            text,
            count=1,
        )
        if substitutions != 1:
            result["reason"] = "updated_at_field_not_found"
            blocked += 1
            results.append(result)
            continue
        updated_text = f"{updated_text.rstrip()}\n\n{proposal['markdown_section'].rstrip()}\n"
        atomic_write_text(path, updated_text)
        result["status"] = "promoted"
        result["reason"] = "factual_coverage_section_appended"
        promoted += 1
        results.append(result)

    report = {
        "schema_version": 1,
        "plan_id": manifest.get("plan_id"),
        "updated_at": promotion_date,
        "counts": {"promoted": promoted, "skipped": skipped, "blocked": blocked},
        "relations_generated": 0,
        "sensory_claims_generated": False,
        "results": results,
    }
    report_path = output_directory / "promotion-report.json"
    atomic_write_text(report_path, f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    if blocked:
        raise ValueError(f"promoção bloqueou {blocked} candidato(s); consulte {report_path}")
    return EnrichmentPromotionResult(
        plan_id=str(manifest.get("plan_id")),
        promoted=promoted,
        skipped=skipped,
        blocked=blocked,
        report_path=report_path,
    )
