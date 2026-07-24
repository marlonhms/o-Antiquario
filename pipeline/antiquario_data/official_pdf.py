from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable

from .io_utils import atomic_write_text, load_json, write_dicts_jsonl
from .models import canonical_json
from .term_resolver import TermResolver, normalize_term

import os
import time
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai_client = genai.Client(api_key=api_key)
    else:
        print("DEBUG_INIT: api_key is None! GEMINI_API_KEY not found in os.environ.")
        genai_client = None
except ImportError as e:
    print(f"DEBUG_INIT: ImportError when importing genai: {e}")
    genai_client = None
except Exception as e:
    print(f"DEBUG_INIT: Unexpected error during genai init: {e}")
    genai_client = None

EXTRACTOR_VERSION = "official-pdf-v2.0-text"


def normalize_text_key(text: str) -> str:
    """Normaliza texto para comparações conservadoras (sem acentos, minúsculo, sem pontuação extra)."""
    normalized = unicodedata.normalize("NFD", text)
    without_accents = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    cleaned = re.sub(r"[^\w\s]", " ", without_accents.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def hash_file(path: Path) -> str:
    """Calcula a hash SHA-256 de um arquivo local."""
    hasher = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class CatalogPage:
    page_number: int
    text: str
    text_length: int
    text_hash: str
    status: str  # "success" ou "no_text"

    def as_dict(self) -> dict[str, Any]:
        return {
            "page": self.page_number,
            "text_length": self.text_length,
            "text_hash": self.text_hash,
            "status": self.status,
        }


@dataclass
class CatalogClaim:
    document_hash: str
    source_id: str
    page: int
    field: str
    value: str
    extraction_method: str = "text-layer"
    confidence: str = "declared"
    review_status: str = "pending"

    def as_dict(self) -> dict[str, Any]:
        return {
            "document_hash": self.document_hash,
            "source_id": self.source_id,
            "page": self.page,
            "field": self.field,
            "value": self.value,
            "extraction_method": self.extraction_method,
            "confidence": self.confidence,
            "review_status": self.review_status,
        }


@dataclass
class ProductCandidate:
    candidate_id: str
    document_hash: str
    brand: str
    product_name: str
    line: str | None = None
    concentration: str | None = None
    volume: str | None = None
    launch_year: int | None = None
    declared_pyramid: dict[str, list[str]] = field(default_factory=lambda: {"top": [], "heart": [], "base": []})
    declared_notes_unlayered: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)
    matching_status: str = "pending"  # "matched", "pending", "ambiguous", "no_match"
    matched_wikidata_id: str | None = None
    product_type: str | None = None
    available_volumes: list[str] = field(default_factory=list)
    declared_accords: list[str] = field(default_factory=list)
    declared_materials: list[str] = field(default_factory=list)
    classification_score: int = 0
    classification_status: str = "needs_review"
    classification_reasons: list[str] = field(default_factory=list)
    curation_status: str = "needs_review"

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "document_hash": self.document_hash,
            "brand": self.brand,
            "product_name": self.product_name,
            "line": self.line,
            "concentration": self.concentration,
            "volume": self.volume,
            "launch_year": self.launch_year,
            "declared_pyramid": self.declared_pyramid,
            "declared_notes_unlayered": sorted(self.declared_notes_unlayered),
            "pages": sorted(list(set(self.pages))),
            "matching_status": self.matching_status,
            "matched_wikidata_id": self.matched_wikidata_id,
            "product_type": self.product_type,
            "available_volumes": sorted(set(self.available_volumes or ([self.volume] if self.volume else []))),
            "declared_accords": sorted(self.declared_accords),
            "declared_materials": sorted(self.declared_materials),
            "classification_score": self.classification_score,
            "classification_status": self.classification_status,
            "classification_reasons": self.classification_reasons,
            "curation_status": self.curation_status,
        }


@dataclass
class QuarantineItem:
    document_hash: str
    page: int
    issue_type: str  # "unknown_term", "ambiguous_match", "missing_layer", "parse_error"
    term_or_value: str
    context: str
    resolution: str = "pending"

    def as_dict(self) -> dict[str, Any]:
        return {
            "document_hash": self.document_hash,
            "page": self.page,
            "issue_type": self.issue_type,
            "term_or_value": self.term_or_value,
            "context": self.context,
            "resolution": self.resolution,
        }


def _extract_pdf_pages_legacy(pdf_path: Path) -> tuple[list[CatalogPage], str]:
    """Lê as páginas de um PDF usando pypdf e gera instâncias de CatalogPage."""
    try:
        import pypdf
    except ModuleNotFoundError as error:
        raise RuntimeError("Biblioteca 'pypdf' ausente no ambiente Python.") from error

    doc_hash = hash_file(pdf_path)
    reader = pypdf.PdfReader(str(pdf_path))
    pages: list[CatalogPage] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        stripped = text.strip()
        page_hash = sha256(text.encode("utf-8")).hexdigest()
        status = "success" if len(stripped) > 0 else "no_text"
        pages.append(
            CatalogPage(
                page_number=index,
                text=text,
                text_length=len(text),
                text_hash=page_hash,
                status=status,
            )
        )

    return pages, doc_hash


def _extract_pdf_pages_spatial(pdf_path: Path) -> tuple[list[CatalogPage], str]:
    """Leitor espacial opcional para diagnóstico de páginas difíceis; não executa OCR."""
    try:
        import logging
        import pdfplumber
        import pypdf
    except ModuleNotFoundError as error:
        raise RuntimeError("Biblioteca 'pdfplumber' ausente no ambiente Python.") from error

    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    logging.getLogger("pdfplumber").setLevel(logging.ERROR)
    doc_hash = hash_file(pdf_path)
    pages: list[CatalogPage] = []
    with pdfplumber.open(str(pdf_path)) as document:
        fallback_reader = pypdf.PdfReader(str(pdf_path))
        if not document.pages:
            for index, page in enumerate(fallback_reader.pages, start=1):
                text = page.extract_text() or ""
                pages.append(CatalogPage(
                    page_number=index,
                    text=text,
                    text_length=len(text),
                    text_hash=sha256(text.encode("utf-8")).hexdigest(),
                    status="success" if text.strip() else "no_text",
                ))
            return pages, doc_hash
        for index, page in enumerate(document.pages, start=1):
            text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
            if not text.strip() and index <= len(fallback_reader.pages):
                text = fallback_reader.pages[index - 1].extract_text() or ""
            stripped = text.strip()
            pages.append(CatalogPage(
                page_number=index,
                text=text,
                text_length=len(text),
                text_hash=sha256(text.encode("utf-8")).hexdigest(),
                status="success" if stripped else "no_text",
            ))
    return pages, doc_hash


