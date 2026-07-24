---
schema_version: 1
id: antiquario:fragrance:parfumo-giorgio-armani-armani-code-profumo
project: o-antiquario
type: fragrance
title: "Armani Code Profumo"
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
    target: antiquario:brand:giorgio-armani
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-mandarin-orange
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-apple
  - predicate: has-heart-note
    target: antiquario:olfactory-note:nutmeg
  - predicate: has-heart-note
    target: antiquario:olfactory-note:orange-blossom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:leather
---

# Armani Code Profumo

**Marca:** [[brand-giorgio-armani]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-green-mandarin-orange]], [[note-green-apple]]
- **Coração:** [[note-nutmeg]], [[note-orange-blossom]], [[note-lavender]]
- **Fundo:** [[note-tonka-bean]], [[note-amber]], [[note-leather]]
