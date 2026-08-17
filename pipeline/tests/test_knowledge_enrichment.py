from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import atomic_write_text, load_json, write_dicts_jsonl
from antiquario_data.knowledge_enrichment import (
    SECTION_MARKER,
    _load_jsonl,
    audit_enrichment_candidates,
    build_knowledge_enrichment_plan,
    promote_knowledge_enrichment_plan,
)


def _prepare_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    data = root / "data"
    retrieval = data / "staging" / "odeuropa" / "fixture" / "equivalence" / "retrieval"
    write_dicts_jsonl(retrieval / "routing-backlog.jsonl", [{
        "schema_version": 1,
        "backlog_item_id": "odeuropa:routing-backlog:fixture",
        "rank": 1,
        "target": {
            "id": "antiquario:olfactory-note:alecrim",
            "type": "olfactory-note",
            "canonical_id": "alecrim",
            "label_pt": "alecrim",
            "label_en": "rosemary",
        },
        "gap": {
            "route_status": "document_without_chunks",
            "document_id": "antiquario:olfactory-note:rosemary",
        },
        "priority": {"tier": "P3"},
    }])
    atomic_write_text(
        data / "staging" / "odeuropa" / "latest.json",
        json.dumps({"staging_directory": "staging/odeuropa/fixture"}) + "\n",
    )
    atomic_write_text(
        data / "sources.yml",
        """
schema_version: 1
sources:
  - id: parfumo_dataset
    classification: allowed_core
""".strip() + "\n",
    )
    knowledge = root / "knowledge" / "compiled"
    documents = [
        {
            "id": "antiquario:olfactory-note:rosemary",
            "type": "olfactory-note",
            "title": "Rosemary",
            "path": "30_Parfumo_Dataset/note-rosemary.md",
            "source_ids": ["parfumo_dataset"],
            "evidence": [{
                "source_id": "parfumo_dataset",
                "license": "CC0-1.0",
                "confidence": "medium",
                "claim_scope": "Extração de entidade",
            }],
            "contentHash": "a" * 64,
        },
        {
            "id": "antiquario:fragrance:one",
            "type": "fragrance",
            "title": "Perfume Um",
            "path": "30_Parfumo_Dataset/fragrance-one.md",
            "source_ids": ["parfumo_dataset"],
            "evidence": [{
                "source_id": "parfumo_dataset",
                "license": "CC0-1.0",
                "confidence": "medium",
                "claim_scope": "Estrutura da pirâmide olfativa",
            }],
            "contentHash": "b" * 64,
        },
    ]
    atomic_write_text(knowledge / "documents.json", json.dumps(documents) + "\n")
    atomic_write_text(knowledge / "graph.json", json.dumps({
        "schemaVersion": 2,
        "nodes": [],
        "edges": [{
            "source": "antiquario:fragrance:one",
            "target": "antiquario:olfactory-note:rosemary",
            "predicate": "has-heart-note",
            "origin": "frontmatter",
        }],
    }) + "\n")
    atomic_write_text(
        knowledge / "knowledge-manifest.json",
        json.dumps({"releaseId": "knowledge-v2-fixture"}) + "\n",
    )
    vault = root / "knowledge" / "vault"
    note_path = vault / "30_Parfumo_Dataset" / "note-rosemary.md"
    atomic_write_text(note_path, """---
schema_version: 1
id: antiquario:olfactory-note:rosemary
project: o-antiquario
type: olfactory-note
title: "Rosemary"
aliases: []
external_ids: {}
tags: [olfactory-note]
source_ids: [parfumo_dataset]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: "Nota olfativa extraída de uma fonte aprovada."
evidence:
  - source_id: parfumo_dataset
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: "Extração de entidade"
relations: []
---

# Rosemary
""")
    return data, retrieval, knowledge, vault


