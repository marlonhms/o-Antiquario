import os
import re
from pathlib import Path

vault_dir = Path('knowledge/vault')
disconnected = []
total = 0

for md_file in vault_dir.rglob('*.md'):
    content = md_file.read_text('utf-8', errors='ignore')
    if re.search(r'^type:\s*fragrance', content, re.MULTILINE):
        total += 1
        has_notes = re.search(r'predicate:\s*has-(top|heart|base)-note', content, re.MULTILINE) or \
                    re.search(r'predicate:\s*has-note', content, re.MULTILINE)
        if not has_notes:
            title_match = re.search(r'^title:\s*\"?(.*?)\"?$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_file.name
            disconnected.append(title)

disconnected.sort(key=lambda x: x.lower())
out_path = r'C:\Users\Marlon\.gemini\antigravity-ide\brain\4db6c8ee-b2db-405b-b743-a55ffdfdf343\disconnected_fragrances.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Relatório de Fragrâncias Desconectadas\n\n')
    f.write('Esta é a lista de pontas soltas no Grafo de Conhecimento (fragrâncias sem notas conectadas):\n\n')
    f.write('| Perfume |\n')
    f.write('|---|\n')
    for title in disconnected:
        f.write(f'| {title} |\n')
print(f"Relatório gerado com sucesso em {out_path} ({len(disconnected)} pontas soltas).")
