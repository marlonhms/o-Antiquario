from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from antiquario_data.warehouse import build_catalog
from antiquario_data.wikidata import sync_wikidata


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class WarehouseTest(unittest.TestCase):
    def test_builds_deterministic_duckdb_and_parquet_catalog(self) -> None:
        import duckdb

        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            first = build_catalog(data)
            second = build_catalog(data)

            self.assertEqual(first["catalog_version"], second["catalog_version"])
            self.assertEqual(2, first["counts"]["fragrances"])
            self.assertEqual(2, first["counts"]["perfumers"])
            self.assertTrue((data / "catalog" / "catalog.duckdb").exists())
            self.assertTrue((data / "catalog" / "parquet" / "fragrances.parquet").exists())

            connection = duckdb.connect(str(data / "catalog" / "catalog.duckdb"), read_only=True)
            try:
                self.assertEqual(2, connection.execute("SELECT count(*) FROM fragrances").fetchone()[0])
                self.assertEqual(
                    ["Aurora Experimental", "Nocturne Fixture"],
                    [row[0] for row in connection.execute("SELECT name FROM fragrances ORDER BY id").fetchall()],
                )
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
