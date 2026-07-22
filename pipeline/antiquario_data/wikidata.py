from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .io_utils import atomic_write_text, load_json, save_raw_snapshot, write_dicts_jsonl, write_records_jsonl
from .models import EntityReference, FragranceRecord, Provenance, QID_PATTERN


WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "O-Antiquario/0.1 (https://github.com/marlonhms/o-Antiquario; contato via GitHub)"


def build_perfume_query(limit: int) -> str:
    if not 1 <= limit <= 5_000:
        raise ValueError("limit deve estar entre 1 e 5000")
    return f"""SELECT ?item ?itemLabel ?brand ?brandLabel ?country ?countryLabel
       ?perfumer ?perfumerLabel ?inception ?publicationDate ?officialWebsite
WHERE {{
  ?item wdt:P31/wdt:P279* wd:Q131746 .
  OPTIONAL {{ ?item wdt:P1716 ?declaredBrand . }}
  OPTIONAL {{ ?item wdt:P176 ?manufacturer . }}
  BIND(COALESCE(?declaredBrand, ?manufacturer) AS ?brand)
  OPTIONAL {{ ?item wdt:P495 ?country . }}
  OPTIONAL {{ ?item wdt:P14539 ?declaredPerfumer . }}
  OPTIONAL {{ ?item wdt:P170 ?creator . }}
  BIND(COALESCE(?declaredPerfumer, ?creator) AS ?perfumer)
  OPTIONAL {{ ?item wdt:P571 ?inception . }}
  OPTIONAL {{ ?item wdt:P577 ?publicationDate . }}
  OPTIONAL {{ ?item wdt:P856 ?officialWebsite . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pt,en". }}
}}
ORDER BY ?item
LIMIT {limit}"""


def fetch_sparql(
    query: str,
    *,
    endpoint: str = WIKIDATA_ENDPOINT,
    attempts: int = 4,
    timeout_seconds: int = 30,
    sleeper: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    request_body = urlencode({"query": query, "format": "json"}).encode("utf-8")
    request = Request(
        endpoint,
        data=request_body,
        method="POST",
        headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": USER_AGENT,
        },
    )

    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            retryable = error.code == 429 or 500 <= error.code < 600
            if not retryable or attempt == attempts - 1:
                raise RuntimeError(f"Wikidata respondeu HTTP {error.code}") from error
            retry_after = error.headers.get("Retry-After")
            wait = min(float(retry_after), 30.0) if retry_after and retry_after.isdigit() else 2**attempt
            sleeper(wait)
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            if attempt == attempts - 1:
                raise RuntimeError(f"Falha ao consultar Wikidata: {error}") from error
            sleeper(2**attempt)

    raise RuntimeError("Falha inesperada ao consultar Wikidata")


def _binding_value(binding: dict[str, Any], key: str) -> str | None:
    value = binding.get(key, {}).get("value")
    return value.strip() if isinstance(value, str) and value.strip() else None


def _entity_id(uri: str | None) -> str | None:
    if not uri:
        return None
    candidate = uri.rsplit("/", 1)[-1]
    return candidate if QID_PATTERN.fullmatch(candidate) else None


def _entity_reference(binding: dict[str, Any], entity_key: str, label_key: str) -> EntityReference | None:
    wikidata_id = _entity_id(_binding_value(binding, entity_key))
    label = _binding_value(binding, label_key)
    if not wikidata_id or not label:
        return None
    return EntityReference(wikidata_id=wikidata_id, label=label)


def _extract_year(value: str | None) -> int | None:
    if not value:
        return None
    match = re.match(r"^(\d{4})", value)
    if not match:
        return None
    year = int(match.group(1))
    return year if 1000 <= year <= 2100 else None


def _quarantine_reason(wikidata_id: str, name: str) -> str | None:
    if name == wikidata_id:
        return "missing_human_label"
    normalized = name.casefold().strip()
    generic_suffixes = (
        " essential oil",
        " flower oil",
        " fragrance oil",
        " perfume concentration",
    )
    if normalized.endswith(generic_suffixes):
        return "possible_non_product_material"
    return None


