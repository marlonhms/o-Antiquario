from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import load_json
from antiquario_data.odeuropa import ATTRIBUTION, LICENSE_ID, normalize_search_key, sync_odeuropa


HEADER = "\t".join([
    "word",
    "source",
    "synset",
    "first appearance",
    "1650-1700",
    "1701-1750",
    "1751-1800",
    "1801-1850",
    "1851-1900",
    "1901-1925",
    "smell-source",
    "quality",
])


def _row(
    word: str,
    source: str = "seed",
    synset: str = "",
    first: str = "1650",
    periods: tuple[str, ...] = ("yes", "yes", "no", "no", "no", "no"),
    smell: str = "",
    quality: str = "",
) -> str:
    return "\t".join([word, source, synset, first, *periods, smell, quality])


def _write_source(root: Path) -> Path:
    taxonomy = root / "taxonomies-v2"
    taxonomy.mkdir(parents=True)
    rows = {
        "EN_taxonomy.tsv": [
            _row("rose_noun", synset="['rose.n.01']", smell="CATEGORY|flowers|plant|tree|soil"),
            _row("rosé_noun", source="cooc", synset="['wine.n.01']", smell="CATEGORY|food|beverage"),
            _row("sweet_adj", synset="['sweet.a.01']", quality="CATEGORY|sweet|spicy"),
            _row("odor_noun"),
            _row("invalid", smell="CATEGORY|industry"),
        ],
        "DE_taxonomy.tsv": [_row("blume_noun", source="WordNetExpansion", synset="s154610", smell="CATEGORY|flowers|plant|tree|soil")],
        "IT_taxonomy.tsv": [_row("dolce_adj", quality="CATEGORY|sweet|spicy")],
        "FR_taxonomy.tsv": [_row("floral_adj", quality="CATEGORY|Fragrant|fruity|floral") + "\tmanual"],
    }
    for filename, records in rows.items():
        header = HEADER + ("\t" if filename == "FR_taxonomy.tsv" else "")
        (taxonomy / filename).write_text(f"{header}\n" + "\n".join(records) + "\n", encoding="utf-8")
    return root


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


class OdeuropaPipelineTest(unittest.TestCase):
    def test_normalization_is_multilingual_and_diacritic_insensitive(self) -> None:
        self.assertEqual(normalize_search_key("  Rosé_du-Bois! "), "rose du bois")

    def test_sync_preserves_provenance_and_quarantines_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = _write_source(root / "source")
            data = root / "data"

            result = sync_odeuropa(data, source_directory=source, source_ref="fixture-v1", retrieved_at="2026-08-17")
            report = load_json(result.staging_directory / "report.json")
            terms = _read_jsonl(result.staging_directory / "terms.jsonl")
            entities = _read_jsonl(result.staging_directory / "entity-candidates.jsonl")
            classifications = _read_jsonl(result.staging_directory / "classification-candidates.jsonl")
            collisions = _read_jsonl(result.staging_directory / "collisions.jsonl")
            quarantine = _read_jsonl(result.staging_directory / "quarantine.jsonl")
            warnings = _read_jsonl(result.staging_directory / "warnings.jsonl")

            self.assertEqual(result.languages, ("de", "en", "fr", "it"))
            self.assertEqual(report["guards"]["target_layer"], "staging")
            self.assertEqual(report["guards"]["promotion_status"], "blocked")
            self.assertFalse(report["guards"]["commercial_claims_generated"])
            self.assertEqual({entity["entity_type"] for entity in entities}, {"odor-descriptor", "odor-quality"})
            self.assertTrue(all(entity["provenance"]["license"] == LICENSE_ID for entity in entities))
            self.assertTrue(all(entity["provenance"]["attribution"] == ATTRIBUTION for entity in entities))
            self.assertEqual(len(classifications), len(entities))
            self.assertTrue(all(item["hierarchy_interpretation"] == "not_assumed" for item in classifications))
            self.assertEqual(len(collisions), 1)
            self.assertEqual(collisions[0]["search_key"], "rose")
            rose_entities = [entity for entity in entities if entity["search_key"] == "rose"]
            self.assertEqual(len(rose_entities), 2)
            self.assertTrue(all(entity["status"] == "quarantined" for entity in rose_entities))
            self.assertTrue(any(item["reason"] == "missing_odeuropa_category" for item in quarantine))
            self.assertTrue(any(item["reason"] == "malformed_row" for item in quarantine))
            self.assertEqual(len(warnings), 1)
            self.assertEqual(warnings[0]["values"], ["manual"])
            self.assertTrue(all(term["promotion_status"] == "blocked" for term in terms))
            self.assertEqual(len({term["id"] for term in terms}), len(terms))
            serialized = json.dumps({"terms": terms, "entities": entities, "classifications": classifications})
            for forbidden in ("has-note", "has-top-note", "has-heart-note", "has-base-note", "declares-"):
                self.assertNotIn(forbidden, serialized)

    def test_same_snapshot_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = _write_source(root / "source")
            data = root / "data"
            first = sync_odeuropa(data, source_directory=source, source_ref="fixture-v1", retrieved_at="2026-08-17")
            first_report = (first.staging_directory / "report.json").read_bytes()
            first_terms = (first.staging_directory / "terms.jsonl").read_bytes()

            second = sync_odeuropa(data, source_directory=source, source_ref="fixture-v1", retrieved_at="2026-08-18")

            self.assertEqual(first.snapshot_id, second.snapshot_id)
            self.assertEqual(first_report, (second.staging_directory / "report.json").read_bytes())
            self.assertEqual(first_terms, (second.staging_directory / "terms.jsonl").read_bytes())
            latest = load_json(data / "staging" / "odeuropa" / "latest.json")
            self.assertEqual(latest["snapshot_id"], first.snapshot_id)

    def test_cli_accepts_odeuropa_specific_options(self) -> None:
        args = create_parser().parse_args([
            "sync",
            "odeuropa",
            "--source-dir",
            "checkout",
            "--ref",
            "fixture-v1",
            "--language",
            "fr",
        ])
        self.assertEqual(args.source, "odeuropa")
        self.assertEqual(args.language, ["fr"])


if __name__ == "__main__":
    unittest.main()
