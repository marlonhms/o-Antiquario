---
schema_version: 1
id: antiquario:fragrance:parfumo-davidoff-cool-water-intense
project: o-antiquario
type: fragrance
title: "Cool Water Intense"
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
    target: antiquario:brand:davidoff
  - predicate: has-top-note
    target: antiquario:olfactory-note:green-mandarin-orange
  - predicate: has-heart-note
    target: antiquario:olfactory-note:coconut-water
  - predicate: has-base-note
    target: antiquario:olfactory-note:amber
---

# Cool Water Intense

**Marca:** [[brand-davidoff]]

## Pirâmide Olfativa

- **Saída:** [[note-green-mandarin-orange]]
- **Coração:** [[note-coconut-water]]
- **Fundo:** [[note-amber]]
