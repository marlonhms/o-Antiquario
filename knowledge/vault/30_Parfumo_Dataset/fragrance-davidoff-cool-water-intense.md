---
schema_version: 1
id: antiquario:fragrance:parfumo-davidoff-cool-water-intense
project: o-antiquario
type: fragrance
title: Cool Water Intense
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
  locator: https://www.parfumo.com/Perfumes/Davidoff/Cool_Water_Intense
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:davidoff
- predicate: has-top-note
  target: antiquario:olfactory-note:green-mandarin-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:coconut-water
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: created-by
  target: antiquario:perfumer:annick-menardo
---

# Cool Water Intense

**Marca:** [[brand-davidoff]]

## Pirâmide Olfativa

- **Saída:** [[note-green-mandarin-orange]]
- **Coração:** [[note-coconut-water]]
- **Fundo:** [[note-ambar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-davidoff|Davidoff]]
- **Perfumista(s):** [[annick-menardo|Annick Ménardo]]
- **Acordes Principais:** [[Fresco|Fresco]], [[doce|Doce]], [[frutado|Frutado]], [[aquatico|Aquático]]
- **Notas de Saída:** [[note-green-mandarin-orange|Green mandarin orange]]
- **Notas de Coração:** [[note-coconut-water|Coconut water]]
- **Notas de Fundo:** [[note-ambar|Âmbar (Amber)]]
