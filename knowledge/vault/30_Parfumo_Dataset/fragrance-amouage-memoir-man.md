---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-memoir-man
project: o-antiquario
type: fragrance
title: Memoir Man
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
  locator: https://www.parfumo.com/Perfumes/Amouage/Memoir_Man
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:amouage
- predicate: has-top-note
  target: antiquario:olfactory-note:absinth
- predicate: has-top-note
  target: antiquario:olfactory-note:mint
- predicate: has-top-note
  target: antiquario:olfactory-note:basil
- predicate: has-top-note
  target: antiquario:olfactory-note:tarragon
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender-absolute
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:gaiac-wood
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:tobacco
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:karine-vinchon-spehner
---

# Memoir Man

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-absinth]], [[note-mint]], [[note-basil]], [[note-tarragon]]
- **Coração:** [[note-frankincense]], [[note-lavender-absolute]], [[note-rose]]
- **Fundo:** [[note-ambar]], [[note-gaiac-wood]], [[note-leather]], [[note-musk]], [[note-oakmoss]], [[note-sandalo]], [[note-tobacco]], [[Baunilha]], [[Vetiver]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-amouage|Amouage]]
- **Perfumista(s):** [[karine-vinchon-spehner|Karine Vinchon-Spehner]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[defumado|Defumado]], [[verde|Verde]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-absinth|Absinth]], [[note-mint|Mint]], [[note-basil|Basil]], [[note-tarragon|Tarragon]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[note-lavender-absolute|Lavender absolute]], [[note-rose|Rose]]
- **Notas de Fundo:** [[note-ambar|Âmbar (Amber)]], [[note-gaiac-wood|Gaiac wood]], [[note-leather|Leather]], [[note-musk|Musk]], [[note-oakmoss|Oakmoss]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-tobacco|Tobacco]], [[Baunilha|Baunilha]], [[note-vetiver|Vetiver]]
