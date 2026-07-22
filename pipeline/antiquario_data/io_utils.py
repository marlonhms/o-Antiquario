from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable

from .models import FragranceRecord, OlfactoryDescriptorRecord, WikidataSemanticClaimRecord, canonical_json


def atomic_write_text(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        delete=False,
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as handle:
        handle.write(contents)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_raw_snapshot(
    payload: dict[str, Any],
    query: str,
    raw_directory: Path,
    retrieved_at: str | None = None,
    *,
    filename_prefix: str = "perfumes",
) -> tuple[Path, dict[str, Any]]:
    if not re.fullmatch(r"[a-z0-9-]+", filename_prefix):
        raise ValueError("filename_prefix deve conter apenas letras minúsculas, números e hífens")
    payload_json = canonical_json(payload)
    query_hash = sha256(query.encode("utf-8")).hexdigest()
    payload_hash = sha256(payload_json.encode("utf-8")).hexdigest()
    snapshot_hash = sha256(f"{query_hash}:{payload_hash}".encode("utf-8")).hexdigest()
    path = raw_directory / f"{filename_prefix}-{snapshot_hash[:12]}.json"

    if path.exists():
        envelope = load_json(path)
        return path, envelope

    date = retrieved_at or datetime.now(timezone.utc).date().isoformat()
    envelope = {
        "schema_version": 1,
        "source_id": "wikidata",
        "retrieved_at": date,
        "query_sha256": query_hash,
        "payload_sha256": payload_hash,
        "snapshot_id": snapshot_hash,
        "payload": payload,
    }
    atomic_write_text(path, f"{json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2)}\n")
    return path, envelope


def write_records_jsonl(path: Path, records: Iterable[FragranceRecord]) -> None:
    lines = [canonical_json(record.as_dict()) for record in records]
    atomic_write_text(path, "".join(f"{line}\n" for line in lines))


def write_dicts_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    lines = [canonical_json(record) for record in records]
    atomic_write_text(path, "".join(f"{line}\n" for line in lines))


def read_records_jsonl(path: Path) -> list[FragranceRecord]:
    records: list[FragranceRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(FragranceRecord.from_dict(json.loads(line)))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise ValueError(f"{path}:{line_number}: registro inválido: {error}") from error
    return records


def read_olfactory_descriptors_jsonl(path: Path) -> list[OlfactoryDescriptorRecord]:
    records: list[OlfactoryDescriptorRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(OlfactoryDescriptorRecord.from_dict(json.loads(line)))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise ValueError(f"{path}:{line_number}: descritor olfativo inválido: {error}") from error
    return records


def write_olfactory_descriptors_jsonl(path: Path, records: Iterable[OlfactoryDescriptorRecord]) -> None:
    lines = [canonical_json(record.as_dict()) for record in records]
    atomic_write_text(path, "".join(f"{line}\n" for line in lines))


def read_semantic_claims_jsonl(path: Path) -> list[WikidataSemanticClaimRecord]:
    records: list[WikidataSemanticClaimRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(WikidataSemanticClaimRecord.from_dict(json.loads(line)))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise ValueError(f"{path}:{line_number}: claim semântico inválido: {error}") from error
    return records


def write_semantic_claims_jsonl(path: Path, records: Iterable[WikidataSemanticClaimRecord]) -> None:
    lines = [canonical_json(record.as_dict()) for record in records]
    atomic_write_text(path, "".join(f"{line}\n" for line in lines))
