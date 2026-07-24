---
schema_version: 1
id: antiquario:fragrance:parfumo-mugler-amen-angel-men
project: o-antiquario
type: fragrance
title: "A*Men Angel Men"
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
    target: antiquario:brand:mugler
  - predicate: has-top-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:coriander
  - predicate: has-top-note
    target: antiquario:olfactory-note:peppermint
  - predicate: has-heart-note
    target: antiquario:olfactory-note:caramel
  - predicate: has-heart-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:honey
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lily-of-the-valley
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-base-note
    target: antiquario:olfactory-note:coffee
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambar
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalo
  - predicate: has-base-note
    target: antiquario:olfactory-note:styrax
---

# A*Men Angel Men

**Marca:** [[brand-mugler]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[Bergamota]], [[note-coriander]], [[note-peppermint]]
- **Coração:** [[note-caramel]], [[note-patchouli]], [[note-cedarwood]], [[note-honey]], [[note-lily-of-the-valley]], [[note-jasmine]]
- **Fundo:** [[note-coffee]], [[note-tonka-bean]], [[note-ambar]], [[note-benzoin]], [[note-musk]], [[Baunilha]], [[note-sandalo]], [[note-styrax]]
