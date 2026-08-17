---
schema_version: 1
id: antiquario:fragrance:parfumo-acqua-di-parma-mandorlo-di-sicilia
project: o-antiquario
type: fragrance
title: Mandorlo di Sicilia
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
  locator: https://www.parfumo.com/Perfumes/Acqua_di_Parma/mandorlo-di-sicilia
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:acqua-di-parma
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-top-note
  target: antiquario:olfactory-note:star-anise
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-citrus-fruits
- predicate: has-heart-note
  target: antiquario:olfactory-note:green-almond
- predicate: has-heart-note
  target: antiquario:olfactory-note:ylang-ylang
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:lebanon-cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:tolu-balm
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:frutado
---

# Mandorlo di Sicilia

**Marca:** [[brand-acqua-di-parma]]

## Pirâmide Olfativa

- **Saída:** [[note-laranja]], [[note-star-anise]], [[note-calabrian-bergamot]], [[note-italian-citrus-fruits]]
- **Coração:** [[note-green-almond]], [[note-ylang-ylang]]
- **Fundo:** [[note-bourbon-vanilla]], [[note-musk]], [[note-lebanon-cedar]], [[note-tolu-balm]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-acqua-di-parma|Acqua di Parma]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[Atalcado|Atalcado]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-laranja|Laranja (Orange)]], [[note-star-anise|Star anise]], [[note-calabrian-bergamot|Calabrian bergamot]], [[note-italian-citrus-fruits|Italian citrus fruits]]
- **Notas de Coração:** [[note-green-almond|Green almond]], [[note-ylang-ylang|Ylang Ylang]]
- **Notas de Fundo:** [[note-bourbon-vanilla|Bourbon vanilla]], [[note-musk|Musk]], [[note-lebanon-cedar|Lebanon cedar]], [[note-tolu-balm|Tolu balm]]
