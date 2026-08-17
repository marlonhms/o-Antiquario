---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-torino22
project: o-antiquario
type: fragrance
title: Torino22
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
  locator: https://www.parfumo.com/Perfumes/Xerjoff/torino22
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:saffron
- predicate: has-top-note
  target: antiquario:olfactory-note:eucalyptus
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:clary-sage
- predicate: has-heart-note
  target: antiquario:olfactory-note:mate
- predicate: has-heart-note
  target: antiquario:olfactory-note:gaiac-wood
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:dry-woods
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:fresco
---

# Torino22

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-saffron]], [[note-eucalyptus]], [[Bergamota]]
- **Coração:** [[note-clary-sage]], [[note-mate]], [[note-gaiac-wood]]
- **Fundo:** [[note-musk]], [[note-dry-woods]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Acordes Principais:** [[doce|Doce]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[Fresco|Fresco]]
- **Notas de Saída:** [[note-saffron|Saffron]], [[note-eucalyptus|Eucalyptus]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-clary-sage|Clary sage]], [[note-mate|Maté]], [[note-gaiac-wood|Gaiac wood]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-dry-woods|Dry woods]]
