---
schema_version: 1
id: antiquario:fragrance:parfumo-zarkoperfume-the-muse
project: o-antiquario
type: fragrance
title: The Muse
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
  locator: https://www.parfumo.com/Perfumes/Zarko_Perfume/the-muse
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:zarkoperfume
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:zarko-ahlmann-pavlov
---

# The Muse

**Marca:** [[brand-zarkoperfume]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-zarkoperfume|Zarkoperfume]]
- **Perfumista(s):** [[zarko-ahlmann-pavlov|Zarko Ahlmann Pavlov]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Atalcado|Atalcado]], [[floral|Floral]]
