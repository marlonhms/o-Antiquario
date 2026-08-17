---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-fars
project: o-antiquario
type: fragrance
title: Fars
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
  locator: https://www.parfumo.com/Perfumes/Xerjoff/fars
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:cade-juniper
- predicate: has-top-note
  target: antiquario:olfactory-note:french-lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-bergamot
- predicate: has-heart-note
  target: antiquario:olfactory-note:egyptian-geranium
- predicate: has-heart-note
  target: antiquario:olfactory-note:atlas-cedar
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:haitian-vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:white-oud
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:resinoso
---

# Fars

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-cade-juniper]], [[note-french-lavender]], [[note-italian-bergamot]]
- **Coração:** [[note-egyptian-geranium]], [[note-atlas-cedar]], [[note-jasmine-absolute]]
- **Fundo:** [[note-ambar]], [[note-haitian-vetiver]], [[note-sandalo]], [[note-white-oud]], [[note-patchouli]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[floral|Floral]], [[ambarado|Ambarado]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-cade-juniper|Cade juniper]], [[note-french-lavender|French lavender]], [[note-italian-bergamot|Italian bergamot]]
- **Notas de Coração:** [[note-egyptian-geranium|Egyptian geranium]], [[note-atlas-cedar|Atlas cedar]], [[note-jasmine-absolute|Jasmine absolute]]
- **Notas de Fundo:** [[note-ambar|Âmbar (Amber)]], [[note-haitian-vetiver|Haitian vetiver]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-white-oud|White oud]], [[note-patchouli|Patchouli]]
