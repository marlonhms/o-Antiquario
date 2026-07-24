---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-accento-overdose
project: o-antiquario
type: fragrance
title: "Accento Overdose"
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
    target: antiquario:olfactory-note:fruity-notes
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-notes
  - predicate: has-heart-note
    target: antiquario:olfactory-note:eucalyptus
  - predicate: has-heart-note
    target: antiquario:olfactory-note:stone-pine
  - predicate: has-base-note
    target: antiquario:olfactory-note:egyptian-jasmine
  - predicate: has-base-note
    target: antiquario:olfactory-note:lily-of-the-valley
  - predicate: has-base-note
    target: antiquario:olfactory-note:bulgarian-rose
---

# Accento Overdose

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-fruity-notes]], [[note-green-notes]]
- **Coração:** [[note-eucalyptus]], [[note-stone-pine]]
- **Fundo:** [[note-egyptian-jasmine]], [[note-lily-of-the-valley]], [[note-bulgarian-rose]]
