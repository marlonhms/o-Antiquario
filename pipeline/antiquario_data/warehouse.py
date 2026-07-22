from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
from typing import Any

from .io_utils import atomic_write_text, read_olfactory_descriptors_jsonl, read_records_jsonl, read_semantic_claims_jsonl
from .models import FragranceRecord, OlfactoryDescriptorRecord, WikidataSemanticClaimRecord, canonical_json


def _duckdb() -> Any:
    try:
        import duckdb
    except ModuleNotFoundError as error:
        raise RuntimeError("DuckDB ausente. Execute a instalação do ambiente Python do projeto.") from error
    return duckdb


def _sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''").replace("\\", "/")


def _relation_rows(records: list[FragranceRecord], attribute: str) -> list[tuple[str, str, str]]:
    rows = {
        (record.id, reference.wikidata_id, reference.label)
        for record in records
        for reference in getattr(record, attribute)
    }
    return sorted(rows)


def _olfactory_descriptor_rows(
    records: list[OlfactoryDescriptorRecord],
    fragrance_ids: dict[str, str],
) -> list[tuple[str, str, str, str, str, str, str, str]]:
    rows = {
        (
            fragrance_ids[record.fragrance_wikidata_id],
            record.descriptor.wikidata_id,
            record.descriptor.label,
            record.provenance.source_id,
            record.provenance.source_url,
            record.provenance.license,
            record.provenance.retrieved_at,
            record.provenance.snapshot_id,
        )
        for record in records
        if record.fragrance_wikidata_id in fragrance_ids
    }
    return sorted(rows)


def _semantic_claim_rows(
    records: list[WikidataSemanticClaimRecord],
    fragrance_ids: dict[str, str],
) -> list[tuple[str, str, str, str, str, str, str, str, str, str]]:
    rows = {
        (
            fragrance_ids[record.fragrance_wikidata_id],
            record.property.wikidata_id,
            record.property.label,
            record.value.wikidata_id,
            record.value.label,
            record.provenance.source_id,
            record.provenance.source_url,
            record.provenance.license,
            record.provenance.retrieved_at,
            record.provenance.snapshot_id,
        )
        for record in records
        if record.fragrance_wikidata_id in fragrance_ids
    }
    return sorted(rows)


