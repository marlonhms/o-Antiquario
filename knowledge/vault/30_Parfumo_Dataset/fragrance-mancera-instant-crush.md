---
schema_version: 1
id: antiquario:fragrance:parfumo-mancera-instant-crush
project: o-antiquario
type: fragrance
title: "Instant Crush"
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
    target: antiquario:brand:mancera
  - predicate: has-top-note
    target: antiquario:olfactory-note:saffron
  - predicate: has-top-note
    target: antiquario:olfactory-note:citrus-fruits
  - predicate: has-top-note
    target: antiquario:olfactory-note:ginger
  - predicate: has-heart-note
    target: antiquario:olfactory-note:amber
  - predicate: has-heart-note
    target: antiquario:olfactory-note:egyptian-jasmine
  - predicate: has-heart-note
    target: antiquario:olfactory-note:moroccan-rose
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:oakmoss
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
---

# Instant Crush

**Marca:** [[brand-mancera]]

## Pirâmide Olfativa

- **Saída:** [[note-saffron]], [[note-citrus-fruits]], [[note-ginger]]
- **Coração:** [[note-amber]], [[note-egyptian-jasmine]], [[note-moroccan-rose]]
- **Fundo:** [[note-white-musk]], [[Baunilha]], [[note-oakmoss]], [[note-sandalwood]]