def normalize_sparql_payload_with_quality(
    payload: dict[str, Any],
    *,
    retrieved_at: str,
    snapshot_id: str,
) -> tuple[list[FragranceRecord], list[dict[str, str]]]:
    bindings = payload.get("results", {}).get("bindings")
    if not isinstance(bindings, list):
        raise ValueError("Resposta SPARQL não contém results.bindings")

    grouped: dict[str, dict[str, Any]] = {}
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        wikidata_id = _entity_id(_binding_value(binding, "item"))
        name = _binding_value(binding, "itemLabel")
        if not wikidata_id or not name:
            continue

        state = grouped.setdefault(wikidata_id, {
            "names": [],
            "years": set(),
            "websites": set(),
            "brands": set(),
            "perfumers": set(),
            "countries": set(),
        })
        language = binding.get("itemLabel", {}).get("xml:lang", "und")
        state["names"].append((0 if language == "pt" else 1 if language == "en" else 2, name, language))
        for date_key in ("inception", "publicationDate"):
            year = _extract_year(_binding_value(binding, date_key))
            if year is not None:
                state["years"].add(year)
        website = _binding_value(binding, "officialWebsite")
        if website:
            state["websites"].add(website)
        for collection, entity_key, label_key in (
            ("brands", "brand", "brandLabel"),
            ("perfumers", "perfumer", "perfumerLabel"),
            ("countries", "country", "countryLabel"),
        ):
            reference = _entity_reference(binding, entity_key, label_key)
            if reference:
                state[collection].add(reference)

    records: list[FragranceRecord] = []
    quarantined: list[dict[str, str]] = []
    for wikidata_id, state in sorted(grouped.items()):
        _, name, language = sorted(set(state["names"]))[0]
        reason = _quarantine_reason(wikidata_id, name)
        if reason:
            quarantined.append({
                "wikidata_id": wikidata_id,
                "name": name,
                "reason": reason,
                "source_url": f"https://www.wikidata.org/wiki/{wikidata_id}",
            })
            continue
        years = sorted(state["years"])
        websites = sorted(state["websites"])
        records.append(FragranceRecord(
            id=f"wd-{wikidata_id.lower()}",
            wikidata_id=wikidata_id,
            name=name,
            name_language=language,
            launch_year=years[0] if years else None,
            official_website=websites[0] if websites else None,
            brands=tuple(sorted(state["brands"])),
            perfumers=tuple(sorted(state["perfumers"])),
            countries=tuple(sorted(state["countries"])),
            provenance=Provenance(
                source_id="wikidata",
                source_url=f"https://www.wikidata.org/wiki/{wikidata_id}",
                license="CC0-1.0",
                retrieved_at=retrieved_at,
                snapshot_id=snapshot_id,
            ),
        ))
    return records, quarantined


def normalize_sparql_payload(
    payload: dict[str, Any],
    *,
    retrieved_at: str,
    snapshot_id: str,
) -> list[FragranceRecord]:
    records, _ = normalize_sparql_payload_with_quality(
        payload,
        retrieved_at=retrieved_at,
        snapshot_id=snapshot_id,
    )
    return records


@dataclass(frozen=True)
class WikidataSyncResult:
    snapshot_path: Path
    staging_path: Path
    records: int
    quarantined: int
    quarantine_path: Path
    quality_report_path: Path
    snapshot_id: str
    retrieved_at: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "snapshot_path": self.snapshot_path.as_posix(),
            "staging_path": self.staging_path.as_posix(),
            "records": self.records,
            "quarantined": self.quarantined,
            "quarantine_path": self.quarantine_path.as_posix(),
            "quality_report_path": self.quality_report_path.as_posix(),
            "snapshot_id": self.snapshot_id,
            "retrieved_at": self.retrieved_at,
        }


def sync_wikidata(
    data_directory: Path,
    *,
    limit: int = 500,
    fixture: Path | None = None,
    retrieved_at: str | None = None,
) -> WikidataSyncResult:
    query = build_perfume_query(limit)
    fixture_contents = load_json(fixture) if fixture else None
    if isinstance(fixture_contents, dict) and fixture_contents.get("source_id") == "wikidata" and "payload" in fixture_contents:
        payload = fixture_contents["payload"]
        retrieved_at = retrieved_at or fixture_contents.get("retrieved_at")
    else:
        payload = fixture_contents if fixture_contents is not None else fetch_sparql(query)
    snapshot_path, envelope = save_raw_snapshot(
        payload,
        query,
        data_directory / "raw" / "wikidata",
        retrieved_at=retrieved_at,
    )
    records, quarantined = normalize_sparql_payload_with_quality(
        envelope["payload"],
        retrieved_at=envelope["retrieved_at"],
        snapshot_id=envelope["snapshot_id"],
    )
    staging_path = data_directory / "staging" / "wikidata" / "fragrances.jsonl"
    quarantine_path = data_directory / "staging" / "wikidata" / "quarantined.jsonl"
    quality_report_path = data_directory / "staging" / "wikidata" / "quality-report.json"
    write_records_jsonl(staging_path, records)
    write_dicts_jsonl(quarantine_path, quarantined)
    quality_report = {
        "schema_version": 1,
        "source_id": "wikidata",
        "snapshot_id": envelope["snapshot_id"],
        "input_rows": len(envelope["payload"].get("results", {}).get("bindings", [])),
        "accepted_records": len(records),
        "quarantined_records": len(quarantined),
        "coverage": {
            "with_brand": sum(bool(record.brands) for record in records),
            "with_perfumer": sum(bool(record.perfumers) for record in records),
            "with_country": sum(bool(record.countries) for record in records),
            "with_launch_year": sum(record.launch_year is not None for record in records),
            "with_official_website": sum(record.official_website is not None for record in records),
        },
    }
    atomic_write_text(
        quality_report_path,
        f"{json.dumps(quality_report, ensure_ascii=False, sort_keys=True, indent=2)}\n",
    )
    return WikidataSyncResult(
        snapshot_path=snapshot_path,
        staging_path=staging_path,
        records=len(records),
        quarantined=len(quarantined),
        quarantine_path=quarantine_path,
        quality_report_path=quality_report_path,
        snapshot_id=envelope["snapshot_id"],
        retrieved_at=envelope["retrieved_at"],
    )
