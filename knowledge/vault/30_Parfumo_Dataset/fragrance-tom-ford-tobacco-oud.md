---
schema_version: 1
id: antiquario:fragrance:parfumo-tom-ford-tobacco-oud
project: o-antiquario
type: fragrance
title: Tobacco Oud
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
  locator: https://www.parfumo.com/Perfumes/Tom_Ford/Tobacco_Oud
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:tom-ford
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:olivier-gillotin
---

# Tobacco Oud

**Marca:** [[brand-tom-ford]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-tom-ford|Tom Ford]]
- **Perfumista(s):** [[olivier-gillotin|Olivier Gillotin]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[defumado|Defumado]], [[resinoso|Resinoso]], [[ambarado|Ambarado]]