def extract_pdf_pages(pdf_path: Path) -> tuple[list[CatalogPage], str]:
    """Leitor textual rápido usado na ingestão integral; não executa OCR."""
    try:
        import pypdf
    except ModuleNotFoundError as error:
        raise RuntimeError("Biblioteca 'pypdf' ausente no ambiente Python.") from error

    doc_hash = hash_file(pdf_path)
    pages: list[CatalogPage] = []
    reader = pypdf.PdfReader(str(pdf_path))
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(CatalogPage(
            page_number=index,
            text=text,
            text_length=len(text),
            text_hash=sha256(text.encode("utf-8")).hexdigest(),
            status="success" if text.strip() else "no_text",
        ))
    return pages, doc_hash


CONCENTRATION_PATTERNS = [
    r"desodorante colônia",
    r"desodorante colonia",
    r"extrait de parfum",
    r"eau de parfum",
    r"eau de toilette",
    r"deo parfum",
    r"body splash",
    r"colônia",
    r"colonia",
    r"parfum",
    r"splash",
]


NON_FRAGRANCE_KEYWORDS = [
    # Maquiagem / Beleza
    "batom", "gloss", "base", "mascara para cilios", "mascara", "delineador", "caneta delineadora",
    "blush", "po compacto", "corretivo", "esmalte", "maquiagem", "makeup", "pincel", "cobertura",

    # Capilar
    "shampoo", "xampu", "condicionador", "mascara capilar", "creme de pentear", "creme para pentear",
    "ampola", "serum capilar", "cabelos", "cabelo", "hair", "anticaspa", "tratamento capilar",

    # Cuidados corporais / Skincare / Antissinais
    "creme hidratante", "hidratante", "oleo corporal", "oleo trifasico", "protetor solar",
    "sabonete em barra", "sabonete liquido", "sabonete", "gel de banho", "antitranspirante",
    "roll on", "desodorante em creme", "creme para as maos", "creme para os pes", "creme desodorante",
    "cremes antissinais", "cuidados para o corpo", "pele hidratada", "efeito 2 vezes", "balm pos barba",

    # Embalagens, Presentes, Acessórios e Textos Comerciais
    "sacola", "embalagem", "caixa", "presente", "kit", "necessaire", "saboneteira", "acessorio",
    "pendure", "sacola de", "favorito", "novos", "refil", "spray de ambientes", "quer fazer um pedido",
    "ampola reparacao", "promove a uniao", "confira a colecao", "confira mais", "criacao exclusiva",
    "de r", "de-r-", "por r", "r$", "quaisquer comprados", "exale sofisticacao",

    # Descritores Genéricos sem Nome Específico de Linha/Produto
    "fragrancia amadeirada", "fragrancia floral", "fragrancia misteriosa", "fragrancia vibrante",
    "fragrancia luxuosa", "fragrancia que veio", "floral aldeidico", "adocicado intenso",
    "moderado intenso", "para mulheres apaixonadas", "nature crianca feliz"
]

GENERIC_DISCARD_NAMES = {
    "natura", "deo", "deo parfum", "desodorante", "desodorante colonia", "fragrancia", "intenso", "amora", "pitanga1", "cynthia"
}


def is_valid_fragrance_candidate(candidate: ProductCandidate) -> bool:
    norm_name = normalize_text_key(candidate.product_name)

    # Rejeita nomes vazios ou genéricos isolados
    if not norm_name or norm_name in GENERIC_DISCARD_NAMES:
        return False

    # Rejeita nomes que comecem com preços ("de r$ 107,90", "de-r-107-90")
    if re.match(r"^de\s*r\b", norm_name) or norm_name.startswith("de-r-"):
        return False

    # Rejeita se contiver palavra de não-perfumaria
    for kw in NON_FRAGRANCE_KEYWORDS:
        if kw in norm_name:
            return False

    # Exige presença de uma linha de perfumaria conhecida ou notas olfativas/pirâmide
    has_notes = bool(
        candidate.declared_pyramid.get("top")
        or candidate.declared_pyramid.get("heart")
        or candidate.declared_pyramid.get("base")
        or candidate.declared_notes_unlayered
    )
    has_fragrance_line = any(
        line in norm_name for line in [
            "essencial", "kaiak", "humor", "biografia", "luna", "ilia", "una",
            "ekos ryos", "ekos castanha", "ekos pitanga", "sr n", "k deo parfum", "tododia"
        ]
    )

    return has_notes or has_fragrance_line



def _parse_notes_string(notes_str: str) -> list[str]:
    """Separa uma string de notas por vírgulas, 'e', barras ou ponto e vírgula."""
    cleaned = re.sub(r"[\.\:]", "", notes_str)
    tokens = re.split(r",|\s+e\s+|/|;", cleaned, flags=re.IGNORECASE)
    results = []
    for token in tokens:
        item = token.strip()
        if item and len(item) > 1 and not re.match(r"^\d+$", item):
            results.append(item.lower())
    return results


