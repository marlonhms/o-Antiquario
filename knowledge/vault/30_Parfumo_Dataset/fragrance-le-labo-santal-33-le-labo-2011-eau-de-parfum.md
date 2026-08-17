---
schema_version: 1
id: antiquario:fragrance:parfumo-le-labo-santal-33-le-labo-2011-eau-de-parfum
project: o-antiquario
type: fragrance
title: Santal 33 Le Labo 2011 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Le_Labo/Santal_33_Eau_de_Parfum
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:le-labo
- predicate: has-top-note
  target: antiquario:olfactory-note:fig
- predicate: has-top-note
  target: antiquario:olfactory-note:violet
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:papyrus
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:frank-voelkl
- predicate: created-by
  target: antiquario:perfumer:firmenich
---

# Santal 33 Le Labo 2011 Eau de Parfum

**Marca:** [[brand-le-labo]]

## Pirâmide Olfativa

- **Saída:** [[note-fig]], [[note-violet]], [[note-cardamom]]
- **Coração:** [[note-iris]], [[note-papyrus]]
- **Fundo:** [[note-sandalo]], [[note-cedar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-le-labo|Le Labo]]
- **Perfumista(s):** [[frank-voelkl|Frank Voelkl]], [[firmenich|Firmenich]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[verde|Verde]], [[antiquario:accord:couro|Couro]], [[Fresco|Fresco]]
- **Notas de Saída:** [[note-fig|Fig]], [[note-violet|Violet]], [[note-cardamom|Cardamom]]
- **Notas de Coração:** [[note-iris|Iris]], [[note-papyrus|Papyrus]]
- **Notas de Fundo:** [[note-sandalo|Sândalo (Sandalwood)]], [[note-cedar|Cedar]]
