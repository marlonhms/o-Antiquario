from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata
from typing import Any

from .io_utils import load_json


def normalize_term(value: str) -> str:
    """Normaliza um termo olfativo para comparação sem acentos e minúsculas."""
    normalized = unicodedata.normalize("NFD", value)
    without_accents = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    cleaned = re.sub(r"[^\w\s]", " ", without_accents.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


@dataclass(frozen=True)
class ResolvedTerm:
    canonical_id: str
    kind: str  # "note" | "family" | "accord"
    label_pt: str
    match_source: str  # "canonical_id" | "canonical_pt" | "canonical_alias" | "source_alias"


class TermResolver:
    def __init__(self, data_directory: Path) -> None:
        self.data_directory = data_directory
        self.notes_index: dict[str, ResolvedTerm] = {}
        self.families_index: dict[str, ResolvedTerm] = {}
        self.accords_index: dict[str, ResolvedTerm] = {}
        self.source_aliases: dict[str, dict[str, dict[str, str]]] = {}
        self._load_indexes()

    def _load_indexes(self) -> None:
        taxonomy_yml = self.data_directory / "taxonomy" / "taxonomy.yml"
        if not taxonomy_yml.exists():
            taxonomy_yml = Path.cwd() / "data" / "taxonomy" / "taxonomy.yml"

        source_aliases_yml = self.data_directory / "taxonomy" / "source-aliases.yml"
        if not source_aliases_yml.exists():
            source_aliases_yml = Path.cwd() / "data" / "taxonomy" / "source-aliases.yml"

        try:
            import yaml
        except ModuleNotFoundError as error:
            raise RuntimeError("Biblioteca 'pyyaml' ausente no ambiente Python.") from error


        if taxonomy_yml.exists():
            with taxonomy_yml.open("r", encoding="utf-8") as handle:
                tax_data = yaml.safe_load(handle) or {}

            for fam in tax_data.get("families", []):
                res = ResolvedTerm(
                    canonical_id=f"family:{fam['id']}",
                    kind="family",
                    label_pt=fam.get("pt", fam["id"]),
                    match_source="canonical_id",
                )
                self.families_index[normalize_term(fam["id"])] = res
                self.families_index[normalize_term(fam["pt"])] = res
                if "en" in fam:
                    self.families_index[normalize_term(fam["en"])] = res

            for acc in tax_data.get("accords", []):
                res = ResolvedTerm(
                    canonical_id=f"accord:{acc['id']}",
                    kind="accord",
                    label_pt=acc.get("pt", acc["id"]),
                    match_source="canonical_id",
                )
                self.accords_index[normalize_term(acc["id"])] = res
                self.accords_index[normalize_term(acc["pt"])] = res
                if "en" in acc:
                    self.accords_index[normalize_term(acc["en"])] = res
                for alias in acc.get("aliases", []):
                    self.accords_index[normalize_term(alias)] = res

            for note in tax_data.get("notes", []):
                res = ResolvedTerm(
                    canonical_id=f"note:{note['id']}",
                    kind="note",
                    label_pt=note.get("pt", note["id"]),
                    match_source="canonical_id",
                )
                self.notes_index[normalize_term(note["id"])] = res
                self.notes_index[normalize_term(note["pt"])] = res
                if "en" in note:
                    self.notes_index[normalize_term(note["en"])] = res
                for alias in note.get("aliases", []):
                    self.notes_index[normalize_term(alias)] = res

        # Indexar todas as notas existentes no Vault (ex: 30_Parfumo_Dataset/note-*.md)
        vault_dir = Path.cwd() / "knowledge" / "vault"
        if vault_dir.exists():
            for note_path in vault_dir.glob("**/note-*.md"):
                slug = note_path.stem[5:]
                res = ResolvedTerm(
                    canonical_id=f"note:{slug}",
                    kind="note",
                    label_pt=slug.replace("-", " "),
                    match_source="vault_file",
                )
                norm_slug = normalize_term(slug)
                if norm_slug not in self.notes_index:
                    self.notes_index[norm_slug] = res
                norm_label = normalize_term(slug.replace("-", " "))
                if norm_label not in self.notes_index:
                    self.notes_index[norm_label] = res

        if source_aliases_yml.exists():
            with source_aliases_yml.open("r", encoding="utf-8") as handle:
                alias_data = yaml.safe_load(handle) or {}
                self.source_aliases = alias_data.get("sources", {})

    def resolve_note(self, term: str, brand: str | None = None) -> ResolvedTerm | None:
        """Resolve um termo de nota para um ID canônico ou None se desconhecido."""
        norm = normalize_term(term)
        if not norm:
            return None

        # 1. Verifica busca exata ou alias na taxonomia canônica e vault
        if norm in self.notes_index:
            return self.notes_index[norm]

        # 2. Verifica aliases por marca/fonte
        if brand:
            brand_key = normalize_term(brand).replace(" ", "_")
            brand_map = self.source_aliases.get(brand_key, {}).get("notes", {})
            if norm in brand_map:
                target_id = brand_map[norm]
                canonical_norm = normalize_term(target_id)
                matched = self.notes_index.get(canonical_norm) or self.notes_index.get(
                    normalize_term(target_id.replace("-", " "))
                )
                if matched:
                    return ResolvedTerm(
                        canonical_id=matched.canonical_id,
                        kind=matched.kind,
                        label_pt=matched.label_pt,
                        match_source="source_alias",
                    )
                return None

        # 3. Verifica todas as fontes de aliases genéricos
        for b_name, b_data in self.source_aliases.items():
            b_notes = b_data.get("notes", {})
            if norm in b_notes:
                target_id = b_notes[norm]
                canonical_norm = normalize_term(target_id)
                matched = self.notes_index.get(canonical_norm) or self.notes_index.get(
                    normalize_term(target_id.replace("-", " "))
                )
                if matched:
                    return ResolvedTerm(
                        canonical_id=matched.canonical_id,
                        kind=matched.kind,
                        label_pt=matched.label_pt,
                        match_source="source_alias",
                    )
                return None

        return None

    def resolve_family(self, term: str) -> ResolvedTerm | None:
        """Resolve um termo de família olfativa para um ID canônico."""
        norm = normalize_term(term)
        return self.families_index.get(norm)
