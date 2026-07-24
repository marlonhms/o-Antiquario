---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-decas
project: o-antiquario
type: fragrance
title: "Decas"
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
    target: antiquario:brand:xerjoff
  - predicate: has-top-note
    target: antiquario:olfactory-note:calabrian-mandarin-orange
  - predicate: has-top-note
    target: antiquario:olfactory-note:tuberose
  - predicate: has-top-note
    target: antiquario:olfactory-note:tobacco
  - predicate: has-heart-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-heart-note
    target: antiquario:olfactory-note:florentine-iris
  - predicate: has-heart-note
    target: antiquario:olfactory-note:opoponax
  - predicate: has-base-note
    target: antiquario:olfactory-note:balsam
  - predicate: has-base-note
    target: antiquario:olfactory-note:musk
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla
---

# Decas

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-mandarin-orange]], [[note-tuberose]], [[note-tobacco]]
- **Coração:** [[note-benzoin]], [[note-florentine-iris]], [[note-opoponax]]
- **Fundo:** [[note-balsam]], [[note-musk]], [[note-bourbon-vanilla]]
