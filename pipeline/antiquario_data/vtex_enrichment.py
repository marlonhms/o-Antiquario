import json
import urllib.request
import urllib.parse
import re
import sys
import unicodedata
import yaml
from pathlib import Path
from .term_resolver import TermResolver

try:
    from ddgs import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False

sys.stdout.reconfigure(encoding='utf-8')

def search_vtex_epoca(query: str):
    q = unicodedata.normalize('NFKD', query).encode('ASCII', 'ignore').decode('utf-8')
    q = q.replace("'", "").replace('"', "")
    url = f"https://www.epocacosmeticos.com.br/api/catalog_system/pub/products/search/?ft={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
        if not data:
            return None
        return data[0]
    except Exception as e:
        print(f"Erro na busca VTEX para '{query}': {e}")
        return None

def search_ddg_fallback(query: str):
    """
    Usa o pacote oficial DuckDuckGo Search (ddgs) para extrair os snippets
    dos resultados de busca sobre o perfume.
    """
    if not HAS_DDGS:
        return None
        
    notes = {
        'has-top-note': [],
        'has-heart-note': [],
        'has-base-note': []
    }
    
    try:
        # Limpa o título removendo anos e concentrações para buscas mais precisas
        clean_title = re.sub(r'\b(19|20)\d{2}\b', '', query)
        clean_title = re.sub(r'(?i)\b(Eau de Parfum|Eau de Toilette|Extrait de Parfum|Perfume)\b', '', clean_title).strip()
        
        results = DDGS().text(f'site:fragrantica.com {clean_title} notes', max_results=3)
        for res in results:
            text = res.get('body', '') + ' ' + res.get('title', '')
            
            # Padrões comuns em inglês
            top_m = re.search(r'(?i)Top notes are (.*?)(?=\. Middle|\. Base|\.$|$)', text)
            mid_m = re.search(r'(?i)Middle notes are (.*?)(?=\. Base|\.$|$)', text)
            base_m = re.search(r'(?i)Base notes are (.*?)(?=\.$|$)', text)
            
            if top_m and not notes['has-top-note']:
                notes['has-top-note'] = [n.strip() for n in top_m.group(1).replace(' and ', ',').split(',')]
            if mid_m and not notes['has-heart-note']:
                notes['has-heart-note'] = [n.strip() for n in mid_m.group(1).replace(' and ', ',').split(',')]
            if base_m and not notes['has-base-note']:
                notes['has-base-note'] = [n.strip() for n in base_m.group(1).replace(' and ', ',').split(',')]
                
        # Limpa vazios
        for k in notes:
            notes[k] = [n for n in notes[k] if n]
            
        return notes if any(notes.values()) else None
    except Exception as e:
        print(f"Erro na busca DuckDuckGo para '{query}': {e}")
        return None

def extract_notes_from_vtex(product_data):
    notes = {
        'has-top-note': [],
        'has-heart-note': [],
        'has-base-note': []
    }
    
    if product_data.get('Notas de Topo'): notes['has-top-note'].extend(product_data['Notas de Topo'])
    if product_data.get('Notas de Coração'): notes['has-heart-note'].extend(product_data['Notas de Coração'])
    if product_data.get('Notas de Fundo'): notes['has-base-note'].extend(product_data['Notas de Fundo'])
    
    desc = product_data.get('description', '')
    if desc:
        desc = re.sub(r'<[^>]+>', ' ', desc)
        
        top_match = re.search(r'(?i)Notas? de Topo[\s:]+(.*?)(?=Notas? de Coração|Notas? de Fundo|Frasco:|Ocasião:|Marca:|Especificações:|$)', desc)
        heart_match = re.search(r'(?i)Notas? de Coração[\s:]+(.*?)(?=Notas? de Fundo|Frasco:|Ocasião:|Marca:|Especificações:|$)', desc)
        base_match = re.search(r'(?i)Notas? de Fundo[\s:]+(.*?)(?=Frasco:|Ocasião:|Marca:|Especificações:|$)', desc)
        
        if top_match and not notes['has-top-note']:
            notes['has-top-note'] = [n.strip() for n in top_match.group(1).replace('.', ',').split(',')]
        if heart_match and not notes['has-heart-note']:
            notes['has-heart-note'] = [n.strip() for n in heart_match.group(1).replace('.', ',').split(',')]
        if base_match and not notes['has-base-note']:
            notes['has-base-note'] = [n.strip() for n in base_match.group(1).replace('.', ',').split(',')]

    for k in notes:
        notes[k] = [n for n in notes[k] if n]
        
    return notes if any(notes.values()) else None

