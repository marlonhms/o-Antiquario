---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-interlude-black-iris
project: o-antiquario
type: fragrance
title: Interlude Black Iris
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
  locator: https://www.parfumo.com/Perfumes/Amouage/interlude-black-iris
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:amouage
- predicate: has-top-note
  target: antiquario:olfactory-note:rosemary
- predicate: has-top-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:myrrh
- predicate: has-heart-note
  target: antiquario:olfactory-note:orris-butter
- predicate: has-heart-note
  target: antiquario:olfactory-note:ambar
- predicate: has-heart-note
  target: antiquario:olfactory-note:cistus
- predicate: has-heart-note
  target: antiquario:olfactory-note:florentine-iris-absolute
- predicate: has-heart-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:smoked-leather
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:pierre-negrin
---

# Interlude Black Iris

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-rosemary]], [[note-violet-leaf]], [[Bergamota]]
- **Coração:** [[note-frankincense]], [[note-myrrh]], [[note-orris-butter]], [[note-ambar]], [[note-cistus]], [[note-florentine-iris-absolute]], [[Baunilha]]
- **Fundo:** [[note-cedarwood]], [[note-patchouli]], [[note-sandalo]], [[note-smoked-leather]], [[note-oud]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-amouage|Amouage]]
- **Perfumista(s):** [[pierre-negrin|Pierre Negrin]]
- **Acordes Principais:** [[defumado|Defumado]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[ambarado|Ambarado]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-rosemary|Rosemary]], [[note-violet-leaf|Violet leaf]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[note-myrrh|Myrrh]], [[note-orris-butter|Orris butter]], [[note-ambar|Âmbar (Amber)]], [[note-cistus|Cistus]], [[note-florentine-iris-absolute|Florentine iris absolute]], [[Baunilha|Baunilha]]
- **Notas de Fundo:** [[note-cedarwood|Cedarwood]], [[note-patchouli|Patchouli]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-smoked-leather|Smoked leather]], [[note-oud|Oud]]