def parse_page_content(
    page_number: int,
    text: str,
    doc_hash: str,
    brand_hint: str,
    source_id: str,
) -> tuple[list[ProductCandidate], list[CatalogClaim], list[QuarantineItem]]:
    """Extrai candidatos, claims e quarentena do texto de uma página."""
    candidates: list[ProductCandidate] = []
    claims: list[CatalogClaim] = []
    quarantine: list[QuarantineItem] = []

    if not text.strip():
        return candidates, claims, quarantine

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Busca por blocos de produto na página
    current_product: str | None = None
    current_line_name: str | None = None
    current_concentration: str | None = None
    current_volume: str | None = None
    current_year: int | None = None
    
    top_notes: list[str] = []
    heart_notes: list[str] = []
    base_notes: list[str] = []
    unlayered_notes: list[str] = []
    has_layered_structure = False

    for idx, line in enumerate(lines):
        norm = normalize_text_key(line)
        
        # Identificação de Nome de Produto / Perfume
        if re.search(r"^(perfume|fragrância|colônia|deo parfum|produto):\s*(.+)$", line, re.IGNORECASE):
            match = re.search(r"^(perfume|fragrância|colônia|deo parfum|produto):\s*(.+)$", line, re.IGNORECASE)
            if match:
                current_product = match.group(2).strip()
        elif idx == 0 and len(line) < 60 and not re.search(r"^(página|catalogo|ciclo|notas|topo|corpo|fundo)", norm):
            current_product = line.strip()

        # Linha
        if match := re.search(r"^(linha):\s*(.+)$", line, re.IGNORECASE):
            current_line_name = match.group(2).strip()

        # Concentração
        for conc in CONCENTRATION_PATTERNS:
            if re.search(r"\b" + re.escape(conc) + r"\b", line, re.IGNORECASE):
                current_concentration = conc.title()
                break

        # Volume
        if match := re.search(r"(\d+\s*ml)\b", line, re.IGNORECASE):
            current_volume = match.group(1).lower()

        # Ano
        if match := re.search(r"\b(19\d\d|20\d\d)\b", line):
            year = int(match.group(1))
            if 1900 <= year <= 2100:
                current_year = year

        # Pirâmide Olfativa - Topo / Saída
        if match := re.search(r"^(notas de topo|topo|saída|notas de saída):\s*(.+)$", line, re.IGNORECASE):
            has_layered_structure = True
            extracted = _parse_notes_string(match.group(2))
            top_notes.extend(extracted)
            for note in extracted:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "top_note", note))

        # Pirâmide Olfativa - Coração / Corpo
        elif match := re.search(r"^(notas de coração|coração|corpo|notas de corpo):\s*(.+)$", line, re.IGNORECASE):
            has_layered_structure = True
            extracted = _parse_notes_string(match.group(2))
            heart_notes.extend(extracted)
            for note in extracted:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "heart_note", note))

        # Pirâmide Olfativa - Fundo / Base
        elif match := re.search(r"^(notas de fundo|fundo|base|notas de base):\s*(.+)$", line, re.IGNORECASE):
            has_layered_structure = True
            extracted = _parse_notes_string(match.group(2))
            base_notes.extend(extracted)
            for note in extracted:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "base_note", note))

        # Lista de Notas Sem Camada
        elif match := re.search(r"^(notas olfativas|notas|ingredientes|família olfativa):\s*(.+)$", line, re.IGNORECASE):
            extracted = _parse_notes_string(match.group(2))
            unlayered_notes.extend(extracted)
            for note in extracted:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "declared_notes_unlayered", note))

    if current_product or top_notes or heart_notes or base_notes or unlayered_notes:
        prod_name = current_product if current_product else f"Produto Candidato Pág {page_number}"
        cand_id = f"pdf-{doc_hash[:8]}-p{page_number}-{normalize_text_key(prod_name).replace(' ', '-')[:20]}"
        
        pyramid = {
            "top": sorted(list(set(top_notes))),
            "heart": sorted(list(set(heart_notes))),
            "base": sorted(list(set(base_notes))),
        }
        
        candidate = ProductCandidate(
            candidate_id=cand_id,
            document_hash=doc_hash,
            brand=brand_hint,
            product_name=prod_name,
            line=current_line_name,
            concentration=current_concentration,
            volume=current_volume,
            launch_year=current_year,
            declared_pyramid=pyramid,
            declared_notes_unlayered=sorted(list(set(unlayered_notes))),
            pages=[page_number],
            matching_status="pending",
        )

        # Filtra rigorosamente apenas fragrâncias e perfumes
        if is_valid_fragrance_candidate(candidate):
            candidates.append(candidate)
            claims.append(CatalogClaim(doc_hash, source_id, page_number, "product_name", prod_name))
            claims.append(CatalogClaim(doc_hash, source_id, page_number, "brand", brand_hint))
            if current_concentration:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "concentration", current_concentration))
            if current_volume:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "volume", current_volume))
            if current_year:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "launch_year", str(current_year)))

    return candidates, claims, quarantine



FRAGRANCE_PRODUCT_TYPES = {
    "extrait de parfum": "extrait de parfum",
    "eau de parfum": "eau de parfum",
    "eau de toilette": "eau de toilette",
    "body splash desodorante colonia": "body splash",
    "body splash": "body splash",
    "desodorante colonia": "desodorante colônia",
    "deo parfum": "deo parfum",
    "parfum": "parfum",
    "colonia": "colônia",
}

_PRODUCT_TYPE_PATTERN = "|".join(
    re.escape(item) for item in sorted(FRAGRANCE_PRODUCT_TYPES, key=len, reverse=True)
)
FRAGRANCE_BLOCK_PATTERN = re.compile(
    rf"\b(?P<product_type>{_PRODUCT_TYPE_PATTERN})\b"
    rf"(?P<name>.{{0,90}}?)"
    rf"\b(?P<volume>\d{{2,3}}(?:[.,]\d+)?\s*ml)\b",
    re.IGNORECASE,
)

GENERIC_PRODUCT_TOKENS = {
    "", "deo", "parfum", "deo parfum", "colonia", "desodorante colonia",
    "masculino", "feminino", "unissex", "frescor", "fragrancia",
}

AMBIGUOUS_LINE_NAMES = {
    "natura essencial", "natura kaiak", "natura luna", "natura ilia",
    "natura una", "natura humor", "biografia", "essencial", "kaiak",
    "luna", "ilia", "una", "humor", "natura homem", "natura tododia",
    "aguas", "colonia humor",
}

HARD_NON_FRAGRANCE_NAMES = {
    "iluminador", "desodorante corporal", "desodorante corporal natura",
    "oleo perfumado", "oleo corporal", "creme perfumado", "balm pos barba",
    "corporal", "da natura", "natura", "desodorante perfumado",
}

OLFACTORY_WORDS = {
    "amadeirado", "ambarado", "aromatico", "aquatico", "citrico", "chipre",
    "especiado", "floral", "fougere", "frutal", "gourmand", "oriental",
    "adocicado", "verde", "almiscarado",
}

