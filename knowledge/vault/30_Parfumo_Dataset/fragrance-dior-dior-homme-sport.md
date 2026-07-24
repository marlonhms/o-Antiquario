---
schema_version: 1
id: antiquario:fragrance:parfumo-dior-dior-homme-sport
project: o-antiquario
type: fragrance
title: "Dior Homme Sport"
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
    target: antiquario:brand:dior
  - predicate: has-top-note
    target: antiquario:olfactory-note:italian-lemon
  - predicate: has-top-note
    target: antiquario:olfactory-note:aldehydes
  - predicate: has-top-note
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-heart-note
    target: antiquario:olfactory-note:elemi-resin
  - predicate: has-heart-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-base-note
    target: antiquario:olfactory-note:frankincense
  - predicate: has-base-note
    target: antiquario:olfactory-note:woods
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
---

# Dior Homme Sport

**Marca:** [[brand-dior]]

## Pirâmide Olfativa

- **Saída:** [[note-italian-lemon]], [[note-aldehydes]], [[note-calabrian-bergamot]]
- **Coração:** [[note-elemi-resin]], [[note-pink-pepper]]
- **Fundo:** [[note-frankincense]], [[note-woods]], [[note-amber]]
