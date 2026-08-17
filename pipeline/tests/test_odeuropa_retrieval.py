from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import atomic_write_text, load_json, write_dicts_jsonl
from antiquario_data.odeuropa_retrieval import (
    build_odeuropa_retrieval_index,
    expand_odeuropa_query,
)


SNAPSHOT_ID = "b" * 64


def _bridge(identifier: str, label: str = "bergamot") -> dict[str, object]:
    return {
        "schema_version": 1,
        "bridge_id": f"odeuropa:retrieval-bridge:{identifier}",
        "source_term": {
            "id": f"odeuropa:term:{identifier}",
            "type": "odor-descriptor",
            "label_original": label,
            "entry_original": f"{label}_noun",
            "language": "en",
            "part_of_speech": "noun",
            "search_key": label,
            "wordnet_synsets": ["bergamot.n.01"],
        },
        "target": {
            "id": "antiquario:olfactory-note:bergamota",
            "type": "olfactory-note",
            "canonical_id": "bergamota",
            "collection": "notes",
            "label_pt": "bergamota",
            "label_en": "bergamot",
            "source_ids": ["internal_curated"],
        },
        "link_kind": "lexical-retrieval-bridge",
        "scope": "retrieval_only",
        "semantic_identity": "unverified",
        "type_compatibility": "cross_ontology",
        "match": {"method": "exact_english_label"},
        "claim_nature": "inferred",
        "confidence": "high",
        "status": "resolved_for_retrieval",
        "promotion_status": "blocked",
        "commercial_claims_generated": False,
        "evidence": {
            "source_id": "odeuropa_multilingual_taxonomy",
            "locator": f"https://example.test/en#L{identifier}",
            "license": "CC-BY-4.0",
            "method": "exact_english_label",
        },
    }


def _prepare_fixture(root: Path) -> tuple[Path, Path]:
    data = root / "data"
    equivalence = data / "staging" / "odeuropa" / "fixture" / "equivalence"
    bridges = [_bridge("one"), _bridge("two")]
    write_dicts_jsonl(equivalence / "resolved-retrieval-bridges.jsonl", bridges)
    write_dicts_jsonl(equivalence / "equivalence-candidates.jsonl", [{"status": "candidate"}])
    atomic_write_text(
        equivalence / "manifest.json",
        json.dumps({
            "snapshot_id": SNAPSHOT_ID,
            "resolution_id": "resolution-fixture",
            "taxonomy_sha256": "c" * 64,
        }) + "\n",
    )
    atomic_write_text(
        equivalence / "report.json",
        json.dumps({"counts": {"equivalence_candidates": 1}}) + "\n",
    )
    atomic_write_text(
        data / "staging" / "odeuropa" / "latest.json",
        json.dumps({"staging_directory": "staging/odeuropa/fixture"}) + "\n",
    )
    knowledge = root / "knowledge" / "compiled"
    atomic_write_text(
        knowledge / "documents.json",
        json.dumps([{"id": "antiquario:olfactory-note:bergamota"}]) + "\n",
    )
    atomic_write_text(
        knowledge / "chunks.json",
        json.dumps([{
            "id": "antiquario:olfactory-note:bergamota#resumo:0",
            "documentId": "antiquario:olfactory-note:bergamota",
        }]) + "\n",
    )
    atomic_write_text(
        knowledge / "knowledge-manifest.json",
        json.dumps({"releaseId": "knowledge-v2-fixture", "contentHash": "d" * 64}) + "\n",
    )
    gold = root / "gold.yml"
    gold.write_text(
        """
schema_version: 1
thresholds:
  precision_min: 1.0
  recall_min: 1.0
  exact_match_accuracy_min: 1.0
  max_safety_violations: 0
  route_coverage_min: 1.0
cases:
  - id: positive
    query: bergamot perfume
    language: en
    expected_target_ids: [antiquario:olfactory-note:bergamota]
  - id: token-boundary
    query: bergamota
    language: en
    expected_target_ids: []
  - id: wrong-language
    query: bergamot
    language: pt-BR
    expected_target_ids: []
""".strip() + "\n",
        encoding="utf-8",
    )
    return data, gold


