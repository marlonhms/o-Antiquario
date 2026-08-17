---
schema_version: 1
id: antiquario:fragrance:parfumo-dunhill-icon
project: o-antiquario
type: fragrance
title: Icon
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
  locator: https://www.parfumo.com/Perfumes/Dunhill/Icon
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:dunhill
- predicate: has-top-note
  target: antiquario:olfactory-note:neroli-absolute
- predicate: has-top-note
  target: antiquario:olfactory-note:black-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-bergamot
- predicate: has-top-note
  target: antiquario:olfactory-note:petitgrain
- predicate: has-heart-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-heart-note
  target: antiquario:olfactory-note:provencal-lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:sage
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:iris
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: created-by
  target: antiquario:perfumer:carlos-benaim
---

# Icon

**Marca:** [[brand-dunhill]]

## Pirâmide Olfativa

- **Saída:** [[note-neroli-absolute]], [[note-black-pepper]], [[note-italian-bergamot]], [[note-petitgrain]]
- **Coração:** [[note-cardamom]], [[note-zimbro]], [[note-provencal-lavender]], [[note-sage]]
- **Fundo:** [[note-oakmoss]], [[Vetiver]], [[note-iris]], [[note-leather]], [[note-oud]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-dunhill|Dunhill]]
- **Perfumista(s):** [[carlos-benaim|Carlos Benaïm]]
- **Acordes Principais:** [[especiado|Especiado]], [[Fresco|Fresco]], [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]], [[verde|Verde]]
- **Notas de Saída:** [[note-neroli-absolute|Neroli absolute]], [[note-black-pepper|Black pepper]], [[note-italian-bergamot|Italian bergamot]], [[note-petitgrain|Petitgrain]]
- **Notas de Coração:** [[note-cardamom|Cardamom]], [[note-zimbro|Zimbro (Juniper Berry)]], [[note-provencal-lavender|Provençal lavender]], [[note-sage|Sage]]
- **Notas de Fundo:** [[note-oakmoss|Oakmoss]], [[note-vetiver|Vetiver]], [[note-iris|Iris]], [[note-leather|Leather]], [[note-oud|Oud]]
