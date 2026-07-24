---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-bois-darmenie
project: o-antiquario
type: fragrance
title: "Bois d'Arménie"
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
    target: antiquario:brand:guerlain
  - predicate: has-top-note
    target: antiquario:olfactory-note:frankincense
  - predicate: has-top-note
    target: antiquario:olfactory-note:iris
  - predicate: has-top-note
    target: antiquario:olfactory-note:pink-pepper
  - predicate: has-heart-note
    target: antiquario:olfactory-note:gaiac-wood
  - predicate: has-heart-note
    target: antiquario:olfactory-note:benzoin
  - predicate: has-heart-note
    target: antiquario:olfactory-note:coriander
  - predicate: has-base-note
    target: antiquario:olfactory-note:copaiba-balsam
  - predicate: has-base-note
    target: antiquario:olfactory-note:patchouli
  - predicate: has-base-note
    target: antiquario:olfactory-note:white-musk
---

# Bois d'Arménie

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[note-frankincense]], [[note-iris]], [[note-pink-pepper]]
- **Coração:** [[note-gaiac-wood]], [[note-benzoin]], [[note-coriander]]
- **Fundo:** [[note-copaiba-balsam]], [[note-patchouli]], [[note-white-musk]]
