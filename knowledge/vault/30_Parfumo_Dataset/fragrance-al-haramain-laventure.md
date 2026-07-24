---
schema_version: 1
id: antiquario:fragrance:parfumo-al-haramain-laventure
project: o-antiquario
type: fragrance
title: "L'Aventure"
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
    target: antiquario:brand:al-haramain
  - predicate: has-top-note
    target: antiquario:olfactory-note:lemon
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:elemi-resin
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lily-of-the-valley
  - predicate: has-heart-note
    target: antiquario:olfactory-note:woody-notes
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# L'Aventure

**Marca:** [[brand-al-haramain]]

## Pirâmide Olfativa

- **Saída:** [[note-lemon]], [[Bergamota]], [[note-elemi-resin]]
- **Coração:** [[note-lily-of-the-valley]], [[note-woody-notes]], [[note-jasmine]]
- **Fundo:** [[note-amber]], [[note-musk]], [[note-patchouli]]
