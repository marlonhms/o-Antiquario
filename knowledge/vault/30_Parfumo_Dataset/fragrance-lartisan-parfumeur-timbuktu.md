---
schema_version: 1
id: antiquario:fragrance:parfumo-lartisan-parfumeur-timbuktu
project: o-antiquario
type: fragrance
title: "Timbuktu"
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
    target: antiquario:brand:lartisan-parfumeur
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-mango
  - predicate: has-top-note
    target: antiquario:olfactory-note:cardamom
  - predicate: has-top-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:frankincense
  - predicate: has-heart-note
    target: antiquario:olfactory-note:papyrus
  - predicate: has-heart-note
    target: antiquario:olfactory-note:karo-karounde
  - predicate: has-base-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-base-note
    target: antiquario:olfactory-note:myrrh
  - predicate: has-base-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
---

# Timbuktu

**Marca:** [[brand-lartisan-parfumeur]]

## Pirâmide Olfativa

- **Saída:** [[note-green-mango]], [[note-cardamom]], [[note-pink-pepper]]
- **Coração:** [[note-frankincense]], [[note-papyrus]], [[note-karo-karounde]]
- **Fundo:** [[Vetiver]], [[note-myrrh]], [[note-benzoin]], [[note-patchouli]]
