from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from antiquario_data.term_resolver import TermResolver, normalize_term


class TestTermResolver(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.data_dir = self.root_path / "data"
        self.taxonomy_dir = self.data_dir / "taxonomy"
        self.taxonomy_dir.mkdir(parents=True, exist_ok=True)

        (self.taxonomy_dir / "taxonomy.yml").write_text(
            """
schema_version: 1
locale_default: pt-BR
license: CC0-1.0
reviewed_at: 2026-07-22

families:
  - { id: citrica, pt: Cítrica, en: Citrus, source_ids: [internal_curated] }

accords:
  - { id: citrico, pt: cítrico, en: citrus, aliases: [hesperídico], family_ids: [citrica], source_ids: [internal_curated] }

notes:
  - { id: bergamota, pt: bergamota, en: bergamot, aliases: [bergamot], family_ids: [citrica], source_ids: [internal_curated] }
  - { id: sandalo, pt: sândalo, en: sandalwood, aliases: [], family_ids: [citrica], source_ids: [internal_curated] }
  - { id: copaiba, pt: copaíba, en: copaiba, aliases: [], family_ids: [citrica], source_ids: [internal_curated] }
""",
            encoding="utf-8",
        )

        (self.taxonomy_dir / "source-aliases.yml").write_text(
            """
schema_version: 1
reviewed_at: 2026-07-22

sources:
  natura:
    notes:
      "copaiba da amazonia": copaiba
      "calabria bergamot": bergamota
""",
            encoding="utf-8",
        )

        self.resolver = TermResolver(self.data_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_normalize_term(self) -> None:
        self.assertEqual(normalize_term("Sândalo do Mistan"), "sandalo do mistan")
        self.assertEqual(normalize_term("Copaíba--Amazônia"), "copaiba amazonia")

    def test_resolve_canonical_note(self) -> None:
        res1 = self.resolver.resolve_note("bergamota")
        self.assertIsNotNone(res1)
        self.assertEqual(res1.canonical_id, "note:bergamota")

        res2 = self.resolver.resolve_note("sândalo")
        self.assertIsNotNone(res2)
        self.assertEqual(res2.canonical_id, "note:sandalo")

        res3 = self.resolver.resolve_note("bergamot")
        self.assertIsNotNone(res3)
        self.assertEqual(res3.canonical_id, "note:bergamota")

    def test_resolve_source_alias(self) -> None:
        res = self.resolver.resolve_note("copaiba da amazonia", brand="natura")
        self.assertIsNotNone(res)
        self.assertEqual(res.canonical_id, "note:copaiba")
        self.assertEqual(res.match_source, "source_alias")

    def test_resolve_family(self) -> None:
        res = self.resolver.resolve_family("Cítrica")
        self.assertIsNotNone(res)
        self.assertEqual(res.canonical_id, "family:citrica")

    def test_unresolved_term_returns_none(self) -> None:
        res = self.resolver.resolve_note("nota_misteriosa_e_desconhecida")
        self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
