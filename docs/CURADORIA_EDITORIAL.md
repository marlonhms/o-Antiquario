# Curadoria Editorial v1

## Objetivo

O enriquecimento editorial transforma identidades factuais do catálogo em conhecimento olfativo útil ao recomendador. A etapa é interna: o usuário final não importa nem classifica dados.

O processo começa com uma fila determinística, não com geração automática de notas. A separação impede que o sistema transforme nome, marca ou país em supostas características olfativas.

## Gerar a fila

```powershell
npm run curation:queue
```

O comando lê o DuckDB factual e o relatório de resolução. Ele:

1. exclui registros que ainda possuem ambiguidade de identidade;
2. prioriza completude factual e diversidade de marca e país;
3. cria até 25 rascunhos em `knowledge/vault/00_Inbox/Curadoria-Catalogo`;
4. publica a auditoria em `data/curation/curation-queue.json`.

`00_Inbox` é ignorado pelo compilador do Knowledge Core. Portanto, esses rascunhos não entram no RAG, na busca nem no ranking.

## Revisão humana

Para cada item, a pessoa curadora deve confirmar identidade e concentração, classificar família/notas/acordes pela taxonomia local e documentar desempenho com método, amostra e confiança. Só então o arquivo pode ser movido para `knowledge/vault/10_Perfumes` e receber `review_status: approved`.

Cada nova afirmação editorial precisa de fonte permitida e escopo de evidência. O Wikidata permanece como fonte de identidade, não de notas ou desempenho.

## Proteção contra perda de trabalho

O gerador nunca sobrescreve um rascunho existente que tenha sido alterado manualmente. Ele o lista em `preserved` e mantém o conteúdo intacto. A fila pode ser executada novamente com segurança após novas releases factuais.

## Cobertura

O relatório também mostra os candidatos atuais por região. Na primeira release, essa medição deve guiar a expansão do conector e da curadoria — especialmente Brasil e perfumaria árabe — sem alegar que o catálogo atual já atende essas metas.
