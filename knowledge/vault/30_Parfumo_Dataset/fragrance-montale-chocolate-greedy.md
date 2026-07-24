---
schema_version: 1
id: antiquario:fragrance:parfumo-montale-chocolate-greedy
project: o-antiquario
type: fragrance
title: "Chocolate Greedy"
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
    target: antiquario:brand:montale
  - predicate: has-top-note
    target: antiquario:olfactory-note:dried-fruits
  - predicate: has-top-note
    target: antiquario:olfactory-note:bitter-orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cocoa
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla
---

# Chocolate Greedy

**Marca:** [[brand-montale]]

## Pirâmide Olfativa

- **Saída:** [[note-dried-fruits]], [[note-bitter-orange]]
- **Coração:** [[note-cocoa]]
- **Fundo:** [[note-bourbon-vanilla]]
