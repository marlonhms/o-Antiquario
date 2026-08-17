---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-santal-royal-guerlain-2014-eau-de-parfum
project: o-antiquario
type: fragrance
title: Santal Royal Guerlain 2014 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Guerlain/Santal_Royal
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:guerlain
- predicate: has-top-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-top-note
  target: antiquario:olfactory-note:neroli
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-heart-note
  target: antiquario:olfactory-note:peach
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: created-by
  target: antiquario:perfumer:thierry-wasser
---

# Santal Royal Guerlain 2014 Eau de Parfum

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[note-jasmine]], [[note-neroli]]
- **Coração:** [[note-rose]], [[note-canela]], [[note-peach]]
- **Fundo:** [[note-oud]], [[note-leather]], [[note-sandalo]], [[note-ambar]], [[note-musk]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-guerlain|Guerlain]]
- **Perfumista(s):** [[thierry-wasser|Thierry Wasser]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[ambarado|Ambarado]], [[especiado|Especiado]], [[floral|Floral]], [[antiquario:accord:couro|Couro]]
- **Notas de Saída:** [[note-jasmine|Jasmine]], [[note-neroli|Neroli]]
- **Notas de Coração:** [[note-rose|Rose]], [[note-canela|Canela]], [[note-peach|Peach]]
- **Notas de Fundo:** [[note-oud|Oud]], [[note-leather|Leather]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-ambar|Âmbar (Amber)]], [[note-musk|Musk]]