MATERIAL_VOCABULARY = {
    "acafrao", "ambar", "ameixa", "baunilha", "bergamota", "breu branco",
    "cacau", "cafe", "canela", "cardamomo", "cedro", "cereja negra",
    "copaiba", "cumaru", "flor do mel", "flor de laranjeira", "grapefruit",
    "iris", "ishpink", "jasmim", "lavanda", "lichia", "limao", "mandarina",
    "madeira de guaiaco", "madeiras nobres", "maracuja", "musk", "patchouli",
    "pimenta preta", "pimenta rosa", "praline", "priprioca", "rosa", "rosa alba",
    "sandalo", "tonka", "vetiver", "violeta", "ylang ylang",
}


def _clean_product_name(value: str) -> str:
    normalized = normalize_text_key(value)
    normalized = re.sub(r"^\d+\s*", "", normalized)
    normalized = re.sub(
        r"\b(?:masculino|feminino|unissex|lancamento|exclusivo|promocao|refil|novo)\d*\b",
        " ",
        normalized,
    )
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return " ".join(part.capitalize() for part in normalized.split())


def _is_distinct_name(value: str) -> bool:
    normalized = normalize_text_key(value)
    if normalized in GENERIC_PRODUCT_TOKENS or len(normalized) < 4:
        return False
    if normalized in HARD_NON_FRAGRANCE_NAMES:
        return False
    if len(normalized.split()) > 8:
        return False
    if re.search(r"\b\d{2,4}\s*g\b", normalized):
        return False
    embedded_product_types = (
        "deo parfum", "eau de parfum", "eau de toilette", "desodorante colonia",
        "body splash", "desodorante corporal", "oleo corporal", "creme corporal",
    )
    if any(product_type in normalized for product_type in embedded_product_types):
        return False
    tokens = normalized.split()
    if len(tokens) >= 4 and len(set(tokens)) / len(tokens) < 0.65:
        return False
    if any(keyword in normalized for keyword in NON_FRAGRANCE_KEYWORDS):
        return False
    if re.search(r"\b(?:r\$|economize|pts|pagina|catalogo|ciclo)\b", normalized):
        return False
    return any(char.isalpha() for char in normalized)


def _infer_page_product_name(lines: list[str], brand_hint: str) -> str | None:
    brand = normalize_text_key(brand_hint)
    perfume_lines = (
        "essencial", "kaiak", "humor", "biografia", "luna", "ilia", "una",
        "ekos", "tododia", "malbec", "egeo", "coffee", "floratta", "glamour",
    )
    ranked: list[tuple[int, int, str]] = []
    for position, raw_line in enumerate(lines[:35]):
        normalized = normalize_text_key(raw_line)
        if not 4 <= len(normalized) <= 70:
            continue
        if any(term in normalized for term in ("presente", "economize", "estoque", "edicao limitada", "fragrancia ")):
            continue
        has_brand = bool(brand and brand in normalized)
        has_line = any(term in normalized for term in perfume_lines)
        if not has_brand and not has_line:
            continue
        score = (4 if has_brand else 0) + (3 if has_line else 0) - min(position, 20)
        ranked.append((score, -position, _clean_product_name(raw_line)))
    if not ranked:
        return None
    ranked.sort(reverse=True)
    return ranked[0][2]


def _extract_explicit_notes(text: str) -> dict[str, list[str]]:
    pyramid = {"top": [], "heart": [], "base": [], "unlayered": []}
    labels = {
        "top": ("notas de topo", "topo", "notas de saida", "saida"),
        "heart": ("notas de coracao", "coracao", "notas de corpo", "corpo"),
        "base": ("notas de fundo", "fundo", "notas de base"),
        "unlayered": ("notas olfativas", "notas", "ingredientes"),
    }
    for raw_line in text.splitlines():
        if ":" not in raw_line:
            continue
        raw_label, raw_value = raw_line.split(":", 1)
        label = normalize_text_key(raw_label)
        for layer, layer_labels in labels.items():
            if label in layer_labels:
                pyramid[layer].extend(_parse_notes_string(raw_value))
                break
    return {key: sorted(set(values)) for key, values in pyramid.items()}


