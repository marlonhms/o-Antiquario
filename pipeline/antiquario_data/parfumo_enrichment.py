from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Iterable
import unicodedata

import yaml

from .io_utils import atomic_write_text, write_dicts_jsonl
from .models import canonical_json
from .term_resolver import TermResolver, normalize_term


SOURCE_ID = "parfumo_dataset"
GENERATED_RELATIONS = {"has-concentration", "has-accord", "created-by"}
MISSING_VALUES = {"", "na", "n/a", "nan", "none", "null"}
CONCENTRATIONS = {
    "eau de toilette": ("eau-de-toilette", "Eau de Toilette", ["edt"]),
    "eau de parfum": ("eau-de-parfum", "Eau de Parfum", ["edp"]),
    "eau de cologne": ("eau-de-cologne", "Eau de Cologne", ["edc"]),
    "perfume": ("perfume", "Perfume", []),
    "cologne": ("cologne", "Cologne", []),
    "eau de toilette concentree": (
        "eau-de-toilette-concentree",
        "Eau de Toilette Concentrée",
        [],
    ),
    "extrait": ("extrait", "Extrait", []),
    "extrait de parfum": ("extrait-de-parfum", "Extrait de Parfum", []),
    "solid perfume": ("solid-perfume", "Solid Perfume", []),
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.strip())
    ascii_value = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    cleaned = re.sub(r"[^a-z0-9\s-]", "", ascii_value.lower())
    return re.sub(r"\s+", "-", cleaned).strip("-")


def _present(value: object) -> bool:
    return normalize_term(str(value)) not in MISSING_VALUES


