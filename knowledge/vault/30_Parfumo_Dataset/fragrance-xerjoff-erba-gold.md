---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-erba-gold
project: o-antiquario
type: fragrance
title: "Erba Gold"
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
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-top-note
    target: antiquario:olfactory-note:ginger
  - predicate: has-top-note
    target: antiquario:olfactory-note:amalfi-lemon
  - predicate: has-top-note
    target: antiquario:olfactory-note:brazilian-orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:melon
  - predicate: has-heart-note
    target: antiquario:olfactory-note:green-apple
  - predicate: has-heart-note
    target: antiquario:olfactory-note:pear
  - predicate: has-heart-note
    target: antiquario:olfactory-note:clove
  - predicate: has-heart-note
    target: antiquario:olfactory-note:guatemala-cardamom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:madagascan-cinnamon
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla
  - predicate: has-base-note
    target: antiquario:olfactory-note:woods
---

# Erba Gold

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-ginger]], [[note-amalfi-lemon]], [[note-brazilian-orange]]
- **Coração:** [[note-melon]], [[note-green-apple]], [[note-pear]], [[note-clove]], [[note-guatemala-cardamom]], [[note-madagascan-cinnamon]]
- **Fundo:** [[note-white-musk]], [[note-amber]], [[note-bourbon-vanilla]], [[note-woods]]
