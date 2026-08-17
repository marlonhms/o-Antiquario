---
schema_version: 1
id: antiquario:fragrance:parfumo-nasomatto-duro-nasomatto-2007-extrait-de-parfum
project: o-antiquario
type: fragrance
title: Duro Nasomatto 2007 Extrait de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Nasomatto/Duro
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:nasomatto
- predicate: has-concentration
  target: antiquario:concentration:extrait-de-parfum
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:alessandro-gualtieri
---

# Duro Nasomatto 2007 Extrait de Parfum

**Marca:** [[brand-nasomatto]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-nasomatto|Nasomatto]]
- **Perfumista(s):** [[alessandro-gualtieri|Alessandro Gualtieri]]
- **Concentração:** [[extrait-de-parfum|Extrait de Parfum]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[resinoso|Resinoso]], [[antiquario:accord:couro|Couro]], [[ambarado|Ambarado]]
