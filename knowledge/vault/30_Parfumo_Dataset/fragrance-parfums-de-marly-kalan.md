---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-kalan
project: o-antiquario
type: fragrance
title: "Kalan"
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
    target: antiquario:olfactory-note:blood-orange
  - predicate: has-top-note
    target: antiquario:olfactory-note:spices
  - predicate: has-top-note
    target: antiquario:olfactory-note:black-pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:orange-blossom-absolute
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:solar-note
  - predicate: has-base-note
    target: antiquario:olfactory-note:roasted-tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:precious-woods
  - predicate: has-base-note
    target: antiquario:olfactory-note:moss
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
---

# Kalan

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-blood-orange]], [[note-spices]], [[note-black-pepper]]
- **Coração:** [[note-orange-blossom-absolute]], [[note-lavender]], [[note-solar-note]]
- **Fundo:** [[note-roasted-tonka-bean]], [[note-amber]], [[note-precious-woods]], [[note-moss]], [[note-sandalwood]]
