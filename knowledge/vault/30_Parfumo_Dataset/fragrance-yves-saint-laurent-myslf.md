---
schema_version: 1
id: antiquario:fragrance:parfumo-yves-saint-laurent-myslf
project: o-antiquario
type: fragrance
title: "Myslf"
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
    target: antiquario:brand:yves-saint-laurent
  - predicate: has-top-note
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamot-leaf
  - predicate: has-heart-note
    target: antiquario:olfactory-note:tunisian-orange-blossom-absolute
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambrofix
  - predicate: has-base-note
    target: antiquario:olfactory-note:woods
  - predicate: has-base-note
    target: antiquario:olfactory-note:indonesian-patchouli
---

# Myslf

**Marca:** [[brand-yves-saint-laurent]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-bergamot-leaf]]
- **Coração:** [[note-tunisian-orange-blossom-absolute]]
- **Fundo:** [[note-ambrofix]], [[note-woods]], [[note-indonesian-patchouli]]
