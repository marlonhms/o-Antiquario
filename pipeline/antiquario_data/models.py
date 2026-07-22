from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Any


QID_PATTERN = re.compile(r"^Q[1-9][0-9]*$")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, order=True)
class EntityReference:
    wikidata_id: str
    label: str

    def __post_init__(self) -> None:
        if not QID_PATTERN.fullmatch(self.wikidata_id):
            raise ValueError(f"Wikidata ID inválido: {self.wikidata_id}")
        if not self.label.strip():
            raise ValueError("Rótulo de entidade não pode ser vazio")

    def as_dict(self) -> dict[str, str]:
        return {"wikidata_id": self.wikidata_id, "label": self.label}


@dataclass(frozen=True)
class Provenance:
    source_id: str
    source_url: str
    license: str
    retrieved_at: str
    snapshot_id: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "source_url": self.source_url,
            "license": self.license,
            "retrieved_at": self.retrieved_at,
            "snapshot_id": self.snapshot_id,
        }


@dataclass(frozen=True)
class FragranceRecord:
    id: str
    wikidata_id: str
    name: str
    name_language: str
    launch_year: int | None
    official_website: str | None
    brands: tuple[EntityReference, ...]
    perfumers: tuple[EntityReference, ...]
    countries: tuple[EntityReference, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        if not re.fullmatch(r"wd-q[1-9][0-9]*", self.id):
            raise ValueError(f"ID canônico inválido: {self.id}")
        if not QID_PATTERN.fullmatch(self.wikidata_id):
            raise ValueError(f"Wikidata ID inválido: {self.wikidata_id}")
        if not self.name.strip():
            raise ValueError("Nome da fragrância não pode ser vazio")
        if self.launch_year is not None and not 1000 <= self.launch_year <= 2100:
            raise ValueError(f"Ano fora da faixa operacional: {self.launch_year}")

    def core_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "wikidata_id": self.wikidata_id,
            "name": self.name,
            "name_language": self.name_language,
            "launch_year": self.launch_year,
            "official_website": self.official_website,
            "brands": [item.as_dict() for item in self.brands],
            "perfumers": [item.as_dict() for item in self.perfumers],
            "countries": [item.as_dict() for item in self.countries],
            "provenance": self.provenance.as_dict(),
        }

    @property
    def record_hash(self) -> str:
        return sha256(canonical_json(self.core_dict()).encode("utf-8")).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return {**self.core_dict(), "record_hash": self.record_hash}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> FragranceRecord:
        provenance = value["provenance"]
        return cls(
            id=value["id"],
            wikidata_id=value["wikidata_id"],
            name=value["name"],
            name_language=value["name_language"],
            launch_year=value.get("launch_year"),
            official_website=value.get("official_website"),
            brands=tuple(EntityReference(**item) for item in value.get("brands", [])),
            perfumers=tuple(EntityReference(**item) for item in value.get("perfumers", [])),
            countries=tuple(EntityReference(**item) for item in value.get("countries", [])),
            provenance=Provenance(**provenance),
        )


@dataclass(frozen=True, order=True)
class OlfactoryDescriptorRecord:
    """Uma relação factual Wikidata ``perfume → cheira a → entidade``.

    Não equivale a uma nota declarada pelo fabricante e não contém a camada da
    pirâmide. Essa separação impede que o catálogo transforme um descritor em
    uma afirmação editorial mais forte do que a fonte permite.
    """

    fragrance_wikidata_id: str
    descriptor: EntityReference
    provenance: Provenance

    def __post_init__(self) -> None:
        if not QID_PATTERN.fullmatch(self.fragrance_wikidata_id):
            raise ValueError(f"Wikidata ID inválido: {self.fragrance_wikidata_id}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "fragrance_wikidata_id": self.fragrance_wikidata_id,
            "descriptor": self.descriptor.as_dict(),
            "provenance": self.provenance.as_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> OlfactoryDescriptorRecord:
        return cls(
            fragrance_wikidata_id=value["fragrance_wikidata_id"],
            descriptor=EntityReference(**value["descriptor"]),
            provenance=Provenance(**value["provenance"]),
        )
