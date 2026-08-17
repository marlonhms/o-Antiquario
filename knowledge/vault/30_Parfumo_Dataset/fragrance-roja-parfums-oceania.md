---
schema_version: 1
id: antiquario:fragrance:parfumo-roja-parfums-oceania
project: o-antiquario
type: fragrance
title: Oceania
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
  locator: https://www.parfumo.com/Perfumes/Roja_Parfums/oceania
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:roja-parfums
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:litsea-cubeba
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:lime
- predicate: has-top-note
  target: antiquario:olfactory-note:mandarin-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:provencal-lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:rosemary
- predicate: has-top-note
  target: antiquario:olfactory-note:thyme
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine-sambac
- predicate: has-heart-note
  target: antiquario:olfactory-note:geranium
- predicate: has-heart-note
  target: antiquario:olfactory-note:grasse-jasmine
- predicate: has-heart-note
  target: antiquario:olfactory-note:violet
- predicate: has-heart-note
  target: antiquario:olfactory-note:ylang-ylang
- predicate: has-base-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-base-note
  target: antiquario:olfactory-note:moss
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:iris
- predicate: has-base-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:galbanum
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:aquatico
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:roja-dove
---

# Oceania

**Marca:** [[brand-roja-parfums]]

## Pirâmide Olfativa

- **Saída:** [[note-limao-siciliano]], [[note-litsea-cubeba]], [[Bergamota]], [[note-grapefruit]], [[note-lime]], [[note-mandarin-orange]], [[note-provencal-lavender]], [[note-rosemary]], [[note-thyme]]
- **Coração:** [[note-jasmine-sambac]], [[note-geranium]], [[note-grasse-jasmine]], [[note-violet]], [[note-ylang-ylang]]
- **Fundo:** [[note-cedarwood]], [[note-zimbro]], [[note-moss]], [[note-musk]], [[Vetiver]], [[note-benzoin]], [[note-iris]], [[note-labdanum]], [[note-sandalo]], [[Baunilha]], [[note-galbanum]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-roja-parfums|Roja Parfums]]
- **Perfumista(s):** [[roja-dove|Roja Dove]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[aquatico|Aquático]], [[floral|Floral]]
- **Notas de Saída:** [[note-limao-siciliano|Limão Siciliano]], [[note-litsea-cubeba|Litsea cubeba]], [[Bergamota|Bergamota]], [[note-grapefruit|Grapefruit]], [[note-lime|Lime]], [[note-mandarin-orange|Mandarin orange]], [[note-provencal-lavender|Provençal lavender]], [[note-rosemary|Rosemary]], [[note-thyme|Thyme]]
- **Notas de Coração:** [[note-jasmine-sambac|Jasmine sambac]], [[note-geranium|Geranium]], [[note-grasse-jasmine|Grasse jasmine]], [[note-violet|Violet]], [[note-ylang-ylang|Ylang Ylang]]
- **Notas de Fundo:** [[note-cedarwood|Cedarwood]], [[note-zimbro|Zimbro (Juniper Berry)]], [[note-moss|Moss]], [[note-musk|Musk]], [[note-vetiver|Vetiver]], [[note-benzoin|Benzoin]], [[note-iris|Iris]], [[note-labdanum|Labdanum]], [[note-sandalo|Sândalo (Sandalwood)]], [[Baunilha|Baunilha]], [[note-galbanum|Galbanum]]
