---
schema_version: 1
id: antiquario:fragrance:parfumo-zadig-voltaire-this-is-him
project: o-antiquario
type: fragrance
title: "This Is Him!"
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
    target: antiquario:brand:zadig-voltaire
  - predicate: has-top-note
    target: antiquario:olfactory-note:black-pepper
  - predicate: has-top-note
    target: antiquario:olfactory-note:grapefruit
  - predicate: has-heart-note
    target: antiquario:olfactory-note:frankincense
  - predicate: has-heart-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalo
---

# This Is Him!

**Marca:** [[brand-zadig-voltaire]]

## Pirâmide Olfativa

- **Saída:** [[note-black-pepper]], [[note-grapefruit]]
- **Coração:** [[note-frankincense]], [[Baunilha]]
- **Fundo:** [[note-sandalo]]