def _extract_notes_via_llm(text: str, candidate_names: list[str]) -> dict[str, dict[str, list[str]]]:
    if not genai_client:
        print("DEBUG: genai_client is None! LLM will not be called.")
        return {}
        
    print(f"DEBUG: Calling LLM for candidates: {candidate_names}")
        
    prompt = f"""
    You are an expert perfumery data extractor.
    I will provide you with the text of a catalog page. 
    There are some fragrances mentioned in this page, likely including: {', '.join(candidate_names)}.
    Extract the olfactory pyramid (top notes, heart/body notes, and base notes) and any unlayered notes for each fragrance you find.
    Return ONLY a valid JSON object matching this schema:
    {{
      "fragrances": [
        {{
          "name": "fragrance name as it appears in the text",
          "pyramid": {{
            "top": ["note 1", "note 2"],
            "heart": ["note 3"],
            "base": ["note 4"],
            "unlayered": []
          }}
        }}
      ]
    }}
    Return empty lists if a layer is not mentioned. Do not include markdown formatting like ```json.
    
    TEXT:
    {text}
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Rate limit preventivo: o plano gratuito permite apenas 15 RPM.
            # 60 segundos / 15 requisições = 4.0s por requisição.
            time.sleep(4.1)
            response = genai_client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            data = json.loads(response.text)
            print(f"DEBUG LLM Data: {json.dumps(data)}")
            
            results = {}
            for f in data.get("fragrances", []):
                name = normalize_text_key(f.get("name", ""))
                pyramid = f.get("pyramid", {})
                results[name] = {
                    "top": pyramid.get("top", []),
                    "heart": pyramid.get("heart", []),
                    "base": pyramid.get("base", []),
                    "unlayered": pyramid.get("unlayered", [])
                }
            return results
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < max_retries - 1:
                    print(f"Instabilidade ou limite de taxa na IA ({'503' if '503' in error_str else '429'}). Aguardando 15 segundos antes de tentar novamente... ({attempt + 1}/{max_retries})")
                    time.sleep(15)
                    continue
            print(f"Erro na extração via LLM: {e}")
            return {}
    return {}


def _extract_olfactory_terms(context: str) -> tuple[list[str], list[str]]:
    accords: list[str] = []
    materials: list[str] = []
    normalized = normalize_text_key(context)
    for first in OLFACTORY_WORDS:
        if re.search(rf"\b{re.escape(first)}\b", normalized):
            phrase_match = re.search(
                rf"\b({re.escape(first)}(?:\s+(?:intenso|leve|especiado|ambarado|floral|amadeirado|aquatico|aromatico))?)\b",
                normalized,
            )
            accords.append(phrase_match.group(1) if phrase_match else first)
    has_material_signal = any(
        signal in normalized
        for signal in ("notas", "combina", "encontro", "blend", "acorde", "fragrancia", "olfativo")
    )
    if has_material_signal:
        for material in MATERIAL_VOCABULARY:
            if re.search(rf"\b{re.escape(material)}\b", normalized):
                materials.append(material)
    return sorted(set(accords)), sorted(set(materials))


def parse_page_content(
    page_number: int,
    text: str,
    doc_hash: str,
    brand_hint: str,
    source_id: str,
) -> tuple[list[ProductCandidate], list[CatalogClaim], list[QuarantineItem]]:
    """Classifica blocos textuais de produto e extrai apenas fragrâncias explícitas."""
    if not text.strip():
        return [], [], []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    normalized_page = normalize_text_key(text)
    matches = list(FRAGRANCE_BLOCK_PATTERN.finditer(normalized_page))
    inferred_name = _infer_page_product_name(lines, brand_hint)
    explicit_notes = _extract_explicit_notes(text)
    
    candidates_in_page = [match.group("name").strip() for match in matches]
    if inferred_name:
        candidates_in_page.append(inferred_name)
    explicit_name_match = re.search(r"^(?:perfume|fragrância|fragrancia|produto):\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
    if explicit_name_match:
        candidates_in_page.append(explicit_name_match.group(1).strip())
        
    candidates_in_page = list(set([c for c in candidates_in_page if c]))
    
    has_explicit = bool(
        explicit_notes.get("top") or 
        explicit_notes.get("heart") or 
        explicit_notes.get("base") or 
        explicit_notes.get("unlayered")
    )
    
    if candidates_in_page and not has_explicit:
        llm_notes = _extract_notes_via_llm(text, candidates_in_page)
    else:
        llm_notes = {}
        
    candidates: list[ProductCandidate] = []
    claims: list[CatalogClaim] = []
    quarantine: list[QuarantineItem] = []
    seen: set[tuple[str, str, str]] = set()

    # Contrato explícito usado por catálogos simples e fixtures: "Perfume: Nome".
    # Ele continua válido mesmo quando o documento não informa volume.
    if not matches:
        explicit_name_match = re.search(
            r"^(?:perfume|fragrância|fragrancia|produto):\s*(.+)$",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        if explicit_name_match:
            product_name = explicit_name_match.group(1).strip()
            normalized_name = normalize_text_key(product_name)
            concentration_match = re.search(_PRODUCT_TYPE_PATTERN, normalized_page, re.IGNORECASE)
            concentration = (
                FRAGRANCE_PRODUCT_TYPES[normalize_text_key(concentration_match.group(0))].title()
                if concentration_match else None
            )
            volume_match = re.search(r"\b\d{2,3}(?:[.,]\d+)?\s*ml\b", normalized_page)
            volume = volume_match.group(0) if volume_match else None
            accords, materials = _extract_olfactory_terms(normalized_page)
            
            llm_match = None
            for llm_name, llm_pyr in llm_notes.items():
                if llm_name in normalized_name or normalized_name in llm_name:
                    llm_match = llm_pyr
                    break
                    
            if llm_match:
                pyramid = {
                    "top": llm_match.get("top", []),
                    "heart": llm_match.get("heart", []),
                    "base": llm_match.get("base", []),
                }
                unlayered = llm_match.get("unlayered", [])
            else:
                pyramid = {
                    "top": explicit_notes["top"],
                    "heart": explicit_notes["heart"],
                    "base": explicit_notes["base"],
                }
                unlayered = explicit_notes["unlayered"]
            
            candidate = ProductCandidate(
                candidate_id=f"pdf-{doc_hash[:8]}-p{page_number}-{normalized_name.replace(' ', '-')[:28]}",
                document_hash=doc_hash,
                brand=brand_hint,
                product_name=product_name,
                concentration=concentration,
                volume=volume,
                declared_pyramid=pyramid,
                declared_notes_unlayered=unlayered,
                pages=[page_number],
                product_type="perfume",
                declared_accords=accords,
                declared_materials=materials,
                classification_score=10,
                classification_status="accepted",
                classification_reasons=["produto rotulado explicitamente como perfume", "estrutura factual declarada"],
                curation_status="auto_approved",
            )
            candidates.append(candidate)
            for field_name, value in (("product_name", product_name), ("brand", brand_hint), ("product_type", "perfume")):
                claims.append(CatalogClaim(doc_hash, source_id, page_number, field_name, value, review_status="auto_approved"))
            for layer, field_name in (("top", "top_note"), ("heart", "heart_note"), ("base", "base_note")):
                for note in pyramid[layer]:
                    claims.append(CatalogClaim(doc_hash, source_id, page_number, field_name, note, review_status="auto_approved"))
            for note in explicit_notes["unlayered"]:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, "declared_notes_unlayered", note, review_status="auto_approved"))
            return candidates, claims, quarantine

    for index, match in enumerate(matches):
        raw_type = normalize_text_key(match.group("product_type"))
        product_type = FRAGRANCE_PRODUCT_TYPES[raw_type]
        product_name = _clean_product_name(match.group("name"))
        volume = re.sub(r"\s+", " ", match.group("volume")).lower()
        reasons = ["tipo de fragrância explícito", "volume declarado"]
        score = 6

        if _is_distinct_name(product_name):
            reasons.append("nome de produto distintivo")
            score += 2
        else:
            product_name = inferred_name or product_name
            if inferred_name:
                reasons.append("nome recuperado do título da página")
                score += 2

        if not _is_distinct_name(product_name):
            quarantine.append(QuarantineItem(
                document_hash=doc_hash,
                page=page_number,
                issue_type="ambiguous_product_name",
                term_or_value=product_name or product_type,
                context=f"Bloco de {product_type} com volume {volume}, mas sem nome distintivo.",
            ))
            continue

        normalized_name = normalize_text_key(product_name)
        next_start = matches[index + 1].start() if index + 1 < len(matches) else min(len(normalized_page), match.end() + 520)
        context = normalized_page[max(0, match.start() - 180):next_start]
        accords, materials = _extract_olfactory_terms(context)
        if accords:
            reasons.append("perfil olfativo declarado")
            score += 1
        if materials:
            reasons.append("matérias-primas reconhecidas")
            score += 1

        ambiguous_line = normalized_name in AMBIGUOUS_LINE_NAMES
        status = "accepted" if score >= 8 and not ambiguous_line else "needs_review"
        curation_status = "auto_approved" if status == "accepted" else "needs_review"
        if ambiguous_line:
            reasons.append("nome corresponde apenas à linha ou família comercial")

        key = (normalized_name, product_type, volume)
        if key in seen:
            continue
        seen.add(key)

        pyramid = {"top": [], "heart": [], "base": []}
        unlayered: list[str] = []
        
        llm_match = None
        for llm_name, llm_pyr in llm_notes.items():
            if llm_name in normalized_name or normalized_name in llm_name:
                llm_match = llm_pyr
                break
                
        if llm_match:
            pyramid = {
                "top": llm_match.get("top", []),
                "heart": llm_match.get("heart", []),
                "base": llm_match.get("base", []),
            }
            unlayered = llm_match.get("unlayered", [])
        elif len(matches) == 1:
            pyramid = {
                "top": explicit_notes["top"],
                "heart": explicit_notes["heart"],
                "base": explicit_notes["base"],
            }
            unlayered = explicit_notes["unlayered"]

        candidate_id = f"pdf-{doc_hash[:8]}-p{page_number}-{normalized_name.replace(' ', '-')[:28]}"
        candidate = ProductCandidate(
            candidate_id=candidate_id,
            document_hash=doc_hash,
            brand=brand_hint,
            product_name=product_name,
            concentration=product_type.title(),
            volume=volume,
            declared_pyramid=pyramid,
            declared_notes_unlayered=unlayered,
            pages=[page_number],
            product_type=product_type,
            available_volumes=[volume],
            declared_accords=accords,
            declared_materials=materials,
            classification_score=score,
            classification_status=status,
            classification_reasons=reasons,
            curation_status=curation_status,
        )
        candidates.append(candidate)

        review_status = "auto_approved" if curation_status == "auto_approved" else "pending"
        base_claims = [
            ("product_name", product_name),
            ("brand", brand_hint),
            ("product_type", product_type),
            ("concentration", product_type),
            ("volume", volume),
        ]
        for field_name, value in base_claims:
            claims.append(CatalogClaim(doc_hash, source_id, page_number, field_name, value, review_status=review_status))
        for layer, field_name in (("top", "top_note"), ("heart", "heart_note"), ("base", "base_note")):
            for note in pyramid[layer]:
                claims.append(CatalogClaim(doc_hash, source_id, page_number, field_name, note, review_status=review_status))
        for note in unlayered:
            claims.append(CatalogClaim(doc_hash, source_id, page_number, "declared_notes_unlayered", note, review_status=review_status))
        for accord in accords:
            claims.append(CatalogClaim(doc_hash, source_id, page_number, "declared_accord", accord, review_status=review_status))
        for material in materials:
            claims.append(CatalogClaim(doc_hash, source_id, page_number, "declared_material", material, review_status=review_status))

        if status == "needs_review":
            quarantine.append(QuarantineItem(
                document_hash=doc_hash,
                page=page_number,
                issue_type="uncertain_fragrance_identity",
                term_or_value=product_name,
                context="; ".join(reasons),
            ))

    return candidates, claims, quarantine


def _merge_repeated_candidates(candidates: list[ProductCandidate]) -> list[ProductCandidate]:
    """Une a mesma fragrância repetida em kits, promoções e páginas do catálogo."""
    merged: dict[tuple[str, str], ProductCandidate] = {}
    for candidate in candidates:
        key = (normalize_text_key(candidate.product_name), candidate.product_type or "")
        current = merged.get(key)
        if current is None:
            candidate.available_volumes = sorted(set(candidate.available_volumes or ([candidate.volume] if candidate.volume else [])))
            merged[key] = candidate
            continue
        current.pages = sorted(set(current.pages + candidate.pages))
        current.available_volumes = sorted(set(
            current.available_volumes
            + candidate.available_volumes
            + ([current.volume] if current.volume else [])
            + ([candidate.volume] if candidate.volume else [])
        ))
        for layer in ("top", "heart", "base"):
            current.declared_pyramid[layer] = sorted(set(
                current.declared_pyramid.get(layer, []) + candidate.declared_pyramid.get(layer, [])
            ))
        current.declared_notes_unlayered = sorted(set(
            current.declared_notes_unlayered + candidate.declared_notes_unlayered
        ))
        current.declared_accords = sorted(set(current.declared_accords + candidate.declared_accords))
        current.declared_materials = sorted(set(current.declared_materials + candidate.declared_materials))
        current.classification_score = max(current.classification_score, candidate.classification_score)
        current.classification_reasons = sorted(set(current.classification_reasons + candidate.classification_reasons))
        if candidate.curation_status == "auto_approved":
            current.classification_status = "accepted"
            current.curation_status = "auto_approved"
    return sorted(merged.values(), key=lambda item: (normalize_text_key(item.product_name), item.product_type or ""))


def match_candidates_against_catalog(
    candidates: list[ProductCandidate],
    quarantine: list[QuarantineItem],
    data_directory: Path,
) -> None:
    """Faz matching conservador de candidatos com o catálogo factual existente em DuckDB ou JSONL de staging."""
    duckdb_path = data_directory / "catalog" / "catalog.duckdb"
    staging_jsonl = data_directory / "staging" / "wikidata" / "fragrances.jsonl"

    db_records: list[dict[str, Any]] = []

    if duckdb_path.exists():
        try:
            import duckdb
            conn = duckdb.connect(str(duckdb_path), read_only=True)
            rows = conn.execute("""
                SELECT f.wikidata_id, f.name, b.label as brand_label
                FROM fragrances f
                LEFT JOIN fragrance_brands b ON f.id = b.fragrance_id
            """).fetchall()
            conn.close()
            for w_id, name, b_label in rows:
                db_records.append({
                    "wikidata_id": w_id,
                    "name": name,
                    "brand": b_label or "",
                })
        except Exception:
            db_records = []

    if not db_records and staging_jsonl.exists():
        try:
            with staging_jsonl.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    brand_name = rec["brands"][0]["label"] if rec.get("brands") else ""
                    db_records.append({
                        "wikidata_id": rec["wikidata_id"],
                        "name": rec["name"],
                        "brand": brand_name,
                    })
        except Exception:
            db_records = []

    if not db_records:
        return

    for candidate in candidates:
        cand_norm_name = normalize_text_key(candidate.product_name)
        cand_norm_brand = normalize_text_key(candidate.brand)

        matches = []
        for record in db_records:
            rec_norm_name = normalize_text_key(record["name"])
            rec_norm_brand = normalize_text_key(record["brand"])

            if cand_norm_name == rec_norm_name and (not cand_norm_brand or cand_norm_brand == rec_norm_brand):
                matches.append(record)

        if len(matches) == 1:
            candidate.matching_status = "matched"
            candidate.matched_wikidata_id = matches[0]["wikidata_id"]
        elif len(matches) > 1:
            candidate.matching_status = "ambiguous"
            quarantine.append(
                QuarantineItem(
                    document_hash=candidate.document_hash,
                    page=candidate.pages[0] if candidate.pages else 1,
                    issue_type="ambiguous_match",
                    term_or_value=candidate.product_name,
                    context=f"Múltiplos registros correspondem a '{candidate.product_name}': {[m['wikidata_id'] for m in matches]}",
                    resolution="pending",
                )
            )
        else:
            candidate.matching_status = "pending"


def _format_target(res_id: str) -> str:
    if res_id.startswith("note:"):
        return f"antiquario:olfactory-note:{res_id[5:]}"
    if res_id.startswith("accord:"):
        return f"antiquario:accord:{res_id[7:]}"
    if res_id.startswith("family:"):
        return f"antiquario:family:{res_id[7:]}"
    return f"antiquario:concentration:{normalize_text_key(res_id).replace(' ', '-')}"


def render_pdf_inbox_draft(
    candidate: ProductCandidate,
    brand: str,
    edition: str,
    source_id: str,
    doc_hash: str,
    processed_at: str,
    resolver: TermResolver,
    quarantine: list[QuarantineItem],
) -> tuple[str, str]:
    slug = normalize_text_key(candidate.product_name).replace(" ", "-")[:30]
    filename = f"{slug}-{doc_hash[:8]}.md"
    cand_id = f"antiquario:fragrance:pdf-{slug}-{doc_hash[:8]}"
    date_iso = processed_at[:10]

    relations: list[dict[str, str]] = []

    top_links = []
    for note_str in candidate.declared_pyramid.get("top", []):
        res = resolver.resolve_note(note_str, brand=brand)
        if res:
            relations.append({"predicate": "has-top-note", "target": _format_target(res.canonical_id)})
            top_links.append(f"[[note-{res.canonical_id.replace('note:', '')}]]")
        else:
            quarantine.append(
                QuarantineItem(
                    document_hash=doc_hash,
                    page=candidate.pages[0] if candidate.pages else 1,
                    issue_type="unknown_term",
                    term_or_value=note_str,
                    context=f"Nota de topo desconhecida: '{note_str}'",
                    resolution="pending",
                )
            )

    heart_links = []
    for note_str in candidate.declared_pyramid.get("heart", []):
        res = resolver.resolve_note(note_str, brand=brand)
        if res:
            relations.append({"predicate": "has-heart-note", "target": _format_target(res.canonical_id)})
            heart_links.append(f"[[note-{res.canonical_id.replace('note:', '')}]]")
        else:
            quarantine.append(
                QuarantineItem(
                    document_hash=doc_hash,
                    page=candidate.pages[0] if candidate.pages else 1,
                    issue_type="unknown_term",
                    term_or_value=note_str,
                    context=f"Nota de corpo desconhecida: '{note_str}'",
                    resolution="pending",
                )
            )

    base_links = []
    for note_str in candidate.declared_pyramid.get("base", []):
        res = resolver.resolve_note(note_str, brand=brand)
        if res:
            relations.append({"predicate": "has-base-note", "target": _format_target(res.canonical_id)})
            base_links.append(f"[[note-{res.canonical_id.replace('note:', '')}]]")
        else:
            quarantine.append(
                QuarantineItem(
                    document_hash=doc_hash,
                    page=candidate.pages[0] if candidate.pages else 1,
                    issue_type="unknown_term",
                    term_or_value=note_str,
                    context=f"Nota de fundo desconhecida: '{note_str}'",
                    resolution="pending",
                )
            )

    unlayered_links = []
    all_unlayered_terms = list(dict.fromkeys(list(candidate.declared_notes_unlayered) + list(candidate.declared_materials)))
    for note_str in all_unlayered_terms:
        res = resolver.resolve_note(note_str, brand=brand)
        if res:
            relations.append({"predicate": "has-note", "target": _format_target(res.canonical_id)})
            unlayered_links.append(f"[[note-{res.canonical_id.replace('note:', '')}]]")
        else:
            quarantine.append(
                QuarantineItem(
                    document_hash=doc_hash,
                    page=candidate.pages[0] if candidate.pages else 1,
                    issue_type="unknown_term",
                    term_or_value=note_str,
                    context=f"Nota sem camada desconhecida: '{note_str}'",
                    resolution="pending",
                )
            )

    title = candidate.product_name
    pages_str = ", ".join(str(p) for p in candidate.pages) if candidate.pages else "1"

    rel_lines = []
    for rel in relations:
        rel_lines.append(f"  - predicate: {rel['predicate']}\n    target: {rel['target']}")
    rel_yaml = "\n".join(rel_lines) if rel_lines else " []"

    summary_str = f"Rascunho factual extraído do catálogo oficial em PDF {brand} ({edition}). Fatos declarados de produto."

    content = f"""---
