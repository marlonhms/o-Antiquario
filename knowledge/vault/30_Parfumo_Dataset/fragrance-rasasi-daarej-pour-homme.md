---
schema_version: 1
id: antiquario:fragrance:parfumo-rasasi-daarej-pour-homme
project: o-antiquario
type: fragrance
title: "Daarej pour Homme"
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
    target: antiquario:brand:rasasi
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:cumin
  - predicate: has-top-note
    target: antiquario:olfactory-note:mugwort
  - predicate: has-heart-note
    target: antiquario:olfactory-note:iris
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalwood
---

# Daarej pour Homme

**Marca:** [[brand-rasasi]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-cumin]], [[note-mugwort]]
- **Coração:** [[note-iris]], [[note-rose]]
- **Fundo:** [[note-musk]], [[note-tonka-bean]], [[Baunilha]], [[note-amber]], [[note-patchouli]], [[note-sandalwood]]
