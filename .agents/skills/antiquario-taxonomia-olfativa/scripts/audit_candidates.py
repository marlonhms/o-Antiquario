#!/usr/bin/env python3
"""Audit olfactory taxonomy relation candidates without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ENTITY_TYPES = {
    "fragrance",
    "olfactory-note",
    "accord",
    "raw-material",
    "molecule",
    "odor-descriptor",
    "odor-quality",
    "olfactory-family",
}

RELATION_CONTRACTS = {
    "described-as": ({"olfactory-note", "raw-material", "molecule"}, {"odor-descriptor"}),
    "has-quality": (
        {"olfactory-note", "raw-material", "molecule", "odor-descriptor"},
        {"odor-quality"},
    ),
    "belongs-to-olfactory-family": ({"odor-descriptor"}, {"olfactory-family"}),
    "broader-descriptor-than": ({"odor-descriptor"}, {"odor-descriptor"}),
    "broader-quality-than": ({"odor-quality"}, {"odor-quality"}),
    "derived-from": ({"olfactory-note"}, {"raw-material"}),
    "contains-odorant": ({"raw-material"}, {"molecule"}),
}

PROTECTED_RELATIONS = {
    "has-note",
    "has-top-note",
    "has-heart-note",
    "has-base-note",
    "declares-top-note",
    "declares-heart-note",
    "declares-base-note",
    "declares-unlayered-note",
    "declares-family",
    "declares-accord",
}

CONFIDENCE_LEVELS = {"high", "medium", "low", "unknown"}
CLAIM_NATURES = {"declared", "observed", "curated", "inferred", "predicted"}
GLOBAL_ID = re.compile(r"^antiquario:[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$")


def load_records(path: Path) -> list[Any]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        return payload["candidates"]
    return [payload]


def require_string(value: Any, field: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field}: deve ser texto não vazio")
        return None
    return value


def audit_entity(value: Any, field: str, errors: list[str]) -> tuple[str | None, str | None]:
    if not isinstance(value, dict):
        errors.append(f"{field}: deve ser objeto")
        return None, None
    entity_id = require_string(value.get("id"), f"{field}.id", errors)
    entity_type = require_string(value.get("type"), f"{field}.type", errors)
    if entity_id and not GLOBAL_ID.fullmatch(entity_id):
        errors.append(f"{field}.id: ID global inválido '{entity_id}'")
    if entity_type and entity_type not in ENTITY_TYPES:
        errors.append(f"{field}.type: tipo desconhecido '{entity_type}'")
    if entity_id and entity_type:
        id_type = entity_id.split(":", 2)[1]
        if id_type != entity_type:
            errors.append(f"{field}: tipo '{entity_type}' difere do segmento do ID '{id_type}'")
    return entity_id, entity_type


def audit_evidence(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("evidence: deve ser objeto")
        return
    for field in ("source_id", "locator", "license", "claim_scope", "method"):
        require_string(value.get(field), f"evidence.{field}", errors)
    confidence = require_string(value.get("confidence"), "evidence.confidence", errors)
    if confidence and confidence not in CONFIDENCE_LEVELS:
        errors.append(f"evidence.confidence: valor inválido '{confidence}'")


def audit_record(record: Any, index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"candidato[{index}]"
    if not isinstance(record, dict):
        return [f"{prefix}: deve ser objeto"]

    if record.get("status") != "candidate":
        errors.append("status: relações automáticas devem permanecer como 'candidate'")

    claim_nature = require_string(record.get("claim_nature"), "claim_nature", errors)
    if claim_nature and claim_nature not in CLAIM_NATURES:
        errors.append(f"claim_nature: valor inválido '{claim_nature}'")

    _, subject_type = audit_entity(record.get("subject"), "subject", errors)
    _, object_type = audit_entity(record.get("object"), "object", errors)
    predicate = require_string(record.get("predicate"), "predicate", errors)
    audit_evidence(record.get("evidence"), errors)

    if subject_type == "fragrance":
        errors.append("subject: esta fila científica não pode criar relações para fragrâncias")

    if predicate in PROTECTED_RELATIONS or (predicate and predicate.startswith("declares-")):
        errors.append(f"predicate: relação comercial protegida '{predicate}'")
    elif predicate:
        contract = RELATION_CONTRACTS.get(predicate)
        if contract is None:
            errors.append(f"predicate: relação científica desconhecida '{predicate}'")
        elif subject_type and object_type:
            sources, targets = contract
            if subject_type not in sources or object_type not in targets:
                errors.append(f"predicate: '{predicate}' não permite {subject_type} -> {object_type}")

    return [f"{prefix}: {error}" for error in errors]


def audit(records: Iterable[Any]) -> list[str]:
    return [error for index, record in enumerate(records) for error in audit_record(record, index)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita candidatos científicos antes de entrarem no grafo olfativo."
    )
    parser.add_argument("path", type=Path, help="Arquivo JSON ou JSONL de candidatos")
    args = parser.parse_args()

    try:
        records = load_records(args.path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2

    errors = audit(records)
    print(
        json.dumps(
            {"valid": not errors, "candidates": len(records), "errors": errors},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
