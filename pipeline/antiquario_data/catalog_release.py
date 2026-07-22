from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable

from .io_utils import atomic_write_text, load_json
from .models import canonical_json
from .warehouse import _duckdb


def normalize_search_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    without_marks = "".join(character for character in decomposed if not unicodedata.combining(character))
    lowered = without_marks.casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", lowered)).strip()


def search_terms(values: Iterable[str]) -> set[str]:
    terms: set[str] = set()
    for value in values:
        normalized = normalize_search_text(value)
        if not normalized:
            continue
        terms.update(token for token in normalized.split() if len(token) >= 2)
        if " " in normalized:
            terms.add(normalized)
    return terms


def resolution_key(name: str, brands: Iterable[str], launch_year: int | None) -> str:
    normalized_brands = sorted(filter(None, (normalize_search_text(brand) for brand in brands)))
    primary_brand = normalized_brands[0] if normalized_brands else "unknown-brand"
    year = str(launch_year) if launch_year is not None else "unknown-year"
    return f"{normalize_search_text(name)}|{primary_brand}|{year}"


def _file_payload(value: Any) -> tuple[str, str, int]:
    text = f"{canonical_json(value)}\n"
    encoded = text.encode("utf-8")
    return text, sha256(encoded).hexdigest(), len(encoded)


def _dimension(
    rows: list[tuple[str, str, str]],
) -> tuple[list[dict[str, str]], dict[str, list[str]], dict[str, str]]:
    labels: dict[str, set[str]] = defaultdict(set)
    relations: dict[str, set[str]] = defaultdict(set)
    for fragrance_id, wikidata_id, label in rows:
        entity_id = f"wd-{wikidata_id.lower()}"
        labels[entity_id].add(label)
        relations[fragrance_id].add(entity_id)
    selected_labels = {
        entity_id: sorted(names, key=lambda name: (normalize_search_text(name), name))[0]
        for entity_id, names in labels.items()
    }
    entities = [
        {"id": entity_id, "wikidataId": entity_id[3:].upper(), "name": selected_labels[entity_id]}
        for entity_id in sorted(selected_labels)
    ]
    return entities, {key: sorted(value) for key, value in relations.items()}, selected_labels


def _knowledge_links(
    documents_path: Path,
    fragrance_qids: set[str],
) -> tuple[dict[str, list[str]], list[dict[str, str]]]:
    documents = load_json(documents_path)
    if not isinstance(documents, list):
        raise ValueError("documents.json do Knowledge Core deve conter uma lista")
    linked: dict[str, list[str]] = defaultdict(list)
    orphans: list[dict[str, str]] = []
    claimed: dict[str, str] = {}
    for document in documents:
        if not isinstance(document, dict) or document.get("type") != "fragrance":
            continue
        qid = document.get("external_ids", {}).get("wikidata")
        if not qid:
            continue
        previous = claimed.get(qid)
        if previous and previous != document.get("id"):
            raise ValueError(f"QID {qid} está ligado a dois documentos: {previous} e {document.get('id')}")
        claimed[qid] = document["id"]
        if qid in fragrance_qids:
            linked[qid].append(document["id"])
        else:
            orphans.append({"knowledgeId": document["id"], "wikidataId": qid})
    return {key: sorted(value) for key, value in linked.items()}, sorted(orphans, key=lambda item: item["knowledgeId"])


@dataclass(frozen=True)
class CatalogReleaseResult:
    release_id: str
    release_directory: Path
    public_directory: Path
    manifest: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "release_directory": self.release_directory.as_posix(),
            "public_directory": self.public_directory.as_posix(),
            "manifest": self.manifest,
        }