def build_catalog(data_directory: Path) -> dict[str, Any]:
    staging_path = data_directory / "staging" / "wikidata" / "fragrances.jsonl"
    descriptors_staging_path = data_directory / "staging" / "wikidata" / "olfactory-descriptors.jsonl"
    claims_staging_path = data_directory / "staging" / "wikidata" / "semantic-claims.jsonl"
    if not staging_path.exists():
        raise FileNotFoundError(f"Staging ausente: {staging_path}. Execute sync wikidata primeiro.")
    records = sorted(read_records_jsonl(staging_path), key=lambda record: record.id)
    descriptors = read_olfactory_descriptors_jsonl(descriptors_staging_path) if descriptors_staging_path.exists() else []
    semantic_claims = read_semantic_claims_jsonl(claims_staging_path) if claims_staging_path.exists() else []
    if not records:
        raise ValueError("O staging não contém fragrâncias válidas")

    ids = [record.id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("O staging contém IDs duplicados")

    catalog_directory = data_directory / "catalog"
    parquet_directory = catalog_directory / "parquet"
    catalog_directory.mkdir(parents=True, exist_ok=True)
    parquet_directory.mkdir(parents=True, exist_ok=True)
    database_path = catalog_directory / "catalog.duckdb"
    temporary_database = catalog_directory / ".catalog.tmp.duckdb"
    if temporary_database.exists():
        temporary_database.unlink()

    duckdb = _duckdb()
    connection = duckdb.connect(str(temporary_database))
    try:
        connection.execute("""
            CREATE TABLE fragrances (
              id VARCHAR PRIMARY KEY,
              wikidata_id VARCHAR UNIQUE NOT NULL,
              name VARCHAR NOT NULL,
              name_language VARCHAR NOT NULL,
              launch_year INTEGER,
              official_website VARCHAR,
              source_id VARCHAR NOT NULL,
              source_url VARCHAR NOT NULL,
              license VARCHAR NOT NULL,
              retrieved_at DATE NOT NULL,
              snapshot_id VARCHAR NOT NULL,
              record_hash VARCHAR NOT NULL
            )
        """)
        connection.executemany(
            "INSERT INTO fragrances VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(
                record.id,
                record.wikidata_id,
                record.name,
                record.name_language,
                record.launch_year,
                record.official_website,
                record.provenance.source_id,
                record.provenance.source_url,
                record.provenance.license,
                record.provenance.retrieved_at,
                record.provenance.snapshot_id,
                record.record_hash,
            ) for record in records],
        )

        for table, attribute in (
            ("fragrance_brands", "brands"),
            ("fragrance_perfumers", "perfumers"),
            ("fragrance_countries", "countries"),
        ):
            connection.execute(f"""
                CREATE TABLE {table} (
                  fragrance_id VARCHAR NOT NULL,
                  wikidata_id VARCHAR NOT NULL,
                  label VARCHAR NOT NULL,
                  PRIMARY KEY (fragrance_id, wikidata_id)
                )
            """)
            rows = _relation_rows(records, attribute)
            if rows:
                connection.executemany(f"INSERT INTO {table} VALUES (?, ?, ?)", rows)

        connection.execute("""
            CREATE TABLE fragrance_olfactory_descriptors (
              fragrance_id VARCHAR NOT NULL,
              wikidata_id VARCHAR NOT NULL,
              label VARCHAR NOT NULL,
              source_id VARCHAR NOT NULL,
              source_url VARCHAR NOT NULL,
              license VARCHAR NOT NULL,
              retrieved_at DATE NOT NULL,
              snapshot_id VARCHAR NOT NULL,
              PRIMARY KEY (fragrance_id, wikidata_id)
            )
        """)
        descriptor_rows = _olfactory_descriptor_rows(
            descriptors,
            {record.wikidata_id: record.id for record in records},
        )
        if descriptor_rows:
            connection.executemany("INSERT INTO fragrance_olfactory_descriptors VALUES (?, ?, ?, ?, ?, ?, ?, ?)", descriptor_rows)

        connection.execute("""
            CREATE TABLE fragrance_semantic_claims (
              fragrance_id VARCHAR NOT NULL,
              property_id VARCHAR NOT NULL,
              property_label VARCHAR NOT NULL,
              value_wikidata_id VARCHAR NOT NULL,
              value_label VARCHAR NOT NULL,
              source_id VARCHAR NOT NULL,
              source_url VARCHAR NOT NULL,
              license VARCHAR NOT NULL,
              retrieved_at DATE NOT NULL,
              snapshot_id VARCHAR NOT NULL,
              PRIMARY KEY (fragrance_id, property_id, value_wikidata_id)
            )
        """)
        claim_rows = _semantic_claim_rows(
            semantic_claims,
            {record.wikidata_id: record.id for record in records},
        )
        if claim_rows:
            connection.executemany("INSERT INTO fragrance_semantic_claims VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", claim_rows)

        connection.execute("CREATE INDEX fragrance_name_idx ON fragrances(name)")
        for table in (
            "fragrances", "fragrance_brands", "fragrance_perfumers", "fragrance_countries",
            "fragrance_olfactory_descriptors",
            "fragrance_semantic_claims",
        ):
            parquet_path = parquet_directory / f"{table}.parquet"
            if parquet_path.exists():
                parquet_path.unlink()
            connection.execute(
                f"COPY (SELECT * FROM {table} ORDER BY ALL) TO '{_sql_path(parquet_path)}' (FORMAT PARQUET, COMPRESSION ZSTD)"
            )
    finally:
        connection.close()

    os.replace(temporary_database, database_path)
    payload = {
        "fragrances": [record.as_dict() for record in records],
        "olfactory_descriptors": [record.as_dict() for record in sorted(descriptors)],
        "semantic_claims": [record.as_dict() for record in sorted(semantic_claims)],
    }
    content_hash = sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    counts = {
        "fragrances": len(records),
        "brands": len(_relation_rows(records, "brands")),
        "perfumers": len(_relation_rows(records, "perfumers")),
        "countries": len(_relation_rows(records, "countries")),
        "olfactory_descriptors": len(descriptor_rows),
        "semantic_claims": len(claim_rows),
    }
    manifest = {
        "schema_version": 1,
        "catalog_version": f"catalog-v1-{content_hash[:12]}",
        "content_hash": content_hash,
        "sources": sorted({
            *(record.provenance.source_id for record in records),
            *(record.provenance.source_id for record in descriptors),
            *(record.provenance.source_id for record in semantic_claims),
        }),
        "snapshot_ids": sorted({
            *(record.provenance.snapshot_id for record in records),
            *(record.provenance.snapshot_id for record in descriptors),
            *(record.provenance.snapshot_id for record in semantic_claims),
        }),
        "counts": counts,
        "files": {
            "database": "catalog.duckdb",
            "parquet_directory": "parquet",
        },
    }
    atomic_write_text(
        catalog_directory / "catalog-manifest.json",
        f"{json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)}\n",
    )
    return manifest
