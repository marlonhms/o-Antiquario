---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-luna-rossa-carbon
project: o-antiquario
type: fragrance
title: Luna Rossa Carbon
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
  locator: https://www.parfumo.com/Perfumes/Prada/Luna_Rossa_Carbon
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:prada
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:daniela-andrier
---

# Luna Rossa Carbon

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-prada|Prada]]
- **Perfumista(s):** [[daniela-andrier|Daniela Andrier]]
- **Acordes Principais:** [[Fresco|Fresco]], [[especiado|Especiado]], [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]]
