from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import time
from typing import Any, Callable, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .io_utils import (
    atomic_write_text,
    load_json,
    save_raw_snapshot,
    write_dicts_jsonl,
    write_olfactory_descriptors_jsonl,
    write_records_jsonl,
)
from .models import EntityReference, FragranceRecord, OlfactoryDescriptorRecord, Provenance, QID_PATTERN
from .warehouse import _duckdb


WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "O-Antiquario/0.1 (https://github.com/marlonhms/o-Antiquario; contato via GitHub)"


def build_perfume_query(limit: int, *, origin_countries: Sequence[str] = ()) -> str:
    if not 1 <= limit <= 5_000:
        raise ValueError("limit deve estar entre 1 e 5000")
    normalized_countries = tuple(sorted(set(origin_countries)))
    invalid_countries = [country for country in normalized_countries if not QID_PATTERN.fullmatch(country)]
    if invalid_countries:
        raise ValueError(f"QIDs de país inválidos: {', '.join(invalid_countries)}")
    country_filter = ""
    if normalized_countries:
        values = " ".join(f"wd:{country}" for country in normalized_countries)
        country_filter = f"  VALUES ?requestedOriginCountry {{ {values} }}\n  ?item wdt:P495 ?requestedOriginCountry .\n"
    return f"""SELECT ?item ?itemLabel ?brand ?brandLabel ?country ?countryLabel
       ?perfumer ?perfumerLabel ?inception ?publicationDate ?officialWebsite
WHERE {{
  ?item wdt:P31/wdt:P279* wd:Q131746 .
{country_filter}
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


def build_discovery_queries(limit: int, discovery_countries: Sequence[str] = ()) -> tuple[str, ...]:
    normalized_countries = tuple(sorted(set(discovery_countries)))
    if len(normalized_countries) > 8:
        raise ValueError("Use no máximo oito países de descoberta por sincronização")
    return (
        build_perfume_query(limit),
        *(build_perfume_query(limit, origin_countries=(country,)) for country in normalized_countries),
    )


def merge_sparql_payloads(payloads: Sequence[dict[str, Any]]) -> dict[str, Any]:
    bindings: list[dict[str, Any]] = []
    for payload in payloads:
        source_bindings = payload.get("results", {}).get("bindings")
        if not isinstance(source_bindings, list):
            raise ValueError("Resposta SPARQL não contém results.bindings")
        bindings.extend(binding for binding in source_bindings if isinstance(binding, dict))
    return {"head": {"vars": []}, "results": {"bindings": bindings}}


def build_property_audit_query(wikidata_ids: Sequence[str]) -> str:
    normalized_ids = tuple(sorted(set(wikidata_ids)))
    if not normalized_ids:
        raise ValueError("A auditoria exige ao menos um QID de fragrância")
    if len(normalized_ids) > 100:
        raise ValueError("A auditoria aceita no máximo 100 QIDs por consulta")
    invalid_ids = [wikidata_id for wikidata_id in normalized_ids if not QID_PATTERN.fullmatch(wikidata_id)]
    if invalid_ids:
        raise ValueError(f"QIDs inválidos na auditoria: {', '.join(invalid_ids)}")
    values = " ".join(f"wd:{wikidata_id}" for wikidata_id in normalized_ids)
    return f"""SELECT ?property ?propertyLabel
       (COUNT(DISTINCT ?item) AS ?itemsWithProperty)
       (COUNT(*) AS ?statements)
WHERE {{
  VALUES ?item {{ {values} }}
  ?item ?directProperty ?value .
  ?property wikibase:directClaim ?directProperty .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pt,en". }}
}}
GROUP BY ?property ?propertyLabel
ORDER BY DESC(?itemsWithProperty) ?property"""


def build_olfactory_descriptor_query(wikidata_ids: Sequence[str]) -> str:
    normalized_ids = tuple(sorted(set(wikidata_ids)))
    if not normalized_ids:
        raise ValueError("A sincronização de descritores exige ao menos um QID de fragrância")
    if len(normalized_ids) > 100:
        raise ValueError("A sincronização de descritores aceita no máximo 100 QIDs por consulta")
    invalid_ids = [wikidata_id for wikidata_id in normalized_ids if not QID_PATTERN.fullmatch(wikidata_id)]
    if invalid_ids:
        raise ValueError(f"QIDs inválidos na sincronização de descritores: {', '.join(invalid_ids)}")
    values = " ".join(f"wd:{wikidata_id}" for wikidata_id in normalized_ids)
    return f"""SELECT ?item ?descriptor ?descriptorLabel
