---
schema_version: 1
id: antiquario:fragrance:parfumo-etnia-factory-beijing
project: o-antiquario
type: fragrance
title: "Factory, Beijing"
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
    target: antiquario:brand:etnia
  - predicate: has-top-note
    target: antiquario:olfactory-note:red-apple
  - predicate: has-top-note
    target: antiquario:olfactory-note:red-pepper
  - predicate: has-top-note
    target: antiquario:olfactory-note:grapefruit
  - predicate: has-top-note
    target: antiquario:olfactory-note:pimento
  - predicate: has-top-note
    target: antiquario:olfactory-note:saffron
  - predicate: has-heart-note
    target: antiquario:olfactory-note:canela-leaf
  - predicate: has-heart-note
    target: antiquario:olfactory-note:habanero-chili
  - predicate: has-heart-note
    target: antiquario:olfactory-note:provencal-lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-base-note
    target: antiquario:olfactory-note:tobacco
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:amberwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:spoiled-spice
---

# Factory, Beijing

**Marca:** [[brand-etnia]]

## Pirâmide Olfativa

- **Saída:** [[note-red-apple]], [[note-red-pepper]], [[note-grapefruit]], [[note-pimento]], [[note-saffron]]
- **Coração:** [[note-cinnamon-leaf]], [[note-habanero-chili]], [[note-provencal-lavender]], [[note-lavender]]
- **Fundo:** [[note-tobacco]], [[note-benzoin]], [[note-amberwood]], [[note-cedarwood]], [[note-spoiled-spice]]
