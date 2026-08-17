---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-godolphin
project: o-antiquario
type: fragrance
title: Godolphin
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
  locator: https://www.parfumo.com/Perfumes/Parfums_de_Marly/Godolphin
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:parfums-de-marly
- predicate: has-top-note
  target: antiquario:olfactory-note:saffron
- predicate: has-top-note
  target: antiquario:olfactory-note:cypress
- predicate: has-top-note
  target: antiquario:olfactory-note:thyme
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:white-cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:michele-saramito
---

# Godolphin

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-saffron]], [[note-cypress]], [[note-thyme]]
- **Coração:** [[note-rose]], [[note-iris]], [[note-jasmine]]
- **Fundo:** [[Vetiver]], [[note-white-cedarwood]], [[note-ambar]], [[note-musk]], [[Baunilha]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-parfums-de-marly|Parfums de Marly]]
- **Perfumista(s):** [[michele-saramito|Michele Saramito]]
- **Acordes Principais:** [[antiquario:accord:couro|Couro]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[frutado|Frutado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-saffron|Saffron]], [[note-cypress|Cypress]], [[note-thyme|Thyme]]
- **Notas de Coração:** [[note-rose|Rose]], [[note-iris|Iris]], [[note-jasmine|Jasmine]]
- **Notas de Fundo:** [[note-vetiver|Vetiver]], [[note-white-cedarwood|White cedarwood]], [[note-ambar|Âmbar (Amber)]], [[note-musk|Musk]], [[Baunilha|Baunilha]]
