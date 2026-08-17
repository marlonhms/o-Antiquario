---
schema_version: 1
id: antiquario:fragrance:parfumo-matiere-premiere-falcon-leather-matiere-premiere-2019-eau-de-parfum
project: o-antiquario
type: fragrance
title: Falcon Leather Matière Première 2019 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/matiere-premiere/falcon-leather
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:matiere-premiere
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:aurelien-guichard
---

# Falcon Leather Matière Première 2019 Eau de Parfum

**Marca:** [[brand-matiere-premiere]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-matiere-premiere|Matière Première]]
- **Perfumista(s):** [[aurelien-guichard|Aurélien Guichard]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[antiquario:accord:couro|Couro]], [[especiado|Especiado]], [[defumado|Defumado]], [[resinoso|Resinoso]], [[Amadeirado|Amadeirado]]
