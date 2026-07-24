---
schema_version: 1
id: antiquario:fragrance:parfumo-creed-himalaya
project: o-antiquario
type: fragrance
title: "Himalaya"
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
    target: antiquario:brand:creed
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:limao-siciliano
  - predicate: has-top-note
    target: antiquario:olfactory-note:mandarin-orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:zimbro
  - predicate: has-heart-note
    target: antiquario:olfactory-note:pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:nutmeg
  - predicate: has-heart-note
    target: antiquario:olfactory-note:gun-powder
  - predicate: has-base-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalo
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
---

# Himalaya

**Marca:** [[brand-creed]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]], [[note-limao-siciliano]], [[note-mandarin-orange]]
- **Coração:** [[note-zimbro]], [[note-pepper]], [[note-jasmine]], [[note-lavender]], [[note-nutmeg]], [[note-gun-powder]]
- **Fundo:** [[note-cedarwood]], [[note-sandalo]], [[note-tonka-bean]], [[Vetiver]]
