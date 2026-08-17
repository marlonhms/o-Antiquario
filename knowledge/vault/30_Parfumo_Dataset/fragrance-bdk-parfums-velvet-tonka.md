---
schema_version: 1
id: antiquario:fragrance:parfumo-bdk-parfums-velvet-tonka
project: o-antiquario
type: fragrance
title: Velvet Tonka
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
  locator: https://www.parfumo.com/Perfumes/bdk_Parfums/velvet-tonka
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:bdk-parfums
- predicate: has-top-note
  target: antiquario:olfactory-note:almond
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-heart-note
  target: antiquario:olfactory-note:balkans-tobacco-absolute
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:amberwood
- predicate: has-base-note
  target: antiquario:olfactory-note:amyris
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: created-by
  target: antiquario:perfumer:alexandra-carlin
---

# Velvet Tonka

**Marca:** [[brand-bdk-parfums]]

## Pirâmide Olfativa

- **Saída:** [[note-almond]], [[note-orange-blossom]]
- **Coração:** [[note-balkans-tobacco-absolute]], [[note-rose-absolute]]
- **Fundo:** [[note-tonka-bean-absolute]], [[note-bourbon-vanilla-absolute]], [[note-amberwood]], [[note-amyris]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-bdk-parfums|bdk Parfums]]
- **Perfumista(s):** [[alexandra-carlin|Alexandra Carlin]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[Atalcado|Atalcado]]
- **Notas de Saída:** [[note-almond|Almond]], [[note-orange-blossom|Orange blossom]]
- **Notas de Coração:** [[note-balkans-tobacco-absolute|Balkans tobacco absolute]], [[note-rose-absolute|Rose absolute]]
- **Notas de Fundo:** [[note-tonka-bean-absolute|Tonka bean absolute]], [[note-bourbon-vanilla-absolute|Bourbon vanilla absolute]], [[note-amberwood|Amberwood]], [[note-amyris|Amyris]]
