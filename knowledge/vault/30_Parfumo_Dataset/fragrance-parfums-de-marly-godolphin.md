---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-godolphin
project: o-antiquario
type: fragrance
title: "Godolphin"
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
    target: antiquario:olfactory-note:saffron
  - predicate: has-top-note
    target: antiquario:olfactory-note:cypress
  - predicate: has-top-note
    target: antiquario:olfactory-note:thyme
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose
  - predicate: has-heart-note
    target: antiquario:olfactory-note:iris
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-cedarwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambar
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
---

# Godolphin

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-saffron]], [[note-cypress]], [[note-thyme]]
- **Coração:** [[note-rose]], [[note-iris]], [[note-jasmine]]
- **Fundo:** [[Vetiver]], [[note-white-cedarwood]], [[note-ambar]], [[note-musk]], [[Baunilha]]
