---
schema_version: 1
id: antiquario:fragrance:parfumo-dior-dior-homme-sport
project: o-antiquario
type: fragrance
title: Dior Homme Sport
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
  locator: https://www.parfumo.com/Perfumes/Dior/dior-homme-sport-2021
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:dior
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-lemon
- predicate: has-top-note
  target: antiquario:olfactory-note:aldehydes
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-heart-note
  target: antiquario:olfactory-note:elemi-resin
- predicate: has-heart-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-base-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-base-note
  target: antiquario:olfactory-note:woods
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:francois-demachy
---

# Dior Homme Sport

**Marca:** [[brand-dior]]

## Pirâmide Olfativa

- **Saída:** [[note-italian-lemon]], [[note-aldehydes]], [[note-calabrian-bergamot]]
- **Coração:** [[note-elemi-resin]], [[note-pink-pepper]]
- **Fundo:** [[note-frankincense]], [[note-woods]], [[note-ambar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-dior|Dior]]
- **Perfumista(s):** [[francois-demachy|François Demachy]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-italian-lemon|Italian lemon]], [[note-aldehydes|Aldehydes]], [[note-calabrian-bergamot|Calabrian bergamot]]
- **Notas de Coração:** [[note-elemi-resin|Elemi resin]], [[note-pink-pepper|Pink pepper]]
- **Notas de Fundo:** [[note-frankincense|Frankincense]], [[note-woods|Woods]], [[note-ambar|Âmbar (Amber)]]
