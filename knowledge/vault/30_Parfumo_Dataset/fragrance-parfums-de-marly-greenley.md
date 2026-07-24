---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-greenley
project: o-antiquario
type: fragrance
title: "Greenley"
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
    target: antiquario:brand:parfums-de-marly
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-apple
  - predicate: has-top-note
    target: antiquario:olfactory-note:sicilian-bergamot
  - predicate: has-top-note
    target: antiquario:olfactory-note:mandarin-orange
  - predicate: has-top-note
    target: antiquario:olfactory-note:cashmere-wood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:pomarose
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:petitgrain
  - predicate: has-heart-note
    target: antiquario:olfactory-note:violet
  - predicate: has-base-note
    target: antiquario:olfactory-note:amberwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:oakmoss
---

# Greenley

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-green-apple]], [[note-sicilian-bergamot]], [[note-mandarin-orange]], [[note-cashmere-wood]]
- **Coração:** [[note-pomarose]], [[note-cedarwood]], [[note-petitgrain]], [[note-violet]]
- **Fundo:** [[note-amberwood]], [[note-musk]], [[note-oakmoss]]
