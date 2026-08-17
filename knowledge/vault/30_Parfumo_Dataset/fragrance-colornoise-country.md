---
schema_version: 1
id: antiquario:fragrance:parfumo-colornoise-country
project: o-antiquario
type: fragrance
title: Country.
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
  locator: https://www.parfumo.com/Perfumes/Colornoise/Country_
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:colornoise
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:green-leaves
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:gymwear
- predicate: has-heart-note
  target: antiquario:olfactory-note:musk
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-heart-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-heart-note
  target: antiquario:olfactory-note:raspberry
- predicate: has-base-note
  target: antiquario:olfactory-note:coffee
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:maurice-roucel
---

# Country.

**Marca:** [[brand-colornoise]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[note-green-leaves]], [[Bergamota]], [[note-gymwear]]
- **Coração:** [[note-musk]], [[note-jasmine]], [[note-lily-of-the-valley]], [[note-raspberry]]
- **Fundo:** [[note-coffee]], [[Baunilha]], [[note-ambar]], [[note-patchouli]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-colornoise|Colornoise]]
- **Perfumista(s):** [[maurice-roucel|Maurice Roucel]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[Atalcado|Atalcado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-lavender|Lavender]], [[note-green-leaves|Green leaves]], [[Bergamota|Bergamota]], [[note-gymwear|Gymwear]]
- **Notas de Coração:** [[note-musk|Musk]], [[note-jasmine|Jasmine]], [[note-lily-of-the-valley|Lily of the valley]], [[note-raspberry|Raspberry]]
- **Notas de Fundo:** [[note-coffee|Coffee]], [[Baunilha|Baunilha]], [[note-ambar|Âmbar (Amber)]], [[note-patchouli|Patchouli]], [[note-sandalo|Sândalo (Sandalwood)]]
