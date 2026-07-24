---
schema_version: 1
id: antiquario:fragrance:parfumo-van-cleef-arpels-bois-dore
project: o-antiquario
type: fragrance
title: "Bois Doré"
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
    target: antiquario:brand:van-cleef-arpels
  - predicate: has-top-note
    target: antiquario:olfactory-note:mineral-notes
  - predicate: has-top-note
    target: antiquario:olfactory-note:pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-musk
---

# Bois Doré

**Marca:** [[brand-van-cleef-arpels]]

## Pirâmide Olfativa

- **Saída:** [[note-mineral-notes]], [[note-pepper]]
- **Coração:** [[Baunilha]], [[note-cedarwood]]
- **Fundo:** [[note-tonka-bean-absolute]], [[note-white-musk]]
