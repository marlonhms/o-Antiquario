---
schema_version: 1
id: antiquario:fragrance:parfumo-loccitane-en-provence-eau-des-baux
project: o-antiquario
type: fragrance
title: "Eau des Baux"
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
    target: antiquario:brand:loccitane-en-provence
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:frankincense
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cypress
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
---

# Eau des Baux

**Marca:** [[brand-loccitane-en-provence]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-pink-pepper]]
- **Coração:** [[note-frankincense]], [[note-cypress]]
- **Fundo:** [[Baunilha]], [[note-tonka-bean]]
