---
schema_version: 1
id: antiquario:fragrance:parfumo-acqua-di-parma-bergamotto-di-calabria
project: o-antiquario
type: fragrance
title: "Bergamotto di Calabria"
aliases: []
external_ids: {}
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
  - predicate: belongs-to-brand
    target: antiquario:brand:acqua-di-parma
  - predicate: has-top-note
    target: antiquario:olfactory-note:lemon
  - predicate: has-top-note
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:red-ginger
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
---

# Bergamotto di Calabria

**Marca:** [[brand-acqua-di-parma]]

## Pirâmide Olfativa

- **Saída:** [[note-lemon]], [[note-calabrian-bergamot]]
- **Coração:** [[note-cedarwood]], [[note-red-ginger]]
- **Fundo:** [[note-musk]], [[note-benzoin]], [[Vetiver]]
