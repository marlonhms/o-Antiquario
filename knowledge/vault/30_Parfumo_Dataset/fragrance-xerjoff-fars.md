---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-fars
project: o-antiquario
type: fragrance
title: "Fars"
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
    target: antiquario:brand:xerjoff
  - predicate: has-top-note
    target: antiquario:olfactory-note:cade-juniper
  - predicate: has-top-note
    target: antiquario:olfactory-note:french-lavender
  - predicate: has-top-note
    target: antiquario:olfactory-note:italian-bergamot
  - predicate: has-heart-note
    target: antiquario:olfactory-note:egyptian-geranium
  - predicate: has-heart-note
    target: antiquario:olfactory-note:atlas-cedar
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:haitian-vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-oud
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# Fars

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-cade-juniper]], [[note-french-lavender]], [[note-italian-bergamot]]
- **Coração:** [[note-egyptian-geranium]], [[note-atlas-cedar]], [[note-jasmine-absolute]]
- **Fundo:** [[note-amber]], [[note-haitian-vetiver]], [[note-sandalwood]], [[note-white-oud]], [[note-patchouli]]
