from __future__ import annotations

import ast
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .io_utils import atomic_write_bytes, atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json


SOURCE_ID = "odeuropa_multilingual_taxonomy"
LICENSE_ID = "CC-BY-4.0"
ATTRIBUTION = "ODEUROPA multilingualTaxonomies — Menini et al. (2022), CC BY 4.0"
REPOSITORY_URL = "https://github.com/Odeuropa/multilingualTaxonomies"
DEFAULT_REF = "7af2fc446c6c399bef601fc952429d34b3945ef4"
LANGUAGE_FILES = {
    "de": "DE_taxonomy.tsv",
    "en": "EN_taxonomy.tsv",
    "fr": "FR_taxonomy.tsv",
    "it": "IT_taxonomy.tsv",
}
TIME_PERIODS = (
    "1650-1700",
    "1701-1750",
    "1751-1800",
    "1801-1850",
    "1851-1900",
    "1901-1925",
)
REQUIRED_COLUMNS = (
    "word",
    "source",
    "synset",
    "first appearance",
    *TIME_PERIODS,
    "smell-source",
    "quality",
)
POS_LABELS = {
    "noun": "noun",
    "adj": "adjective",
    "verb": "verb",
    "adv": "adverb",
}
_REF_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")


@dataclass(frozen=True)
class OdeuropaSyncResult:
    snapshot_id: str
    source_ref: str
    languages: tuple[str, ...]
    terms: int
    entity_candidates: int
    classification_candidates: int
    collisions: int
    quarantined: int
    warnings: int
    raw_directory: Path
    staging_directory: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "snapshot_id": self.snapshot_id,
            "source_ref": self.source_ref,
            "languages": list(self.languages),
            "terms": self.terms,
            "entity_candidates": self.entity_candidates,
            "classification_candidates": self.classification_candidates,
            "collisions": self.collisions,
            "quarantined": self.quarantined,
            "warnings": self.warnings,
            "raw_directory": self.raw_directory.as_posix(),
            "staging_directory": self.staging_directory.as_posix(),
            "promotion_status": "blocked",
        }


