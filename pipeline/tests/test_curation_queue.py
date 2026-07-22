from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from antiquario_data.curation_queue import build_curation_queue
from antiquario_data.warehouse import build_catalog
from antiquario_data.wikidata import sync_wikidata


FIXTURE = Path(__file__).parent / "fixtures" / "wikidata-perfumes.json"


class CurationQueueTest(unittest.TestCase):
    def test_builds_preserving_draft_queue_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            vault = root / "vault"
            release = root / "release"
            report = root / "report.json"
            sync_wikidata(data, limit=10, fixture=FIXTURE, retrieved_at="2026-07-22")
            build_catalog(data)
            (release / "resolution-report.json").parent.mkdir(parents=True)
            (release / "resolution-report.json").write_text(json.dumps({
                "ambiguousClusters": [{"fragranceIds": ["wd-q999999992"]}],
            }), encoding="utf-8")

            first = build_curation_queue(
                data_directory=data,
                vault_directory=vault,
                release_directory=release,
                report_path=report,
                limit=10,
            )
            self.assertEqual(1, len(first.selected))
            self.assertEqual("Q999999991", first.selected[0].wikidata_id)
            self.assertEqual(1, len(first.created))
            draft = first.created[0]
            contents = draft.read_text(encoding="utf-8")
            self.assertIn("wikidata: Q999999991", contents)
            self.assertIn("curadoria-pendente", contents)
            self.assertIn("não deve ser usado pelo motor de ranking", contents)

            draft.write_text(f"{contents}\nNota humana preservada.\n", encoding="utf-8")
            second = build_curation_queue(
                data_directory=data,
                vault_directory=vault,
                release_directory=release,
                report_path=report,
                limit=10,
            )
            self.assertEqual(0, len(second.created))
            self.assertEqual([draft], list(second.preserved))
            queue_report = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(["wd-q999999992"], queue_report["selection"]["excludedAmbiguousRecords"])


if __name__ == "__main__":
    unittest.main()