def _split(value: object) -> list[str]:
    if not _present(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _parse_document(path: Path) -> tuple[dict[str, Any], str]:
    contents = path.read_text(encoding="utf-8")
    if not contents.startswith("---\n"):
        raise ValueError(f"{path}: frontmatter ausente")
    parts = contents.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: frontmatter inválido")
    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter precisa ser objeto")
    return frontmatter, parts[2]


def _render_document(frontmatter: dict[str, Any], body: str) -> str:
    rendered = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{rendered}\n---\n{body}"


def _row_key(row: dict[str, str]) -> str | None:
    name = slugify(row.get("Name", ""))
    brand = slugify(row.get("Brand", ""))
    if not name or not brand:
        return None
    return f"antiquario:fragrance:parfumo-{brand}-{name}"


def _rating_count(row: dict[str, str]) -> float:
    try:
        return float(row.get("Rating_Count", ""))
    except (TypeError, ValueError):
        return float("-inf")


def _load_priority_rows(csv_path: Path, *, limit: int) -> dict[str, dict[str, str]]:
    if not csv_path.is_file():
        raise FileNotFoundError(csv_path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=_rating_count, reverse=True)
    indexed: dict[str, dict[str, str]] = {}
    for row in rows[:limit]:
        key = _row_key(row)
        if key:
            indexed[key] = row
    return indexed


def _load_taxonomy(data_directory: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    path = data_directory / "taxonomy" / "taxonomy.yml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    accords = {str(item["id"]): item for item in payload.get("accords", [])}
    families = {str(item["id"]): str(item.get("pt", item["id"])) for item in payload.get("families", [])}
    return accords, families


def _existing_entity_index(vault_directory: Path, document_type: str) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in sorted(vault_directory.glob("**/*.md")):
        frontmatter, _ = _parse_document(path)
        if frontmatter.get("type") != document_type:
            continue
        target = str(frontmatter.get("id", ""))
        terms = [frontmatter.get("title", ""), *frontmatter.get("aliases", [])]
        for term in terms:
            normalized = normalize_term(str(term))
            if normalized:
                index.setdefault(normalized, target)
        if target:
            index.setdefault(normalize_term(target.split(":")[-1].replace("-", " ")), target)
    return index


def _concentration_document(slug: str, title: str, aliases: list[str], updated_at: str) -> str:
    frontmatter = {
        "schema_version": 1,
        "id": f"antiquario:concentration:{slug}",
        "project": "o-antiquario",
        "type": "concentration",
        "title": title,
        "aliases": [title.lower(), *aliases],
        "external_ids": {},
        "tags": ["concentracao", "vocabulario-controlado"],
        "source_ids": ["internal_curated"],
        "license": "CC0-1.0",
        "confidence": "high",
        "review_status": "approved",
        "updated_at": updated_at,
        "language": "pt-BR",
        "summary": f"Categoria canônica que preserva a concentração {title} informada por uma fonte estruturada.",
        "evidence": [{
            "source_id": "internal_curated",
            "kind": "curated",
            "license": "CC0-1.0",
            "confidence": "high",
            "claim_scope": "Vocabulário controlado de concentrações para normalização sem inferência de desempenho.",
        }],
        "relations": [],
    }
    body = (
        f"\n# {title}\n\nIdentificador operacional de concentração. Não implica duração, projeção "
        "ou percentual químico sem evidência específica do produto.\n"
    )
    return _render_document(frontmatter, body)


def _accord_document(item: dict[str, Any], updated_at: str) -> str:
    accord_id = str(item["id"])
    title = str(item.get("pt", accord_id)).capitalize()
    frontmatter = {
        "schema_version": 1,
        "id": f"antiquario:accord:{accord_id}",
        "project": "o-antiquario",
        "type": "accord",
        "title": title,
        # Aliases multilíngues permanecem na taxonomia/resolvedor. Replicá-los no
        # Vault cria referências Obsidian ambíguas entre notas e acordes (ex: amber).
        "aliases": [],
        "external_ids": {},
        "tags": ["acorde", "vocabulario-controlado", "navegacao"],
        "source_ids": ["internal_curated"],
        "license": "CC0-1.0",
        "confidence": "medium",
        "review_status": "approved",
        "updated_at": updated_at,
        "language": "pt-BR",
        "summary": f"Acorde operacional {title} preservado no vocabulário controlado do Antiquário.",
        "evidence": [{
            "source_id": "internal_curated",
            "kind": "curated",
            "license": "CC0-1.0",
            "confidence": "medium",
            "claim_scope": "Vocabulário olfativo canônico para estruturação, busca e navegação no projeto.",
        }],
        "relations": [],
    }
    families = ", ".join(str(value) for value in item.get("family_ids", [])) or "não projetadas"
    body = (
        f"\n# {title}\n\nAcorde canônico usado para preservar descrições estruturadas da fonte. "
        f"Rotas taxonômicas possíveis: {families}. Essas rotas não declaram a família de um perfume.\n"
    )
    return _render_document(frontmatter, body)


def _perfumer_document(name: str, locator: str, updated_at: str) -> str:
    slug = slugify(name)
    frontmatter = {
        "schema_version": 1,
        "id": f"antiquario:perfumer:{slug}",
        "project": "o-antiquario",
        "type": "perfumer",
        "title": name,
        "aliases": [],
        "external_ids": {},
        "tags": ["perfumista", "parfumo"],
        "source_ids": [SOURCE_ID],
        "license": "CC0-1.0",
        "confidence": "medium",
        "review_status": "approved",
        "updated_at": updated_at,
        "language": "pt-BR",
        "summary": "Perfumista identificado em um registro estruturado do Parfumo Fragrance Dataset.",
        "evidence": [{
            "source_id": SOURCE_ID,
            "kind": "open_source",
            "license": "CC0-1.0",
            "confidence": "medium",
            "claim_scope": "Nome do perfumista e vínculo com uma fragrância no registro estruturado.",
            "locator": locator,
            "retrieved_at": updated_at,
        }],
        "relations": [],
    }
    return _render_document(frontmatter, f"\n# {name}\n\nEntidade factual importada do dataset; biografia não declarada.\n")


def _unique_relations(relations: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for relation in relations:
        signature = (relation["predicate"], relation["target"])
        if signature not in seen:
            result.append(relation)
            seen.add(signature)
    return result


@dataclass(frozen=True)
class ParfumoEnrichmentResult:
    inspected: int
    matched: int
    changed: int
    locators_added: int
    concentrations_linked: int
    accords_linked: int
    perfumer_links: int
    perfumer_documents_created: int
    accord_documents_created: int
    family_candidates: int
    quarantined_terms: int
    input_sha256: str
    dry_run: bool

    def as_dict(self) -> dict[str, object]:
        return self.__dict__.copy()


def enrich_parfumo_documents(
    csv_path: Path,
    data_directory: Path,
    vault_directory: Path,
    *,
    staging_directory: Path | None = None,
    limit: int = 200,
    updated_at: str | None = None,
    dry_run: bool = False,
) -> ParfumoEnrichmentResult:
    csv_path = csv_path.resolve()
    vault_directory = vault_directory.resolve()
    data_directory = data_directory.resolve()
    staging_directory = (staging_directory or data_directory / "staging" / "parfumo").resolve()
    updated_at = updated_at or date.today().isoformat()
    rows = _load_priority_rows(csv_path, limit=limit)
    resolver = TermResolver(data_directory)
    taxonomy_accords, family_labels = _load_taxonomy(data_directory)
    accord_entities = _existing_entity_index(vault_directory, "accord")
    perfumer_entities = _existing_entity_index(vault_directory, "perfumer")

    inspected = matched = changed = locators_added = 0
    concentrations_linked = accords_linked = perfumer_links = 0
    perfumer_documents_created = accord_documents_created = 0
    candidates: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    pending_writes: dict[Path, str] = {}

    fragrance_paths = sorted((vault_directory / "30_Parfumo_Dataset").glob("fragrance-*.md"))
    for path in fragrance_paths:
        inspected += 1
        frontmatter, body = _parse_document(path)
        if SOURCE_ID not in frontmatter.get("source_ids", []):
            continue
        row = rows.get(str(frontmatter.get("id", "")))
        if not row:
            continue
        matched += 1
        locator = row.get("URL", "").strip()
        if not locator.startswith("https://"):
            raise ValueError(f"{path}: URL de origem inválida")

        updated = dict(frontmatter)
        evidence = [dict(item) for item in frontmatter.get("evidence", [])]
        source_evidence = next((item for item in evidence if item.get("source_id") == SOURCE_ID), None)
        if source_evidence is None:
            raise ValueError(f"{path}: evidência {SOURCE_ID} ausente")
        if not source_evidence.get("locator"):
            locators_added += 1
        source_evidence.update({
            "license": "CC0-1.0",
            "confidence": "medium",
            "claim_scope": "Identidade e campos olfativos estruturados disponíveis no registro do dataset.",
            "locator": locator,
            "retrieved_at": updated_at,
        })
        updated["evidence"] = evidence

        relations = [
            dict(item) for item in frontmatter.get("relations", [])
            if item.get("predicate") not in GENERATED_RELATIONS
        ]

        concentration = row.get("Concentration", "")
        if _present(concentration):
            concentration_spec = CONCENTRATIONS.get(normalize_term(concentration))
            if concentration_spec:
                concentration_slug, concentration_title, concentration_aliases = concentration_spec
                relations.append({
                    "predicate": "has-concentration",
                    "target": f"antiquario:concentration:{concentration_slug}",
                })
                concentrations_linked += 1
                concentration_path = vault_directory / "16_Concentracoes" / f"{concentration_slug}.md"
                if not concentration_path.exists():
                    pending_writes.setdefault(
                        concentration_path,
                        _concentration_document(
                            concentration_slug,
                            concentration_title,
                            concentration_aliases,
                            updated_at,
                        ),
                    )
            else:
                quarantine.append({
                    "kind": "concentration",
                    "raw_term": concentration,
                    "subject_id": updated["id"],
                    "source_id": SOURCE_ID,
                    "locator": locator,
                    "reason": "unresolved_exact_vocabulary",
                })

        family_support: dict[str, set[str]] = {}
        for raw_accord in _split(row.get("Main_Accords", "")):
            resolved = resolver.resolve_accord(raw_accord)
            if resolved is None:
                quarantine.append({
                    "kind": "accord",
                    "raw_term": raw_accord,
                    "subject_id": updated["id"],
                    "source_id": SOURCE_ID,
                    "locator": locator,
                    "reason": "unresolved_exact_taxonomy",
                })
                continue
            accord_id = resolved.canonical_id.removeprefix("accord:")
            accord_item = taxonomy_accords[accord_id]
            target = accord_entities.get(normalize_term(raw_accord))
            if target is None:
                target = f"antiquario:accord:{accord_id}"
                accord_path = vault_directory / "30_Acordes" / f"{accord_id}.md"
                if not accord_path.exists() and accord_path not in pending_writes:
                    pending_writes[accord_path] = _accord_document(accord_item, updated_at)
                    accord_documents_created += 1
                accord_entities[normalize_term(raw_accord)] = target
                accord_entities[normalize_term(accord_item.get("pt", accord_id))] = target
                accord_entities[normalize_term(accord_item.get("en", accord_id))] = target
            relations.append({"predicate": "has-accord", "target": target})
            accords_linked += 1
            for family_id in accord_item.get("family_ids", []):
                family_support.setdefault(str(family_id), set()).add(accord_id)

        for perfumer in _split(row.get("Perfumers", "")):
            normalized_perfumer = normalize_term(perfumer)
            target = perfumer_entities.get(normalized_perfumer)
            if target is None:
                perfumer_slug = slugify(perfumer)
                if not perfumer_slug:
                    continue
                target = f"antiquario:perfumer:{perfumer_slug}"
                perfumer_path = vault_directory / "16_Perfumistas" / f"{perfumer_slug}.md"
                if not perfumer_path.exists() and perfumer_path not in pending_writes:
                    pending_writes[perfumer_path] = _perfumer_document(perfumer, locator, updated_at)
                    perfumer_documents_created += 1
                perfumer_entities[normalized_perfumer] = target
            relations.append({"predicate": "created-by", "target": target})
            perfumer_links += 1

        updated["relations"] = _unique_relations(relations)
        for family_id, supporting_accords in sorted(family_support.items()):
            candidate_basis = {
                "subject_id": updated["id"],
                "target_id": f"antiquario:olfactory-family:{family_id}",
                "supporting_accord_ids": sorted(supporting_accords),
                "locator": locator,
            }
            candidate_hash = sha256(canonical_json(candidate_basis).encode("utf-8")).hexdigest()[:16]
            candidates.append({
                "schema_version": 1,
                "candidate_id": f"parfumo-family-{candidate_hash}",
                "subject_id": updated["id"],
                "predicate": "belongs-to-family",
                "target_id": f"antiquario:olfactory-family:{family_id}",
                "target_label": family_labels.get(family_id, family_id),
                "claim_nature": "inferred",
                "status": "candidate",
                "method": "main_accord_taxonomy_projection",
                "supporting_accord_ids": sorted(supporting_accords),
                "source_id": SOURCE_ID,
                "locator": locator,
            })

        rendered = _render_document(updated, body)
        if rendered != path.read_text(encoding="utf-8"):
            changed += 1
            pending_writes[path] = rendered

    if not dry_run:
        for path, contents in sorted(pending_writes.items(), key=lambda item: str(item[0])):
            atomic_write_text(path, contents)
        write_dicts_jsonl(staging_directory / "family-candidates.jsonl", candidates)
        write_dicts_jsonl(staging_directory / "quarantine.jsonl", quarantine)
        manifest = {
            "schema_version": 1,
            "source_id": SOURCE_ID,
            "input": str(csv_path),
            "input_sha256": sha256(csv_path.read_bytes()).hexdigest(),
            "updated_at": updated_at,
            "limit": limit,
            "family_candidates": len(candidates),
            "quarantined_terms": len(quarantine),
        }
        atomic_write_text(staging_directory / "manifest.json", f"{json.dumps(manifest, ensure_ascii=False, indent=2)}\n")

    return ParfumoEnrichmentResult(
        inspected=inspected,
        matched=matched,
        changed=changed,
        locators_added=locators_added,
        concentrations_linked=concentrations_linked,
        accords_linked=accords_linked,
        perfumer_links=perfumer_links,
        perfumer_documents_created=perfumer_documents_created,
        accord_documents_created=accord_documents_created,
        family_candidates=len(candidates),
        quarantined_terms=len(quarantine),
        input_sha256=sha256(csv_path.read_bytes()).hexdigest(),
        dry_run=dry_run,
    )


def audit_parfumo_candidates(staging_directory: Path, vault_directory: Path) -> dict[str, object]:
    candidates_path = staging_directory.resolve() / "family-candidates.jsonl"
    if not candidates_path.is_file():
        raise FileNotFoundError(candidates_path)
    candidates = [json.loads(line) for line in candidates_path.read_text(encoding="utf-8").splitlines() if line]
    errors: list[str] = []
    seen: set[str] = set()
    for line_number, candidate in enumerate(candidates, start=1):
        candidate_id = candidate.get("candidate_id")
        if candidate_id in seen:
            errors.append(f"linha {line_number}: candidate_id duplicado")
        seen.add(candidate_id)
        if candidate.get("claim_nature") != "inferred" or candidate.get("status") != "candidate":
            errors.append(f"linha {line_number}: família precisa permanecer inferred/candidate")
        if candidate.get("predicate") != "belongs-to-family":
            errors.append(f"linha {line_number}: predicado inesperado")
        if not str(candidate.get("locator", "")).startswith("https://"):
            errors.append(f"linha {line_number}: locator ausente")
        if not candidate.get("supporting_accord_ids"):
            errors.append(f"linha {line_number}: acorde de suporte ausente")
    promoted: list[str] = []
    for path in sorted((vault_directory.resolve() / "30_Parfumo_Dataset").glob("fragrance-*.md")):
        frontmatter, _ = _parse_document(path)
        if any(item.get("predicate") == "belongs-to-family" for item in frontmatter.get("relations", [])):
            promoted.append(str(frontmatter.get("id")))
    if promoted:
        errors.append(f"{len(promoted)} família(s) inferida(s) promovida(s) indevidamente ao core")
    return {
        "ok": not errors,
        "candidate_count": len(candidates),
        "promoted_subject_ids": promoted,
        "errors": errors,
    }