class OdeuropaRetrievalTest(unittest.TestCase):
    def test_build_aggregates_duplicate_evidence_and_passes_gold_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, gold = _prepare_fixture(Path(temporary))
            result = build_odeuropa_retrieval_index(data, gold_path=gold)
            index = load_json(result.output_directory / "index.json")
            evaluation = load_json(result.output_directory / "evaluation.json")

            self.assertEqual(result.source_bridges, 2)
            self.assertEqual(result.entries, 1)
            self.assertEqual(result.query_keys, 2)
            self.assertEqual(result.targets, 1)
            self.assertEqual(result.retrieval_ready_targets, 1)
            self.assertTrue(result.evaluation_passed)
            self.assertEqual(index["candidate_bridges_included"], 0)
            self.assertEqual(len(index["entries"][0]["provenance"]["bridge_ids"]), 2)
            self.assertEqual(evaluation["metrics"]["micro_precision"], 1.0)
            self.assertEqual(evaluation["metrics"]["micro_recall"], 1.0)
            self.assertEqual(evaluation["metrics"]["safety_violations"], 0)
            self.assertEqual(evaluation["metrics"]["knowledge_route_coverage"], 1.0)
            index_before = (result.output_directory / "index.json").read_bytes()
            manifest_before = (result.output_directory / "manifest.json").read_bytes()
            second = build_odeuropa_retrieval_index(data, gold_path=gold)
            self.assertEqual(index_before, (second.output_directory / "index.json").read_bytes())
            self.assertEqual(manifest_before, (second.output_directory / "manifest.json").read_bytes())

    def test_query_expansion_requires_language_and_respects_token_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, gold = _prepare_fixture(Path(temporary))
            result = build_odeuropa_retrieval_index(data, gold_path=gold)
            index = load_json(result.output_directory / "index.json")

            matched = expand_odeuropa_query(index, "bergamot perfume", language="en")
            self.assertEqual(
                [target["id"] for target in matched["canonical_targets"]],
                ["antiquario:olfactory-note:bergamota"],
            )
            self.assertFalse(matched["facts_generated"])
            self.assertEqual(
                matched["retrieval_routes"][0]["chunk_ids"],
                ["antiquario:olfactory-note:bergamota#resumo:0"],
            )
            self.assertEqual(expand_odeuropa_query(index, "bergamota", language="en")["matches"], [])
            self.assertEqual(expand_odeuropa_query(index, "bergamot", language="pt-BR")["matches"], [])
            self.assertEqual(
                [target["id"] for target in expand_odeuropa_query(index, "bergamota", language="pt-BR")["canonical_targets"]],
                ["antiquario:olfactory-note:bergamota"],
            )
            with self.assertRaisesRegex(ValueError, "idioma de consulta não suportado"):
                expand_odeuropa_query(index, "bergamot", language="und")

    def test_unsafe_bridge_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, gold = _prepare_fixture(Path(temporary))
            bridge_path = data / "staging" / "odeuropa" / "fixture" / "equivalence" / "resolved-retrieval-bridges.jsonl"
            unsafe = _bridge("unsafe")
            unsafe["predicate"] = "has-note"
            write_dicts_jsonl(bridge_path, [unsafe])
            with self.assertRaisesRegex(ValueError, "não pode conter predicado"):
                build_odeuropa_retrieval_index(data, gold_path=gold)

    def test_document_reconciliation_requires_unique_exact_label_and_same_type(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data, gold = _prepare_fixture(root)
            knowledge = root / "knowledge" / "compiled"
            documents_path = knowledge / "documents.json"
            chunks_path = knowledge / "chunks.json"
            atomic_write_text(
                documents_path,
                json.dumps([{
                    "id": "antiquario:olfactory-note:bergamot-document",
                    "type": "olfactory-note",
                    "title": "Bergamot",
                    "aliases": [],
                }]) + "\n",
            )
            atomic_write_text(
                chunks_path,
                json.dumps([{
                    "id": "antiquario:olfactory-note:bergamot-document:chunk:001",
                    "documentId": "antiquario:olfactory-note:bergamot-document",
                }]) + "\n",
            )
            unique = build_odeuropa_retrieval_index(data, gold_path=gold)
            unique_index = load_json(unique.output_directory / "index.json")
            route = unique_index["entries"][0]["retrieval"]
            self.assertEqual(route["route_status"], "reconciled")
            self.assertEqual(route["document_id"], "antiquario:olfactory-note:bergamot-document")

            atomic_write_text(
                documents_path,
                json.dumps([
                    {
                        "id": "antiquario:olfactory-note:bergamot-document",
                        "type": "olfactory-note",
                        "title": "Bergamot",
                        "aliases": [],
                    },
                    {
                        "id": "antiquario:olfactory-note:bergamot-alternative",
                        "type": "olfactory-note",
                        "title": "Bergamot",
                        "aliases": [],
                    },
                ]) + "\n",
            )
            ambiguous = build_odeuropa_retrieval_index(data, gold_path=gold)
            ambiguous_index = load_json(ambiguous.output_directory / "index.json")
            blocked_route = ambiguous_index["entries"][0]["retrieval"]
            self.assertEqual(blocked_route["route_status"], "ambiguous_document_match")
            self.assertFalse(blocked_route["retrieval_ready"])

    def test_cli_exposes_index_and_language_bound_query(self) -> None:
        parser = create_parser()
        index_args = parser.parse_args(["odeuropa-index", "--gold", "gold.yml"])
        query_args = parser.parse_args(["odeuropa-query", "fresh bread", "--language", "en"])
        self.assertEqual(index_args.command, "odeuropa-index")
        self.assertEqual(query_args.language, "en")


if __name__ == "__main__":
    unittest.main()
