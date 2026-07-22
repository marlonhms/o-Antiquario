---
schema_version: 1
id: antiquario:guide:fontes-de-conhecimento
project: o-antiquario
type: guide
title: Fontes de conhecimento
aliases: [Fontes-De-Conhecimento]
tags: [guia, fontes, proveniencia, licenca]
source_ids: [internal_curated]
license: CC0-1.0
confidence: high
review_status: approved
updated_at: 2026-07-22
language: pt-BR
summary: Regras editoriais para transformar fontes permitidas em conhecimento rastreável e recuperável.
evidence:
  - source_id: internal_curated
    kind: curated
    license: CC0-1.0
    confidence: high
    claim_scope: Política de governança original do Knowledge Core.
relations:
  - predicate: governed-by
    target: antiquario:index:principal
---

# Fontes de conhecimento

Cada afirmação recuperável precisa indicar sua origem, licença, confiança e estado de revisão. A presença pública de uma página não constitui autorização automática para incorporá-la ao RAG.

## Promoção ao core

Somente documentos aprovados e sustentados por fontes classificadas como `allowed_core` entram nos artefatos publicados. Fontes pendentes permanecem em staging até revisão específica.

## Conteúdo editorial

Sínteses originais podem entrar como `internal_curated`. Elas devem separar interpretação de fatos externos e evitar reproduzir textos promocionais ou avaliações de terceiros.

## Navegação

O [[Antiquario-Index|índice principal]] funciona como mapa editorial, enquanto as relações tipadas formam o grafo consumido pelo sistema.
