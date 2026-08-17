---
schema_version: 1
id: antiquario:fragrance:parfumo-hermes-ambre-narguile
project: o-antiquario
type: fragrance
title: Ambre Narguilé
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
  locator: https://www.parfumo.com/Perfumes/Hermes/ambre-narguile
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:hermes
- predicate: has-top-note
  target: antiquario:olfactory-note:canela
- predicate: has-top-note
  target: antiquario:olfactory-note:honey
- predicate: has-top-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-top-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-top-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-top-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-heart-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-heart-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-heart-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-heart-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-heart-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:jean-claude-ellena
---

# Ambre Narguilé

**Marca:** [[brand-hermes]]

## Pirâmide Olfativa

- **Saída:** [[note-canela]], [[note-honey]], [[note-labdanum]], [[note-ambergris]], [[note-tonka-bean]], [[note-patchouli]]
- **Coração:** [[note-benzoin]], [[note-labdanum]], [[note-ambergris]], [[note-tonka-bean]], [[note-patchouli]]
- **Fundo:** [[note-tonka-bean]], [[note-patchouli]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-hermes|Hermès]]
- **Perfumista(s):** [[jean-claude-ellena|Jean-Claude Ellena]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-canela|Canela]], [[note-honey|Honey]], [[note-labdanum|Labdanum]], [[note-ambergris|Ambergris]], [[note-tonka-bean|Tonka bean]], [[note-patchouli|Patchouli]]
- **Notas de Coração:** [[note-benzoin|Benzoin]], [[note-labdanum|Labdanum]], [[note-ambergris|Ambergris]], [[note-tonka-bean|Tonka bean]], [[note-patchouli|Patchouli]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-patchouli|Patchouli]]
