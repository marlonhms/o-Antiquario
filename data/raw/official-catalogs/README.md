# Catálogos Oficiais em PDF (`data/raw/official-catalogs/`)

Este diretório armazena catálogos em formato PDF fornecidos **manualmente pelo proprietário do projeto** para processamento pelo conector local (`official-pdf`).

## Convenção de Organização

```text
data/raw/official-catalogs/
  <marca>/
    <edicao-ou-ano>.pdf
```

Exemplos:
- `data/raw/official-catalogs/natura/2026-ciclo-01.pdf`
- `data/raw/official-catalogs/o-boticario/2025-catalogo.pdf`

## Regras de Governança

1. **Nenhum arquivo PDF é baixado automaticamente pelo pipeline**.
2. **Os PDFs não devem ser commitados no Git**. O arquivo `.gitignore` bloqueia arquivos `*.pdf` dentro deste diretório.
3. Antes de processar qualquer catálogo, verifique se a fonte e o `source_id` correspondente estão autorizados e registrados em `data/sources.yml`.