def compile_catalog_release(
    *,
    data_directory: Path,
    knowledge_directory: Path,
    releases_directory: Path,
    public_directory: Path,
) -> CatalogReleaseResult:
    database_path = data_directory / "catalog" / "catalog.duckdb"
    catalog_manifest_path = data_directory / "catalog" / "catalog-manifest.json"
    knowledge_manifest_path = knowledge_directory / "knowledge-manifest.json"
    documents_path = knowledge_directory / "documents.json"
    for path in (database_path, catalog_manifest_path, knowledge_manifest_path, documents_path):
        if not path.exists():
            raise FileNotFoundError(f"Entrada ausente: {path}")

    catalog_manifest = load_json(catalog_manifest_path)
    knowledge_manifest = load_json(knowledge_manifest_path)
    connection = _duckdb().connect(str(database_path), read_only=True)
    try:
        fragrance_rows = connection.execute("""
            SELECT id, wikidata_id, name, name_language, launch_year, official_website,
                   source_id, source_url, license, CAST(retrieved_at AS VARCHAR), record_hash
            FROM fragrances ORDER BY id
        """).fetchall()
        brand_rows = connection.execute(
            "SELECT fragrance_id, wikidata_id, label FROM fragrance_brands ORDER BY ALL"
        ).fetchall()
        perfumer_rows = connection.execute(
            "SELECT fragrance_id, wikidata_id, label FROM fragrance_perfumers ORDER BY ALL"
        ).fetchall()
        country_rows = connection.execute(
            "SELECT fragrance_id, wikidata_id, label FROM fragrance_countries ORDER BY ALL"
        ).fetchall()
    finally:
        connection.close()

    brands, brands_by_fragrance, brand_labels = _dimension(brand_rows)
    perfumers, perfumers_by_fragrance, perfumer_labels = _dimension(perfumer_rows)
    countries, countries_by_fragrance, country_labels = _dimension(country_rows)
    fragrance_qids = {row[1] for row in fragrance_rows}
    knowledge_by_qid, orphan_knowledge = _knowledge_links(documents_path, fragrance_qids)

    fragrances: list[dict[str, Any]] = []
    candidate_groups: dict[str, list[str]] = defaultdict(list)
    for row in fragrance_rows:
        (
            fragrance_id, wikidata_id, name, language, launch_year, official_website,
            source_id, source_url, license_name, retrieved_at, record_hash,
        ) = row
        brand_ids = brands_by_fragrance.get(fragrance_id, [])
        perfumer_ids = perfumers_by_fragrance.get(fragrance_id, [])
        country_ids = countries_by_fragrance.get(fragrance_id, [])
        linked_knowledge = knowledge_by_qid.get(wikidata_id, [])
        product = {
            "id": fragrance_id,
            "wikidataId": wikidata_id,
            "name": name,
            "language": language,
            "launchYear": launch_year,
            "officialWebsite": official_website,
            "brandIds": brand_ids,
            "perfumerIds": perfumer_ids,
            "countryIds": country_ids,
            "knowledgeIds": linked_knowledge,
            "sourceId": source_id,
            "sourceUrl": source_url,
            "license": license_name,
            "retrievedAt": retrieved_at,
            "recordHash": record_hash,
        }
        fragrances.append(product)
        candidate_groups[resolution_key(
            name,
            (brand_labels[entity_id] for entity_id in brand_ids),
            launch_year,
        )].append(fragrance_id)

    ambiguous_clusters = [
        {"key": key, "fragranceIds": sorted(ids), "action": "manual_review"}
        for key, ids in sorted(candidate_groups.items())
        if len(ids) > 1
    ]

    entity_payload = {
        "schemaVersion": 1,
        "brands": brands,
        "perfumers": perfumers,
        "countries": countries,
    }
    fragrance_payload = {"schemaVersion": 1, "items": fragrances}

    document_ids = [product["id"] for product in fragrances]
    inverted: dict[str, set[int]] = defaultdict(set)
    for position, product in enumerate(fragrances):
        values = [product["name"], str(product["launchYear"] or "")]
        values.extend(brand_labels[entity_id] for entity_id in product["brandIds"])
        values.extend(perfumer_labels[entity_id] for entity_id in product["perfumerIds"])
        values.extend(country_labels[entity_id] for entity_id in product["countryIds"])
        for term in search_terms(values):
            inverted[term].add(position)
    search_payload = {
        "schemaVersion": 1,
        "documentIds": document_ids,
        "terms": {term: sorted(positions) for term, positions in sorted(inverted.items())},
    }
    resolution_payload = {
        "schemaVersion": 1,
        "strategy": "normalized-name+primary-brand+launch-year",
        "automaticMerges": 0,
        "ambiguousClusters": ambiguous_clusters,
        "orphanKnowledgeDocuments": orphan_knowledge,
    }

    payloads = {
        "fragrances.json": fragrance_payload,
        "entities.json": entity_payload,
        "search-index.json": search_payload,
        "resolution-report.json": resolution_payload,
    }
    rendered = {name: _file_payload(payload) for name, payload in payloads.items()}
    source_rows = sorted({(row[6], row[8], row[9]) for row in fragrance_rows})
    sources = [
        {"id": source_id, "license": license_name, "retrievedAt": retrieved_at}
        for source_id, license_name, retrieved_at in source_rows
    ]
    release_content = {
        "schemaVersion": 1,
        "catalogVersion": catalog_manifest["catalog_version"],
        "knowledgeReleaseId": knowledge_manifest["releaseId"],
        "sources": sources,
        "payloads": payloads,
    }
    content_hash = sha256(canonical_json(release_content).encode("utf-8")).hexdigest()
    release_id = f"catalog-web-v1-{content_hash[:12]}"
    manifest = {
        "schemaVersion": 1,
        "releaseId": release_id,
        "contentHash": content_hash,
        "catalogVersion": catalog_manifest["catalog_version"],
        "knowledgeReleaseId": knowledge_manifest["releaseId"],
        "counts": {
            "fragrances": len(fragrances),
            "brands": len(brands),
            "perfumers": len(perfumers),
            "countries": len(countries),
            "knowledgeLinks": sum(len(ids) for ids in knowledge_by_qid.values()),
            "searchTerms": len(inverted),
            "ambiguousClusters": len(ambiguous_clusters),
        },
        "sources": sources,
        "files": {
            name.removesuffix(".json").replace("-", "_"): {
                "path": name,
                "sha256": file_hash,
                "bytes": size,
            }
            for name, (_text, file_hash, size) in rendered.items()
        },
    }

    release_directory = releases_directory / release_id
    for directory in (release_directory, public_directory):
        directory.mkdir(parents=True, exist_ok=True)
        for name, (text, _file_hash, _size) in rendered.items():
            atomic_write_text(directory / name, text)
        atomic_write_text(
            directory / "manifest.json",
            f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n",
        )
    atomic_write_text(
        releases_directory / "latest.json",
        f"{json.dumps({'releaseId': release_id, 'manifestPath': f'{release_id}/manifest.json'}, sort_keys=True, indent=2)}\n",
    )
    return CatalogReleaseResult(
        release_id=release_id,
        release_directory=release_directory,
        public_directory=public_directory,
        manifest=manifest,
    )
