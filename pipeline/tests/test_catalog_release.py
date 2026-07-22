from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.catalog_release import (
    compile_catalog_release,
    normalize_search_text,
    resolution_key,
)
from antiquario_data.warehouse import build_catalog
from antiquario_data.wikidata import sync_wikidata


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class CatalogReleaseTest(unittest.TestCase):
    def test_normalizes_accents_and_builds_resolution_key(self) -> None:
        self.assertEqual("miss dior cherie", normalize_search_text("Miss Dior Chérie"))
        self.assertEqual(
            "aurora experimental|casa teste|2020",
            resolution_key("Aurora Experimental", ["Casa Teste"], 2020),
        )

    def test_compiles_deterministic_web_release_with_knowledge_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            knowledge = root / "knowledge"
            releases = root / "releases"
            public = root / "public"
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            build_catalog(data)
            knowledge.mkdir()
            (knowledge / "documents.json").write_text(json.dumps([{
                "id": "antiquario:fragrance:aurora-experimental",
                "type": "fragrance",
                "external_ids": {"wikidata": "Q999999991"},
            }]), encoding="utf-8")
            (knowledge / "knowledge-manifest.json").write_text(json.dumps({
                "releaseId": "knowledge-v2-aaaaaaaaaaaa",
            }), encoding="utf-8")

            first = compile_catalog_release(
                data_directory=data,
                knowledge_directory=knowledge,
                releases_directory=releases,
                public_directory=public,
            )
            second = compile_catalog_release(
                data_directory=data,
                knowledge_directory=knowledge,
                releases_directory=releases,
                public_directory=public,
            )

            self.assertEqual(first.release_id, second.release_id)
            self.assertEqual(2, first.manifest["counts"]["fragrances"])
            self.assertEqual(1, first.manifest["counts"]["knowledgeLinks"])
            self.assertTrue((first.release_directory / "search-index.json").exists())
            self.assertTrue((public / "manifest.json").exists())

            fragrances = json.loads((public / "fragrances.json").read_text(encoding="utf-8"))["items"]
            aurora = next(item for item in fragrances if item["wikidataId"] == "Q999999991")
            self.assertEqual(
                ["antiquario:fragrance:aurora-experimental"],
                aurora["knowledgeIds"],
            )
            search_index = json.loads((public / "search-index.json").read_text(encoding="utf-8"))
            self.assertIn("aurora", search_index["terms"])

            (knowledge / "knowledge-manifest.json").write_text(json.dumps({
                "releaseId": "knowledge-v2-bbbbbbbbbbbb",
            }), encoding="utf-8")
            editorial_update = compile_catalog_release(
                data_directory=data,
                knowledge_directory=knowledge,
                releases_directory=releases,
                public_directory=public,
            )
            self.assertNotEqual(first.release_id, editorial_update.release_id)


if __name__ == "__main__":
    unittest.main()
