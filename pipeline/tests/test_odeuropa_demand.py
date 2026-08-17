from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import atomic_write_text, load_json, write_dicts_jsonl
from antiquario_data.odeuropa_demand import build_p4_demand_gate, record_anonymized_query_demand


def _target(identifier: str) -> dict[str, object]:
    return {
        "id": f"antiquario:olfactory-note:{identifier}",
        "type": "olfactory-note",
        "canonical_id": identifier,
        "collection": "notes",
        "label_pt": identifier,
        "label_en": identifier,
        "source_ids": ["internal_curated"],
    }


def _query_key(identifier: str) -> dict[str, object]:
    target = _target(identifier)
    return {
        "query_key_id": f"odeuropa:query-key:{identifier}",
        "language": "pt-BR",
        "key": identifier,
        "token_count": 1,
        "target": target,
        "expansions": [{"language": "pt-BR", "role": "canonical_label", "value": identifier}],
        "entry_ids": [f"odeuropa:retrieval-entry:{identifier}"],
        "origins": ["canonical_taxonomy_label"],
        "source_values": [identifier],
        "scope": "retrieval_only",
        "semantic_identity": "canonical",
        "retrieval": {
            "candidate_document_ids": [],
            "chunk_ids": [],
            "document_id": None,
            "knowledge_document_available": False,
            "matched_canonical_labels": [],
            "retrieval_ready": False,
            "route_method": "none",
            "route_status": "missing_document",
        },
        "status": "active",
    }


def _prepare_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    data = root / "data"
    retrieval = data / "staging" / "odeuropa" / "fixture" / "equivalence" / "retrieval"
    identifiers = ["banana", "cereja", "mineral", "uva", "papoula"]
    backlog = [
        {
            "schema_version": 1,
            "backlog_item_id": f"odeuropa:backlog:{identifier}",
            "target": _target(identifier),
            "priority": {"tier": "P4", "lane": "content_coverage"},
        }
        for identifier in identifiers
    ]
    write_dicts_jsonl(retrieval / "routing-backlog.jsonl", backlog)
    atomic_write_text(
        data / "staging" / "odeuropa" / "latest.json",
        json.dumps({"staging_directory": "staging/odeuropa/fixture"}) + "\n",
    )
    index_path = retrieval / "index.json"
    atomic_write_text(
        index_path,
        json.dumps({
            "schema_version": 1,
            "index_id": "index-fixture",
            "scope": "retrieval_only",
            "entries": [],
            "query_keys": [_query_key(identifier) for identifier in identifiers],
        }) + "\n",
    )
    catalog_path = root / "apps" / "web" / "public" / "catalog" / "recommendation-catalog.json"
    atomic_write_text(
        catalog_path,
        json.dumps({
            "schemaVersion": 1,
            "releaseId": "catalog-fixture",
            "fragrances": [{
                "id": "fragrance-one",
                "topNotes": ["cereja"],
                "heartNotes": [],
                "baseNotes": [],
                "accords": [],
            }],
        }) + "\n",
    )
    policy_path = data / "evaluation" / "odeuropa-p4-demand.yml"
    atomic_write_text(
        policy_path,
        """
schema_version: 1
policy:
  window_days: 90
  min_query_events: 3
  min_active_days: 2
  min_catalog_fragrances: 1
priorities:
  - target_id: antiquario:olfactory-note:mineral
    priority: high
    rationale: Prioridade para pesquisa editorial temática.
""".strip() + "\n",
    )
    return data, retrieval, index_path, catalog_path


