---
schema_version: 1
id: antiquario:fragrance:parfumo-aldi-hofer-dynamic-style
project: o-antiquario
type: fragrance
title: Dynamic Style
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
  locator: https://www.parfumo.com/Perfumes/Aldi_Hofer/Dynamic_Style
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:aldi-hofer
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:quentin-bisch
---

# Dynamic Style

**Marca:** [[brand-aldi-hofer]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-aldi-hofer|Aldi / Hofer]]
- **Perfumista(s):** [[quentin-bisch|Quentin Bisch]]
- **Acordes Principais:** [[doce|Doce]], [[frutado|Frutado]], [[Fresco|Fresco]]
