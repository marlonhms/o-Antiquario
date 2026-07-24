import re
import yaml
from pathlib import Path
from curl_cffi import requests
import unicodedata
import time
import urllib.parse

def _slugify(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(character for character in decomposed if not unicodedata.combining(character))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-")
    return slug

def search_ddg_notes(title: str) -> dict:
    query = f'site:fragrantica.com "{title}"'
    print(f"Searching: {query}")
    try:
        url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
        res = requests.get(url, impersonate="chrome110")
        if res.status_code != 200:
            print(f"DDG HTTP {res.status_code}")
            return {}
            
        html = res.text
        snippets = re.findall(r'class="result__snippet[^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
        if not snippets:
            return {}
            
        for s in snippets:
            s = re.sub(r'<[^>]+>', '', s).strip()
            
            top_m = re.search(r'(?i)Top notes are (.*?)(?=\. Middle|\. Base|\.$|$)', s)
            mid_m = re.search(r'(?i)Middle notes are (.*?)(?=\. Base|\.$|$)', s)
            base_m = re.search(r'(?i)Base notes are (.*?)(?=\.$|$)', s)
            
            if top_m or mid_m or base_m:
                return {
                    'top': top_m.group(1).split(',') if top_m else [],
                    'mid': mid_m.group(1).split(',') if mid_m else [],
                    'base': base_m.group(1).split(',') if base_m else []
                }
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return {}

def update_fragrance_file(path: Path):
    content = path.read_text(encoding="utf-8")
    parts = content.split("---\n")
    if len(parts) < 3:
        return
        
    try:
        fm = yaml.safe_load(parts[1])
        relations = fm.get("relations", [])
        
        # Check if already has notes
        has_notes = False
        for rel in relations:
            if rel.get("predicate", "").startswith("has-") and "note" in rel.get("predicate", ""):
                has_notes = True
                break
                
        if has_notes:
            return
            
        title = fm.get("title", "")
        if not title:
            return
            
        notes = search_ddg_notes(title)
        time.sleep(1) # delay to avoid rate limiting
        if not notes:
            return
            
        new_relations = [r for r in relations]
        
        # Clean up existing empty notes section
        body = "---\n".join(parts[2:])
        body = re.sub(r'- \*\*Saída:\*\*\s*N/A', '', body)
        body = re.sub(r'- \*\*Coração:\*\*\s*N/A', '', body)
        body = re.sub(r'- \*\*Fundo:\*\*\s*N/A', '', body)
        
        pyramid_lines = []
        
        def add_notes(note_type: str, pred: str, label: str):
            raw_notes = notes.get(note_type, [])
            clean_notes = []
            links = []
            for n in raw_notes:
                n = n.replace('and ', '').strip()
                if not n: continue
                slug = _slugify(n)
                clean_notes.append(slug)
                links.append(f"[[note-{slug}]]")
                new_relations.append({
                    "predicate": pred,
                    "target": f"antiquario:olfactory-note:{slug}"
                })
            if links:
                pyramid_lines.append(f"- **{label}:** {', '.join(links)}")
            else:
                pyramid_lines.append(f"- **{label}:** N/A")
                
        add_notes('top', 'has-top-note', 'Saída')
        add_notes('mid', 'has-heart-note', 'Coração')
        add_notes('base', 'has-base-note', 'Fundo')
        
        fm["relations"] = new_relations
        new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
        
        # Rebuild body with pyramid
        if "## Pirâmide Olfativa" in body:
            body = re.sub(
                r'## Pirâmide Olfativa\s*[\n\- \w\*:/\[\]]*', 
                "## Pirâmide Olfativa\n\n" + "\n".join(pyramid_lines) + "\n\n", 
                body
            )
        else:
            body += "\n## Pirâmide Olfativa\n\n" + "\n".join(pyramid_lines) + "\n\n"
            
        new_content = f"---\n{new_fm}\n---\n{body.strip()}\n"
        path.write_text(new_content, encoding="utf-8")
        print(f"Updated: {path.name}")
        
    except Exception as e:
        print(f"Error parsing {path.name}: {e}")

def main():
    vault = Path("knowledge/vault")
    dirs_to_check = [vault / "10_Perfumes", vault / "30_Parfumo_Dataset"]
    
    for d in dirs_to_check:
        if d.exists():
            for p in d.rglob("*.md"):
                update_fragrance_file(p)

if __name__ == "__main__":
    main()
