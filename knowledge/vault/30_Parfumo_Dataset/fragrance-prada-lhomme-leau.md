---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-lhomme-leau
project: o-antiquario
type: fragrance
title: L'Homme L'Eau
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
  locator: https://www.parfumo.com/Perfumes/Prada/L_Homme_L_Eau
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:prada
- predicate: has-top-note
  target: antiquario:olfactory-note:ginger
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-top-note
  target: antiquario:olfactory-note:white-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:cedar
- predicate: has-heart-note
  target: antiquario:olfactory-note:spices
- predicate: has-heart-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-heart-note
  target: antiquario:olfactory-note:white-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: created-by
  target: antiquario:perfumer:daniela-andrier
---

# L'Homme L'Eau

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** [[note-ginger]], [[Bergamota]], [[note-violet-leaf]], [[note-white-pepper]], [[note-cedar]]
- **Coração:** [[note-spices]], [[note-violet-leaf]], [[note-white-pepper]], [[note-cedar]]
- **Fundo:** [[note-tonka-bean]], [[note-cedar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-prada|Prada]]
- **Perfumista(s):** [[daniela-andrier|Daniela Andrier]]
- **Acordes Principais:** [[Atalcado|Atalcado]], [[Fresco|Fresco]], [[floral|Floral]], [[doce|Doce]]
- **Notas de Saída:** [[note-ginger|Ginger]], [[Bergamota|Bergamota]], [[note-violet-leaf|Violet leaf]], [[note-white-pepper|White pepper]], [[note-cedar|Cedar]]
- **Notas de Coração:** [[note-spices|Spices]], [[note-violet-leaf|Violet leaf]], [[note-white-pepper|White pepper]], [[note-cedar|Cedar]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-cedar|Cedar]]
