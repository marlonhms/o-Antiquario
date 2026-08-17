---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-perseus
project: o-antiquario
type: fragrance
title: Perseus
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
  locator: https://www.parfumo.com/Perfumes/Parfums_de_Marly/perseus
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:parfums-de-marly
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:blackcurrant-bud
- predicate: has-heart-note
  target: antiquario:olfactory-note:green-mandarin-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-heart-note
  target: antiquario:olfactory-note:geranium
- predicate: has-base-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-base-note
  target: antiquario:olfactory-note:cashmere-wood
- predicate: has-base-note
  target: antiquario:olfactory-note:dry-woods
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:verde
---

# Perseus

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-grapefruit]], [[Bergamota]], [[note-blackcurrant-bud]]
- **Coração:** [[note-green-mandarin-orange]], [[Vetiver]], [[note-geranium]]
- **Fundo:** [[note-ambergris]], [[note-cashmere-wood]], [[note-dry-woods]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-parfums-de-marly|Parfums de Marly]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]], [[frutado|Frutado]], [[verde|Verde]]
- **Notas de Saída:** [[note-grapefruit|Grapefruit]], [[Bergamota|Bergamota]], [[note-blackcurrant-bud|Blackcurrant bud]]
- **Notas de Coração:** [[note-green-mandarin-orange|Green mandarin orange]], [[note-vetiver|Vetiver]], [[note-geranium|Geranium]]
- **Notas de Fundo:** [[note-ambergris|Ambergris]], [[note-cashmere-wood|Cashmere wood]], [[note-dry-woods|Dry woods]]
