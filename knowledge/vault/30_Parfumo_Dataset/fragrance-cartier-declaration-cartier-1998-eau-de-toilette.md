---
schema_version: 1
id: antiquario:fragrance:parfumo-cartier-declaration-cartier-1998-eau-de-toilette
project: o-antiquario
type: fragrance
title: Déclaration Cartier 1998 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Cartier/Declaration
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:cartier
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:birch-wood
- predicate: has-heart-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedar
- predicate: has-heart-note
  target: antiquario:olfactory-note:mugwort
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: created-by
  target: antiquario:perfumer:jean-claude-ellena
---

# Déclaration Cartier 1998 Eau de Toilette

**Marca:** [[brand-cartier]]

## Pirâmide Olfativa

- **Saída:** [[note-laranja]], [[Bergamota]], [[note-birch-wood]]
- **Coração:** [[note-cardamom]], [[note-cedar]], [[note-mugwort]]
- **Fundo:** [[note-cedar]], [[Vetiver]], [[note-oakmoss]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-cartier|Cartier]]
- **Perfumista(s):** [[jean-claude-ellena|Jean-Claude Ellena]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[Fresco|Fresco]], [[Citricos|Cítricos]], [[verde|Verde]]
- **Notas de Saída:** [[note-laranja|Laranja (Orange)]], [[Bergamota|Bergamota]], [[note-birch-wood|Birch wood]]
- **Notas de Coração:** [[note-cardamom|Cardamom]], [[note-cedar|Cedar]], [[note-mugwort|Mugwort]]
- **Notas de Fundo:** [[note-cedar|Cedar]], [[note-vetiver|Vetiver]], [[note-oakmoss|Oakmoss]]
