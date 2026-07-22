from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.io_utils import load_json, save_raw_snapshot
from antiquario_data.wikidata import (
    USER_AGENT,
    audit_wikidata_properties,
    audit_wikidata_property_values,
    build_discovery_queries,
    build_olfactory_descriptor_query,
    build_semantic_claim_query,
    build_property_value_audit_query,
    build_property_audit_query,
    build_perfume_query,
    merge_sparql_payloads,
    normalize_sparql_payload,
    normalize_sparql_payload_with_quality,
    normalize_olfactory_descriptor_payload,
    normalize_semantic_claim_payload,
    sync_wikidata,
    summarize_property_audit,
    summarize_property_value_audit,
)


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class WikidataPipelineTest(unittest.TestCase):
    def test_query_uses_scoped_perfume_class_and_current_perfumer_property(self) -> None:
        query = build_perfume_query(125)
        self.assertIn("wd:Q131746", query)
        self.assertIn("wdt:P14539", query)
        self.assertIn("LIMIT 125", query)
        self.assertIn("github.com/marlonhms/o-Antiquario", USER_AGENT)

    def test_property_audit_query_and_summary_are_deterministic(self) -> None:
        query = build_property_audit_query(["Q999999992", "Q999999991"])
        self.assertIn("wd:Q999999991 wd:Q999999992", query)
        payload = {"results": {"bindings": [
            {
                "property": {"value": "http://www.wikidata.org/entity/P571"},
                "propertyLabel": {"value": "inception"},
                "itemsWithProperty": {"value": "2"},
                "statements": {"value": "2"},
            },
            {
                "property": {"value": "http://www.wikidata.org/entity/P180"},
                "propertyLabel": {"value": "depicts"},
                "itemsWithProperty": {"value": "1"},
                "statements": {"value": "3"},
            },
        ]}}
        self.assertEqual("P571", summarize_property_audit(payload)[0]["propertyId"])
        with self.assertRaisesRegex(ValueError, "QIDs inválidos"):
            build_property_audit_query(["Brasil"])

    def test_normalizes_wikidata_olfactory_descriptors_without_claiming_pyramid_layer(self) -> None:
        query = build_olfactory_descriptor_query(["Q999999992", "Q999999991"])
        self.assertIn("wdt:P5872", query)
        payload = {"results": {"bindings": [
            {
                "item": {"value": "http://www.wikidata.org/entity/Q999999991"},
                "descriptor": {"value": "http://www.wikidata.org/entity/Q123"},
                "descriptorLabel": {"value": "vetiver", "xml:lang": "pt"},
            },
            {
                "item": {"value": "http://www.wikidata.org/entity/Q999999991"},
                "descriptor": {"value": "http://www.wikidata.org/entity/Q123"},
                "descriptorLabel": {"value": "vetiver", "xml:lang": "pt"},
            },
            {
                "item": {"value": "http://www.wikidata.org/entity/Q999999999"},
                "descriptor": {"value": "http://www.wikidata.org/entity/Q456"},
                "descriptorLabel": {"value": "baunilha", "xml:lang": "pt"},
            },
        ]}}
        records = normalize_olfactory_descriptor_payload(
            payload,
            accepted_fragrance_ids={"Q999999991", "Q999999992"},
            retrieved_at="2026-07-22",
            snapshot_id="a" * 64,
        )
        self.assertEqual(1, len(records))
        self.assertEqual("Q999999991", records[0].fragrance_wikidata_id)
        self.assertEqual("vetiver", records[0].descriptor.label)
        self.assertFalse(hasattr(records[0], "pyramid_layer"))

    def test_property_value_audit_keeps_each_wikidata_value_explicit(self) -> None:
        query = build_property_value_audit_query(["Q999999992", "Q999999991"], ["P366", "P1552"])
        self.assertIn("(wd:P1552 wdt:P1552) (wd:P366 wdt:P366)", query)
        payload = {"results": {"bindings": [
            {
                "property": {"value": "http://www.wikidata.org/entity/P1552"},
                "propertyLabel": {"value": "has quality"},
                "value": {"value": "http://www.wikidata.org/entity/Q1"},
                "valueLabel": {"value": "floral"},
                "itemsWithValue": {"value": "2"},
                "links": {"value": "3"},
            },
            {
                "property": {"value": "http://www.wikidata.org/entity/P366"},
                "propertyLabel": {"value": "use"},
                "value": {"value": "http://www.wikidata.org/entity/Q2"},
                "valueLabel": {"value": "office"},
                "itemsWithValue": {"value": "1"},
                "links": {"value": "1"},
            },
        ]}}
        summary = summarize_property_value_audit(payload)
        self.assertEqual(["P1552", "P366"], [item["propertyId"] for item in summary])
        self.assertEqual("floral", summary[0]["values"][0]["label"])

    def test_normalizes_semantic_claims_without_forcing_editorial_roles(self) -> None:
        query = build_semantic_claim_query(["Q999999991"], ["P1552"])
        self.assertIn("wdt:P1552", query)
        payload = {"results": {"bindings": [{
            "item": {"value": "http://www.wikidata.org/entity/Q999999991"},
            "property": {"value": "http://www.wikidata.org/entity/P1552"},
            "propertyLabel": {"value": "has quality"},
            "value": {"value": "http://www.wikidata.org/entity/Q9376212"},
            "valueLabel": {"value": "eau de parfum"},
        }]}}
        records = normalize_semantic_claim_payload(
            payload,
            accepted_fragrance_ids={"Q999999991"},
            retrieved_at="2026-07-22",
            snapshot_id="d" * 64,
        )
        self.assertEqual(1, len(records))
        self.assertEqual("P1552", records[0].property.wikidata_id)
        self.assertEqual("eau de parfum", records[0].value.label)

    def test_audits_property_values_with_injected_fetcher(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "data"
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            from antiquario_data.warehouse import build_catalog
            build_catalog(data)
            report = audit_wikidata_property_values(
                data,
                output_path=Path(directory) / "values-audit.json",
                property_ids=["P1552"],
                retrieved_at="2026-07-22",
                fetcher=lambda _query: {"results": {"bindings": [{
                    "property": {"value": "http://www.wikidata.org/entity/P1552"},
                    "propertyLabel": {"value": "has quality"},
                    "value": {"value": "http://www.wikidata.org/entity/Q1"},
                    "valueLabel": {"value": "floral"},
                    "itemsWithValue": {"value": "2"},
                    "links": {"value": "2"},
                }]}} ,
            )
            self.assertEqual([], report["missingProperties"])
            self.assertEqual("Q1", report["properties"][0]["values"][0]["wikidataId"])

    def test_audits_catalog_properties_with_injected_fetcher(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "data"
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            from antiquario_data.warehouse import build_catalog
            build_catalog(data)
            report = audit_wikidata_properties(
                data,
                output_path=Path(directory) / "audit.json",
                retrieved_at="2026-07-22",
                fetcher=lambda _query: {"results": {"bindings": [{
                    "property": {"value": "http://www.wikidata.org/entity/P14539"},
                    "propertyLabel": {"value": "perfumer"},
                    "itemsWithProperty": {"value": "2"},
                    "statements": {"value": "2"},
                }]}},
            )
            self.assertEqual(2, report["scope"]["fragranceQids"])
            self.assertEqual([], report["unmappedProperties"])

    def test_regional_discovery_adds_strict_origin_filter_without_replacing_base_query(self) -> None:
        queries = build_discovery_queries(125, ["Q878", "Q155", "Q878"])
        self.assertEqual(3, len(queries))
        self.assertNotIn("requestedOriginCountry", queries[0])
        self.assertIn("wd:Q155", queries[1])
        self.assertIn("?item wdt:P495 ?requestedOriginCountry", queries[1])
        self.assertIn("wd:Q878", queries[2])
        with self.assertRaisesRegex(ValueError, "QIDs de país inválidos"):
            build_perfume_query(125, origin_countries=["Brasil"])

    def test_merges_additional_discovery_payloads_before_normalization(self) -> None:
        payload = load_json(FIXTURE)
        merged = merge_sparql_payloads([payload, payload])
        records = normalize_sparql_payload(
            merged,
            retrieved_at="2026-07-22",
            snapshot_id="regional",
        )
        self.assertEqual(2, len(records))

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
            report = load_json(second.quality_report_path)
            self.assertEqual([], report["discovery_countries"])

    def test_fixture_rejects_regional_discovery_that_it_cannot_represent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Fixtures não podem"):
                sync_wikidata(
                    Path(directory),
                    limit=10,
                    fixture=FIXTURE,
                    discovery_countries=["Q155"],
                )

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
