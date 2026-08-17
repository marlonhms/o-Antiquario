---
schema_version: 1
id: antiquario:fragrance:parfumo-versace-blue-jeans
project: o-antiquario
type: fragrance
title: Blue Jeans
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
  locator: https://www.parfumo.com/Perfumes/Versace/Blue_Jeans
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:versace
- predicate: has-top-note
  target: antiquario:olfactory-note:citrus-fruits
- predicate: has-top-note
  target: antiquario:olfactory-note:aniseed
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:rosewood
- predicate: has-top-note
  target: antiquario:olfactory-note:basil
- predicate: has-top-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-heart-note
  target: antiquario:olfactory-note:heliotrope
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:cravo-flor
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-heart-note
  target: antiquario:olfactory-note:sage
- predicate: has-heart-note
  target: antiquario:olfactory-note:fir
- predicate: has-heart-note
  target: antiquario:olfactory-note:geranium
- predicate: has-heart-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:iris
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:jacques-cavallier-belletrud
---

# Blue Jeans

**Marca:** [[brand-versace]]

## Pirâmide Olfativa

- **Saída:** [[note-citrus-fruits]], [[note-aniseed]], [[Bergamota]], [[note-rosewood]], [[note-basil]], [[note-zimbro]]
- **Coração:** [[note-heliotrope]], [[note-lavender]], [[note-cravo-flor]], [[note-jasmine]], [[note-sage]], [[note-fir]], [[note-geranium]], [[note-lily-of-the-valley]], [[note-rose]]
- **Fundo:** [[note-tonka-bean]], [[note-ambar]], [[note-cedar]], [[note-iris]], [[note-musk]], [[note-patchouli]], [[note-sandalo]], [[Baunilha]], [[Vetiver]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-versace|Versace]]
- **Perfumista(s):** [[jacques-cavallier-belletrud|Jacques Cavallier-Belletrud]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Citricos|Cítricos]], [[doce|Doce]], [[floral|Floral]]
- **Notas de Saída:** [[note-citrus-fruits|Citrus fruits]], [[note-aniseed|Aniseed]], [[Bergamota|Bergamota]], [[note-rosewood|Rosewood]], [[note-basil|Basil]], [[note-zimbro|Zimbro (Juniper Berry)]]
- **Notas de Coração:** [[note-heliotrope|Heliotrope]], [[note-lavender|Lavender]], [[note-cravo-flor|Cravo-flor]], [[note-jasmine|Jasmine]], [[note-sage|Sage]], [[note-fir|Fir]], [[note-geranium|Geranium]], [[note-lily-of-the-valley|Lily of the valley]], [[note-rose|Rose]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-ambar|Âmbar (Amber)]], [[note-cedar|Cedar]], [[note-iris|Iris]], [[note-musk|Musk]], [[note-patchouli|Patchouli]], [[note-sandalo|Sândalo (Sandalwood)]], [[Baunilha|Baunilha]], [[note-vetiver|Vetiver]]
