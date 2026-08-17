---
schema_version: 1
id: antiquario:fragrance:parfumo-jo-malone-myrrh-tonka
project: o-antiquario
type: fragrance
title: Myrrh & Tonka
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
  locator: https://www.parfumo.com/Perfumes/Jo_Malone/Myrrh__Tonka
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:jo-malone
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:namibian-myrrh
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:almond
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:mathilde-bijaoui
---

# Myrrh & Tonka

**Marca:** [[brand-jo-malone]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]]
- **Coração:** [[note-namibian-myrrh]]
- **Fundo:** [[note-tonka-bean]], [[note-almond]], [[Baunilha]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-jo-malone|Jo Malone]]
- **Perfumista(s):** [[mathilde-bijaoui|Mathilde Bijaoui]]
- **Acordes Principais:** [[especiado|Especiado]], [[doce|Doce]], [[Amadeirado|Amadeirado]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-lavender|Lavender]]
- **Notas de Coração:** [[note-namibian-myrrh|Namibian myrrh]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-almond|Almond]], [[Baunilha|Baunilha]]
