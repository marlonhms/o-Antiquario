---
schema_version: 1
id: antiquario:fragrance:parfumo-dior-eau-sauvage-parfum
project: o-antiquario
type: fragrance
title: Eau Sauvage Parfum
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
  locator: https://www.parfumo.com/Perfumes/Dior/Eau_Sauvage_Parfum_2017
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:dior
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender-absolute
- predicate: has-heart-note
  target: antiquario:olfactory-note:hedione
- predicate: has-heart-note
  target: antiquario:olfactory-note:wild-flowers
- predicate: has-base-note
  target: antiquario:olfactory-note:philippine-elemi
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-base-note
  target: antiquario:olfactory-note:canela
- predicate: has-base-note
  target: antiquario:olfactory-note:star-anise
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:francois-demachy
---

# Eau Sauvage Parfum

**Marca:** [[brand-dior]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-laranja]]
- **Coração:** [[note-lavender-absolute]], [[note-hedione]], [[note-wild-flowers]]
- **Fundo:** [[note-philippine-elemi]], [[Vetiver]], [[note-labdanum]], [[note-canela]], [[note-star-anise]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-dior|Dior]]
- **Perfumista(s):** [[francois-demachy|François Demachy]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[Fresco|Fresco]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-calabrian-bergamot|Calabrian bergamot]], [[note-laranja|Laranja (Orange)]]
- **Notas de Coração:** [[note-lavender-absolute|Lavender absolute]], [[note-hedione|Hedione]], [[note-wild-flowers|Wild flowers]]
- **Notas de Fundo:** [[note-philippine-elemi|Philippine elemi]], [[note-vetiver|Vetiver]], [[note-labdanum|Labdanum]], [[note-canela|Canela]], [[note-star-anise|Star anise]]
