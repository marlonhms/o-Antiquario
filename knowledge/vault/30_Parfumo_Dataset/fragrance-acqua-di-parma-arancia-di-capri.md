---
schema_version: 1
id: antiquario:fragrance:parfumo-acqua-di-parma-arancia-di-capri
project: o-antiquario
type: fragrance
title: Arancia di Capri
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
  locator: https://www.parfumo.com/Perfumes/Acqua_di_Parma/arancia-di-capri
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:acqua-di-parma
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-mandarin-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-lemon
- predicate: has-heart-note
  target: antiquario:olfactory-note:petitgrain
- predicate: has-heart-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:caramel
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:verde
---

# Arancia di Capri

**Marca:** [[brand-acqua-di-parma]]

## Pirâmide Olfativa

- **Saída:** [[note-italian-mandarin-orange]], [[note-italian-orange]], [[note-italian-lemon]]
- **Coração:** [[note-petitgrain]], [[note-cardamom]]
- **Fundo:** [[note-musk]], [[note-caramel]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-acqua-di-parma|Acqua di Parma]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[frutado|Frutado]], [[doce|Doce]], [[verde|Verde]]
- **Notas de Saída:** [[note-italian-mandarin-orange|Italian mandarin orange]], [[note-italian-orange|Italian orange]], [[note-italian-lemon|Italian lemon]]
- **Notas de Coração:** [[note-petitgrain|Petitgrain]], [[note-cardamom|Cardamom]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-caramel|Caramel]]
