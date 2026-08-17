---
schema_version: 1
id: antiquario:fragrance:parfumo-mugler-mugler-cologne
project: o-antiquario
type: fragrance
title: Mugler Cologne
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
  locator: https://www.parfumo.com/Perfumes/mugler/Mugler_Cologne
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:mugler
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:alberto-morillas
---

# Mugler Cologne

**Marca:** [[brand-mugler]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-mugler|Mugler]]
- **Perfumista(s):** [[alberto-morillas|Alberto Morillas]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Citricos|Cítricos]], [[verde|Verde]], [[floral|Floral]]
