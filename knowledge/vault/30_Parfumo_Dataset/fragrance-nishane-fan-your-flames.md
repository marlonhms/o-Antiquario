---
schema_version: 1
id: antiquario:fragrance:parfumo-nishane-fan-your-flames
project: o-antiquario
type: fragrance
title: Fan Your Flames
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
  locator: https://www.parfumo.com/Perfumes/Nishane/Fan_Your_Flames
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:nishane
- predicate: has-top-note
  target: antiquario:olfactory-note:coconut
- predicate: has-top-note
  target: antiquario:olfactory-note:rum
- predicate: has-heart-note
  target: antiquario:olfactory-note:tobacco
- predicate: has-heart-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-base-note
  target: antiquario:olfactory-note:chinese-toon
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:gourmand
---

# Fan Your Flames

**Marca:** [[brand-nishane]]

## Pirâmide Olfativa

- **Saída:** [[note-coconut]], [[note-rum]]
- **Coração:** [[note-tobacco]], [[note-tonka-bean]]
- **Fundo:** [[note-oakmoss]], [[note-chinese-toon]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-nishane|Nishane]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[doce|Doce]], [[defumado|Defumado]], [[gourmand|Gourmand]]
- **Notas de Saída:** [[note-coconut|Coconut]], [[note-rum|Rum]]
- **Notas de Coração:** [[note-tobacco|Tobacco]], [[note-tonka-bean|Tonka bean]]
- **Notas de Fundo:** [[note-oakmoss|Oakmoss]], [[note-chinese-toon|Chinese toon]]
