---
schema_version: 1
id: antiquario:fragrance:parfumo-rasasi-daarej-pour-homme
project: o-antiquario
type: fragrance
title: Daarej pour Homme
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
  locator: https://www.parfumo.com/Perfumes/Rasasi/Daarej_pour_Homme
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:rasasi
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:cumin
- predicate: has-top-note
  target: antiquario:olfactory-note:mugwort
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:floral
---

# Daarej pour Homme

**Marca:** [[brand-rasasi]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-cumin]], [[note-mugwort]]
- **Coração:** [[note-iris]], [[note-rose]]
- **Fundo:** [[note-musk]], [[note-tonka-bean]], [[Baunilha]], [[note-ambar]], [[note-patchouli]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-rasasi|Rasasi]]
- **Acordes Principais:** [[doce|Doce]], [[ambarado|Ambarado]], [[especiado|Especiado]], [[Atalcado|Atalcado]], [[floral|Floral]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[note-cumin|Cumin]], [[note-mugwort|Mugwort]]
- **Notas de Coração:** [[note-iris|Iris]], [[note-rose|Rose]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-tonka-bean|Tonka bean]], [[Baunilha|Baunilha]], [[note-ambar|Âmbar (Amber)]], [[note-patchouli|Patchouli]], [[note-sandalo|Sândalo (Sandalwood)]]
