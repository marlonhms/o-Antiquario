---
schema_version: 1
id: antiquario:fragrance:parfumo-montale-chocolate-greedy
project: o-antiquario
type: fragrance
title: Chocolate Greedy
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
  locator: https://www.parfumo.com/Perfumes/Montale/Chocolate_Greedy
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:montale
- predicate: has-top-note
  target: antiquario:olfactory-note:dried-fruits
- predicate: has-top-note
  target: antiquario:olfactory-note:bitter-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:cocoa
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:especiado
---

# Chocolate Greedy

**Marca:** [[brand-montale]]

## Pirâmide Olfativa

- **Saída:** [[note-dried-fruits]], [[note-bitter-orange]]
- **Coração:** [[note-cocoa]]
- **Fundo:** [[note-bourbon-vanilla]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-montale|Montale]]
- **Acordes Principais:** [[gourmand|Gourmand]], [[doce|Doce]], [[Atalcado|Atalcado]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-dried-fruits|Dried fruits]], [[note-bitter-orange|Bitter orange]]
- **Notas de Coração:** [[note-cocoa|Cocoa]]
- **Notas de Fundo:** [[note-bourbon-vanilla|Bourbon vanilla]]
