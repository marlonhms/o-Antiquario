---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-lhomme-leau
project: o-antiquario
type: fragrance
title: L'Homme L'Eau
aliases: []
external_ids: {}
tags:
- perfume
- parfumo
- draft
source_ids:
- parfumo_dataset
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: Fragrância extraída do Parfumo Fragrance Dataset (TidyTuesday).
evidence:
- source_id: parfumo_dataset
  kind: open_source
  license: CC0-1.0
  confidence: medium
  claim_scope: Estrutura da pirâmide olfativa
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:prada
- predicate: has-top-note
  target: antiquario:olfactory-note:ginger
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-top-note
  target: antiquario:olfactory-note:white-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:cedar
- predicate: has-heart-note
  target: antiquario:olfactory-note:spices
- predicate: has-heart-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-heart-note
  target: antiquario:olfactory-note:white-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
---

# L'Homme L'Eau

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** [[note-ginger]], [[Bergamota]], [[note-violet-leaf]], [[note-white-pepper]], [[note-cedar]]
- **Coração:** [[note-spices]], [[note-violet-leaf]], [[note-white-pepper]], [[note-cedar]]
- **Fundo:** [[note-tonka-bean]], [[note-cedar]]
