---
schema_version: 1
id: antiquario:fragrance:parfumo-gucci-guilty-absolute-pour-homme
project: o-antiquario
type: fragrance
title: Guilty Absolute pour Homme
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
  locator: https://www.parfumo.com/Perfumes/Gucci/Guilty_Absolute
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:gucci
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:terroso
- predicate: created-by
  target: antiquario:perfumer:alberto-morillas
---

# Guilty Absolute pour Homme

**Marca:** [[brand-gucci]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-gucci|Gucci]]
- **Perfumista(s):** [[alberto-morillas|Alberto Morillas]]
- **Acordes Principais:** [[antiquario:accord:couro|Couro]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[defumado|Defumado]], [[terroso|Terroso]]
