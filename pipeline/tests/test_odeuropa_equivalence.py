from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.cli import create_parser
from antiquario_data.io_utils import atomic_write_text, load_json, write_dicts_jsonl
from antiquario_data.odeuropa import normalize_search_key
from antiquario_data.odeuropa_equivalence import resolve_odeuropa_equivalences


SNAPSHOT_ID = "a" * 64


def _term(
    identifier: str,
    label: str,
    language: str,
    entity_type: str,
    *,
    synsets: list[str] | None = None,
    status: str = "candidate",
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "id": f"odeuropa:term:{identifier}",
        "source_ref": "fixture-v1",
        "snapshot_id": SNAPSHOT_ID,
        "source_file": f"taxonomies-v2/{language.upper()}_taxonomy.tsv",
        "source_row": 2,
        "source_locator": f"https://example.test/{language}#L2",
        "license": "CC-BY-4.0",
        "attribution": "fixture",
        "language": language,
        "entry_original": f"{label}_noun",
        "term_original": label,
        "search_key": normalize_search_key(label),
        "part_of_speech": "noun",
        "source_method": "seed",
        "evidence_nature": "curated",
        "wordnet_synsets": synsets or [],
        "entity_type_candidate": entity_type,
        "status": status,
        "promotion_status": "blocked",
    }


def _prepare_fixture(root: Path) -> tuple[Path, Path]:
    data = root / "data"
    taxonomy_path = data / "taxonomy" / "taxonomy.yml"
    taxonomy_path.parent.mkdir(parents=True)
    taxonomy_path.write_text(
        """
schema_version: 1
locale_default: pt-BR
license: CC0-1.0
reviewed_at: 2026-08-17
families:
  - { id: floral, pt: Floral, en: Floral, source_ids: [internal_curated] }
accords:
  - { id: floral, pt: floral, en: Floral, aliases: [], family_ids: [floral], source_ids: [internal_curated] }
  - { id: doce, pt: doce, en: Sweet, aliases: [], family_ids: [floral], source_ids: [internal_curated] }
notes:
  - { id: bergamota, pt: bergamota, en: Bergamot, aliases: [citrus-zest], family_ids: [floral], source_ids: [internal_curated] }
  - { id: rosa, pt: rosa, en: Rose, aliases: [], family_ids: [floral], source_ids: [internal_curated] }
""".strip() + "\n",
        encoding="utf-8",
    )
    staging = data / "staging" / "odeuropa" / "fixture"
    terms = [
        _term("bergamot-en", "bergamot", "en", "odor-descriptor", synsets=["bergamot.n.01"]),
        _term("bergamotto-it", "bergamotto", "it", "odor-descriptor", synsets=["bergamot.n.01"]),
        _term("sweet-en", "sweet", "en", "odor-quality", synsets=["sweet.a.01"]),
        _term("dolce-it", "dolce", "it", "odor-quality", synsets=["sweet.a.01"]),
        _term("sweet-source-fr", "sucré", "fr", "odor-descriptor", synsets=["sweet.a.01"]),
        _term("floral-en", "floral", "en", "odor-descriptor"),
        _term("rosa-fr", "rosa", "fr", "odor-descriptor"),
        _term("alias-en", "citrus-zest", "en", "odor-descriptor"),
        _term("unknown-en", "moon-dust", "en", "odor-descriptor"),
        _term("quarantined-en", "rose", "en", "odor-descriptor", status="quarantined"),
    ]
    write_dicts_jsonl(staging / "terms.jsonl", terms)
    atomic_write_text(staging / "report.json", json.dumps({"snapshot_id": SNAPSHOT_ID}) + "\n")
    atomic_write_text(
        data / "staging" / "odeuropa" / "latest.json",
        json.dumps({"staging_directory": "staging/odeuropa/fixture"}) + "\n",
    )
    return data, taxonomy_path


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


class OdeuropaEquivalenceTest(unittest.TestCase):
    def test_resolver_separates_retrieval_bridges_candidates_and_ambiguities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, taxonomy_path = _prepare_fixture(Path(temporary))
            taxonomy_before = sha256(taxonomy_path.read_bytes()).hexdigest()

            result = resolve_odeuropa_equivalences(data)
            report = load_json(result.output_directory / "report.json")
            bridges = _read_jsonl(result.output_directory / "resolved-retrieval-bridges.jsonl")
            candidates = _read_jsonl(result.output_directory / "equivalence-candidates.jsonl")
            ambiguities = _read_jsonl(result.output_directory / "ambiguities.jsonl")
            unresolved = _read_jsonl(result.output_directory / "unresolved.jsonl")

            self.assertEqual(result.resolved_bridges, 2)
            self.assertEqual(result.candidates, 3)
            self.assertEqual(result.ambiguities, 3)
            self.assertEqual(result.unresolved, 2)
            self.assertEqual(report["contract"]["scope"], "retrieval_only")
            self.assertEqual(report["contract"]["semantic_identity"], "unverified")
            self.assertFalse(report["contract"]["commercial_claims_generated"])
            self.assertTrue(all(item["status"] == "resolved_for_retrieval" for item in bridges))
            self.assertTrue(all(item["semantic_identity"] == "unverified" for item in bridges + candidates))
            self.assertIn("shared_wordnet_synset", {item["match"]["method"] for item in candidates})
            self.assertEqual(
                {item["reason"] for item in ambiguities},
                {"canonical_english_label_collision", "cross_language_homograph", "synset_crosses_odeuropa_types"},
            )
            self.assertEqual(
                {item["reason"] for item in unresolved},
                {"no_supported_equivalence_evidence", "source_term_quarantined"},
            )
            self.assertEqual(taxonomy_before, sha256(taxonomy_path.read_bytes()).hexdigest())
            serialized_links = json.dumps(bridges + candidates)
            for forbidden in ("has-note", "has-top-note", "has-heart-note", "has-base-note", "declares-"):
                self.assertNotIn(forbidden, serialized_links)

    def test_resolution_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _ = _prepare_fixture(Path(temporary))
            first = resolve_odeuropa_equivalences(data)
            first_manifest = (first.output_directory / "manifest.json").read_bytes()
            first_bridges = (first.output_directory / "resolved-retrieval-bridges.jsonl").read_bytes()
            second = resolve_odeuropa_equivalences(data)
            self.assertEqual(first_manifest, (second.output_directory / "manifest.json").read_bytes())
            self.assertEqual(first_bridges, (second.output_directory / "resolved-retrieval-bridges.jsonl").read_bytes())

    def test_duplicate_source_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data, _ = _prepare_fixture(Path(temporary))
            terms_path = data / "staging" / "odeuropa" / "fixture" / "terms.jsonl"
            terms = _read_jsonl(terms_path)
            write_dicts_jsonl(terms_path, [*terms, terms[0]])
            with self.assertRaisesRegex(ValueError, "IDs de termo vazios ou duplicados"):
                resolve_odeuropa_equivalences(data)

    def test_cli_exposes_batch_resolver(self) -> None:
        args = create_parser().parse_args(["odeuropa-resolve", "--taxonomy", "taxonomy.yml"])
        self.assertEqual(args.command, "odeuropa-resolve")
        self.assertEqual(args.taxonomy, Path("taxonomy.yml"))


if __name__ == "__main__":
    unittest.main()
