---
schema_version: 1
id: antiquario:fragrance:parfumo-dunhill-icon
project: o-antiquario
type: fragrance
title: "Icon"
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
    target: antiquario:brand:dunhill
  - predicate: has-top-note
    target: antiquario:olfactory-note:neroli-absolute
  - predicate: has-top-note
    target: antiquario:olfactory-note:black-pepper
  - predicate: has-top-note
    target: antiquario:olfactory-note:italian-bergamot
  - predicate: has-top-note
    target: antiquario:olfactory-note:petitgrain
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:juniper-berry
  - predicate: has-heart-note
    target: antiquario:olfactory-note:provencal-lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:sage
  - predicate: has-base-note
    target: antiquario:olfactory-note:oakmoss
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:iris
  - predicate: has-base-note
    target: antiquario:olfactory-note:leather
  - predicate: has-base-note
    target: antiquario:olfactory-note:oud
---

# Icon

**Marca:** [[brand-dunhill]]

## Pirâmide Olfativa

- **Saída:** [[note-neroli-absolute]], [[note-black-pepper]], [[note-italian-bergamot]], [[note-petitgrain]]
- **Coração:** [[note-cardamom]], [[note-juniper-berry]], [[note-provencal-lavender]], [[note-sage]]
- **Fundo:** [[note-oakmoss]], [[Vetiver]], [[note-iris]], [[note-leather]], [[note-oud]]
