---
schema_version: 1
id: antiquario:fragrance:parfumo-mugler-amen-angel-men
project: o-antiquario
type: fragrance
title: A*Men Angel Men
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
  locator: https://www.parfumo.com/Perfumes/mugler/A_Men_Angel_Men
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:mugler
- predicate: has-top-note
  target: antiquario:olfactory-note:lavender
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:coriander
- predicate: has-top-note
  target: antiquario:olfactory-note:peppermint
- predicate: has-heart-note
  target: antiquario:olfactory-note:caramel
- predicate: has-heart-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-heart-note
  target: antiquario:olfactory-note:honey
- predicate: has-heart-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-base-note
  target: antiquario:olfactory-note:coffee
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:styrax
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:jacques-huclier
---

# A*Men Angel Men

**Marca:** [[brand-mugler]]

## Pirâmide Olfativa

- **Saída:** [[note-lavender]], [[Bergamota]], [[note-coriander]], [[note-peppermint]]
- **Coração:** [[note-caramel]], [[note-patchouli]], [[note-cedarwood]], [[note-honey]], [[note-lily-of-the-valley]], [[note-jasmine]]
- **Fundo:** [[note-coffee]], [[note-tonka-bean]], [[note-ambar]], [[note-benzoin]], [[note-musk]], [[Baunilha]], [[note-sandalo]], [[note-styrax]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-mugler|Mugler]]
- **Perfumista(s):** [[jacques-huclier|Jacques Huclier]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-lavender|Lavender]], [[Bergamota|Bergamota]], [[note-coriander|Coriander]], [[note-peppermint|Peppermint]]
- **Notas de Coração:** [[note-caramel|Caramel]], [[note-patchouli|Patchouli]], [[note-cedarwood|Cedarwood]], [[note-honey|Honey]], [[note-lily-of-the-valley|Lily of the valley]], [[note-jasmine|Jasmine]]
- **Notas de Fundo:** [[note-coffee|Coffee]], [[note-tonka-bean|Tonka bean]], [[note-ambar|Âmbar (Amber)]], [[note-benzoin|Benzoin]], [[note-musk|Musk]], [[Baunilha|Baunilha]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-styrax|Styrax]]
