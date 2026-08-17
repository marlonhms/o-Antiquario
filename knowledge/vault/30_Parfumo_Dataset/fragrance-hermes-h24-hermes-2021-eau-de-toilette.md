---
schema_version: 1
id: antiquario:fragrance:parfumo-hermes-h24-hermes-2021-eau-de-toilette
project: o-antiquario
type: fragrance
title: H24 Hermès 2021 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Hermes/h24-eau-de-toilette
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:hermes
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:christine-nagel
---

# H24 Hermès 2021 Eau de Toilette

**Marca:** [[brand-hermes]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-hermes|Hermès]]
- **Perfumista(s):** [[christine-nagel|Christine Nagel]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[Fresco|Fresco]], [[verde|Verde]], [[Citricos|Cítricos]], [[floral|Floral]], [[Amadeirado|Amadeirado]]
