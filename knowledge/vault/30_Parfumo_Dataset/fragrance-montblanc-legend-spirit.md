---
schema_version: 1
id: antiquario:fragrance:parfumo-montblanc-legend-spirit
project: o-antiquario
type: fragrance
title: Legend Spirit
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
  locator: https://www.parfumo.com/Perfumes/Montblanc/Legend_Spirit
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:montblanc
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:aquatic-notes
- predicate: has-heart-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-base-note
  target: antiquario:olfactory-note:cashmere-wood
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:nathalie-lorson
- predicate: created-by
  target: antiquario:perfumer:olivier-cresp
---

# Legend Spirit

**Marca:** [[brand-montblanc]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]], [[note-grapefruit]], [[note-pink-pepper]]
- **Coração:** [[note-aquatic-notes]], [[note-cardamom]], [[note-lavender]]
- **Fundo:** [[note-white-musk]], [[note-cashmere-wood]], [[note-cedar]], [[note-oakmoss]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-montblanc|Montblanc]]
- **Perfumista(s):** [[nathalie-lorson|Nathalie Lorson]], [[olivier-cresp|Olivier Cresp]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Citricos|Cítricos]], [[aquatico|Aquático]], [[frutado|Frutado]]
- **Notas de Saída:** [[Bergamota|Bergamota]], [[note-grapefruit|Grapefruit]], [[note-pink-pepper|Pink pepper]]
- **Notas de Coração:** [[note-aquatic-notes|Aquatic notes]], [[note-cardamom|Cardamom]], [[note-lavender|Lavender]]
- **Notas de Fundo:** [[note-white-musk|White Musk]], [[note-cashmere-wood|Cashmere wood]], [[note-cedar|Cedar]], [[note-oakmoss|Oakmoss]], [[note-sandalo|Sândalo (Sandalwood)]]
