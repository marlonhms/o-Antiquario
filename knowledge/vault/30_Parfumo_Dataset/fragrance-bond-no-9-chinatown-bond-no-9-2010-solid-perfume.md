---
schema_version: 1
id: antiquario:fragrance:parfumo-bond-no-9-chinatown-bond-no-9-2010-solid-perfume
project: o-antiquario
type: fragrance
title: Chinatown Bond No. 9 2010 Solid Perfume
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
  locator: https://www.parfumo.com/Perfumes/Bond_No_9/Chinatown_Solid_Perfume
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:bond-no-9
- predicate: has-top-note
  target: antiquario:olfactory-note:mineral-notes
- predicate: has-top-note
  target: antiquario:olfactory-note:pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:drenzlor
- predicate: has-heart-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-base-note
  target: antiquario:olfactory-note:noxiousness
- predicate: has-concentration
  target: antiquario:concentration:solid-perfume
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

# Chinatown Bond No. 9 2010 Solid Perfume

**Marca:** [[brand-bond-no-9]]

## Pirâmide Olfativa

- **Saída:** [[note-mineral-notes]], [[note-pepper]], [[note-drenzlor]]
- **Coração:** [[Baunilha]], [[note-cedarwood]]
- **Fundo:** [[note-tonka-bean-absolute]], [[note-white-musk]], [[note-noxiousness]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-bond-no-9|Bond No. 9]]
- **Perfumista(s):** [[fabrice-pellegrin|Fabrice Pellegrin]]
- **Concentração:** [[solid-perfume|Solid Perfume]]
- **Acordes Principais:** [[doce|Doce]], [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[Atalcado|Atalcado]]
- **Notas de Saída:** [[note-mineral-notes|Mineral notes]], [[note-pepper|Pepper]], [[note-drenzlor|Drenzlor]]
- **Notas de Coração:** [[Baunilha|Baunilha]], [[note-cedarwood|Cedarwood]]
- **Notas de Fundo:** [[note-tonka-bean-absolute|Tonka bean absolute]], [[note-white-musk|White Musk]], [[note-noxiousness|Noxiousness]]