def run_vtex_enrichment():
    resolver = TermResolver(Path('data'))
    vault_dir = Path('knowledge/vault')
    disconnected = []
    
    for md_file in vault_dir.rglob('*.md'):
        content = md_file.read_text('utf-8', errors='ignore')
        if re.search(r'^type:\s*fragrance', content, re.MULTILINE):
            has_notes = re.search(r'predicate:\s*has-(top|heart|base)-note', content, re.MULTILINE) or \
                        re.search(r'predicate:\s*has-note', content, re.MULTILINE)
            if not has_notes:
                title_match = re.search(r'^title:\s*\"?(.*?)\"?$', content, re.MULTILINE)
                if title_match:
                    disconnected.append((md_file, title_match.group(1).strip(), content))

    print(f"Iniciando enriquecimento gratuito para {len(disconnected)} fragrâncias...")
    
    enriched_count = 0
    for md_file, title, content in disconnected:
        print(f"Buscando: {title}")
        
        extracted = None
        # 1. Tenta via VTEX
        product_data = search_vtex_epoca(title)
        if product_data:
            extracted = extract_notes_from_vtex(product_data)
            
        # 2. Fallback via DuckDuckGo (site:fragrantica.com)
        if not extracted and HAS_DDGS:
            extracted = search_ddg_fallback(title)
            if extracted:
                print(" -> Resgatado via DuckDuckGo OSINT!")
                
        if not extracted:
            print(f" -> Sem notas estruturadas.")
            continue
            
        relations_to_add = []
        links_to_add = []
        
        for predicate, note_list in extracted.items():
            for n in note_list:
                resolved = resolver.resolve_note(n)
                if resolved:
                    slug = resolved.canonical_id.split(":")[-1]
                    if resolved.kind == "note":
                        target = f"antiquario:olfactory-note:{slug}"
                    else:
                        target = f"antiquario:{resolved.kind}:{slug}"
                    n_file = f'{resolved.kind}-{slug}'
                    relations_to_add.append(f"  - predicate: {predicate}\n    target: {target}")
                    links_to_add.append(f"[[{n_file}]]")
                
        if not relations_to_add:
            print(f" -> Notas encontradas, mas nenhuma foi resolvida no vocabulário.")
            continue
            
        # Parse do Frontmatter usando PyYAML para evitar qualquer corrupção de sintaxe
        parts = content.split('---\n')
        if len(parts) >= 3:
            try:
                fm_data = yaml.safe_load(parts[1])
                if not isinstance(fm_data, dict):
                    continue
                    
                if 'relations' not in fm_data or not isinstance(fm_data['relations'], list):
                    fm_data['relations'] = []
                    
                for rel_str in relations_to_add:
                    # rel_str é "  - predicate: X\n    target: Y"
                    pred_m = re.search(r'predicate:\s*(\S+)', rel_str)
                    targ_m = re.search(r'target:\s*(\S+)', rel_str)
                    if pred_m and targ_m:
                        fm_data['relations'].append({
                            'predicate': pred_m.group(1),
                            'target': targ_m.group(1)
                        })
                        
                new_fm = yaml.dump(fm_data, allow_unicode=True, sort_keys=False).strip()
                body = '---\n'.join(parts[2:])
                new_content = f"---\n{new_fm}\n---\n{body}"
                
                top_links = [l for p, l in zip(relations_to_add, links_to_add) if 'has-top' in p]
                heart_links = [l for p, l in zip(relations_to_add, links_to_add) if 'has-heart' in p]
                base_links = [l for p, l in zip(relations_to_add, links_to_add) if 'has-base' in p]
                
                new_content = re.sub(r'- \*\*Saída:\*\* N/A', f'- **Saída:** {", ".join(top_links) if top_links else "N/A"}', new_content)
                new_content = re.sub(r'- \*\*Coração:\*\* N/A', f'- **Coração:** {", ".join(heart_links) if heart_links else "N/A"}', new_content)
                new_content = re.sub(r'- \*\*Fundo:\*\* N/A', f'- **Fundo:** {", ".join(base_links) if base_links else "N/A"}', new_content)
                
                md_file.write_text(new_content, encoding='utf-8')
                print(f" -> [SUCESSO] {title} enriquecido com {len(relations_to_add)} notas.")
                enriched_count += 1
            except Exception as ex:
                print(f" -> Erro ao atualizar YAML do arquivo {md_file.name}: {ex}")
                continue
                
    print(f"\nResumo: {enriched_count} fragrâncias enriquecidas.")

if __name__ == '__main__':
    run_vtex_enrichment()
