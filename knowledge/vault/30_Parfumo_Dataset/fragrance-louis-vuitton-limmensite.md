---
schema_version: 1
id: antiquario:fragrance:parfumo-louis-vuitton-limmensite
project: o-antiquario
type: fragrance
title: L'Immensité
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
  locator: https://www.parfumo.com/Perfumes/Louis_Vuitton/L_Immensite
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:louis-vuitton
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:jacques-cavallier-belletrud
---

# L'Immensité

**Marca:** [[brand-louis-vuitton]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-louis-vuitton|Louis Vuitton]]
- **Perfumista(s):** [[jacques-cavallier-belletrud|Jacques Cavallier-Belletrud]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Citricos|Cítricos]], [[especiado|Especiado]], [[aquatico|Aquático]], [[Amadeirado|Amadeirado]]