schema_version: 1
id: {cand_id}
project: o-antiquario
type: fragrance
title: {json.dumps(title, ensure_ascii=False)}
aliases: []
external_ids: {{}}
tags: [perfume, curadoria-oficial-pdf, rascunho]
source_ids: [{source_id}]
license: CC0-1.0
confidence: medium
review_status: draft
updated_at: {date_iso}
language: pt-BR
summary: {json.dumps(summary_str, ensure_ascii=False)}
evidence:
  - source_id: {source_id}
    kind: manufacturer
    license: CC0-1.0
    confidence: medium
    claim_scope: "Fatos olfativos e metadados declarados em catálogo oficial."
    retrieved_at: {date_iso}
relations:
{rel_yaml}
---

# {title}

## Base factual do catálogo

- Marca: {brand}
- Linha: {candidate.line or "não declarada"}
- Concentração: {candidate.concentration or "não declarada"}
- Volume: {candidate.volume or "não declarado"}
- Página(s): {pages_str}
- Hash do documento: `{doc_hash}`

## Pirâmide Olfativa Extraída

- **Saída:** {', '.join(top_links) if top_links else 'N/A'}
- **Coração:** {', '.join(heart_links) if heart_links else 'N/A'}
- **Fundo:** {', '.join(base_links) if base_links else 'N/A'}
- **Outras Notas (Sem Camada):** {', '.join(unlayered_links) if unlayered_links else 'N/A'}

