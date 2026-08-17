---
schema_version: 1
id: antiquario:fragrance:parfumo-parfums-de-marly-kalan
project: o-antiquario
type: fragrance
title: Kalan
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
  locator: https://www.parfumo.com/Perfumes/Parfums_de_Marly/kalan
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:parfums-de-marly
- predicate: has-top-note
  target: antiquario:olfactory-note:blood-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:spices
- predicate: has-top-note
  target: antiquario:olfactory-note:black-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:laranja-blossom-absolute
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:solar-note
- predicate: has-base-note
  target: antiquario:olfactory-note:roasted-tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:precious-woods
- predicate: has-base-note
  target: antiquario:olfactory-note:moss
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:ambarado
---

# Kalan

**Marca:** [[brand-parfums-de-marly]]

## Pirâmide Olfativa

- **Saída:** [[note-blood-orange]], [[note-spices]], [[note-black-pepper]]
- **Coração:** [[note-orange-blossom-absolute]], [[note-lavender]], [[note-solar-note]]
- **Fundo:** [[note-roasted-tonka-bean]], [[note-ambar]], [[note-precious-woods]], [[note-moss]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-parfums-de-marly|Parfums de Marly]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[doce|Doce]], [[frutado|Frutado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-blood-orange|Blood orange]], [[note-spices|Spices]], [[note-black-pepper|Black pepper]]
- **Notas de Coração:** [[note-orange-blossom-absolute|Orange blossom absolute]], [[note-lavender|Lavender]], [[note-solar-note|Solar note]]
- **Notas de Fundo:** [[note-roasted-tonka-bean|Roasted tonka bean]], [[note-ambar|Âmbar (Amber)]], [[note-precious-woods|Precious woods]], [[note-moss|Moss]], [[note-sandalo|Sândalo (Sandalwood)]]
