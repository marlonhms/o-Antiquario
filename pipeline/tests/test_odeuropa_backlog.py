from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import atomic_write_text, load_json, write_dicts_jsonl
from antiquario_data.odeuropa_backlog import build_odeuropa_routing_backlog


def _target(identifier: str, *, kind: str = "olfactory-note") -> dict[str, object]:
    collection = "accords" if kind == "accord" else "notes"
    return {
        "id": f"antiquario:{kind}:{identifier}",
        "type": kind,
        "canonical_id": identifier,
        "collection": collection,
        "label_pt": identifier,
        "label_en": identifier,
        "source_ids": ["internal_curated"],
    }


def _gap(
    identifier: str,
    status: str,
    *,
    kind: str = "olfactory-note",
    candidates: list[str] | None = None,
) -> dict[str, object]:
    candidate_ids = candidates or []
    return {
        "target": _target(identifier, kind=kind),
        "retrieval": {
            "knowledge_document_available": bool(candidate_ids),
            "retrieval_ready": False,
            "route_status": status,
            "route_method": "exact_same_type_label" if candidate_ids else "none",
            "document_id": candidate_ids[0] if len(candidate_ids) == 1 else None,
            "candidate_document_ids": candidate_ids,
            "matched_canonical_labels": [identifier] if candidate_ids else [],
            "chunk_ids": [],
        },
        "source_entry_id": f"odeuropa:retrieval-entry:{identifier}",
        "status": "blocked_until_retrievable_content",
    }


def _prepare_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    data = root / "data"
    retrieval = data / "staging" / "odeuropa" / "fixture" / "equivalence" / "retrieval"
    gaps = [
        _gap("ambiguous", "ambiguous_document_match", candidates=[
            "antiquario:olfactory-note:ambiguous-a",
            "antiquario:olfactory-note:ambiguous-b",
        ]),
        _gap("gold", "missing_document"),
        _gap("catalog", "document_without_chunks", candidates=["antiquario:olfactory-note:catalog"]),
        _gap("shallow", "document_without_chunks", candidates=["antiquario:olfactory-note:shallow"]),
        _gap("missing", "missing_document"),
    ]
    write_dicts_jsonl(retrieval / "routing-gaps.jsonl", gaps)
    atomic_write_text(
        retrieval / "manifest.json",
        json.dumps({"index_id": "index-fixture", "knowledge_release_id": "knowledge-fixture"}) + "\n",
    )
    atomic_write_text(
        data / "staging" / "odeuropa" / "latest.json",
        json.dumps({"staging_directory": "staging/odeuropa/fixture"}) + "\n",
    )
    gold = data / "evaluation" / "odeuropa-retrieval-gold.yml"
    atomic_write_text(
        gold,
        """
schema_version: 1
cases:
  - id: gold-demand
    query: gold
    language: en
    expected_target_ids: [antiquario:olfactory-note:gold]
  - id: ambiguity-safety
    query: ambiguous
    language: en
    expected_target_ids: [antiquario:olfactory-note:ambiguous]
""".strip() + "\n",
    )
    knowledge = root / "knowledge" / "compiled"
    graph = {
        "schemaVersion": 2,
        "nodes": [
            {"id": "antiquario:olfactory-note:catalog", "kind": "document"},
            {"id": "antiquario:fragrance:one", "kind": "document"},
        ],
        "edges": [
            {
                "source": "antiquario:fragrance:one",
                "target": "antiquario:olfactory-note:catalog",
                "predicate": "has-heart-note",
                "origin": "frontmatter",
            },
            {
                "source": "antiquario:fragrance:one",
                "target": "antiquario:olfactory-note:catalog",
                "predicate": "references",
                "origin": "wikilink",
            },
        ],
    }
    atomic_write_text(knowledge / "graph.json", json.dumps(graph) + "\n")
    catalog_path = root / "apps" / "web" / "public" / "catalog" / "recommendation-catalog.json"
    catalog = {
        "schemaVersion": 1,
        "releaseId": "catalog-fixture",
        "fragrances": [{
            "id": "one",
            "topNotes": [],
            "heartNotes": ["catalog"],
            "baseNotes": [],
            "accords": [],
        }],
    }
    atomic_write_text(catalog_path, json.dumps(catalog) + "\n")
    return data, retrieval, knowledge, catalog_path


class OdeuropaBacklogTest(unittest.TestCase):
    def test_builds_deterministic_separated_priority_lanes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, retrieval, knowledge, catalog = _prepare_fixture(Path(temporary))
            result = build_odeuropa_routing_backlog(
                data,
                knowledge_directory=knowledge,
                catalog_path=catalog,
            )
            items = [json.loads(line) for line in (retrieval / "routing-backlog.jsonl").read_text().splitlines()]
            report = load_json(retrieval / "backlog-report.json")

            self.assertEqual(result.items, 5)
            self.assertEqual(result.identity_items, 1)
            self.assertEqual(result.content_items, 4)
            self.assertEqual([item["priority"]["tier"] for item in items], ["P0", "P1", "P2", "P3", "P4"])
            self.assertEqual(items[0]["remediation"]["action"], "reconcile_canonical_identity")
            self.assertEqual(items[0]["priority"]["lane"], "identity_resolution")
            self.assertEqual(items[1]["target"]["canonical_id"], "gold")
            self.assertEqual(items[2]["target"]["canonical_id"], "catalog")
            self.assertEqual(items[2]["priority"]["signals"]["catalog_distinct_fragrances"], 1)
            self.assertEqual(items[2]["priority"]["signals"]["graph_connected_documents"], 1)
            self.assertFalse(items[0]["remediation"]["automatic_knowledge_mutation_allowed"])
            self.assertFalse(items[0]["governance"]["odeuropa_may_supply_document_facts"])
            self.assertFalse(report["safety"]["protected_relations_generated"])

            first_items = (retrieval / "routing-backlog.jsonl").read_bytes()
            first_manifest = (retrieval / "backlog-manifest.json").read_bytes()
            second = build_odeuropa_routing_backlog(data, knowledge_directory=knowledge, catalog_path=catalog)
            self.assertEqual(result.backlog_id, second.backlog_id)
            self.assertEqual(first_items, (retrieval / "routing-backlog.jsonl").read_bytes())
            self.assertEqual(first_manifest, (retrieval / "backlog-manifest.json").read_bytes())

    def test_cli_exposes_backlog_inputs(self) -> None:
        args = create_parser().parse_args([
            "odeuropa-backlog",
            "--catalog",
            "catalog.json",
            "--knowledge-dir",
            "knowledge",
        ])
        self.assertEqual(args.command, "odeuropa-backlog")
        self.assertEqual(args.catalog, Path("catalog.json"))
        self.assertEqual(args.knowledge_dir, Path("knowledge"))


if __name__ == "__main__":
    unittest.main()
