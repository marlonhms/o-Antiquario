from __future__ import annotations

import json
from pathlib import Path
import re
import unicodedata
import yaml
from typing import Any

def _slugify(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(character for character in decomposed if not unicodedata.combining(character))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-")
    return slug or "fragrancia"

def evaluate_quality_gate(fm_data: dict[str, Any], content: str) -> tuple[bool, list[str]]:
    """
    Avalia se um rascunho de fragrância atinge a régua de qualidade
    para aprovação automática e promoção para 10_Perfumes.
    """
    reasons = []
    
    # 1. Tipo deve ser fragrance
    if fm_data.get("type") != "fragrance":
        reasons.append("tipo diferente de fragrance")
        return False, reasons
        
    # 2. Deve ter evidência declarada
    evidence = fm_data.get("evidence", [])
    if not evidence or not isinstance(evidence, list):
        reasons.append("sem evidência declarada")
        return False, reasons
        
    # 3. Deve possuir notas conectadas em relations
    relations = fm_data.get("relations", [])
    has_notes = False
    if isinstance(relations, list):
        for rel in relations:
            if isinstance(rel, dict):
                pred = rel.get("predicate", "")
                if "note" in pred or pred in ("has-top-note", "has-heart-note", "has-base-note", "has-note"):
                    has_notes = True
                    break
                    
    if not has_notes:
        reasons.append("sem notas olfativas estruturadas em relations")
        return False, reasons

    return True, ["cumpre todos os critérios de qualidade (notas + evidências)"]

def run_auto_approval(*, vault_directory: Path | None = None, dry_run: bool = False) -> dict[str, Any]:
    if vault_directory is None:
        vault_directory = Path("knowledge/vault")
        
    inbox_dir = vault_directory / "00_Inbox"
    perfumes_dir = vault_directory / "10_Perfumes"
    perfumes_dir.mkdir(parents=True, exist_ok=True)
    
    if not inbox_dir.exists():
        print(f"Diretório Inbox não encontrado: {inbox_dir}")
        return {"approved": 0, "skipped": 0}
        
    approved_count = 0
    skipped_count = 0
    approved_files = []
    skipped_files = []
    
    inbox_files = list(inbox_dir.rglob("*.md"))
    print(f"Avaliando {len(inbox_files)} rascunhos na Inbox para Aprovação Automática...")
    
    for md_file in inbox_files:
        content = md_file.read_text("utf-8", errors="ignore")
        parts = content.split("---\n")
        if len(parts) < 3:
            skipped_count += 1
            skipped_files.append((md_file.name, ["frontmatter inválido"]))
            continue
            
        try:
            fm_data = yaml.safe_load(parts[1])
            if not isinstance(fm_data, dict):
                skipped_count += 1
                skipped_files.append((md_file.name, ["frontmatter não é dicionário"]))
                continue
                
            passed, reasons = evaluate_quality_gate(fm_data, content)
            if not passed:
                skipped_count += 1
                skipped_files.append((md_file.name, reasons))
                continue
                
            # Atualiza metadados para APROVADO
            fm_data["review_status"] = "approved"
            
            tags = fm_data.get("tags", [])
            if isinstance(tags, list):
                new_tags = [t for t in tags if t not in ("curadoria-pendente", "rascunho")]
                if "aprovado" not in new_tags:
                    new_tags.append("aprovado")
                if "auto-aprovado" not in new_tags:
                    new_tags.append("auto-aprovado")
                fm_data["tags"] = new_tags
                
            new_fm = yaml.dump(fm_data, allow_unicode=True, sort_keys=False).strip()
            body = "---\n".join(parts[2:])
            
            # Remove aviso de rascunho se presente
            body = re.sub(
                r"## Limite de uso\s*\n\nEste rascunho não é uma recomendação.*?\n\n",
                "",
                body,
                flags=re.DOTALL
            )
            
            new_content = f"---\n{new_fm}\n---\n{body}"
            
            # Define o novo caminho na pasta 10_Perfumes
            doc_id = fm_data.get("id", "")
            title = fm_data.get("title", md_file.stem)
            target_slug = _slugify(title)
            target_path = perfumes_dir / f"{target_slug}.md"
            
            # Procurar se já existe um arquivo com esse mesmo ID em 10_Perfumes
            existing_with_id = None
            for p_file in perfumes_dir.glob("*.md"):
                if p_file == md_file:
                    continue
                try:
                    p_text = p_file.read_text("utf-8", errors="ignore")
                    p_parts = p_text.split("---\n")
                    if len(p_parts) >= 3:
                        p_fm = yaml.safe_load(p_parts[1])
                        if isinstance(p_fm, dict) and p_fm.get("id") == doc_id:
                            existing_with_id = p_file
                            break
                except Exception:
                    pass
                    
            if existing_with_id:
                target_path = existing_with_id
                
            if not dry_run:
                target_path.write_text(new_content, encoding="utf-8")
                if md_file.resolve() != target_path.resolve() and md_file.exists():
                    md_file.unlink() # remove da inbox
                
            approved_count += 1
            approved_files.append((title, target_path.name))
            print(f" -> [APROVADO] '{title}' promovido para 10_Perfumes/{target_path.name}")
            
        except Exception as ex:
            skipped_count += 1
            skipped_files.append((md_file.name, [f"erro no parse: {ex}"]))
            
    print(f"\nResumo da Aprovação Automática:")
    print(f" - Aprovadas e Promovidas para 10_Perfumes: {approved_count}")
    print(f" - Mantidas na Inbox (incompletas/sem notas): {skipped_count}")
    
    return {
        "approved": approved_count,
        "skipped": skipped_count,
        "approved_files": approved_files,
        "skipped_files": skipped_files
    }

if __name__ == "__main__":
    run_auto_approval()
