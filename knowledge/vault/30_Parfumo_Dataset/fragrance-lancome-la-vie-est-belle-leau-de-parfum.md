---
schema_version: 1
id: antiquario:fragrance:parfumo-lancome-la-vie-est-belle-leau-de-parfum
project: o-antiquario
type: fragrance
title: "La Vie est Belle L'Eau de Parfum"
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
    target: antiquario:brand:lancome
  - predicate: has-top-note
    target: antiquario:olfactory-note:blackcurrant
  - predicate: has-top-note
    target: antiquario:olfactory-note:pear
  - predicate: has-heart-note
    target: antiquario:olfactory-note:iris
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine
  - predicate: has-heart-note
    target: antiquario:olfactory-note:orange-blossom
  - predicate: has-base-note
    target: antiquario:olfactory-note:praline
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
---

# La Vie est Belle L'Eau de Parfum

**Marca:** [[brand-lancome]]

## Pirâmide Olfativa

- **Saída:** [[note-blackcurrant]], [[note-pear]]
- **Coração:** [[note-iris]], [[note-jasmine]], [[note-orange-blossom]]
- **Fundo:** [[note-praline]], [[note-tonka-bean]], [[note-patchouli]], [[Baunilha]]
