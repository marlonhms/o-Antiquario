from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import yaml

from antiquario_data.cli import create_parser
from antiquario_data.presentation_migration import migrate_official_presentation_metadata


PROFILE = """recommendation_profile:
  segments: [nacional, acessivel]
  formality: 0.5
  priceTier: 2
  accords: {amadeirado: 0.8, floral: 0.7, citricos: 0.6}
  occasions: {casual: 0.9, encontro: 0.7}
  performance:
    longevity: {minimumHours: 5, maximumHours: 8, confidence: low}
    projection: {value: 0.6, confidence: low}
    sillage: {value: 0.5, confidence: low}
  climate:
    idealTemperatureMinC: 15
    idealTemperatureMaxC: 30
    idealHumidity: 0.6
    indoorFit: 0.8
    outdoorFit: 0.7
"""


def document(profile: str = PROFILE) -> str:
    return f"""---
schema_version: 1
id: antiquario:fragrance:test
type: fragrance
title: Teste
source_ids: [official_catalog_o_boticario]
updated_at: 2026-07-23
evidence:
  - source_id: official_catalog_o_boticario
    kind: manufacturer
relations:
  - predicate: has-accord
    target: antiquario:accord:citricos
  - predicate: suited-to
    target: antiquario:context:escritorio
  - predicate: has-top-note
    target: antiquario:note:bergamota
{profile}---
# Teste

- Marca: O Boticário
- Concentração: Eau de Parfum

- [x] Revisão manual automatizada para cumprir o contrato de ranking com dados do PDF.
"""


def parse_frontmatter(path: Path) -> dict[str, object]:
    contents = path.read_text(encoding="utf-8")
    return yaml.safe_load(contents.split("---\n", 2)[1])


class TestPresentationMigration(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault = Path(self.temp_dir.name) / "vault"
        self.perfumes = self.vault / "10_Perfumes"
        self.perfumes.mkdir(parents=True)
        self.path = self.perfumes / "teste.md"
        self.path.write_text(document(), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_dry_run_does_not_change_document(self) -> None:
        before = self.path.read_text(encoding="utf-8")
        result = migrate_official_presentation_metadata(self.vault, dry_run=True)

        self.assertEqual(result.migrated, 1)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)

    def test_migrates_only_supported_structural_claims_and_is_idempotent(self) -> None:
        result = migrate_official_presentation_metadata(self.vault)
        migrated = parse_frontmatter(self.path)
        relations = {
            (relation["predicate"], relation["target"])
            for relation in migrated["relations"]
        }

        self.assertEqual(result.migrated, 1)
        self.assertNotIn("recommendation_profile", migrated)
        self.assertIn(("belongs-to-brand", "antiquario:brand:o-boticario"), relations)
        self.assertIn(("declares-concentration", "antiquario:concentration:eau-de-parfum"), relations)
        self.assertIn(("declares-top-note", "antiquario:note:bergamota"), relations)
        self.assertNotIn(("has-accord", "antiquario:accord:citricos"), relations)
        self.assertNotIn(("suited-to", "antiquario:context:escritorio"), relations)
        self.assertIn("este registro não entra no ranking", self.path.read_text(encoding="utf-8"))
        self.assertEqual(result.unsupported_defaults_removed, 1)
        self.assertEqual(result.body_markers_repaired, 1)

        second = migrate_official_presentation_metadata(self.vault)
        self.assertEqual(second.migrated, 0)
        self.assertEqual(second.unchanged, 1)

    def test_refuses_to_remove_a_divergent_profile(self) -> None:
        self.path.write_text(document(PROFILE.replace("formality: 0.5", "formality: 0.7")), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "diverge do fallback conhecido"):
            migrate_official_presentation_metadata(self.vault)

    def test_cli_exposes_migration_command(self) -> None:
        args = create_parser().parse_args(["presentation-migrate-official", "--dry-run"])
        self.assertEqual(args.command, "presentation-migrate-official")
        self.assertTrue(args.dry_run)


if __name__ == "__main__":
    unittest.main()