def normalize_search_key(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_letters = "".join(character for character in decomposed if not unicodedata.combining(character))
    lowered = ascii_letters.casefold().replace("_", " ").replace("-", " ")
    without_punctuation = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
    return " ".join(without_punctuation.split())


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256("\0".join(parts).encode("utf-8")).hexdigest()[:20]
    return f"odeuropa:{prefix}:{digest}"


def _validate_ref(source_ref: str) -> str:
    if not _REF_PATTERN.fullmatch(source_ref) or ".." in source_ref:
        raise ValueError("ref ODEUROPA inválida")
    return source_ref


def _source_urls(source_ref: str, filename: str, row_number: int | None = None) -> tuple[str, str]:
    raw_url = f"https://raw.githubusercontent.com/Odeuropa/multilingualTaxonomies/{source_ref}/taxonomies-v2/{filename}"
    locator = f"{REPOSITORY_URL}/blob/{source_ref}/taxonomies-v2/{filename}"
    if row_number is not None:
        locator = f"{locator}#L{row_number}"
    return raw_url, locator


def _download(url: str, *, retries: int = 3, timeout: int = 45) -> bytes:
    request = Request(url, headers={"User-Agent": "O-Antiquario/0.1 (+local research pipeline)"})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < retries:
                time.sleep(2**attempt)
    raise RuntimeError(f"não foi possível baixar {url}: {last_error}")


def _read_source_file(source_directory: Path | None, source_ref: str, filename: str) -> bytes:
    if source_directory is None:
        raw_url, _ = _source_urls(source_ref, filename)
        return _download(raw_url)

    candidates = (source_directory / "taxonomies-v2" / filename, source_directory / filename)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.read_bytes()
    raise FileNotFoundError(f"arquivo ODEUROPA ausente: {filename} em {source_directory}")


def _snapshot_id(source_ref: str, file_hashes: dict[str, str]) -> str:
    fingerprint = canonical_json({"source_ref": source_ref, "files": file_hashes})
    return sha256(fingerprint.encode("utf-8")).hexdigest()


def _parse_synsets(value: str) -> list[str]:
    raw = value.strip()
    if not raw:
        return []
    if not raw.startswith("["):
        if not re.fullmatch(r"[\w.-]+", raw, flags=re.UNICODE):
            raise ValueError("identificador de synset escalar inválido")
        return [raw]
    parsed = ast.literal_eval(raw)
    if not isinstance(parsed, list) or any(not isinstance(item, str) or not item.strip() for item in parsed):
        raise ValueError("synset precisa ser uma lista de strings")
    return sorted(set(item.strip() for item in parsed))


def _parse_category(value: str) -> tuple[str | None, list[str]]:
    raw = value.strip()
    if not raw:
        return None, []
    parts = [part.strip() for part in raw.split("|")]
    if not parts or parts[0].casefold() != "category" or any(not part for part in parts[1:]):
        raise ValueError("categoria fora do formato CATEGORY|rótulo")
    return raw, parts[1:]


def _parse_word(value: str) -> tuple[str, str, str]:
    entry = value.strip()
    if "_" not in entry:
        raise ValueError("entrada sem sufixo gramatical")
    term, suffix = entry.rsplit("_", 1)
    if not term.strip() or suffix not in POS_LABELS:
        raise ValueError(f"classe gramatical desconhecida: {suffix or '<vazia>'}")
    return entry, term.strip().replace("_", " "), POS_LABELS[suffix]


def _evidence_nature(source_method: str) -> str:
    if source_method.casefold() in {"seed", "startingcategories", "startinglist"}:
        return "curated"
    return "inferred"


def _parse_tsv(
    contents: bytes,
    *,
    language: str,
    filename: str,
    source_ref: str,
    snapshot_id: str,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError(f"{filename}: conteúdo não está em UTF-8") from error

    reader = csv.reader(io.StringIO(text), delimiter="\t")
    try:
        header = next(reader)
    except StopIteration as error:
        raise ValueError(f"{filename}: arquivo vazio") from error

    normalized_header = [column.strip() for column in header]
    positions = {column: index for index, column in enumerate(normalized_header) if column}
    missing = [column for column in REQUIRED_COLUMNS if column not in positions]
    if missing:
        raise ValueError(f"{filename}: colunas obrigatórias ausentes: {', '.join(missing)}")

    terms: list[dict[str, object]] = []
    quarantine: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    _, file_locator = _source_urls(source_ref, filename)

    for row_number, row in enumerate(reader, start=2):
        if not any(cell.strip() for cell in row):
            continue
        values = {column: row[index].strip() if index < len(row) else "" for column, index in positions.items()}
        row_context = {
            "source_id": SOURCE_ID,
            "source_ref": source_ref,
            "snapshot_id": snapshot_id,
            "language": language,
            "source_file": f"taxonomies-v2/{filename}",
            "source_row": row_number,
            "source_locator": f"{file_locator}#L{row_number}",
            "license": LICENSE_ID,
            "attribution": ATTRIBUTION,
        }

        extra_values = [cell.strip() for cell in row[len(normalized_header):] if cell.strip()]
        trailing_named_values = [
            row[index].strip()
            for index, column in enumerate(normalized_header)
            if not column and index < len(row) and row[index].strip()
        ]
        annotations = trailing_named_values + extra_values
        if annotations:
            warnings.append({**row_context, "reason": "extra_annotation", "values": annotations})

        try:
            entry, term_original, part_of_speech = _parse_word(values["word"])
            synsets = _parse_synsets(values["synset"])
            smell_raw, smell_labels = _parse_category(values["smell-source"])
            quality_raw, quality_labels = _parse_category(values["quality"])
            if smell_labels and quality_labels:
                raise ValueError("entrada classificada simultaneamente como fonte e qualidade")
            first_appearance_raw = values["first appearance"]
            if first_appearance_raw and not re.fullmatch(r"\d{3,4}", first_appearance_raw):
                raise ValueError("primeira ocorrência não é um ano válido")
            unexpected_periods = [
                f"{period}={values[period]}"
                for period in TIME_PERIODS
                if values[period].casefold() not in {"", "yes", "no"}
            ]
            if unexpected_periods:
                raise ValueError(f"marcadores temporais inválidos: {', '.join(unexpected_periods)}")
        except (SyntaxError, ValueError) as error:
            quarantine.append({
                **row_context,
                "reason": "malformed_row",
                "details": str(error),
                "raw_entry": values.get("word", ""),
            })
            continue

        search_key = normalize_search_key(term_original)
        if not search_key:
            quarantine.append({
                **row_context,
                "reason": "empty_normalized_term",
                "raw_entry": entry,
            })
            continue

        category_kind: str | None = None
        entity_type_candidate: str | None = None
        category_raw: str | None = None
        category_labels: list[str] = []
        if smell_labels:
            category_kind = "smell-source"
            entity_type_candidate = "odor-descriptor"
            category_raw = smell_raw
            category_labels = smell_labels
        elif quality_labels:
            category_kind = "quality"
            entity_type_candidate = "odor-quality"
            category_raw = quality_raw
            category_labels = quality_labels

        term_id = _stable_id("term", source_ref, language, filename, str(row_number))
        terms.append({
            "schema_version": 1,
            "id": term_id,
            "source_id": SOURCE_ID,
            "source_ref": source_ref,
            "snapshot_id": snapshot_id,
            "source_file": f"taxonomies-v2/{filename}",
            "source_row": row_number,
            "source_locator": f"{file_locator}#L{row_number}",
            "license": LICENSE_ID,
            "attribution": ATTRIBUTION,
            "language": language,
            "entry_original": entry,
            "term_original": term_original,
            "search_key": search_key,
            "part_of_speech": part_of_speech,
            "source_method": values["source"],
            "evidence_nature": _evidence_nature(values["source"]),
            "wordnet_synsets": synsets,
            "first_appearance": int(first_appearance_raw) if first_appearance_raw else None,
            "time_periods": [period for period in TIME_PERIODS if values[period].casefold() == "yes"],
            "category_kind": category_kind,
            "category_original": category_raw,
            "category_labels_original": category_labels,
            "entity_type_candidate": entity_type_candidate,
            "status": "candidate",
            "promotion_status": "blocked",
            "commercial_claims_generated": False,
        })

    return terms, quarantine, warnings


def _detect_collisions(terms: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    for term in terms:
        key = (str(term["language"]), str(term["search_key"]))
        groups.setdefault(key, []).append(term)

    collisions: list[dict[str, object]] = []
    for (language, search_key), records in sorted(groups.items()):
        signatures = {
            (
                str(record["entry_original"]),
                str(record["entity_type_candidate"]),
                tuple(record["wordnet_synsets"]),
                str(record["category_original"]),
            )
            for record in records
        }
        if len(signatures) <= 1:
            continue
        ids = sorted(str(record["id"]) for record in records)
        collisions.append({
            "schema_version": 1,
            "collision_id": _stable_id("collision", language, search_key, *ids),
            "source_id": SOURCE_ID,
            "language": language,
            "search_key": search_key,
            "candidate_ids": ids,
            "entries": sorted(set(str(record["entry_original"]) for record in records)),
            "reason": "normalized_term_maps_to_multiple_concepts",
            "status": "quarantined",
            "promotion_status": "blocked",
        })
        for record in records:
            record["status"] = "quarantined"
    return collisions


def _build_candidates(
    terms: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    entities: list[dict[str, object]] = []
    classifications: list[dict[str, object]] = []
    quarantine: list[dict[str, object]] = []
    for term in terms:
        entity_type = term["entity_type_candidate"]
        if entity_type is None:
            quarantine.append({
                "source_id": SOURCE_ID,
                "source_ref": term["source_ref"],
                "snapshot_id": term["snapshot_id"],
                "language": term["language"],
                "source_file": term["source_file"],
                "source_row": term["source_row"],
                "source_locator": term["source_locator"],
                "license": LICENSE_ID,
                "attribution": ATTRIBUTION,
                "term_id": term["id"],
                "raw_entry": term["entry_original"],
                "reason": "missing_odeuropa_category",
                "details": "sem categoria smell-source ou quality; tipo canônico não foi inferido",
                "status": "quarantined",
                "promotion_status": "blocked",
            })
            term["status"] = "quarantined"
            continue

        entity_id = _stable_id("entity-candidate", str(term["id"]), str(entity_type))
        entities.append({
            "schema_version": 1,
            "candidate_id": entity_id,
            "source_term_id": term["id"],
            "entity_type": entity_type,
            "label_original": term["term_original"],
            "language": term["language"],
            "search_key": term["search_key"],
            "part_of_speech": term["part_of_speech"],
            "wordnet_synsets": term["wordnet_synsets"],
            "mapping_nature": "inferred",
            "evidence_nature": term["evidence_nature"],
            "status": term["status"],
            "promotion_status": "blocked",
            "provenance": {
                "source_id": SOURCE_ID,
                "source_ref": term["source_ref"],
                "snapshot_id": term["snapshot_id"],
                "locator": term["source_locator"],
                "license": LICENSE_ID,
                "attribution": ATTRIBUTION,
                "method": term["source_method"],
            },
        })
        classifications.append({
            "schema_version": 1,
            "candidate_id": _stable_id("classification", str(term["id"]), str(term["category_original"])),
            "subject_candidate_id": entity_id,
            "classification_kind": term["category_kind"],
            "category_original": term["category_original"],
            "category_labels_original": term["category_labels_original"],
            "hierarchy_interpretation": "not_assumed",
            "evidence_nature": term["evidence_nature"],
            "status": term["status"],
            "promotion_status": "blocked",
            "provenance": {
                "source_id": SOURCE_ID,
                "source_ref": term["source_ref"],
                "snapshot_id": term["snapshot_id"],
                "locator": term["source_locator"],
                "license": LICENSE_ID,
                "attribution": ATTRIBUTION,
                "method": term["source_method"],
            },
        })
    return entities, classifications, quarantine


def sync_odeuropa(
    data_directory: Path,
    *,
    source_directory: Path | None = None,
    source_ref: str = DEFAULT_REF,
    languages: tuple[str, ...] | list[str] | None = None,
    retrieved_at: str | None = None,
) -> OdeuropaSyncResult:
    source_ref = _validate_ref(source_ref)
    selected_languages = tuple(sorted(set(languages or LANGUAGE_FILES)))
    invalid_languages = [language for language in selected_languages if language not in LANGUAGE_FILES]
    if invalid_languages:
        raise ValueError(f"idiomas ODEUROPA inválidos: {', '.join(invalid_languages)}")
    if not selected_languages:
        raise ValueError("selecione ao menos um idioma ODEUROPA")

    source_directory = source_directory.resolve() if source_directory else None
    payloads: dict[str, bytes] = {}
    file_hashes: dict[str, str] = {}
    for language in selected_languages:
        filename = LANGUAGE_FILES[language]
        contents = _read_source_file(source_directory, source_ref, filename)
        payloads[language] = contents
        file_hashes[f"taxonomies-v2/{filename}"] = sha256(contents).hexdigest()

    snapshot_id = _snapshot_id(source_ref, file_hashes)
    snapshot_key = snapshot_id[:16]
    raw_directory = data_directory / "raw" / "odeuropa" / snapshot_key
    staging_directory = data_directory / "staging" / "odeuropa" / snapshot_key
    manifest_path = raw_directory / "snapshot.json"
    retrieval_date = retrieved_at or datetime.now(timezone.utc).date().isoformat()

    if not manifest_path.exists():
        for language in selected_languages:
            filename = LANGUAGE_FILES[language]
            atomic_write_bytes(raw_directory / "taxonomies-v2" / filename, payloads[language])
        snapshot_manifest = {
            "schema_version": 1,
            "source_id": SOURCE_ID,
            "source_ref": source_ref,
            "snapshot_id": snapshot_id,
            "retrieved_at": retrieval_date,
            "license": LICENSE_ID,
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "attribution": ATTRIBUTION,
            "repository_url": REPOSITORY_URL,
            "files": [
                {
                    "language": language,
                    "path": f"taxonomies-v2/{LANGUAGE_FILES[language]}",
                    "sha256": file_hashes[f"taxonomies-v2/{LANGUAGE_FILES[language]}"],
                    "source_url": _source_urls(source_ref, LANGUAGE_FILES[language])[0],
                }
                for language in selected_languages
            ],
        }
        atomic_write_text(manifest_path, f"{json.dumps(snapshot_manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    else:
        existing_manifest = load_json(manifest_path)
        if existing_manifest.get("snapshot_id") != snapshot_id:
            raise RuntimeError("colisão de diretório no snapshot ODEUROPA")
        retrieval_date = str(existing_manifest["retrieved_at"])

    terms: list[dict[str, object]] = []
    quarantine: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    for language in selected_languages:
        parsed_terms, parsed_quarantine, parsed_warnings = _parse_tsv(
            payloads[language],
            language=language,
            filename=LANGUAGE_FILES[language],
            source_ref=source_ref,
            snapshot_id=snapshot_id,
        )
        terms.extend(parsed_terms)
        quarantine.extend(parsed_quarantine)
        warnings.extend(parsed_warnings)

    terms.sort(key=lambda record: (str(record["language"]), str(record["search_key"]), str(record["id"])))
    collisions = _detect_collisions(terms)
    entities, classifications, classification_quarantine = _build_candidates(terms)
    quarantine.extend(classification_quarantine)
    entities.sort(key=lambda record: str(record["candidate_id"]))
    classifications.sort(key=lambda record: str(record["candidate_id"]))
    quarantine.sort(key=lambda record: (str(record.get("language", "")), int(record.get("source_row", 0)), str(record.get("reason", ""))))
    warnings.sort(key=lambda record: (str(record.get("language", "")), int(record.get("source_row", 0))))

    write_dicts_jsonl(staging_directory / "terms.jsonl", terms)
    write_dicts_jsonl(staging_directory / "entity-candidates.jsonl", entities)
    write_dicts_jsonl(staging_directory / "classification-candidates.jsonl", classifications)
    write_dicts_jsonl(staging_directory / "collisions.jsonl", collisions)
    write_dicts_jsonl(staging_directory / "quarantine.jsonl", quarantine)
    write_dicts_jsonl(staging_directory / "warnings.jsonl", warnings)

    counts_by_language = {
        language: sum(1 for term in terms if term["language"] == language)
        for language in selected_languages
    }
    counts_by_entity_type = {
        entity_type: sum(1 for entity in entities if entity["entity_type"] == entity_type)
        for entity_type in ("odor-descriptor", "odor-quality")
    }
    report = {
        "schema_version": 1,
        "source_id": SOURCE_ID,
        "source_ref": source_ref,
        "snapshot_id": snapshot_id,
        "retrieved_at": retrieval_date,
        "license": LICENSE_ID,
        "attribution": ATTRIBUTION,
        "languages": list(selected_languages),
        "counts": {
            "terms": len(terms),
            "entity_candidates": len(entities),
            "classification_candidates": len(classifications),
            "collisions": len(collisions),
            "quarantined": len(quarantine),
            "warnings": len(warnings),
            "by_language": counts_by_language,
            "by_entity_type": counts_by_entity_type,
        },
        "guards": {
            "target_layer": "staging",
            "promotion_status": "blocked",
            "commercial_claims_generated": False,
            "forbidden_predicates": [
                "has-note",
                "has-top-note",
                "has-heart-note",
                "has-base-note",
                "declares-*",
            ],
            "category_hierarchy_interpretation": "not_assumed",
        },
        "files": {
            "terms": "terms.jsonl",
            "entity_candidates": "entity-candidates.jsonl",
            "classification_candidates": "classification-candidates.jsonl",
            "collisions": "collisions.jsonl",
            "quarantine": "quarantine.jsonl",
            "warnings": "warnings.jsonl",
        },
    }
    atomic_write_text(staging_directory / "report.json", f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    latest = {
        "schema_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": snapshot_id,
        "source_ref": source_ref,
        "staging_directory": staging_directory.relative_to(data_directory).as_posix(),
        "report_sha256": sha256(canonical_json(report).encode("utf-8")).hexdigest(),
    }
    atomic_write_text(
        data_directory / "staging" / "odeuropa" / "latest.json",
        f"{json.dumps(latest, ensure_ascii=False, sort_keys=True, indent=2)}\n",
    )

    return OdeuropaSyncResult(
        snapshot_id=snapshot_id,
        source_ref=source_ref,
        languages=selected_languages,
        terms=len(terms),
        entity_candidates=len(entities),
        classification_candidates=len(classifications),
        collisions=len(collisions),
        quarantined=len(quarantine),
        warnings=len(warnings),
        raw_directory=raw_directory,
        staging_directory=staging_directory,
    )
