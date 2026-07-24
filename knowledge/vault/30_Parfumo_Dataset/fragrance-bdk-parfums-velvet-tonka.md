---
schema_version: 1
id: antiquario:fragrance:parfumo-bdk-parfums-velvet-tonka
project: o-antiquario
type: fragrance
title: "Velvet Tonka"
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
    target: antiquario:brand:bdk-parfums
  - predicate: has-top-note
    target: antiquario:olfactory-note:almond
  - predicate: has-top-note
    target: antiquario:olfactory-note:orange-blossom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:balkans-tobacco-absolute
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:amberwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:amyris
---

# Velvet Tonka

**Marca:** [[brand-bdk-parfums]]

## Pirâmide Olfativa

- **Saída:** [[note-almond]], [[note-orange-blossom]]
- **Coração:** [[note-balkans-tobacco-absolute]], [[note-rose-absolute]]
- **Fundo:** [[note-tonka-bean-absolute]], [[note-bourbon-vanilla-absolute]], [[note-amberwood]], [[note-amyris]]