## Enriquecimento editorial pendente

- [ ] Confirmar identidade e acurácia dos fatos declarados.
- [ ] Mover para `10_Perfumes` após revisão humana.
"""
    return filename, content



def process_official_pdf(
    pdf_path: Path,
    brand: str,
    edition: str,
    source_id: str,
    data_directory: Path,
    dry_run: bool = False,
    generate_inbox: bool = False,
) -> dict[str, Any]:
    """Processa um PDF oficial e grava os artefatos de staging e rascunhos no Obsidian."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

    pages, doc_hash = extract_pdf_pages(pdf_path)

    all_candidates: list[ProductCandidate] = []
    all_claims: list[CatalogClaim] = []
    all_quarantine: list[QuarantineItem] = []

    for page in pages:
        cands, claims, quars = parse_page_content(
            page_number=page.page_number,
            text=page.text,
            doc_hash=doc_hash,
            brand_hint=brand,
            source_id=source_id,
        )
        all_candidates.extend(cands)
        all_claims.extend(claims)
        all_quarantine.extend(quars)

    all_candidates = _merge_repeated_candidates(all_candidates)

    # Matching conservador contra o catálogo factual
    match_candidates_against_catalog(all_candidates, all_quarantine, data_directory)

    # Resolução de termos e geração de rascunhos de curadoria
    resolver = TermResolver(data_directory)
    now_iso = datetime.now(timezone.utc).isoformat()
    inbox_dir = data_directory.parent / "knowledge" / "vault" / "00_Inbox" / "Curadoria-Oficial-PDF"
    created_inbox_files: list[str] = []

    for cand in all_candidates:
        if cand.curation_status == "auto_approved":
            continue
        fn, content = render_pdf_inbox_draft(
            candidate=cand,
            brand=brand,
            edition=edition,
            source_id=source_id,
            doc_hash=doc_hash,
            processed_at=now_iso,
            resolver=resolver,
            quarantine=all_quarantine,
        )
        if generate_inbox and not dry_run:
            inbox_dir.mkdir(parents=True, exist_ok=True)
            target_file = inbox_dir / fn
            atomic_write_text(target_file, content)
            created_inbox_files.append(str(target_file))

    matched_count = sum(1 for c in all_candidates if c.matching_status == "matched")
    pending_count = sum(1 for c in all_candidates if c.matching_status in ("pending", "ambiguous"))
    auto_curated = [c for c in all_candidates if c.curation_status == "auto_approved"]
    needs_review = [c for c in all_candidates if c.curation_status == "needs_review"]

    document_meta = {
        "schema_version": 1,
        "document_hash": doc_hash,
        "source_id": source_id,
        "brand": brand,
        "edition": edition,
        "input_path": str(pdf_path),
        "extractor_version": EXTRACTOR_VERSION,
        "processed_at": now_iso,
        "pages_total": len(pages),
    }

    report = {
        "document_hash": doc_hash,
        "brand": brand,
        "edition": edition,
        "pages_total": len(pages),
        "pages_with_text": sum(1 for p in pages if p.status == "success"),
        "candidates_count": len(all_candidates),
        "claims_count": len(all_claims),
        "quarantine_count": len(all_quarantine),
        "matched_candidates": matched_count,
        "pending_candidates": pending_count,
        "auto_curated_candidates": len(auto_curated),
        "needs_review_candidates": len(needs_review),
        "candidates_with_layered_notes": sum(
            1 for candidate in all_candidates
            if any(candidate.declared_pyramid.get(layer) for layer in ("top", "heart", "base"))
        ),
        "candidates_with_unlayered_notes": sum(
            1 for candidate in all_candidates if candidate.declared_notes_unlayered
        ),
        "candidates_with_accords": sum(1 for candidate in all_candidates if candidate.declared_accords),
        "candidates_with_materials": sum(1 for candidate in all_candidates if candidate.declared_materials),
        "inbox_drafts_created": len(created_inbox_files),
    }

    staging_dir = data_directory / "staging" / "official-pdf" / doc_hash

    if not dry_run:
        staging_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_text(
            staging_dir / "document.json",
            f"{json.dumps(document_meta, ensure_ascii=False, indent=2)}\n",
        )
        write_dicts_jsonl(staging_dir / "pages.jsonl", [p.as_dict() for p in pages])
        write_dicts_jsonl(staging_dir / "claims.jsonl", [c.as_dict() for c in all_claims])
        write_dicts_jsonl(staging_dir / "candidates.jsonl", [c.as_dict() for c in all_candidates])
        write_dicts_jsonl(staging_dir / "auto-curated-candidates.jsonl", [c.as_dict() for c in auto_curated])
        write_dicts_jsonl(staging_dir / "quarantine.jsonl", [q.as_dict() for q in all_quarantine])
        atomic_write_text(
            staging_dir / "report.json",
            f"{json.dumps(report, ensure_ascii=False, indent=2)}\n",
        )

    return {
        "document": document_meta,
        "report": report,
        "staging_directory": str(staging_dir),
        "inbox_files": created_inbox_files,
        "preview": {
            "auto_curated": [c.product_name for c in auto_curated[:25]],
            "needs_review": [c.product_name for c in needs_review[:25]],
            "quarantine": [
                {"page": item.page, "issue": item.issue_type, "value": item.term_or_value}
                for item in all_quarantine[:25]
            ],
        },
    }
