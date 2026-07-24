---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-sunshine-man
project: o-antiquario
type: fragrance
title: "Sunshine Man"
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
    target: antiquario:brand:amouage
  - predicate: has-top-note
    target: antiquario:olfactory-note:lavender
  - predicate: has-top-note
    target: antiquario:olfactory-note:everlasting-flower
  - predicate: has-top-note
    target: antiquario:olfactory-note:orange-brandy
  - predicate: has-heart-note
    target: antiquario:olfactory-note:clary-sage
  - predicate: has-heart-note
    target: antiquario:olfactory-note:juniper-berry
  - predicate: has-heart-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-base-note
    target: antiquario:olfactory-note:baunilha
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
  - predicate: has-base-note
    target: antiquario:olfactory-note:cedarwood
---

# Sunshine Man

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[note-everlasting-flower]], [[note-orange-brandy]]
- **Coração:** [[note-clary-sage]], [[note-juniper-berry]], [[Bergamota]]
- **Fundo:** [[Baunilha]], [[note-tonka-bean]], [[note-cedarwood]]
