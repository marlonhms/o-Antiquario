---
schema_version: 1
id: antiquario:fragrance:parfumo-serge-lutens-five-oclock-au-gingembre
project: o-antiquario
type: fragrance
title: Five o'clock au gingembre
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
  locator: https://www.parfumo.com/Perfumes/Serge_Lutens/Five_O_Clock_Au_Gingembre
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:serge-lutens
- predicate: has-top-note
  target: antiquario:olfactory-note:tea
- predicate: has-top-note
  target: antiquario:olfactory-note:honey
- predicate: has-top-note
  target: antiquario:olfactory-note:ambar
- predicate: has-top-note
  target: antiquario:olfactory-note:cocoa
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-heart-note
  target: antiquario:olfactory-note:honey
- predicate: has-heart-note
  target: antiquario:olfactory-note:ambar
- predicate: has-heart-note
  target: antiquario:olfactory-note:cocoa
- predicate: has-base-note
  target: antiquario:olfactory-note:pepper
- predicate: has-base-note
  target: antiquario:olfactory-note:honey
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:cocoa
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:christopher-sheldrake
- predicate: created-by
  target: antiquario:perfumer:serge-lutens
---

# Five o'clock au gingembre

**Marca:** [[brand-serge-lutens]]

## Pirâmide Olfativa

- **Saída:** [[note-tea]], [[note-honey]], [[note-ambar]], [[note-cocoa]]
- **Coração:** [[note-canela]], [[note-honey]], [[note-ambar]], [[note-cocoa]]
- **Fundo:** [[note-pepper]], [[note-honey]], [[note-ambar]], [[note-cocoa]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-serge-lutens|Serge Lutens]]
- **Perfumista(s):** [[christopher-sheldrake|Christopher Sheldrake]], [[antiquario:perfumer:serge-lutens|Serge Lutens]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[doce|Doce]], [[gourmand|Gourmand]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-tea|Tea]], [[note-honey|Honey]], [[note-ambar|Âmbar (Amber)]], [[note-cocoa|Cocoa]]
- **Notas de Coração:** [[note-canela|Canela]], [[note-honey|Honey]], [[note-ambar|Âmbar (Amber)]], [[note-cocoa|Cocoa]]
- **Notas de Fundo:** [[note-pepper|Pepper]], [[note-honey|Honey]], [[note-ambar|Âmbar (Amber)]], [[note-cocoa|Cocoa]]
