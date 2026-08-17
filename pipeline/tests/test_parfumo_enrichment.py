from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from antiquario_data.cli import create_parser
from antiquario_data.parfumo_enrichment import audit_parfumo_candidates, enrich_parfumo_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def fragrance_document() -> str:
    return """---
schema_version: 1
id: antiquario:fragrance:parfumo-test-brand-test-perfume
project: o-antiquario
type: fragrance
title: Test Perfume
aliases: []
external_ids: {}
tags: [perfume, parfumo]
source_ids: [parfumo_dataset]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: Fragrância de teste extraída de um registro estruturado do dataset.
evidence:
  - source_id: parfumo_dataset
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: Estrutura da pirâmide olfativa no registro.
relations:
  - predicate: belongs-to-brand
    target: antiquario:brand:test-brand
---

# Test Perfume
"""


def parse_frontmatter(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---\n", 2)[1])


class TestParfumoEnrichment(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.vault = root / "vault"
        self.staging = root / "staging"
        perfume_dir = self.vault / "30_Parfumo_Dataset"
        perfume_dir.mkdir(parents=True)
        self.fragrance_path = perfume_dir / "fragrance-test-brand-test-perfume.md"
        self.fragrance_path.write_text(fragrance_document(), encoding="utf-8")
        self.csv_path = root / "parfumo.csv"
        with self.csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=[
                "Number", "Name", "Brand", "Release_Year", "Concentration",
                "Rating_Value", "Rating_Count", "Main_Accords", "Top_Notes",
                "Middle_Notes", "Base_Notes", "Perfumers", "URL",
            ])
            writer.writeheader()
            writer.writerow({
                "Number": "1",
                "Name": "Test Perfume",
                "Brand": "Test Brand",
                "Release_Year": "2024",
                "Concentration": "Eau de Toilette",
                "Rating_Value": "8",
                "Rating_Count": "500",
                "Main_Accords": "Sweet, Synthetic",
                "Top_Notes": "Bergamot",
                "Middle_Notes": "Rose",
                "Base_Notes": "Vanilla",
                "Perfumers": "Ada Aroma, Bruno Olfato",
                "URL": "https://www.parfumo.com/Perfumes/Test_Brand/test-perfume",
            })

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_enriches_facts_and_keeps_family_in_staging(self) -> None:
        result = enrich_parfumo_documents(
            self.csv_path,
            PROJECT_ROOT / "data",
            self.vault,
            staging_directory=self.staging,
            updated_at="2026-08-17",
        )
        document = parse_frontmatter(self.fragrance_path)
        relations = {(item["predicate"], item["target"]) for item in document["relations"]}

        self.assertEqual(result.matched, 1)
        self.assertIn(("has-concentration", "antiquario:concentration:eau-de-toilette"), relations)
        self.assertIn(("has-accord", "antiquario:accord:doce"), relations)
        self.assertIn(("created-by", "antiquario:perfumer:ada-aroma"), relations)
        self.assertFalse(any(predicate == "belongs-to-family" for predicate, _ in relations))
        self.assertEqual(document["evidence"][0]["locator"], "https://www.parfumo.com/Perfumes/Test_Brand/test-perfume")
        self.assertTrue((self.vault / "16_Concentracoes" / "eau-de-toilette.md").exists())
        self.assertTrue((self.vault / "30_Acordes" / "doce.md").exists())
        self.assertTrue((self.vault / "16_Perfumistas" / "ada-aroma.md").exists())

        candidates = [json.loads(line) for line in (self.staging / "family-candidates.jsonl").read_text().splitlines()]
        self.assertEqual({item["target_id"] for item in candidates}, {
            "antiquario:olfactory-family:ambarada",
            "antiquario:olfactory-family:gourmand",
        })
        self.assertTrue(all(item["claim_nature"] == "inferred" for item in candidates))
        quarantine = [json.loads(line) for line in (self.staging / "quarantine.jsonl").read_text().splitlines()]
        self.assertEqual(quarantine[0]["raw_term"], "Synthetic")
        self.assertTrue(audit_parfumo_candidates(self.staging, self.vault)["ok"])

        second = enrich_parfumo_documents(
            self.csv_path,
            PROJECT_ROOT / "data",
            self.vault,
            staging_directory=self.staging,
            updated_at="2026-08-17",
        )
        self.assertEqual(second.changed, 0)

    def test_dry_run_writes_nothing(self) -> None:
        before = self.fragrance_path.read_text(encoding="utf-8")
        result = enrich_parfumo_documents(
            self.csv_path,
            PROJECT_ROOT / "data",
            self.vault,
            staging_directory=self.staging,
            updated_at="2026-08-17",
            dry_run=True,
        )
        self.assertEqual(result.changed, 1)
        self.assertEqual(self.fragrance_path.read_text(encoding="utf-8"), before)
        self.assertFalse(self.staging.exists())

    def test_cli_exposes_enrichment_and_audit(self) -> None:
        enrich = create_parser().parse_args(["parfumo-enrich", "--input", "local.csv", "--dry-run"])
        audit = create_parser().parse_args(["parfumo-audit-candidates"])
        self.assertEqual(enrich.command, "parfumo-enrich")
        self.assertTrue(enrich.dry_run)
        self.assertEqual(audit.command, "parfumo-audit-candidates")


if __name__ == "__main__":
    unittest.main()
