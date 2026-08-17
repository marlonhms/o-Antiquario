---
schema_version: 1
id: antiquario:fragrance:parfumo-yves-saint-laurent-le-vestiaire---babycat
project: o-antiquario
type: fragrance
title: Le Vestiaire - Babycat
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
  locator: https://www.parfumo.com/Perfumes/Yves_Saint_Laurent/le-vestiaire-babycat
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:yves-saint-laurent
- predicate: has-top-note
  target: antiquario:olfactory-note:elemi-resin
- predicate: has-top-note
  target: antiquario:olfactory-note:black-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense-resin
- predicate: has-heart-note
  target: antiquario:olfactory-note:saffron
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:suede
- predicate: has-base-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: created-by
  target: antiquario:perfumer:dominique-ropion
---

# Le Vestiaire - Babycat

**Marca:** [[brand-yves-saint-laurent]]

## Pirâmide Olfativa

- **Saída:** [[note-elemi-resin]], [[note-black-pepper]], [[note-pink-pepper]]
- **Coração:** [[note-frankincense]], [[note-frankincense-resin]], [[note-saffron]]
- **Fundo:** [[Baunilha]], [[note-suede]], [[note-cedarwood]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-yves-saint-laurent|Yves Saint Laurent]]
- **Perfumista(s):** [[dominique-ropion|Dominique Ropion]]
- **Acordes Principais:** [[doce|Doce]], [[defumado|Defumado]], [[especiado|Especiado]], [[resinoso|Resinoso]], [[antiquario:accord:couro|Couro]]
- **Notas de Saída:** [[note-elemi-resin|Elemi resin]], [[note-black-pepper|Black pepper]], [[note-pink-pepper|Pink pepper]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[note-frankincense-resin|Frankincense resin]], [[note-saffron|Saffron]]
- **Notas de Fundo:** [[Baunilha|Baunilha]], [[note-suede|Suede]], [[note-cedarwood|Cedarwood]]
