---
schema_version: 1
id: antiquario:fragrance:parfumo-m-micallef-desirtoxic
project: o-antiquario
type: fragrance
title: DesirToxic
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
  locator: https://www.parfumo.com/Perfumes/Martine_Micallef/desirtoxic
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:m-micallef
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-heart-note
  target: antiquario:olfactory-note:blackcurrant
- predicate: has-heart-note
  target: antiquario:olfactory-note:hemp
- predicate: has-heart-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:moss
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:frutado
---

# DesirToxic

**Marca:** [[brand-m-micallef]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[Bergamota]], [[note-limao-siciliano]]
- **Coração:** [[note-blackcurrant]], [[note-hemp]], [[note-tonka-bean]], [[note-canela]]
- **Fundo:** [[note-musk]], [[note-benzoin]], [[note-moss]], [[note-patchouli]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-m-micallef|M. Micallef]]
- **Acordes Principais:** [[especiado|Especiado]], [[doce|Doce]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[Bergamota|Bergamota]], [[note-limao-siciliano|Limão Siciliano]]
- **Notas de Coração:** [[note-blackcurrant|Blackcurrant]], [[note-hemp|Hemp]], [[note-tonka-bean|Tonka bean]], [[note-canela|Canela]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-benzoin|Benzoin]], [[note-moss|Moss]], [[note-patchouli|Patchouli]]
