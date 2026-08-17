---
schema_version: 1
id: antiquario:fragrance:parfumo-initio-paragon
project: o-antiquario
type: fragrance
title: Paragon
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
  locator: https://www.parfumo.com/Perfumes/Initio/paragon
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:initio
- predicate: has-top-note
  target: antiquario:olfactory-note:white-sage
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:ameixa
- predicate: has-heart-note
  target: antiquario:olfactory-note:palo-santo
- predicate: has-heart-note
  target: antiquario:olfactory-note:black-pepper
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
---

# Paragon

**Marca:** [[brand-initio]]

## Pirâmide Olfativa

- **Saída:** [[note-white-sage]], [[note-lavender]], [[Bergamota]]
- **Coração:** [[note-ameixa]], [[note-palo-santo]], [[note-black-pepper]]
- **Fundo:** [[note-sandalo]], [[note-oud]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-initio|Initio]]
- **Acordes Principais:** [[frutado|Frutado]], [[doce|Doce]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-white-sage|White sage]], [[note-lavender|Lavender]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-ameixa|Ameixa (Plum)]], [[note-palo-santo|Palo Santo]], [[note-black-pepper|Black pepper]]
- **Notas de Fundo:** [[note-sandalo|Sândalo (Sandalwood)]], [[note-oud|Oud]]
