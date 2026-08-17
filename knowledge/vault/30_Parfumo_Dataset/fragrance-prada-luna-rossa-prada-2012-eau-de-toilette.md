---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-luna-rossa-prada-2012-eau-de-toilette
project: o-antiquario
type: fragrance
title: Luna Rossa Prada 2012 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Prada/Luna_Rossa_Eau_de_Toilette
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:prada
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender-absolute
- predicate: has-top-note
  target: antiquario:olfactory-note:bitter-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:nana-mint
- predicate: has-heart-note
  target: antiquario:olfactory-note:clary-sage
- predicate: has-base-note
  target: antiquario:olfactory-note:ambroxan
- predicate: has-base-note
  target: antiquario:olfactory-note:ambrette-seed-absolute
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: created-by
  target: antiquario:perfumer:daniela-andrier
---

# Luna Rossa Prada 2012 Eau de Toilette

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender-absolute]], [[note-bitter-orange]]
- **Coração:** [[note-nana-mint]], [[note-clary-sage]]
- **Fundo:** [[note-ambroxan]], [[note-ambrette-seed-absolute]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-prada|Prada]]
- **Perfumista(s):** [[daniela-andrier|Daniela Andrier]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[Fresco|Fresco]], [[especiado|Especiado]], [[Citricos|Cítricos]], [[Atalcado|Atalcado]]
- **Notas de Saída:** [[note-lavender-absolute|Lavender absolute]], [[note-bitter-orange|Bitter orange]]
- **Notas de Coração:** [[note-nana-mint|Nana mint]], [[note-clary-sage|Clary sage]]
- **Notas de Fundo:** [[note-ambroxan|Ambroxan]], [[note-ambrette-seed-absolute|Ambrette seed absolute]]
