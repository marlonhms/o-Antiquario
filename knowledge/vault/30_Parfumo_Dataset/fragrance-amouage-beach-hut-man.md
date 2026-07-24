---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-beach-hut-man
project: o-antiquario
type: fragrance
title: "Beach Hut Man"
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
    target: antiquario:olfactory-note:mint
  - predicate: has-top-note
    target: antiquario:olfactory-note:galbanum
  - predicate: has-top-note
    target: antiquario:olfactory-note:laranja-blossom
  - predicate: has-heart-note
    target: antiquario:olfactory-note:ivy
  - predicate: has-heart-note
    target: antiquario:olfactory-note:moss
  - predicate: has-heart-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:dry-woods
  - predicate: has-base-note
    target: antiquario:olfactory-note:myrrh
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# Beach Hut Man

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-mint]], [[note-galbanum]], [[note-orange-blossom]]
- **Coração:** [[note-ivy]], [[note-moss]], [[Vetiver]]
- **Fundo:** [[note-dry-woods]], [[note-myrrh]], [[note-patchouli]]
