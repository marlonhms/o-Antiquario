---
schema_version: 1
id: antiquario:fragrance:parfumo-tom-ford-grey-vetiver-tom-ford-2009-eau-de-parfum
project: o-antiquario
type: fragrance
title: Grey Vetiver Tom Ford 2009 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Tom_Ford/Grey_Vetiver
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:tom-ford
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-top-note
  target: antiquario:olfactory-note:sage
- predicate: has-top-note
  target: antiquario:olfactory-note:woods
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:pimento
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-base-note
  target: antiquario:olfactory-note:amberwood
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: created-by
  target: antiquario:perfumer:harry-fremont
---

# Grey Vetiver Tom Ford 2009 Eau de Parfum

**Marca:** [[brand-tom-ford]]

## Pirâmide Olfativa

- **Saída:** [[note-grapefruit]], [[note-orange-blossom]], [[note-sage]], [[note-woods]]
- **Coração:** [[note-nutmeg]], [[note-iris]], [[note-pimento]]
- **Fundo:** [[Vetiver]], [[note-oakmoss]], [[note-amberwood]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-tom-ford|Tom Ford]]
- **Perfumista(s):** [[harry-fremont|Harry Frémont]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[Fresco|Fresco]], [[verde|Verde]], [[Amadeirado|Amadeirado]], [[Citricos|Cítricos]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-grapefruit|Grapefruit]], [[note-orange-blossom|Orange blossom]], [[note-sage|Sage]], [[note-woods|Woods]]
- **Notas de Coração:** [[note-nutmeg|Nutmeg]], [[note-iris|Iris]], [[note-pimento|Pimento]]
- **Notas de Fundo:** [[note-vetiver|Vetiver]], [[note-oakmoss|Oakmoss]], [[note-amberwood|Amberwood]]
