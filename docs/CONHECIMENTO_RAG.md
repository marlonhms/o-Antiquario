# Knowledge Core e memória RAG

## Objetivo

O Knowledge Core transforma um vault Markdown compatível com Obsidian em documentos, chunks e sinapses validados. Ele é a camada editorial e recuperável do Antiquário; o catálogo factual continua separado e estruturado.

## Princípios

- RAG é o núcleo de recuperação, não a única fonte da verdade.
- O usuário final nunca importa ou organiza arquivos.
- Somente documentos `approved` entram nos artefatos compilados.
- Documento aprovado aceita apenas fontes `allowed_core` do manifesto.
- Cada fonte precisa de evidência e licença compatível.
- Wikilinks quebrados, IDs duplicados e relações inexistentes interrompem o build.
- O diretório `00_Inbox` não é indexado.
- Templates ficam fora do vault para não contaminarem o RAG.

## Contrato de uma nota

Toda nota possui:

- ID global `antiquario:tipo:slug`;
- tipo de entidade;
- resumo recuperável;
- fontes e evidências;
- confiança e estado de revisão;
- relações tipadas no YAML;
- wikilinks no conteúdo editorial.

As relações tipadas servem para raciocínio e filtros. Os wikilinks mantêm a navegação natural no Obsidian. Ambos são compilados como sinapses.

## Compilação

```text
knowledge/vault
  → parsing de frontmatter
  → validação de fontes e licenças
  → resolução de relações e wikilinks
  → chunking por seção semântica
  → hash determinístico
  → knowledge/compiled
```

Comandos:

```powershell
npm run knowledge:validate
npm run knowledge:build
```

Artefatos:

| Arquivo | Finalidade |
|---|---|
| `documents.json` | Documentos aprovados com texto e metadados |
| `chunks.json` | Unidades prontas para busca textual e embeddings |
| `graph.json` | Nós e sinapses resolvidas |
| `knowledge-manifest.json` | Versão, hash, contagens e nomes dos artefatos |

O hash é derivado do conteúdo, não do horário da execução. Duas compilações da mesma entrada produzem a mesma versão.

## Obsidian

O diretório `knowledge/vault` pode ser aberto diretamente como vault. A pasta `.obsidian` é local e ignorada pelo projeto. O funcionamento do compilador não depende do aplicativo Obsidian.

## Cerberus

A integração futura será uma exportação seletiva. Ela criará um gateway do Antiquário no Cerberus contendo arquitetura, decisões, métricas e aprendizados, sem duplicar o catálogo ou a memória privada.
