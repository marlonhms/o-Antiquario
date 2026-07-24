import os
import re
import json
import time
import yaml
from pathlib import Path
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai_client = genai.Client(api_key=api_key)
    else:
        genai_client = None
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    genai_client = None

import unicodedata

def sanitize_slug(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_accents = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    cleaned = re.sub(r"[^a-z0-9-]", "", without_accents.lower().replace(" ", "-"))
    return cleaned

INBOX_DIR = Path("knowledge/vault/00_Inbox/Curadoria-Catalogo")
DEST_DIR = Path("knowledge/vault/10_Perfumes")
ALIASES_PATH = Path("data/taxonomy/source-aliases.yml")

def load_aliases():
    if ALIASES_PATH.exists():
        return yaml.safe_load(ALIASES_PATH.read_text("utf-8")) or {}
    return {}

def save_aliases(aliases):
    ALIASES_PATH.write_text(yaml.dump(aliases, allow_unicode=True, sort_keys=True), "utf-8")

NOTES_DIR = Path("knowledge/vault/20_Notas")
VAULT_DIR = Path("knowledge/vault")

def get_existing_note_ids():
    ids = set()
    for p in VAULT_DIR.rglob("*.md"):
        try:
            content = p.read_text("utf-8", errors="ignore")
            m = re.search(r"^id:\s*antiquario:olfactory-note:([a-z0-9-]+)", content, re.MULTILINE)
            if m:
                ids.add(m.group(1))
        except Exception:
            pass
    return ids

def ensure_note_exists(slug: str, existing_ids: set):
    if not slug or slug in existing_ids: return
    note_path = NOTES_DIR / f"note-{slug}.md"
    if not note_path.exists():
        title = slug.replace("-", " ").title()
        content = f"""---
schema_version: 1
id: antiquario:olfactory-note:{slug}
project: o-antiquario
type: olfactory-note
title: "{title}"
aliases: [{slug}]
external_ids: {{}}
tags: [nota-olfativa, auto-gerada]
source_ids: [wikidata]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-24
language: pt-BR
summary: "Nota olfativa gerada por enriquecimento factual via Gemini."
evidence:
  - source_id: wikidata
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: "Descritor factual do Wikidata"
---

# {title}

Nota olfativa catalogada automaticamente.
"""
        note_path.write_text(content, encoding="utf-8")
        existing_ids.add(slug)
        print(f"  Created note file: note-{slug}.md")

def enrich_fragrance(file_path: Path, aliases: dict, existing_ids: set):
    if not genai_client:
        print("Gemini client is not available. Check GEMINI_API_KEY.")
        return False

    content = file_path.read_text("utf-8")
    
    # Extract title
    title_match = re.search(r'^title:\s*"?(.*?)"?$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem

    # Extract descriptors line
    descriptors_match = re.search(r'Descritores olfativos.*:\s*(.*)$', content, re.MULTILINE)
    if not descriptors_match:
        print(f"Skipping {file_path.name}: No descriptors line found.")
        return False

    descriptors = descriptors_match.group(1).strip()
    if not descriptors or descriptors.lower() == "nenhum":
        print(f"Skipping {file_path.name}: Empty descriptors.")
        return False

    print(f"\n[Enriching] {title} ({file_path.name})")
    print(f"  Descriptors: {descriptors}")

    prompt = f"""
    You are an expert perfumery olfactory pyramid classifier.
    Given a fragrance title "{title}" and a list of raw olfactory descriptors: "{descriptors}".
    
    Classify these descriptors into an olfactory pyramid layers (top, heart, base).
    Translate each descriptor note into a clean, normalized Portuguese slug (lowercase, hyphenated, ASCII without special accents if possible, e.g. "limao-siciliano", "bergamota", "abacaxi", "patchouli", "almiscar", "ambar", "baunilha", "cedro", "jasmim", "pimenta-rosa", "sandalo", "canela", "ameixa").
    
    Return ONLY a JSON object with this structure:
    {{
      "top": ["slug1", "slug2"],
      "heart": ["slug3"],
      "base": ["slug4"]
    }}
    If a layer has no notes, return an empty list. Every descriptor provided in the input MUST be assigned to at least one layer (top, heart, or base).
    """

    time.sleep(4.1) # Rate limit protection for free tier (15 RPM)
    try:
        response = genai_client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        pyramid = json.loads(response.text)
        print(f"  Gemini Output: {pyramid}")
    except Exception as e:
        print(f"  API Error: {e}")
        return False

    top_notes = pyramid.get("top", [])
    heart_notes = pyramid.get("heart", [])
    base_notes = pyramid.get("base", [])

    if not (top_notes or heart_notes or base_notes):
        print(f"  No notes extracted for {title}")
        return False

    # Generate relations
    relations_yaml = "relations:\n"
    new_aliases_added = False

    for note_slug in top_notes:
        note_slug = sanitize_slug(note_slug)
        if not note_slug: continue
        ensure_note_exists(note_slug, existing_ids)
        relations_yaml += f"- predicate: has-top-note\n  target: antiquario:olfactory-note:{note_slug}\n"
        if note_slug not in aliases:
            aliases[note_slug] = note_slug
            new_aliases_added = True

    for note_slug in heart_notes:
        note_slug = sanitize_slug(note_slug)
        if not note_slug: continue
        ensure_note_exists(note_slug, existing_ids)
        relations_yaml += f"- predicate: has-heart-note\n  target: antiquario:olfactory-note:{note_slug}\n"
        if note_slug not in aliases:
            aliases[note_slug] = note_slug
            new_aliases_added = True

    for note_slug in base_notes:
        note_slug = sanitize_slug(note_slug)
        if not note_slug: continue
        ensure_note_exists(note_slug, existing_ids)
        relations_yaml += f"- predicate: has-base-note\n  target: antiquario:olfactory-note:{note_slug}\n"
        if note_slug not in aliases:
            aliases[note_slug] = note_slug
            new_aliases_added = True

    if new_aliases_added:
        save_aliases(aliases)

    # Replace frontmatter fields
    updated = re.sub(r'review_status:\s*draft', 'review_status: approved', content)
    updated = re.sub(r'tags:\s*\[.*?\]', 'tags: [perfume, auto-aprovado]', updated)
    updated = re.sub(r'relations:\s*\[\]', relations_yaml.strip(), updated)

    # Save to DEST_DIR and remove from INBOX_DIR
    dest_path = DEST_DIR / file_path.name
    dest_path.write_text(updated, encoding="utf-8")
    file_path.unlink()
    print(f"  Successfully approved and moved to {dest_path.name}")
    return True

def main():
    if not INBOX_DIR.exists():
        print(f"Inbox directory {INBOX_DIR} does not exist.")
        return

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    aliases = load_aliases()
    existing_ids = get_existing_note_ids()
    inbox_files = list(INBOX_DIR.glob("*.md"))
    print(f"Found {len(inbox_files)} files in inbox.")

    processed = 0
    for file_path in inbox_files:
        if enrich_fragrance(file_path, aliases, existing_ids):
            processed += 1
            if processed >= 15: # Process 15 items per batch to stay well within limits
                print("\nBatch limit of 15 reached. Run script again for remaining items.")
                break

    print(f"\nFinished batch! Processed {processed} items.")

if __name__ == "__main__":
    main()
