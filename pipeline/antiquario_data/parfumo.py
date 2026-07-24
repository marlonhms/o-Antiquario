import pandas as pd
from pathlib import Path
import re
import unicodedata

def slugify(text):
    text = str(text).strip()
    if not text or text.lower() == 'nan':
        return None
    normalized = unicodedata.normalize('NFD', text)
    without_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    cleaned = re.sub(r'[^a-z0-9\s-]', '', without_accents.lower())
    return re.sub(r'\s+', '-', cleaned).strip('-')

def run_parfumo_etl():
    # Construir mapa de aliases do cofre existente para evitar colisões
    alias_map = {}
    for vault_dir in ['knowledge/vault/20_Notas', 'knowledge/vault/15_Marcas']:
        path = Path(vault_dir)
        if not path.exists(): continue
        for md in path.glob('*.md'):
            text = md.read_text('utf-8', errors='ignore')
            id_match = re.search(r'^id:\s*(.*)$', text, re.MULTILINE)
            if not id_match: continue
            doc_id = id_match.group(1).strip()
            file_name = md.stem
            
            title_match = re.search(r'^title:\s*(.+)$', text, re.MULTILINE)
            if title_match:
                alias_map[title_match.group(1).strip().strip('"').lower()] = (doc_id, file_name)
                
            aliases_match = re.search(r'^aliases:\s*\[(.*?)\]', text, re.MULTILINE)
            if aliases_match:
                aliases = [a.strip().strip('"').strip("'") for a in aliases_match.group(1).split(',')]
                for a in aliases:
                    if a: alias_map[a.lower()] = (doc_id, file_name)

    url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2024/2024-12-10/parfumo_data_clean.csv'
    print(f'Baixando dataset Parfumo de {url}...')
    df = pd.read_csv(url)
    
    # Processar top 200 por rating_count como MVP inicial
    df = df.sort_values(by='Rating_Count', ascending=False).head(200)
    
    inbox_dir = Path('knowledge/vault/30_Parfumo_Dataset')
    inbox_dir.mkdir(parents=True, exist_ok=True)
    
    brands = set()
    notes = set()
    
    for idx, row in df.iterrows():
        if pd.isna(row['Name']) or pd.isna(row['Brand']):
            continue
            
        brand = str(row['Brand']).strip()
        brand_slug = slugify(brand)
        brand_lower = brand.lower()
        if brand_lower in alias_map:
            brand_target, brand_file = alias_map[brand_lower]
        else:
            brand_target = f'antiquario:brand:{brand_slug}'
            brand_file = f'brand-{brand_slug}'
            if brand_slug: brands.add((brand, brand_slug))
            
        name = str(row['Name']).strip()
        name_slug = slugify(name)
        
        if not name_slug:
            continue
            
        frag_id = f'antiquario:fragrance:parfumo-{brand_slug}-{name_slug}'
        
        relations = []
        relations.append(f'  - predicate: belongs-to-brand\n    target: {brand_target}')
        
        top_links = []
        heart_links = []
        base_links = []
        
        def process_notes(notes_str, predicate, link_list):
            if pd.isna(notes_str) or str(notes_str).strip() == '':
                return
            parts = [n.strip() for n in str(notes_str).split(',')]
            for n in parts:
                n_lower = n.lower()
                n_file = ''
                if n_lower in alias_map:
                    target, n_file = alias_map[n_lower]
                    relations.append(f'  - predicate: {predicate}\n    target: {target}')
                else:
                    n_slug = slugify(n)
                    if n_slug:
                        n_file = f'note-{n_slug}'
                        notes.add((n, n_slug))
                        relations.append(f'  - predicate: {predicate}\n    target: antiquario:olfactory-note:{n_slug}')
                if n_file:
                    link_list.append(f'[[{n_file}]]')
                    
        process_notes(row.get('Top_Notes'), 'has-top-note', top_links)
        process_notes(row.get('Middle_Notes'), 'has-heart-note', heart_links)
        process_notes(row.get('Base_Notes'), 'has-base-note', base_links)
        
        rel_str = '\n'.join(relations) if relations else ''
        
        md_content = f"""---
schema_version: 1
id: {frag_id}
project: o-antiquario
type: fragrance
title: "{name}"
aliases: []
external_ids: {{}}
tags: [perfume, parfumo, draft]
source_ids: [parfumo_dataset]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: "Fragrância extraída do Parfumo Fragrance Dataset (TidyTuesday)."
evidence:
  - source_id: parfumo_dataset
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: "Estrutura da pirâmide olfativa"
relations:
{rel_str}
---

# {name}

**Marca:** [[{brand_file}]]

## Pirâmide Olfativa

- **Saída:** {', '.join(top_links) if top_links else 'N/A'}
- **Coração:** {', '.join(heart_links) if heart_links else 'N/A'}
- **Fundo:** {', '.join(base_links) if base_links else 'N/A'}
"""
        with open(inbox_dir / f'fragrance-{brand_slug}-{name_slug}.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
            
    # Escrever Marcas
    for b_name, b_slug in brands:
        md_content = f"""---
schema_version: 1
id: antiquario:brand:{b_slug}
project: o-antiquario
type: brand
title: "{b_name}"
aliases: []
external_ids: {{}}
tags: [brand, parfumo]
source_ids: [parfumo_dataset]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: "Marca extraída do Parfumo Dataset."
evidence:
  - source_id: parfumo_dataset
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: "Extração de entidade"
relations: []
---

# {b_name}
"""
        with open(inbox_dir / f'brand-{b_slug}.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
            
    # Escrever Notas
    for n_name, n_slug in notes:
        md_content = f"""---
schema_version: 1
id: antiquario:olfactory-note:{n_slug}
project: o-antiquario
type: olfactory-note
title: "{n_name}"
aliases: []
external_ids: {{}}
tags: [olfactory-note, parfumo]
source_ids: [parfumo_dataset]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: "Nota olfativa extraída do Parfumo Dataset."
evidence:
  - source_id: parfumo_dataset
    kind: open_source
    license: CC0-1.0
    confidence: medium
    claim_scope: "Extração de entidade"
relations: []
---

# {n_name}
"""
        with open(inbox_dir / f'note-{n_slug}.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
            
    print(f'Extração concluída: {len(df)} perfumes, {len(brands)} marcas, {len(notes)} notas extraídas.')

if __name__ == '__main__':
    run_parfumo_etl()
