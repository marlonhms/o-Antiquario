---
schema_version: 1
id: antiquario:fragrance:parfumo-m-micallef-desirtoxic
project: o-antiquario
type: fragrance
title: "DesirToxic"
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
    target: antiquario:brand:m-micallef
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:limao-siciliano
  - predicate: has-heart-note
    target: antiquario:olfactory-note:blackcurrant
  - predicate: has-heart-note
    target: antiquario:olfactory-note:hemp
  - predicate: has-heart-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-heart-note
    target: antiquario:olfactory-note:canela
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:moss
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# DesirToxic

**Marca:** [[brand-m-micallef]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[Bergamota]], [[note-limao-siciliano]]
- **Coração:** [[note-blackcurrant]], [[note-hemp]], [[note-tonka-bean]], [[note-canela]]
- **Fundo:** [[note-musk]], [[note-benzoin]], [[note-moss]], [[note-patchouli]]