class OdeuropaDemandTest(unittest.TestCase):
    def test_records_only_anonymized_canonical_targets_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _retrieval, index_path, _catalog = _prepare_fixture(Path(temporary))
            first = record_anonymized_query_demand(
                data,
                "quero perfume de banana",
                language="pt-BR",
                index_path=index_path,
                occurred_on="2026-08-16",
                event_id="event-one",
            )
            second = record_anonymized_query_demand(
                data,
                "quero perfume de banana",
                language="pt-BR",
                index_path=index_path,
                occurred_on="2026-08-16",
                event_id="event-one",
            )
            contents = first.events_path.read_text(encoding="utf-8")
            event = json.loads(contents)

            self.assertTrue(first.recorded)
            self.assertFalse(second.recorded)
            self.assertEqual(event["matched_target_ids"], ["antiquario:olfactory-note:banana"])
            self.assertNotIn("quero", contents)
            self.assertNotIn("query", event)
            self.assertFalse(event["privacy"]["raw_query_stored"])

    def test_gate_combines_demand_catalog_and_editorial_without_creating_knowledge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, retrieval, index_path, catalog_path = _prepare_fixture(Path(temporary))
            for event_id, occurred_on in [
                ("banana-one", "2026-08-15"),
                ("banana-two", "2026-08-15"),
                ("banana-three", "2026-08-16"),
            ]:
                record_anonymized_query_demand(
                    data,
                    "banana",
                    language="pt-BR",
                    index_path=index_path,
                    occurred_on=occurred_on,
                    event_id=event_id,
                )
            record_anonymized_query_demand(
                data,
                "uva",
                language="pt-BR",
                index_path=index_path,
                occurred_on="2026-08-16",
                event_id="uva-one",
            )

            result = build_p4_demand_gate(data, catalog_path=catalog_path, as_of="2026-08-17")
            items = {
                item["target"]["canonical_id"]: item
                for item in [json.loads(line) for line in (retrieval / "demand-gate" / "items.jsonl").read_text().splitlines()]
            }
            report = load_json(retrieval / "demand-gate" / "report.json")

            self.assertEqual((result.research_ready, result.watchlist, result.dormant), (3, 1, 1))
            self.assertEqual(items["banana"]["gate_status"], "research_ready")
            self.assertEqual(items["cereja"]["gate_status"], "research_ready")
            self.assertEqual(items["mineral"]["gate_status"], "research_ready")
            self.assertEqual(items["uva"]["gate_status"], "watchlist")
            self.assertEqual(items["papoula"]["gate_status"], "dormant")
            self.assertFalse(items["banana"]["gate"]["document_creation_allowed"])
            self.assertFalse(items["cereja"]["gate"]["core_promotion_allowed"])
            self.assertTrue(report["safety"]["demand_is_not_evidence"])
            self.assertEqual(report["counts"]["documents_created"], 0)

            first_manifest = (retrieval / "demand-gate" / "manifest.json").read_bytes()
            second = build_p4_demand_gate(data, catalog_path=catalog_path, as_of="2026-08-17")
            self.assertEqual(result.gate_id, second.gate_id)
            self.assertEqual(first_manifest, (retrieval / "demand-gate" / "manifest.json").read_bytes())
            shifted = build_p4_demand_gate(data, catalog_path=catalog_path, as_of="2026-08-18")
            self.assertNotEqual(result.gate_id, shifted.gate_id)

    def test_gate_rejects_private_fields_in_event_log(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _retrieval, _index, catalog_path = _prepare_fixture(Path(temporary))
            events = data / "private" / "demand" / "olfactory-query-events.jsonl"
            write_dicts_jsonl(events, [{
                "schema_version": 1,
                "event_id": "unsafe",
                "occurred_on": "2026-08-16",
                "language": "pt-BR",
                "matched_target_ids": ["antiquario:olfactory-note:banana"],
                "source": "local_companion",
                "query": "banana",
                "privacy": {"raw_query_stored": False, "personal_identifiers_stored": False},
            }])
            with self.assertRaisesRegex(ValueError, "campos privados proibidos"):
                build_p4_demand_gate(data, catalog_path=catalog_path, as_of="2026-08-17")

    def test_cli_exposes_private_recorder_and_gate(self) -> None:
        parser = create_parser()
        record = parser.parse_args(["odeuropa-demand-record", "banana", "--language", "pt-BR"])
        gate = parser.parse_args(["odeuropa-demand-gate", "--as-of", "2026-08-17"])
        self.assertEqual(record.command, "odeuropa-demand-record")
        self.assertEqual(record.language, "pt-BR")
        self.assertEqual(gate.command, "odeuropa-demand-gate")
        self.assertEqual(gate.as_of, "2026-08-17")


if __name__ == "__main__":
    unittest.main()
