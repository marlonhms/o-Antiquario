---
schema_version: 1
id: antiquario:fragrance:parfumo-fragrance-one-office-for-men
project: o-antiquario
type: fragrance
title: "Office for Men"
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
    target: antiquario:brand:fragrance-one
  - predicate: has-top-note
    target: antiquario:olfactory-note:ambrox
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-top-note
    target: antiquario:olfactory-note:iris
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cachalox
  - predicate: has-heart-note
    target: antiquario:olfactory-note:paradisone
  - predicate: has-heart-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:cedro-notes
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# Office for Men

**Marca:** [[brand-fragrance-one]]

## Pirâmide Olfativa

- **Saída:** [[note-ambrox]], [[Bergamota]], [[note-iris]]
- **Coração:** [[note-cachalox]], [[note-paradisone]], [[note-pink-pepper]]
- **Fundo:** [[note-musk]], [[note-woody-notes]], [[note-patchouli]]
