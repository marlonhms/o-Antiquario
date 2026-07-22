from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from antiquario_data.io_utils import write_olfactory_descriptors_jsonl, write_semantic_claims_jsonl
from antiquario_data.models import EntityReference, OlfactoryDescriptorRecord, PropertyReference, Provenance, WikidataSemanticClaimRecord
from antiquario_data.warehouse import build_catalog
from antiquario_data.wikidata import sync_wikidata


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class WarehouseTest(unittest.TestCase):
    def test_builds_deterministic_duckdb_and_parquet_catalog(self) -> None:
        import duckdb

        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            write_olfactory_descriptors_jsonl(
                data / "staging" / "wikidata" / "olfactory-descriptors.jsonl",
                [OlfactoryDescriptorRecord(
                    fragrance_wikidata_id="Q999999991",
                    descriptor=EntityReference(wikidata_id="Q999999961", label="Vetiver"),
                    provenance=Provenance(
                        source_id="wikidata",
                        source_url="https://www.wikidata.org/wiki/Q999999991",
                        license="CC0-1.0",
                        retrieved_at="2026-07-22",
                        snapshot_id="b" * 64,
                    ),
                )],
            )
            write_semantic_claims_jsonl(
                data / "staging" / "wikidata" / "semantic-claims.jsonl",
                [WikidataSemanticClaimRecord(
                    fragrance_wikidata_id="Q999999991",
                    property=PropertyReference(wikidata_id="P1552", label="has quality"),
                    value=EntityReference(wikidata_id="Q9376212", label="eau de parfum"),
                    provenance=Provenance(
                        source_id="wikidata",
                        source_url="https://www.wikidata.org/wiki/Q999999991",
                        license="CC0-1.0",
                        retrieved_at="2026-07-22",
                        snapshot_id="e" * 64,
                    ),
                )],
            )
            first = build_catalog(data)
            second = build_catalog(data)

            self.assertEqual(first["catalog_version"], second["catalog_version"])
            self.assertEqual(2, first["counts"]["fragrances"])
            self.assertEqual(2, first["counts"]["perfumers"])
            self.assertEqual(1, first["counts"]["olfactory_descriptors"])
            self.assertEqual(1, first["counts"]["semantic_claims"])
            self.assertTrue((data / "catalog" / "catalog.duckdb").exists())
            self.assertTrue((data / "catalog" / "parquet" / "fragrances.parquet").exists())

            connection = duckdb.connect(str(data / "catalog" / "catalog.duckdb"), read_only=True)
            try:
                self.assertEqual(2, connection.execute("SELECT count(*) FROM fragrances").fetchone()[0])
                self.assertEqual(1, connection.execute("SELECT count(*) FROM fragrance_olfactory_descriptors").fetchone()[0])
                self.assertEqual(1, connection.execute("SELECT count(*) FROM fragrance_semantic_claims").fetchone()[0])
                self.assertEqual(
                    ["Aurora Experimental", "Nocturne Fixture"],
                    [row[0] for row in connection.execute("SELECT name FROM fragrances ORDER BY id").fetchall()],
                )
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
