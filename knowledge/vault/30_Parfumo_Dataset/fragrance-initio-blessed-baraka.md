---
schema_version: 1
id: antiquario:fragrance:parfumo-initio-blessed-baraka
project: o-antiquario
type: fragrance
title: Blessed Baraka
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
  locator: https://www.parfumo.com/Perfumes/Initio/Blessed_Baraka
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:initio
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
---

# Blessed Baraka

**Marca:** [[brand-initio]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-initio|Initio]]
- **Acordes Principais:** [[doce|Doce]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[ambarado|Ambarado]]
