---
schema_version: 1
id: antiquario:fragrance:parfumo-versace-blue-jeans
project: o-antiquario
type: fragrance
title: "Blue Jeans"
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
    target: antiquario:brand:versace
  - predicate: has-top-note
    target: antiquario:olfactory-note:citrus-fruits
  - predicate: has-top-note
    target: antiquario:olfactory-note:aniseed
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:rosewood
  - predicate: has-top-note
    target: antiquario:olfactory-note:basil
  - predicate: has-top-note
    target: antiquario:olfactory-note:juniper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:heliotrope
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:carnation
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-heart-note
    target: antiquario:olfactory-note:sage
  - predicate: has-heart-note
    target: antiquario:olfactory-note:fir
  - predicate: has-heart-note
    target: antiquario:olfactory-note:geranium
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lily-of-the-valley
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:cedar
  - predicate: has-base-note
    target: antiquario:olfactory-note:iris
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
---

# Blue Jeans

**Marca:** [[brand-versace]]

## Pirâmide Olfativa

- **Saída:** [[note-citrus-fruits]], [[note-aniseed]], [[Bergamota]], [[note-rosewood]], [[note-basil]], [[note-juniper]]
- **Coração:** [[note-heliotrope]], [[note-lavender]], [[note-carnation]], [[note-jasmine]], [[note-sage]], [[note-fir]], [[note-geranium]], [[note-lily-of-the-valley]], [[note-rose]]
- **Fundo:** [[note-tonka-bean]], [[note-amber]], [[note-cedar]], [[note-iris]], [[note-musk]], [[note-patchouli]], [[note-sandalwood]], [[Baunilha]], [[Vetiver]]
