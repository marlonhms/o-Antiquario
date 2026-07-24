---
schema_version: 1
id: antiquario:fragrance:parfumo-jo-malone-myrrh-tonka
project: o-antiquario
type: fragrance
title: "Myrrh & Tonka"
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
    target: antiquario:brand:jo-malone
  - predicate: has-top-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-heart-note
    target: antiquario:olfactory-note:namibian-myrrh
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:almond
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
---

# Myrrh & Tonka

**Marca:** [[brand-jo-malone]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]]
- **Coração:** [[note-namibian-myrrh]]
- **Fundo:** [[note-tonka-bean]], [[note-almond]], [[Baunilha]]
