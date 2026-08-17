---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-apollonia
project: o-antiquario
type: fragrance
title: Apollonia
aliases: []
external_ids: {}
tags:
- perfume
- parfumo
- draft
source_ids:
- parfumo_dataset
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: Fragrância extraída do Parfumo Fragrance Dataset (TidyTuesday).
evidence:
- source_id: parfumo_dataset
  kind: open_source
  license: CC0-1.0
  confidence: medium
  claim_scope: Identidade e campos olfativos estruturados disponíveis no registro
    do dataset.
  locator: https://www.parfumo.com/Perfumes/Xerjoff/apollonia
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:white-blossoms
- predicate: has-heart-note
  target: antiquario:olfactory-note:orris-butter
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:doce
---

# Apollonia

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-white-blossoms]]
- **Coração:** [[note-orris-butter]]
- **Fundo:** [[note-white-musk]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Acordes Principais:** [[Atalcado|Atalcado]], [[floral|Floral]], [[Fresco|Fresco]], [[doce|Doce]]
- **Notas de Saída:** [[note-white-blossoms|White blossoms]]
- **Notas de Coração:** [[note-orris-butter|Orris butter]]
- **Notas de Fundo:** [[note-white-musk|White Musk]]
