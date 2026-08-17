---
schema_version: 1
id: antiquario:fragrance:parfumo-orto-parisi-megamare
project: o-antiquario
type: fragrance
title: Megamare
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
  locator: https://www.parfumo.com/Perfumes/Orto_Parisi/Megamare
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:orto-parisi
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:alessandro-gualtieri
---

# Megamare

**Marca:** [[brand-orto-parisi]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-orto-parisi|Orto Parisi]]
- **Perfumista(s):** [[alessandro-gualtieri|Alessandro Gualtieri]]
- **Acordes Principais:** [[aquatico|Aquático]], [[especiado|Especiado]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]]
