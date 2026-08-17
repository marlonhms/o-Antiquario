---
schema_version: 1
id: antiquario:fragrance:parfumo-creed-original-vetiver
project: o-antiquario
type: fragrance
title: Original Vetiver
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
  locator: https://www.parfumo.com/Perfumes/Creed/Original_Vetiver
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:creed
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:vetiver-leaf
- predicate: has-top-note
  target: antiquario:olfactory-note:bitter-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:mandarin-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:coriander
- predicate: has-heart-note
  target: antiquario:olfactory-note:white-pepper
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
---

# Original Vetiver

**Marca:** [[brand-creed]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]], [[note-vetiver-leaf]], [[note-bitter-orange]], [[note-mandarin-orange]]
- **Coração:** [[note-pink-pepper]], [[note-coriander]], [[note-white-pepper]]
- **Fundo:** [[Vetiver]], [[note-musk]], [[note-ambergris]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-creed|Creed]]
- **Acordes Principais:** [[verde|Verde]], [[Fresco|Fresco]], [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]]
- **Notas de Saída:** [[Bergamota|Bergamota]], [[note-vetiver-leaf|Vetiver leaf]], [[note-bitter-orange|Bitter orange]], [[note-mandarin-orange|Mandarin orange]]
- **Notas de Coração:** [[note-pink-pepper|Pink pepper]], [[note-coriander|Coriander]], [[note-white-pepper|White pepper]]
- **Notas de Fundo:** [[note-vetiver|Vetiver]], [[note-musk|Musk]], [[note-ambergris|Ambergris]], [[note-sandalo|Sândalo (Sandalwood)]]
