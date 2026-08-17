---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-la-capitale
project: o-antiquario
type: fragrance
title: La Capitale
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
  locator: https://www.parfumo.com/Perfumes/Xerjoff/la-capitale
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:strawberry
- predicate: has-top-note
  target: antiquario:olfactory-note:caramel
- predicate: has-top-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-top-note
  target: antiquario:olfactory-note:peach
- predicate: has-heart-note
  target: antiquario:olfactory-note:ambar
- predicate: has-heart-note
  target: antiquario:olfactory-note:leather
- predicate: has-heart-note
  target: antiquario:olfactory-note:persian-saffron
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-heart-note
  target: antiquario:olfactory-note:ginger
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: created-by
  target: antiquario:perfumer:christian-carbonnel-aka-chris-maurice
---

# La Capitale

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-strawberry]], [[note-caramel]], [[note-labdanum]], [[note-peach]]
- **Coração:** [[note-ambar]], [[note-leather]], [[note-persian-saffron]], [[note-rose]], [[note-ginger]]
- **Fundo:** [[note-benzoin]], [[note-bourbon-vanilla]], [[note-oud]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Perfumista(s):** [[christian-carbonnel-aka-chris-maurice|Christian Carbonnel a.k.a. Chris Maurice]]
- **Acordes Principais:** [[doce|Doce]], [[frutado|Frutado]], [[gourmand|Gourmand]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-strawberry|Strawberry]], [[note-caramel|Caramel]], [[note-labdanum|Labdanum]], [[note-peach|Peach]]
- **Notas de Coração:** [[note-ambar|Âmbar (Amber)]], [[note-leather|Leather]], [[note-persian-saffron|Persian saffron]], [[note-rose|Rose]], [[note-ginger|Ginger]]
- **Notas de Fundo:** [[note-benzoin|Benzoin]], [[note-bourbon-vanilla|Bourbon vanilla]], [[note-oud|Oud]]
