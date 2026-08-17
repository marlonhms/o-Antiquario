---
schema_version: 1
id: antiquario:fragrance:parfumo-nautica-voyage-nautica-2006-eau-de-toilette
project: o-antiquario
type: fragrance
title: Voyage Nautica 2006 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Nautica/Voyage_Eau_de_Toilette
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:nautica
- predicate: has-top-note
  target: antiquario:olfactory-note:apple
- predicate: has-top-note
  target: antiquario:olfactory-note:leaves
- predicate: has-heart-note
  target: antiquario:olfactory-note:lotus
- predicate: has-heart-note
  target: antiquario:olfactory-note:mimosa
- predicate: has-base-note
  target: antiquario:olfactory-note:moss
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:maurice-roucel
---

# Voyage Nautica 2006 Eau de Toilette

**Marca:** [[brand-nautica]]

## Pirâmide Olfativa

- **Saída:** [[note-apple]], [[note-leaves]]
- **Coração:** [[note-lotus]], [[note-mimosa]]
- **Fundo:** [[note-moss]], [[note-musk]], [[note-cedar]], [[note-ambar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-nautica|Nautica]]
- **Perfumista(s):** [[maurice-roucel|Maurice Roucel]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[aquatico|Aquático]], [[Fresco|Fresco]], [[verde|Verde]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-apple|Apple]], [[note-leaves|Leaves]]
- **Notas de Coração:** [[note-lotus|Lotus]], [[note-mimosa|Mimosa]]
- **Notas de Fundo:** [[note-moss|Moss]], [[note-musk|Musk]], [[note-cedar|Cedar]], [[note-ambar|Âmbar (Amber)]]
