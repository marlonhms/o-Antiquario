---
schema_version: 1
id: antiquario:fragrance:parfumo-loccitane-en-provence-eau-des-baux
project: o-antiquario
type: fragrance
title: Eau des Baux
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
  locator: https://www.parfumo.com/Perfumes/LOccitane_en_Provence/Eau_De_Baux
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:loccitane-en-provence
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:cypress
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:karine-dubreuil-sereni
---

# Eau des Baux

**Marca:** [[brand-loccitane-en-provence]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-pink-pepper]]
- **Coração:** [[note-frankincense]], [[note-cypress]]
- **Fundo:** [[Baunilha]], [[note-tonka-bean]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-loccitane-en-provence|L'Occitane en Provence]]
- **Perfumista(s):** [[karine-dubreuil-sereni|Karine Dubreuil-Sereni]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[doce|Doce]], [[defumado|Defumado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[note-pink-pepper|Pink pepper]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[note-cypress|Cypress]]
- **Notas de Fundo:** [[Baunilha|Baunilha]], [[note-tonka-bean|Tonka bean]]
