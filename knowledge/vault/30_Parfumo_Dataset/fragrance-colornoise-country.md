---
schema_version: 1
id: antiquario:fragrance:parfumo-colornoise-country
project: o-antiquario
type: fragrance
title: "Country."
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
    target: antiquario:brand:colornoise
  - predicate: has-top-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-leaves
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:gymwear
  - predicate: has-heart-note
    target: antiquario:olfactory-note:musk
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lily-of-the-valley
  - predicate: has-heart-note
    target: antiquario:olfactory-note:raspberry
  - predicate: has-base-note
    target: antiquario:olfactory-note:coffee
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
---

# Country.

**Marca:** [[brand-colornoise]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[note-green-leaves]], [[Bergamota]], [[note-gymwear]]
- **Coração:** [[note-musk]], [[note-jasmine]], [[note-lily-of-the-valley]], [[note-raspberry]]
- **Fundo:** [[note-coffee]], [[Baunilha]], [[note-amber]], [[note-patchouli]], [[note-sandalwood]]
