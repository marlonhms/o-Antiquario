---
schema_version: 1
id: antiquario:fragrance:parfumo-gisada-ambassador-for-men
project: o-antiquario
type: fragrance
title: "Ambassador for Men"
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
    target: antiquario:brand:gisada
  - predicate: has-top-note
    target: antiquario:olfactory-note:apple
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-mandarin-orange
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:violet
  - predicate: has-heart-note
    target: antiquario:olfactory-note:mango
  - predicate: has-heart-note
    target: antiquario:olfactory-note:black-pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-heart-note
    target: antiquario:olfactory-note:peony
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambar
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:moss
  - predicate: has-base-note
    target: antiquario:olfactory-note:teak
---

# Ambassador for Men

**Marca:** [[brand-gisada]]

## Pirâmide Olfativa

- **Saída:** [[note-apple]], [[note-green-mandarin-orange]], [[note-cardamom]], [[note-violet]]
- **Coração:** [[note-mango]], [[note-black-pepper]], [[note-lavender]], [[note-patchouli]], [[note-peony]]
- **Fundo:** [[note-ambar]], [[Baunilha]], [[Vetiver]], [[note-moss]], [[note-teak]]
