---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-lhomme-ideal-guerlain-2014-eau-de-toilette
project: o-antiquario
type: fragrance
title: L'Homme Idéal Guerlain 2014 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Guerlain/L_homme_ideal
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:guerlain
- predicate: has-top-note
  target: antiquario:olfactory-note:citrus-fruits
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-top-note
  target: antiquario:olfactory-note:rosemary
- predicate: has-heart-note
  target: antiquario:olfactory-note:almond
- predicate: has-heart-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:indian-vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:thierry-wasser
---

# L'Homme Idéal Guerlain 2014 Eau de Toilette

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[note-citrus-fruits]], [[note-orange-blossom]], [[note-rosemary]]
- **Coração:** [[note-almond]], [[note-tonka-bean]]
- **Fundo:** [[note-cedar]], [[note-indian-vetiver]], [[note-leather]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-guerlain|Guerlain]]
- **Perfumista(s):** [[thierry-wasser|Thierry Wasser]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-citrus-fruits|Citrus fruits]], [[note-orange-blossom|Orange blossom]], [[note-rosemary|Rosemary]]
- **Notas de Coração:** [[note-almond|Almond]], [[note-tonka-bean|Tonka bean]]
- **Notas de Fundo:** [[note-cedar|Cedar]], [[note-indian-vetiver|Indian vetiver]], [[note-leather|Leather]]
