---
schema_version: 1
id: antiquario:fragrance:parfumo-halloween-halloween-man-x
project: o-antiquario
type: fragrance
title: Halloween Man X
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
  locator: https://www.parfumo.com/Perfumes/Halloween/Halloween_Man_X
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:halloween
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:provencal-lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:coffee
- predicate: has-heart-note
  target: antiquario:olfactory-note:mineral-notes
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-heart-note
  target: antiquario:olfactory-note:leather
- predicate: has-heart-note
  target: antiquario:olfactory-note:whisky
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:nicolas-beaulieu
---

# Halloween Man X

**Marca:** [[brand-halloween]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-limao-siciliano]], [[note-provencal-lavender]]
- **Coração:** [[note-coffee]], [[note-mineral-notes]], [[note-canela]], [[note-leather]], [[note-whisky]]
- **Fundo:** [[note-tonka-bean]], [[note-ambar]], [[note-frankincense]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-halloween|Halloween]]
- **Perfumista(s):** [[nicolas-beaulieu|Nicolas Beaulieu]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[note-limao-siciliano|Limão Siciliano]], [[note-provencal-lavender|Provençal lavender]]
- **Notas de Coração:** [[note-coffee|Coffee]], [[note-mineral-notes|Mineral notes]], [[note-canela|Canela]], [[note-leather|Leather]], [[note-whisky|Uísque]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-ambar|Âmbar (Amber)]], [[note-frankincense|Frankincense]]
