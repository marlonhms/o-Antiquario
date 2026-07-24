---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-paradoxe
project: o-antiquario
type: fragrance
title: "Paradoxe"
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
    target: antiquario:brand:prada
  - predicate: has-top-note
    target: antiquario:olfactory-note:pear
  - predicate: has-top-note
    target: antiquario:olfactory-note:tangerine
  - predicate: has-top-note
    target: antiquario:olfactory-note:calabrian-bergamot
  - predicate: has-heart-note
    target: antiquario:olfactory-note:jasmine-sambac-absolute
  - predicate: has-heart-note
    target: antiquario:olfactory-note:tunisian-orange-blossom-absolute
  - predicate: has-heart-note
    target: antiquario:olfactory-note:bitter-orange-blossom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:neroli
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambrofix
  - predicate: has-base-note
    target: antiquario:olfactory-note:bourbon-vanilla
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin-siam
  - predicate: has-base-note
    target: antiquario:olfactory-note:serenolide
---

# Paradoxe

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** [[note-pear]], [[note-tangerine]], [[note-calabrian-bergamot]]
- **Coração:** [[note-jasmine-sambac-absolute]], [[note-tunisian-orange-blossom-absolute]], [[note-bitter-orange-blossom]], [[note-neroli]]
- **Fundo:** [[note-ambrofix]], [[note-bourbon-vanilla]], [[note-benzoin-siam]], [[note-serenolide]]
