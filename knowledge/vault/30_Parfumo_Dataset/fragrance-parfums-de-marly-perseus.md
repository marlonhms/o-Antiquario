---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-perseus
project: o-antiquario
type: fragrance
title: "Perseus"
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
    target: antiquario:brand:parfums-de-marly
  - predicate: has-top-note
    target: antiquario:olfactory-note:grapefruit
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:blackcurrant-bud
  - predicate: has-heart-note
    target: antiquario:olfactory-note:green-mandarin-orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-heart-note
    target: antiquario:olfactory-note:geranium
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambergris
  - predicate: has-base-note
    target: antiquario:olfactory-note:cashmere-wood
  - predicate: has-base-note
    target: antiquario:olfactory-note:dry-woods
---

# Perseus

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-grapefruit]], [[Bergamota]], [[note-blackcurrant-bud]]
- **Coração:** [[note-green-mandarin-orange]], [[Vetiver]], [[note-geranium]]
- **Fundo:** [[note-ambergris]], [[note-cashmere-wood]], [[note-dry-woods]]
