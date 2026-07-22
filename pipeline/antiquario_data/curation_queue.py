from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import unicodedata
from typing import Any

from .catalog_release import normalize_search_text
from .io_utils import atomic_write_text, load_json
from .warehouse import _duckdb


@dataclass(frozen=True)
class CurationCandidate:
    id: str
    wikidata_id: str
    name: str
    launch_year: int | None
    official_website: str | None
    brands: tuple[str, ...]
    perfumers: tuple[str, ...]
    countries: tuple[str, ...]
    retrieved_at: str

    @property
    def completeness(self) -> int:
        return (
            1
            + int(bool(self.brands))
            + int(bool(self.perfumers))
            + int(bool(self.countries))
            + int(self.launch_year is not None)
            + int(self.official_website is not None)
        )


@dataclass(frozen=True)
class CurationQueueResult:
    selected: tuple[CurationCandidate, ...]
    created: tuple[Path, ...]
    preserved: tuple[Path, ...]
    report_path: Path

    def as_dict(self) -> dict[str, Any]:
        return {
            "selected": len(self.selected),
            "created": [path.as_posix() for path in self.created],
            "preserved": [path.as_posix() for path in self.preserved],
            "reportPath": self.report_path.as_posix(),
        }


def _slugify(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(character for character in decomposed if not unicodedata.combining(character))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-")
    return slug or "fragrancia"


def _dimension_values(connection: Any, table: str) -> dict[str, tuple[str, ...]]:
    rows = connection.execute(
        f"SELECT fragrance_id, label FROM {table} ORDER BY fragrance_id, label"
    ).fetchall()
    grouped: dict[str, list[str]] = defaultdict(list)
    for fragrance_id, label in rows:
        grouped[fragrance_id].append(label)
    return {fragrance_id: tuple(labels) for fragrance_id, labels in grouped.items()}


def load_curation_candidates(data_directory: Path) -> list[CurationCandidate]:
    database_path = data_directory / "catalog" / "catalog.duckdb"
    if not database_path.exists():
        raise FileNotFoundError(f"Catálogo DuckDB ausente: {database_path}")
    connection = _duckdb().connect(str(database_path), read_only=True)
    try:
        brands = _dimension_values(connection, "fragrance_brands")
        perfumers = _dimension_values(connection, "fragrance_perfumers")
        countries = _dimension_values(connection, "fragrance_countries")
        rows = connection.execute("""
            SELECT id, wikidata_id, name, launch_year, official_website, CAST(retrieved_at AS VARCHAR)
            FROM fragrances
            ORDER BY id
        """).fetchall()
    finally:
        connection.close()
    return [
        CurationCandidate(
            id=identifier,
            wikidata_id=wikidata_id,
            name=name,
            launch_year=launch_year,
            official_website=official_website,
            brands=brands.get(identifier, ()),
            perfumers=perfumers.get(identifier, ()),
            countries=countries.get(identifier, ()),
            retrieved_at=retrieved_at,
        )
        for identifier, wikidata_id, name, launch_year, official_website, retrieved_at in rows
    ]


def _ambiguous_ids(release_directory: Path) -> set[str]:
    report_path = release_directory / "resolution-report.json"
    if not report_path.exists():
        return set()
    report = load_json(report_path)
    return {
        identifier
        for cluster in report.get("ambiguousClusters", [])
        for identifier in cluster.get("fragranceIds", [])
    }


def select_curation_candidates(
    candidates: list[CurationCandidate],
    *,
    limit: int,
    excluded_ids: set[str],
) -> list[CurationCandidate]:
    if limit < 1:
        raise ValueError("O limite da fila deve ser maior que zero")
    remaining = [candidate for candidate in candidates if candidate.id not in excluded_ids]
    selected: list[CurationCandidate] = []
    used_brands: set[str] = set()
    used_countries: set[str] = set()

    while remaining and len(selected) < limit:
        def priority(candidate: CurationCandidate) -> tuple[int, int, str]:
            novelty = (
                2 * len(set(candidate.brands) - used_brands)
                + len(set(candidate.countries) - used_countries)
            )
            return (candidate.completeness * 10 + novelty, candidate.completeness, candidate.id)

        best_score = max(priority(candidate)[:2] for candidate in remaining)
        chosen = min(
            (candidate for candidate in remaining if priority(candidate)[:2] == best_score),
            key=lambda candidate: candidate.id,
        )
        selected.append(chosen)
        used_brands.update(chosen.brands)
        used_countries.update(chosen.countries)
        remaining.remove(chosen)
    return selected


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_curation_draft(candidate: CurationCandidate) -> str:
    title = _yaml_string(candidate.name)
    brands = ", ".join(candidate.brands) if candidate.brands else "não informado no Wikidata"
    perfumers = ", ".join(candidate.perfumers) if candidate.perfumers else "não informado no Wikidata"
    countries = ", ".join(candidate.countries) if candidate.countries else "não informado no Wikidata"
    year = str(candidate.launch_year) if candidate.launch_year is not None else "não informado no Wikidata"
    website = candidate.official_website or "não informado no Wikidata"
    return f'''---
schema_version: 1
id: antiquario:fragrance:{_slugify(candidate.name)}-{candidate.wikidata_id.lower()}
project: o-antiquario
type: fragrance
title: {title}
aliases: []
external_ids:
  wikidata: {candidate.wikidata_id}
tags: [perfume, curadoria-pendente]
source_ids: [wikidata]
license: CC0-1.0
confidence: medium
review_status: draft
updated_at: {candidate.retrieved_at}
language: pt-BR
summary: Rascunho de curadoria vinculado ao registro factual do Wikidata; aguarda enriquecimento editorial verificável.
evidence:
  - source_id: wikidata
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: Identidade, marca, país, ano, perfumista e site oficial quando presentes no Wikidata.
    locator: https://www.wikidata.org/wiki/{candidate.wikidata_id}
    retrieved_at: {candidate.retrieved_at}
relations: []
---

# {candidate.name}

## Base factual

- QID: `{candidate.wikidata_id}`
- Marca: {brands}
- Perfumista: {perfumers}
- País: {countries}
- Ano: {year}
- Site oficial: {website}

## Enriquecimento editorial obrigatório

- [ ] Confirmar a identidade e a concentração da fragrância.
- [ ] Classificar família, notas e acordes usando a taxonomia do Antiquário.
- [ ] Registrar contexto de uso e desempenho com método, amostra e confiança.
- [ ] Adicionar evidências permitidas para cada afirmação editorial.
- [ ] Mover este arquivo para `10_Perfumes` somente após revisão humana.

## Limite de uso

Este rascunho não é uma recomendação e não deve ser usado pelo motor de ranking. Não inferir notas, desempenho, preço ou disponibilidade a partir de nome, marca ou país.
'''


def _regional_coverage(candidates: list[CurationCandidate]) -> dict[str, int]:
    labels = [normalize_search_text(country) for candidate in candidates for country in candidate.countries]
    return {
        "brasil": sum(label in {"brasil", "brazil"} for label in labels),
        "paises-arabes": sum(
            label in {"emirados arabes unidos", "arabia saudita", "catar", "kuwait", "oma", "bahrein"}
            for label in labels
        ),
    }


def build_curation_queue(
    *,
    data_directory: Path,
    vault_directory: Path,
    release_directory: Path,
    report_path: Path,
    limit: int = 25,
) -> CurationQueueResult:
    candidates = load_curation_candidates(data_directory)
    excluded_ids = _ambiguous_ids(release_directory)
    selected = select_curation_candidates(candidates, limit=limit, excluded_ids=excluded_ids)
    queue_directory = vault_directory / "00_Inbox" / "Curadoria-Catalogo"
    created: list[Path] = []
    preserved: list[Path] = []
    for candidate in selected:
        path = queue_directory / f"{_slugify(candidate.name)}-{candidate.wikidata_id.lower()}.md"
        contents = render_curation_draft(candidate)
        if path.exists():
            if path.read_text(encoding="utf-8") != contents:
                preserved.append(path)
            continue
        atomic_write_text(path, contents)
        created.append(path)

    report = {
        "schemaVersion": 1,
        "purpose": "internal-editorial-curation-queue",
        "selection": {
            "requested": limit,
            "selected": len(selected),
            "excludedAmbiguousRecords": sorted(excluded_ids),
            "strategy": "metadata-completeness+brand-country-diversity",
        },
        "coverage": {
            "catalogFragrances": len(candidates),
            "regionalCandidates": _regional_coverage(candidates),
        },
        "items": [
            {
                "id": candidate.id,
                "wikidataId": candidate.wikidata_id,
                "name": candidate.name,
                "completeness": candidate.completeness,
                "draftPath": str(
                    Path("knowledge") / "vault" / "00_Inbox" / "Curadoria-Catalogo"
                    / f"{_slugify(candidate.name)}-{candidate.wikidata_id.lower()}.md"
                ).replace("\\", "/"),
            }
            for candidate in selected
        ],
    }
    atomic_write_text(report_path, f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return CurationQueueResult(tuple(selected), tuple(created), tuple(preserved), report_path)
