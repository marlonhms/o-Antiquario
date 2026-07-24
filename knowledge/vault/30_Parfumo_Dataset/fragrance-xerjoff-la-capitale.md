---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-la-capitale
project: o-antiquario
type: fragrance
title: "La Capitale"
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
    target: antiquario:brand:xerjoff
  - predicate: has-top-note
    target: antiquario:olfactory-note:strawberry
  - predicate: has-top-note
    target: antiquario:olfactory-note:caramel
  - predicate: has-top-note
    target: antiquario:olfactory-note:labdanum
  - predicate: has-top-note
    target: antiquario:olfactory-note:peach
  - predicate: has-heart-note
    target: antiquario:olfactory-note:amber
  - predicate: has-heart-note
    target: antiquario:olfactory-note:leather
  - predicate: has-heart-note
    target: antiquario:olfactory-note:persian-saffron
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose
  - predicate: has-heart-note
    target: antiquario:olfactory-note:ginger
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla
  - predicate: has-base-note
    target: antiquario:olfactory-note:oud
---

# La Capitale

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-strawberry]], [[note-caramel]], [[note-labdanum]], [[note-peach]]
- **Coração:** [[note-amber]], [[note-leather]], [[note-persian-saffron]], [[note-rose]], [[note-ginger]]
- **Fundo:** [[note-benzoin]], [[note-bourbon-vanilla]], [[note-oud]]
