---
schema_version: 1
id: antiquario:fragrance:parfumo-black-ship-grooming-co-davy-jones
project: o-antiquario
type: fragrance
title: Davy Jones
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
  locator: https://www.parfumo.com/Perfumes/Black_Ship_Grooming_Co_/Davy_Jones
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:black-ship-grooming-co
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-mandarin-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:tuberose
- predicate: has-top-note
  target: antiquario:olfactory-note:tobacco
- predicate: has-heart-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-heart-note
  target: antiquario:olfactory-note:florentine-iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:opoponax
- predicate: has-base-note
  target: antiquario:olfactory-note:balsam
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla
- predicate: has-base-note
  target: antiquario:olfactory-note:must
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:especiado
---

# Davy Jones

**Marca:** [[brand-black-ship-grooming-co]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-mandarin-orange]], [[note-tuberose]], [[note-tobacco]]
- **Coração:** [[note-benzoin]], [[note-florentine-iris]], [[note-opoponax]]
- **Fundo:** [[note-balsam]], [[note-musk]], [[note-bourbon-vanilla]], [[note-must]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-black-ship-grooming-co|Black Ship Grooming Co.]]
- **Acordes Principais:** [[doce|Doce]], [[frutado|Frutado]], [[floral|Floral]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-calabrian-mandarin-orange|Calabrian mandarin orange]], [[note-tuberose|Tuberose]], [[note-tobacco|Tobacco]]
- **Notas de Coração:** [[note-benzoin|Benzoin]], [[note-florentine-iris|Florentine iris]], [[note-opoponax|Opoponax]]
- **Notas de Fundo:** [[note-balsam|Balsam]], [[note-musk|Musk]], [[note-bourbon-vanilla|Bourbon vanilla]], [[note-must|Must]]
