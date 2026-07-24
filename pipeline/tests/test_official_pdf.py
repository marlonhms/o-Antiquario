from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from antiquario_data.official_pdf import (
    ProductCandidate,
    QuarantineItem,
    extract_pdf_pages,
    hash_file,
    normalize_text_key,
    parse_page_content,
    process_official_pdf,
)


import pypdf


def create_synthetic_pdf(text_lines_per_page: list[list[str]], output_path: Path) -> Path:
    """Gera um arquivo PDF sintético e reproduzível com camadas de texto para cada página."""
    writer = pypdf.PdfWriter()

    font_dict = pypdf.generic.DictionaryObject({
        pypdf.generic.NameObject("/Type"): pypdf.generic.NameObject("/Font"),
        pypdf.generic.NameObject("/Subtype"): pypdf.generic.NameObject("/Type1"),
        pypdf.generic.NameObject("/BaseFont"): pypdf.generic.NameObject("/Helvetica"),
    })

    resources = pypdf.generic.DictionaryObject({
        pypdf.generic.NameObject("/Font"): pypdf.generic.DictionaryObject({
            pypdf.generic.NameObject("/F1"): font_dict
        })
    })

    for page_lines in text_lines_per_page:
        page = writer.add_blank_page(width=612, height=792)
        bt_lines = ["BT", "/F1 12 Tf", "100 700 Td"]
        for idx, line in enumerate(page_lines):
            safe_line = line.replace("(", "\\(").replace(")", "\\)")
            if idx == 0:
                bt_lines.append(f"({safe_line}) Tj")
            else:
                bt_lines.append(f"0 -20 Td ({safe_line}) Tj")
        bt_lines.append("ET")
        stream_str = "\n".join(bt_lines)

        content_stream = pypdf.generic.DecodedStreamObject()
        content_stream._data = stream_str.encode("latin-1", errors="replace")

        page[pypdf.generic.NameObject("/Resources")] = resources
        page[pypdf.generic.NameObject("/Contents")] = content_stream

    with output_path.open("wb") as handle:
        writer.write(handle)

    return output_path



