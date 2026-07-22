from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.io_utils import load_json, save_raw_snapshot
from antiquario_data.wikidata import (
    USER_AGENT,
    build_perfume_query,
    normalize_sparql_payload,
    normalize_sparql_payload_with_quality,
    sync_wikidata,
)


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class WikidataPipelineTest(unittest.TestCase):
    def test_query_uses_scoped_perfume_class_and_current_perfumer_property(self) -> None:
        query = build_perfume_query(125)
        self.assertIn("wd:Q131746", query)
        self.assertIn("wdt:P14539", query)
        self.assertIn("LIMIT 125", query)
        self.assertIn("github.com/marlonhms/o-Antiquario", USER_AGENT)

    def test_normalization_merges_repeated_rows(self) -> None:
        records = normalize_sparql_payload(
            load_json(FIXTURE),
            retrieved_at="2026-07-22",
            snapshot_id="abc123",
        )
        self.assertEqual(2, len(records))
        aurora = records[0]
        self.assertEqual("wd-q999999991", aurora.id)
        self.assertEqual("Aurora Experimental", aurora.name)
        self.assertEqual(2020, aurora.launch_year)
        self.assertEqual(["Ana Exemplo", "Bruno Exemplo"], [item.label for item in aurora.perfumers])
        self.assertEqual("CC0-1.0", aurora.provenance.license)

    def test_snapshot_preserves_first_retrieval_date_for_same_content(self) -> None:
        payload = load_json(FIXTURE)
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory)
            first_path, first = save_raw_snapshot(payload, "SELECT {}", raw, "2026-07-22")
            second_path, second = save_raw_snapshot(payload, "SELECT {}", raw, "2026-08-01")
            self.assertEqual(first_path, second_path)
            self.assertEqual("2026-07-22", first["retrieved_at"])
            self.assertEqual(first, second)

    def test_sync_fixture_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            first = sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            first_contents = first.staging_path.read_text(encoding="utf-8")
            second = sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-08-01")
            self.assertEqual(first.snapshot_id, second.snapshot_id)
            self.assertEqual(first_contents, second.staging_path.read_text(encoding="utf-8"))
            self.assertEqual(2, second.records)
            self.assertEqual(0, second.quarantined)
            self.assertTrue(second.quality_report_path.exists())
            for line in first_contents.splitlines():
                self.assertIn("record_hash", json.loads(line))

    def test_quarantines_missing_labels_and_generic_materials(self) -> None:
        payload = load_json(FIXTURE)
        payload["results"]["bindings"].extend([
            {
                "item": {"type": "uri", "value": "http://www.wikidata.org/entity/Q999999993"},
                "itemLabel": {"type": "literal", "value": "Q999999993"},
            },
            {
                "item": {"type": "uri", "value": "http://www.wikidata.org/entity/Q999999994"},
                "itemLabel": {"type": "literal", "xml:lang": "en", "value": "Jasminum flower oil"},
            },
        ])
        records, quarantined = normalize_sparql_payload_with_quality(
            payload,
            retrieved_at="2026-07-22",
            snapshot_id="abc123",
        )
        self.assertEqual(2, len(records))
        self.assertEqual(
            ["missing_human_label", "possible_non_product_material"],
            [item["reason"] for item in quarantined],
        )


if __name__ == "__main__":
    unittest.main()
