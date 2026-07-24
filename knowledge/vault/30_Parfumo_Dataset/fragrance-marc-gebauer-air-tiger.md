---
schema_version: 1
id: antiquario:fragrance:parfumo-marc-gebauer-air-tiger
project: o-antiquario
type: fragrance
title: "Air Tiger"
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
    target: antiquario:brand:marc-gebauer
  - predicate: has-top-note
    target: antiquario:olfactory-note:zimbro
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:limao-siciliano
  - predicate: has-heart-note
    target: antiquario:olfactory-note:leather
  - predicate: has-heart-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedar
  - predicate: has-heart-note
    target: antiquario:olfactory-note:iris
  - predicate: has-base-note
    target: antiquario:olfactory-note:labdanum
  - predicate: has-base-note
    target: antiquario:olfactory-note:woods
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambar
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
---

# Air Tiger

**Marca:** [[brand-marc-gebauer]]

## Pirâmide Olfativa

- **Saída:** [[note-zimbro]], [[note-cardamom]], [[note-limao-siciliano]]
- **Coração:** [[note-leather]], [[note-patchouli]], [[note-cedar]], [[note-iris]]
- **Fundo:** [[note-labdanum]], [[note-woods]], [[note-ambar]], [[note-benzoin]]