class TestOfficialPdfConnector(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.data_dir = self.root_path / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_normalize_text_key(self) -> None:
        self.assertEqual(normalize_text_key("Essencial Único!"), "essencial unico")
        self.assertEqual(normalize_text_key("Água de Cheiro -- 2026"), "agua de cheiro 2026")

    def test_extract_pdf_pages_synthetic(self) -> None:
        pdf_path = self.root_path / "sample.pdf"
        create_synthetic_pdf(
            [
                ["Perfume: Natura Ekos Castanha", "Linha: Ekos", "Notas: castanha, bergamota"],
                ["Página sem notas de produto"],
            ],
            pdf_path,
        )

        pages, doc_hash = extract_pdf_pages(pdf_path)
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0].status, "success")
        self.assertEqual(pages[1].status, "success")
        self.assertEqual(len(doc_hash), 64)
        self.assertIn("Natura Ekos Castanha", pages[0].text)

    def test_unlayered_notes_preservation(self) -> None:
        cands, claims, quars = parse_page_content(
            page_number=1,
            text="Perfume: Frescor de Maracujá\nNotas Olfativas: maracujá, bergamota, cedro",
            doc_hash="abc123hash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual(len(cands), 1)
        cand = cands[0]
        self.assertEqual(cand.product_name, "Frescor de Maracujá")
        self.assertEqual(cand.declared_notes_unlayered, ["bergamota", "cedro", "maracujá"])
        self.assertEqual(cand.declared_pyramid["top"], [])
        self.assertEqual(cand.declared_pyramid["heart"], [])
        self.assertEqual(cand.declared_pyramid["base"], [])

        unlayered_claims = [c for c in claims if c.field == "declared_notes_unlayered"]
        self.assertEqual(len(unlayered_claims), 3)

    def test_layered_pyramid_extraction(self) -> None:
        cands, claims, quars = parse_page_content(
            page_number=2,
            text="Perfume: Essencial Estilo\nDeo Parfum\nNotas de topo: bergamota, mandarina\nNotas de corpo: iris, rosa\nNotas de fundo: sandalo, ambar",
            doc_hash="def456hash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual(len(cands), 1)
        cand = cands[0]
        self.assertEqual(cand.concentration, "Deo Parfum")
        self.assertEqual(cand.declared_pyramid["top"], ["bergamota", "mandarina"])
        self.assertEqual(cand.declared_pyramid["heart"], ["iris", "rosa"])
        self.assertEqual(cand.declared_pyramid["base"], ["ambar", "sandalo"])

        top_claims = [c for c in claims if c.field == "top_note"]
        self.assertEqual(len(top_claims), 2)

    def test_extracts_multiple_perfumes_and_ignores_adjacent_body_care(self) -> None:
        candidates, claims, quarantine = parse_page_content(
            page_number=41,
            text=(
                "Creme de barbear essencial 75 g\n"
                "Balm pós-barba essencial 75 ml\n"
                "Deo parfum essencial único masculino 90 ml\n"
                "Amadeirado intenso.\n"
                "Deo parfum essencial atrai masculino 100 ml\n"
                "Amadeirado especiado."
            ),
            doc_hash="cataloghash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual([candidate.product_name for candidate in candidates], ["Essencial Unico", "Essencial Atrai"])
        self.assertTrue(all(candidate.curation_status == "auto_approved" for candidate in candidates))
        self.assertNotIn("Balm pós-barba", [candidate.product_name for candidate in candidates])
        self.assertNotIn("Creme de barbear", [candidate.product_name for candidate in candidates])

    def test_ignores_catalog_page_without_fragrance_product_anchor(self) -> None:
        candidates, claims, quarantine = parse_page_content(
            page_number=149,
            text=(
                "Kit presente com caixa e pente\n"
                "Creme hidratante corporal 400 ml\n"
                "Desodorante antitranspirante roll-on 70 ml\n"
                "Óleo corporal perfumado 200 ml"
            ),
            doc_hash="cataloghash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual(candidates, [])
        self.assertEqual(claims, [])

    def test_quarantines_text_created_by_mixed_catalog_columns(self) -> None:
        candidates, claims, quarantine = parse_page_content(
            page_number=60,
            text="Deo parfum deo parfum essencial essencial atrai único 100 ml",
            doc_hash="cataloghash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual(candidates, [])
        self.assertEqual(claims, [])
        self.assertEqual(quarantine[0].issue_type, "ambiguous_product_name")

    def test_extracts_declared_accords_and_materials_from_product_context(self) -> None:
        candidates, claims, quarantine = parse_page_content(
            page_number=63,
            text=(
                "Eau de parfum aura alba 75 ml\n"
                "Floral amadeirado. Combina rosa alba, lichia, sândalo e patchouli.\n"
                "Creme aveludado corporal aura alba 200 g"
            ),
            doc_hash="cataloghash",
            brand_hint="natura",
            source_id="official_catalog_natura",
        )

        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate.product_name, "Aura Alba")
        self.assertIn("floral amadeirado", candidate.declared_accords)
        self.assertIn("amadeirado", candidate.declared_accords)
        self.assertIn("lichia", candidate.declared_materials)
        self.assertIn("sandalo", candidate.declared_materials)
        self.assertIn("patchouli", candidate.declared_materials)
        self.assertEqual(candidate.curation_status, "auto_approved")

    def test_idempotency_and_staging_output(self) -> None:
        pdf_path = self.root_path / "idempotent.pdf"
        create_synthetic_pdf(
            [
                ["Perfume: Malbec Absolute", "Linha: Malbec", "Deo Parfum", "Notas de topo: pimenta preta", "Notas de fundo: couro"],
            ],
            pdf_path,
        )

        result1 = process_official_pdf(
            pdf_path=pdf_path,
            brand="o-boticario",
            edition="2025",
            source_id="official_catalog_o_boticario",
            data_directory=self.data_dir,
        )

        doc_hash = result1["document"]["document_hash"]
        staging_dir = self.data_dir / "staging" / "official-pdf" / doc_hash

        self.assertTrue((staging_dir / "document.json").exists())
        self.assertTrue((staging_dir / "pages.jsonl").exists())
        self.assertTrue((staging_dir / "claims.jsonl").exists())
        self.assertTrue((staging_dir / "candidates.jsonl").exists())
        self.assertTrue((staging_dir / "quarantine.jsonl").exists())
        self.assertTrue((staging_dir / "report.json").exists())

        # Executa uma segunda vez e valida idempotência da hash e saídas
        result2 = process_official_pdf(
            pdf_path=pdf_path,
            brand="o-boticario",
            edition="2025",
            source_id="official_catalog_o_boticario",
            data_directory=self.data_dir,
        )

        self.assertEqual(result1["document"]["document_hash"], result2["document"]["document_hash"])
        self.assertEqual(result1["report"]["candidates_count"], result2["report"]["candidates_count"])

    def test_dry_run_does_not_write(self) -> None:
        pdf_path = self.root_path / "dryrun.pdf"
        create_synthetic_pdf(
            [["Perfume: Natura Homem Madeiras", "Notas: sândalo, cedro"]],
            pdf_path,
        )

        result = process_official_pdf(
            pdf_path=pdf_path,
            brand="natura",
            edition="2026",
            source_id="official_catalog_natura",
            data_directory=self.data_dir,
            dry_run=True,
        )

        doc_hash = result["document"]["document_hash"]
        staging_dir = self.data_dir / "staging" / "official-pdf" / doc_hash
        self.assertFalse(staging_dir.exists())
        self.assertEqual(result["report"]["candidates_count"], 1)


    def test_high_confidence_candidate_is_auto_curated(self) -> None:
        pdf_path = self.root_path / "inbox_test.pdf"
        create_synthetic_pdf(
            [["Perfume: Natura Ekos Copaíba", "Notas: bergamota, sândalo"]],
            pdf_path,
        )

        result = process_official_pdf(
            pdf_path=pdf_path,
            brand="natura",
            edition="2026",
            source_id="official_catalog_natura",
            data_directory=self.data_dir,
            generate_inbox=True,
        )

        self.assertEqual(result["report"]["inbox_drafts_created"], 0)
        self.assertGreaterEqual(result["report"]["auto_curated_candidates"], 1)
        doc_hash = result["document"]["document_hash"]
        auto_curated_path = self.data_dir / "staging" / "official-pdf" / doc_hash / "auto-curated-candidates.jsonl"
        self.assertTrue(auto_curated_path.exists())
        inbox_dir = self.data_dir.parent / "knowledge" / "vault" / "00_Inbox" / "Curadoria-Oficial-PDF"
        self.assertFalse(inbox_dir.exists())


if __name__ == "__main__":
    unittest.main()
