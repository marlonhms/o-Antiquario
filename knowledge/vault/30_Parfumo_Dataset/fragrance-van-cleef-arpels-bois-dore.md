---
schema_version: 1
id: antiquario:fragrance:parfumo-van-cleef-arpels-bois-dore
project: o-antiquario
type: fragrance
title: Bois Doré
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
  locator: https://www.parfumo.com/Perfumes/Van_Cleef_Arpels/bois-dore
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:van-cleef-arpels
- predicate: has-top-note
  target: antiquario:olfactory-note:mineral-notes
- predicate: has-top-note
  target: antiquario:olfactory-note:pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: created-by
  target: antiquario:perfumer:fabrice-pellegrin
---

# Bois Doré

**Marca:** [[brand-van-cleef-arpels]]

## Pirâmide Olfativa

- **Saída:** [[note-mineral-notes]], [[note-pepper]]
- **Coração:** [[Baunilha]], [[note-cedarwood]]
- **Fundo:** [[note-tonka-bean-absolute]], [[note-white-musk]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-van-cleef-arpels|Van Cleef & Arpels]]
- **Perfumista(s):** [[fabrice-pellegrin|Fabrice Pellegrin]]
- **Acordes Principais:** [[doce|Doce]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[Atalcado|Atalcado]]
- **Notas de Saída:** [[note-mineral-notes|Mineral notes]], [[note-pepper|Pepper]]
- **Notas de Coração:** [[Baunilha|Baunilha]], [[note-cedarwood|Cedarwood]]
- **Notas de Fundo:** [[note-tonka-bean-absolute|Tonka bean absolute]], [[note-white-musk|White Musk]]
