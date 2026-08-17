---
schema_version: 1
id: antiquario:fragrance:parfumo-hugo-boss-the-scent-for-him-hugo-boss-2015-eau-de-toilette
project: o-antiquario
type: fragrance
title: The Scent for Him Hugo Boss 2015 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Hugo_Boss/The_Scent_Eau_de_Toilette
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:hugo-boss
- predicate: has-top-note
  target: antiquario:olfactory-note:ginger
- predicate: has-heart-note
  target: antiquario:olfactory-note:maninka-fruit
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:bruno-jovanovic
---

# The Scent for Him Hugo Boss 2015 Eau de Toilette

**Marca:** [[brand-hugo-boss]]

## Pirâmide Olfativa

- **Saída:** [[note-ginger]]
- **Coração:** [[note-maninka-fruit]], [[note-lavender]]
- **Fundo:** [[note-leather]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-hugo-boss|Hugo Boss]]
- **Perfumista(s):** [[bruno-jovanovic|Bruno Jovanovic]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[especiado|Especiado]], [[doce|Doce]], [[antiquario:accord:couro|Couro]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-ginger|Ginger]]
- **Notas de Coração:** [[note-maninka-fruit|Maninka fruit]], [[note-lavender|Lavender]]
- **Notas de Fundo:** [[note-leather|Leather]]