class KnowledgeEnrichmentTest(unittest.TestCase):
    def test_plan_audits_and_promotes_only_existing_declared_relations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, retrieval, knowledge, vault = _prepare_fixture(Path(temporary))
            plan = build_knowledge_enrichment_plan(
                data,
                knowledge_directory=knowledge,
                vault_directory=vault,
            )
            candidates = _load_jsonl(retrieval / "enrichment" / "candidates.jsonl")

            self.assertEqual(plan.candidates, 1)
            self.assertEqual(plan.eligible, 1)
            self.assertEqual(plan.blocked, 0)
            self.assertEqual(candidates[0]["proposal"]["relations_to_add"], [])
            self.assertFalse(candidates[0]["safety"]["odeuropa_used_as_factual_evidence"])
            self.assertEqual(
                candidates[0]["provenance"]["declared_relations"][0]["predicate"],
                "has-heart-note",
            )
            self.assertTrue(load_json(retrieval / "enrichment" / "audit.json")["passed"])

            promoted = promote_knowledge_enrichment_plan(data, vault_directory=vault, updated_at="2026-08-17")
            note = (vault / "30_Parfumo_Dataset" / "note-rosemary.md").read_text(encoding="utf-8")
            self.assertEqual(promoted.promoted, 1)
            self.assertIn(SECTION_MARKER, note)
            self.assertIn("coração: 1", note)
            self.assertIn("[[fragrance-one|Perfume Um]]", note)
            self.assertIn("updated_at: 2026-08-17", note)
            self.assertNotIn("predicate: has-heart-note", note)

            repeated = promote_knowledge_enrichment_plan(data, vault_directory=vault, updated_at="2026-08-17")
            self.assertEqual(repeated.promoted, 0)
            self.assertEqual(repeated.skipped, 1)

    def test_promotion_blocks_concurrent_file_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _, knowledge, vault = _prepare_fixture(Path(temporary))
            build_knowledge_enrichment_plan(data, knowledge_directory=knowledge, vault_directory=vault)
            path = vault / "30_Parfumo_Dataset" / "note-rosemary.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nMudança concorrente.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "promoção bloqueou 1"):
                promote_knowledge_enrichment_plan(data, vault_directory=vault, updated_at="2026-08-17")

    def test_audit_rejects_generated_relations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, retrieval, knowledge, vault = _prepare_fixture(Path(temporary))
            build_knowledge_enrichment_plan(data, knowledge_directory=knowledge, vault_directory=vault)
            candidates = _load_jsonl(retrieval / "enrichment" / "candidates.jsonl")
            candidates[0]["proposal"]["relations_to_add"] = [{"predicate": "has-note"}]
            result = audit_enrichment_candidates(candidates)
            self.assertFalse(result["passed"])
            self.assertIn("relations_must_remain_empty", {issue["code"] for issue in result["issues"]})

    def test_promotion_reaudits_current_source_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _, knowledge, vault = _prepare_fixture(Path(temporary))
            build_knowledge_enrichment_plan(data, knowledge_directory=knowledge, vault_directory=vault)
            atomic_write_text(
                data / "sources.yml",
                """
schema_version: 1
sources:
  - id: parfumo_dataset
    classification: pending_review
""".strip() + "\n",
            )
            with self.assertRaisesRegex(ValueError, "reauditoria"):
                promote_knowledge_enrichment_plan(data, vault_directory=vault, updated_at="2026-08-17")

    def test_cli_exposes_plan_and_promotion(self) -> None:
        parser = create_parser()
        plan = parser.parse_args(["odeuropa-enrichment-plan"])
        promote = parser.parse_args(["odeuropa-enrichment-promote", "--updated-at", "2026-08-17"])
        self.assertEqual(plan.command, "odeuropa-enrichment-plan")
        self.assertEqual(promote.command, "odeuropa-enrichment-promote")
        self.assertEqual(promote.updated_at, "2026-08-17")


if __name__ == "__main__":
    unittest.main()
