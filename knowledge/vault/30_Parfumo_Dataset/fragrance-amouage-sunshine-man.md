---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-sunshine-man
project: o-antiquario
type: fragrance
title: Sunshine Man
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
  locator: https://www.parfumo.com/Perfumes/Amouage/Sunshine_Man
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:amouage
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:everlasting-flower
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja-brandy
- predicate: has-heart-note
  target: antiquario:olfactory-note:clary-sage
- predicate: has-heart-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-heart-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:pierre-negrin
- predicate: created-by
  target: antiquario:perfumer:fabrice-pellegrin
---

# Sunshine Man

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[note-everlasting-flower]], [[note-orange-brandy]]
- **Coração:** [[note-clary-sage]], [[note-zimbro]], [[Bergamota]]
- **Fundo:** [[Baunilha]], [[note-tonka-bean]], [[note-cedarwood]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-amouage|Amouage]]
- **Perfumista(s):** [[pierre-negrin|Pierre Negrin]], [[fabrice-pellegrin|Fabrice Pellegrin]]
- **Acordes Principais:** [[doce|Doce]], [[floral|Floral]], [[especiado|Especiado]], [[Fresco|Fresco]]
- **Notas de Saída:** [[note-lavender|Lavender]], [[note-everlasting-flower|Everlasting flower]], [[note-orange-brandy|Orange brandy]]
- **Notas de Coração:** [[note-clary-sage|Clary sage]], [[note-zimbro|Zimbro (Juniper Berry)]], [[Bergamota|Bergamota]]
- **Notas de Fundo:** [[Baunilha|Baunilha]], [[note-tonka-bean|Tonka bean]], [[note-cedarwood|Cedarwood]]
