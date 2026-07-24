---
schema_version: 1
id: antiquario:fragrance:parfumo-comme-des-garcons-wonderwood
project: o-antiquario
type: fragrance
title: "Wonderwood"
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
    target: antiquario:brand:comme-des-garcons
  - predicate: has-top-note
    target: antiquario:olfactory-note:madagascan-pepper
  - predicate: has-top-note
    target: antiquario:olfactory-note:somalian-frankincense
  - predicate: has-top-note
    target: antiquario:olfactory-note:nutmeg
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cashmeran
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cedarwood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:gaiac-wood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:caraway
  - predicate: has-heart-note
    target: antiquario:olfactory-note:christalon
  - predicate: has-base-note
    target: antiquario:olfactory-note:sandalo
  - predicate: has-base-note
    target: antiquario:olfactory-note:javanol
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:oud
---

# Wonderwood

**Marca:** [[brand-comme-des-garcons]]

## Pirâmide Olfativa

- **Saída:** [[note-madagascan-pepper]], [[note-somalian-frankincense]], [[note-nutmeg]], [[Bergamota]]
- **Coração:** [[note-cashmeran]], [[note-cedarwood]], [[note-gaiac-wood]], [[note-caraway]], [[note-christalon]]
- **Fundo:** [[note-sandalo]], [[note-javanol]], [[Vetiver]], [[note-oud]]
