---
schema_version: 1
id: antiquario:fragrance:parfumo-jean-paul-gaultier-le-beau
project: o-antiquario
type: fragrance
title: "Le Beau"
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
    target: antiquario:brand:jean-paul-gaultier
  - predicate: has-top-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-heart-note
    target: antiquario:olfactory-note:coconut-palmwood
  - predicate: has-base-note
    target: antiquario:olfactory-note:tonka-bean
---

# Le Beau

**Marca:** [[brand-jean-paul-gaultier]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]]
- **Coração:** [[note-coconut-palmwood]]
- **Fundo:** [[note-tonka-bean]]
