---
schema_version: 1
id: antiquario:fragrance:parfumo-al-haramain-laventure
project: o-antiquario
type: fragrance
title: L'Aventure
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
  locator: https://www.parfumo.com/Perfumes/Al_Haramain/L_Aventure
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:al-haramain
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:elemi-resin
- predicate: has-heart-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedro-notes
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:defumado
---

# L'Aventure

**Marca:** [[brand-al-haramain]]

## Pirâmide Olfativa

- **Saída:** [[note-limao-siciliano]], [[Bergamota]], [[note-elemi-resin]]
- **Coração:** [[note-lily-of-the-valley]], [[note-woody-notes]], [[note-jasmine]]
- **Fundo:** [[note-ambar]], [[note-musk]], [[note-patchouli]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-al-haramain|Al Haramain / الحرمين]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[frutado|Frutado]], [[Amadeirado|Amadeirado]], [[defumado|Defumado]]
- **Notas de Saída:** [[note-limao-siciliano|Limão Siciliano]], [[Bergamota|Bergamota]], [[note-elemi-resin|Elemi resin]]
- **Notas de Coração:** [[note-lily-of-the-valley|Lily of the valley]], [[note-woody-notes|Woody notes]], [[note-jasmine|Jasmine]]
- **Notas de Fundo:** [[note-ambar|Âmbar (Amber)]], [[note-musk|Musk]], [[note-patchouli|Patchouli]]
