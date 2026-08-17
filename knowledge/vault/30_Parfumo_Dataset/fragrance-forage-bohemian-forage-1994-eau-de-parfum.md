---
schema_version: 1
id: antiquario:fragrance:parfumo-forage-bohemian-forage-1994-eau-de-parfum
project: o-antiquario
type: fragrance
title: Bohemian Forage 1994 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Forage/Bohemian_Eau_de_Parfum
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:forage
- predicate: has-top-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
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

# Bohemian Forage 1994 Eau de Parfum

**Marca:** [[brand-forage]]

## Pirâmide Olfativa

- **Saída:** [[note-zimbro]]
- **Coração:** N/A
- **Fundo:** [[Baunilha]], [[note-zimbro]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-forage|Forage]]
- **Perfumista(s):** [[alessandro-gualtieri|Alessandro Gualtieri]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[resinoso|Resinoso]], [[antiquario:accord:couro|Couro]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-zimbro|Zimbro (Juniper Berry)]]
- **Notas de Fundo:** [[Baunilha|Baunilha]], [[note-zimbro|Zimbro (Juniper Berry)]]
