---
schema_version: 1
id: antiquario:fragrance:parfumo-al-battash-adventure-story
project: o-antiquario
type: fragrance
title: Adventure Story
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
  locator: https://www.parfumo.com/Perfumes/Al_Battash/Adventure_Story
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:al-battash
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:frank-voelkl
- predicate: created-by
  target: antiquario:perfumer:firmenich
---

# Adventure Story

**Marca:** [[brand-al-battash]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-al-battash|Al Battash]]
- **Perfumista(s):** [[frank-voelkl|Frank Voelkl]], [[firmenich|Firmenich]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[verde|Verde]], [[antiquario:accord:couro|Couro]], [[Fresco|Fresco]]
