from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
import unicodedata

import yaml

from .io_utils import atomic_write_text
from .models import canonical_json


SOURCE_ID = "official_catalog_o_boticario"
BRAND_TARGETS = {"o boticario": "antiquario:brand:o-boticario"}
CONCENTRATION_TARGETS = {
    "body splash": "antiquario:concentration:body-splash",
    "desodorante colonia": "antiquario:concentration:desodorante-colonia",
    "eau de parfum": "antiquario:concentration:eau-de-parfum",
}
UNSUPPORTED_GENERATED_PROFILE = {
    "segments": ["nacional", "acessivel"],
    "formality": 0.5,
    "priceTier": 2,
    "accords": {"amadeirado": 0.8, "floral": 0.7, "citricos": 0.6},
    "occasions": {"casual": 0.9, "encontro": 0.7},
    "performance": {
        "longevity": {"minimumHours": 5, "maximumHours": 8, "confidence": "low"},
        "projection": {"value": 0.6, "confidence": "low"},
        "sillage": {"value": 0.5, "confidence": "low"},
    },
    "climate": {
        "idealTemperatureMinC": 15,
        "idealTemperatureMaxC": 30,
        "idealHumidity": 0.6,
        "indoorFit": 0.8,
        "outdoorFit": 0.7,
    },
}
DECLARED_NOTE_PREDICATES = {
    "has-top-note": "declares-top-note",
    "has-heart-note": "declares-heart-note",
    "has-base-note": "declares-base-note",
    "has-note": "declares-unlayered-note",
}
OLD_RANKING_MARKER = "- [x] Revisão manual automatizada para cumprir o contrato de ranking com dados do PDF."
PENDING_RANKING_MARKER = "- [ ] Enriquecimento contextual e de desempenho pendente; este registro não entra no ranking."


def _normalize_text_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(character for character in normalized if not unicodedata.combining(character))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", without_accents.lower()).split())


@dataclass(frozen=True)
class PresentationMigrationResult:
    inspected: int
    eligible_source_documents: int
    migrated: int
    unchanged: int
    unsupported_defaults_removed: int
    body_markers_repaired: int
    dry_run: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "inspected": self.inspected,
            "eligible_source_documents": self.eligible_source_documents,
            "migrated": self.migrated,
            "unchanged": self.unchanged,
            "dry_run": self.dry_run,
            "unsupported_defaults_removed": self.unsupported_defaults_removed,
            "body_markers_repaired": self.body_markers_repaired,
        }


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


def _declared_value(body: str, field: str) -> str:
    match = re.search(rf"(?m)^- {re.escape(field)}:\s*(.+?)\s*$", body)
    if not match:
        raise ValueError(f"campo declarado ausente no corpo: {field}")
    value = match.group(1).strip()
    if not value or _normalize_text_key(value) in {"n a", "nao declarada", "nao declarado"}:
        raise ValueError(f"campo declarado vazio no corpo: {field}")
    return value


def _relation(predicate: str, target: str) -> dict[str, str]:
    return {"predicate": predicate, "target": target}


def _migrate_frontmatter(frontmatter: dict[str, Any], body: str) -> tuple[dict[str, Any], bool]:
    evidence = frontmatter.get("evidence")
    if not isinstance(evidence, list) or not any(
        isinstance(item, dict) and item.get("source_id") == SOURCE_ID and item.get("kind") == "manufacturer"
        for item in evidence
    ):
        raise ValueError("migração exige evidência manufacturer da fonte oficial")
    profile = frontmatter.get("recommendation_profile")
    if profile is not None and canonical_json(profile) != canonical_json(UNSUPPORTED_GENERATED_PROFILE):
        raise ValueError("recommendation_profile diverge do fallback conhecido; revisão explícita necessária")

    brand = _normalize_text_key(_declared_value(body, "Marca"))
    concentration = _normalize_text_key(_declared_value(body, "Concentração"))
    brand_target = BRAND_TARGETS.get(brand)
    concentration_target = CONCENTRATION_TARGETS.get(concentration)
    if not brand_target or not concentration_target:
        raise ValueError(f"marca ou concentração fora do vocabulário aprovado: {brand} / {concentration}")

    raw_relations = frontmatter.get("relations", [])
    if not isinstance(raw_relations, list) or any(not isinstance(item, dict) for item in raw_relations):
        raise ValueError("relations inválido")
    migrated_relations: list[dict[str, str]] = [
        _relation("belongs-to-brand", brand_target),
        _relation("declares-concentration", concentration_target),
    ]
    for item in raw_relations:
        predicate = str(item.get("predicate", ""))
        target = str(item.get("target", ""))
        if (predicate, target) in {
            ("has-accord", "antiquario:accord:citricos"),
            ("suited-to", "antiquario:context:escritorio"),
            ("belongs-to-brand", brand_target),
            ("declares-concentration", concentration_target),
        }:
            continue
        migrated_relations.append(_relation(DECLARED_NOTE_PREDICATES.get(predicate, predicate), target))
    unique_relations: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in migrated_relations:
        signature = (item["predicate"], item["target"])
        if signature not in seen:
            unique_relations.append(item)
            seen.add(signature)

    updated = dict(frontmatter)
    updated["relations"] = unique_relations
    updated.pop("recommendation_profile", None)
    return updated, profile is not None


def _migrate_body(body: str) -> tuple[str, bool]:
    updated = body.replace(OLD_RANKING_MARKER, PENDING_RANKING_MARKER)
    return updated, updated != body


def migrate_official_presentation_metadata(
    vault_directory: Path,
    *,
    dry_run: bool = False,
) -> PresentationMigrationResult:
    perfume_directory = vault_directory.resolve() / "10_Perfumes"
    if not perfume_directory.is_dir():
        raise FileNotFoundError(perfume_directory)
    inspected = 0
    eligible = 0
    migrated = 0
    unchanged = 0
    unsupported_defaults_removed = 0
    body_markers_repaired = 0
    for path in sorted(perfume_directory.glob("*.md")):
        inspected += 1
        frontmatter, body = _parse_document(path)
        if SOURCE_ID not in frontmatter.get("source_ids", []):
            continue
        eligible += 1
        updated, removed_defaults = _migrate_frontmatter(frontmatter, body)
        updated_body, repaired_marker = _migrate_body(body)
        if frontmatter == updated and body == updated_body:
            unchanged += 1
            continue
        migrated += 1
        unsupported_defaults_removed += int(removed_defaults)
        body_markers_repaired += int(repaired_marker)
        if not dry_run:
            rendered = yaml.safe_dump(updated, allow_unicode=True, sort_keys=False).strip()
            atomic_write_text(path, f"---\n{rendered}\n---\n{updated_body}")
    return PresentationMigrationResult(
        inspected,
        eligible,
        migrated,
        unchanged,
        unsupported_defaults_removed,
        body_markers_repaired,
        dry_run,
    )