WHERE {{
  VALUES ?item {{ {values} }}
  ?item wdt:P5872 ?descriptor .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language \"pt,en\". }}
}}
ORDER BY ?item ?descriptor"""


def _property_id(uri: str | None) -> str | None:
    if not uri:
        return None
    candidate = uri.rsplit("/", 1)[-1]
    return candidate if re.fullmatch(r"P[1-9][0-9]*", candidate) else None


def summarize_property_audit(payload: dict[str, Any]) -> list[dict[str, Any]]:
    bindings = payload.get("results", {}).get("bindings")
    if not isinstance(bindings, list):
        raise ValueError("Resposta SPARQL não contém results.bindings")
    properties: dict[str, dict[str, Any]] = {}
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        property_id = _property_id(_binding_value(binding, "property"))
        label = _binding_value(binding, "propertyLabel")
        items = _binding_value(binding, "itemsWithProperty")
        statements = _binding_value(binding, "statements")
        if not property_id or not label or not items or not statements:
            continue
        current = properties.setdefault(property_id, {
            "propertyId": property_id,
            "label": label,
            "itemsWithProperty": 0,
            "statements": 0,
        })
        current["itemsWithProperty"] += int(items)
        current["statements"] += int(statements)
    return sorted(
        properties.values(),
        key=lambda item: (-item["itemsWithProperty"], -item["statements"], item["propertyId"]),
    )


def normalize_olfactory_descriptor_payload(
    payload: dict[str, Any],
    *,
    accepted_fragrance_ids: set[str],
    retrieved_at: str,
    snapshot_id: str,
) -> list[OlfactoryDescriptorRecord]:
    bindings = payload.get("results", {}).get("bindings")
    if not isinstance(bindings, list):
        raise ValueError("Resposta SPARQL não contém results.bindings")
    records: set[OlfactoryDescriptorRecord] = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        fragrance_id = _entity_id(_binding_value(binding, "item"))
        descriptor = _entity_reference(binding, "descriptor", "descriptorLabel")
        if not fragrance_id or fragrance_id not in accepted_fragrance_ids or not descriptor:
            continue
        records.add(OlfactoryDescriptorRecord(
            fragrance_wikidata_id=fragrance_id,
            descriptor=descriptor,
            provenance=Provenance(
                source_id="wikidata",
                source_url=f"https://www.wikidata.org/wiki/{fragrance_id}",
                license="CC0-1.0",
                retrieved_at=retrieved_at,
                snapshot_id=snapshot_id,
            ),
        ))
    return sorted(records)


def audit_wikidata_properties(
    data_directory: Path,
    *,
    output_path: Path,
    batch_size: int = 100,
    retrieved_at: str | None = None,
    fetcher: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if not 1 <= batch_size <= 100:
        raise ValueError("batch_size deve estar entre 1 e 100")
    database_path = data_directory / "catalog" / "catalog.duckdb"
    if not database_path.exists():
        raise FileNotFoundError("Catálogo DuckDB ausente. Execute data:build antes da auditoria.")
    connection = _duckdb().connect(str(database_path), read_only=True)
    try:
        wikidata_ids = [row[0] for row in connection.execute("SELECT wikidata_id FROM fragrances ORDER BY wikidata_id").fetchall()]
    finally:
        connection.close()
    queries = [build_property_audit_query(wikidata_ids[index:index + batch_size]) for index in range(0, len(wikidata_ids), batch_size)]
    query_fetcher = fetcher or fetch_sparql
    payload = merge_sparql_payloads([query_fetcher(query) for query in queries])
    raw_path, envelope = save_raw_snapshot(
        payload,
        "\n\n".join(queries),
        data_directory / "raw" / "wikidata" / "property-audits",
        retrieved_at=retrieved_at,
        filename_prefix="properties",
    )
    known_identity_properties = {
        "P31", "P170", "P495", "P571", "P577", "P856", "P14539", "P1716", "P176", "P5872",
    }
    properties = summarize_property_audit(envelope["payload"])
    report = {
        "schemaVersion": 1,
        "sourceId": "wikidata",
        "retrievedAt": envelope["retrieved_at"],
        "snapshotId": envelope["snapshot_id"],
        "rawPath": raw_path.relative_to(data_directory).as_posix(),
        "scope": {"fragranceQids": len(wikidata_ids), "batchSize": batch_size},
        "knownIdentityProperties": sorted(known_identity_properties),
        "unmappedProperties": [item for item in properties if item["propertyId"] not in known_identity_properties],
        "properties": properties,
        "interpretation": "A auditoria identifica propriedades estruturadas existentes; P5872 entra como descritor factual, sem inferir pirâmide, acorde ou desempenho.",
    }
    atomic_write_text(output_path, f"{json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return report


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
    olfactory_descriptors_path: Path
    olfactory_descriptors: int
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
            "olfactory_descriptors_path": self.olfactory_descriptors_path.as_posix(),
            "olfactory_descriptors": self.olfactory_descriptors,
            "snapshot_id": self.snapshot_id,
            "retrieved_at": self.retrieved_at,
        }


def sync_wikidata(
    data_directory: Path,
    *,
    limit: int = 500,
    fixture: Path | None = None,
    retrieved_at: str | None = None,
    discovery_countries: Sequence[str] = (),
) -> WikidataSyncResult:
    queries = build_discovery_queries(limit, discovery_countries)
    query = "\n\n".join(f"# discovery-query-{index}\n{item}" for index, item in enumerate(queries, start=1))
    fixture_contents = load_json(fixture) if fixture else None
    if fixture_contents is not None and discovery_countries:
        raise ValueError("Fixtures não podem ser combinadas com descoberta regional")
    if isinstance(fixture_contents, dict) and fixture_contents.get("source_id") == "wikidata" and "payload" in fixture_contents:
        payload = fixture_contents["payload"]
        retrieved_at = retrieved_at or fixture_contents.get("retrieved_at")
    else:
        payload = fixture_contents if fixture_contents is not None else merge_sparql_payloads(
            [fetch_sparql(item) for item in queries]
        )
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
    descriptors_path = data_directory / "staging" / "wikidata" / "olfactory-descriptors.jsonl"
    quarantine_path = data_directory / "staging" / "wikidata" / "quarantined.jsonl"
    quality_report_path = data_directory / "staging" / "wikidata" / "quality-report.json"
    write_records_jsonl(staging_path, records)
    descriptors: list[OlfactoryDescriptorRecord] = []
    if fixture_contents is None and records:
        descriptor_queries = [
            build_olfactory_descriptor_query([record.wikidata_id for record in records[index:index + 100]])
            for index in range(0, len(records), 100)
        ]
        descriptor_payload = merge_sparql_payloads([fetch_sparql(item) for item in descriptor_queries])
        _, descriptor_envelope = save_raw_snapshot(
            descriptor_payload,
            "\n\n".join(descriptor_queries),
            data_directory / "raw" / "wikidata" / "olfactory-descriptors",
            retrieved_at=envelope["retrieved_at"],
            filename_prefix="descriptors",
        )
        descriptors = normalize_olfactory_descriptor_payload(
            descriptor_envelope["payload"],
            accepted_fragrance_ids={record.wikidata_id for record in records},
            retrieved_at=descriptor_envelope["retrieved_at"],
            snapshot_id=descriptor_envelope["snapshot_id"],
        )
    write_olfactory_descriptors_jsonl(descriptors_path, descriptors)
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
            "with_olfactory_descriptors": len({record.fragrance_wikidata_id for record in descriptors}),
        },
        "discovery_countries": sorted(set(discovery_countries)),
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
        olfactory_descriptors_path=descriptors_path,
        olfactory_descriptors=len(descriptors),
        snapshot_id=envelope["snapshot_id"],
        retrieved_at=envelope["retrieved_at"],
    )
