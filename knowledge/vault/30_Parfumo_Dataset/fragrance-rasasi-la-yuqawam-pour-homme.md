---
schema_version: 1
id: antiquario:fragrance:parfumo-rasasi-la-yuqawam-pour-homme
project: o-antiquario
type: fragrance
title: La Yuqawam pour Homme
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
  locator: https://www.parfumo.com/Perfumes/Rasasi/La_Yuqawam_pour_Homme
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:rasasi
- predicate: has-top-note
  target: antiquario:olfactory-note:blue-blossoms
- predicate: has-top-note
  target: antiquario:olfactory-note:rose
- predicate: has-top-note
  target: antiquario:olfactory-note:saffron
- predicate: has-top-note
  target: antiquario:olfactory-note:geranium
- predicate: has-heart-note
  target: antiquario:olfactory-note:yemenite-frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:french-jasmine
- predicate: has-base-note
  target: antiquario:olfactory-note:indian-oud
- predicate: has-base-note
  target: antiquario:olfactory-note:italian-leather
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
---

# La Yuqawam pour Homme

**Marca:** [[brand-rasasi]]

## Pirâmide Olfativa

- **Saída:** [[note-blue-blossoms]], [[note-rose]], [[note-saffron]], [[note-geranium]]
- **Coração:** [[note-yemenite-frankincense]], [[note-french-jasmine]]
- **Fundo:** [[note-indian-oud]], [[note-italian-leather]], [[note-ambar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-rasasi|Rasasi]]
- **Acordes Principais:** [[antiquario:accord:couro|Couro]], [[defumado|Defumado]], [[frutado|Frutado]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-blue-blossoms|Blue blossoms]], [[note-rose|Rose]], [[note-saffron|Saffron]], [[note-geranium|Geranium]]
- **Notas de Coração:** [[note-yemenite-frankincense|Yemenite frankincense]], [[note-french-jasmine|French jasmine]]
- **Notas de Fundo:** [[note-indian-oud|Indian oud]], [[note-italian-leather|Italian leather]], [[note-ambar|Âmbar (Amber)]]
