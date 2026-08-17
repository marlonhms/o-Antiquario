from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from antiquario_data.knowledge_enrichment import _load_jsonl, audit_enrichment_candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita candidatos de enriquecimento factual do Antiquário")
    parser.add_argument("path", type=Path, help="arquivo candidates.jsonl")
    args = parser.parse_args()
    result = audit_enrichment_candidates(_load_jsonl(args.path.resolve()))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
