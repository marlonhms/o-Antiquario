---
schema_version: 1
id: antiquario:fragrance:parfumo-dior-eau-sauvage-parfum
project: o-antiquario
type: fragrance
title: "Eau Sauvage Parfum"
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
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-top-note
    target: antiquario:olfactory-note:orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:lavender-absolute
  - predicate: has-heart-note
    target: antiquario:olfactory-note:hedione
  - predicate: has-heart-note
    target: antiquario:olfactory-note:wild-flowers
  - predicate: has-base-note
    target: antiquario:olfactory-note:philippine-elemi
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:labdanum
  - predicate: has-base-note
    target: antiquario:olfactory-note:cinnamon
  - predicate: has-base-note
    target: antiquario:olfactory-note:star-anise
---

# Eau Sauvage Parfum

**Marca:** [[brand-dior]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-orange]]
- **Coração:** [[note-lavender-absolute]], [[note-hedione]], [[note-wild-flowers]]
- **Fundo:** [[note-philippine-elemi]], [[Vetiver]], [[note-labdanum]], [[note-cinnamon]], [[note-star-anise]]
