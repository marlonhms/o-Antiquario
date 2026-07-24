---
schema_version: 1
id: antiquario:fragrance:parfumo-moschino-toy-boy
project: o-antiquario
type: fragrance
title: "Toy Boy"
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
    target: antiquario:brand:moschino
  - predicate: has-top-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-top-note
    target: antiquario:olfactory-note:pear
  - predicate: has-top-note
    target: antiquario:olfactory-note:clove
  - predicate: has-top-note
    target: antiquario:olfactory-note:elemi-resin
  - predicate: has-top-note
    target: antiquario:olfactory-note:indonesian-nutmeg
  - predicate: has-top-note
    target: antiquario:olfactory-note:italian-bergamot
  - predicate: has-heart-note
    target: antiquario:olfactory-note:rose
  - predicate: has-heart-note
    target: antiquario:olfactory-note:cashmeran
  - predicate: has-heart-note
    target: antiquario:olfactory-note:magnolia
  - predicate: has-heart-note
    target: antiquario:olfactory-note:flax-blossom
  - predicate: has-base-note
    target: antiquario:olfactory-note:ambermax
  - predicate: has-base-note
    target: antiquario:olfactory-note:sylkolide
  - predicate: has-base-note
    target: antiquario:olfactory-note:haitian-vetiver
---

# Toy Boy

**Marca:** [[brand-moschino]]

## Pirâmide Olfativa

- **Saída:** [[note-pink-pepper]], [[note-pear]], [[note-clove]], [[note-elemi-resin]], [[note-indonesian-nutmeg]], [[note-italian-bergamot]]
- **Coração:** [[note-rose]], [[note-cashmeran]], [[note-magnolia]], [[note-flax-blossom]]
- **Fundo:** [[note-ambermax]], [[note-sylkolide]], [[note-haitian-vetiver]]
