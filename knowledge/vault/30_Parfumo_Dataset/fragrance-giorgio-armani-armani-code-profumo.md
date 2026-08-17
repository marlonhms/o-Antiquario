---
schema_version: 1
id: antiquario:fragrance:parfumo-giorgio-armani-armani-code-profumo
project: o-antiquario
type: fragrance
title: Armani Code Profumo
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
  locator: https://www.parfumo.com/Perfumes/Giorgio_Armani/Armani_Code_Profumo
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:giorgio-armani
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:green-mandarin-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:green-apple
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-heart-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:amadeirado
---

# Armani Code Profumo

**Marca:** [[brand-giorgio-armani]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-green-mandarin-orange]], [[note-green-apple]]
- **Coração:** [[note-nutmeg]], [[note-orange-blossom]], [[note-lavender]]
- **Fundo:** [[note-tonka-bean]], [[note-ambar]], [[note-leather]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-giorgio-armani|Giorgio Armani]]
- **Acordes Principais:** [[doce|Doce]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[gourmand|Gourmand]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[note-green-mandarin-orange|Green mandarin orange]], [[note-green-apple|Green apple]]
- **Notas de Coração:** [[note-nutmeg|Nutmeg]], [[note-orange-blossom|Orange blossom]], [[note-lavender|Lavender]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-ambar|Âmbar (Amber)]], [[note-leather|Leather]]
