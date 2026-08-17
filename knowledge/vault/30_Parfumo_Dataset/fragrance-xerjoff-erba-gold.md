---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-erba-gold
project: o-antiquario
type: fragrance
title: Erba Gold
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
  locator: https://www.parfumo.com/Perfumes/Xerjoff/Erba_Gold
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-top-note
  target: antiquario:olfactory-note:ginger
- predicate: has-top-note
  target: antiquario:olfactory-note:amalfi-lemon
- predicate: has-top-note
  target: antiquario:olfactory-note:brazilian-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:melon
- predicate: has-heart-note
  target: antiquario:olfactory-note:green-apple
- predicate: has-heart-note
  target: antiquario:olfactory-note:pear
- predicate: has-heart-note
  target: antiquario:olfactory-note:cravo-especiaria
- predicate: has-heart-note
  target: antiquario:olfactory-note:guatemala-cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:madagascan-cinnamon
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:bourbon-vanilla
- predicate: has-base-note
  target: antiquario:olfactory-note:woods
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:christian-carbonnel-aka-chris-maurice
---

# Erba Gold

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-ginger]], [[note-amalfi-lemon]], [[note-brazilian-orange]]
- **Coração:** [[note-melon]], [[note-green-apple]], [[note-pear]], [[note-cravo-especiaria]], [[note-guatemala-cardamom]], [[note-madagascan-cinnamon]]
- **Fundo:** [[note-white-musk]], [[note-ambar]], [[note-bourbon-vanilla]], [[note-woods]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Perfumista(s):** [[christian-carbonnel-aka-chris-maurice|Christian Carbonnel a.k.a. Chris Maurice]]
- **Acordes Principais:** [[frutado|Frutado]], [[doce|Doce]], [[Citricos|Cítricos]], [[Fresco|Fresco]]
- **Notas de Saída:** [[note-calabrian-bergamot|Calabrian bergamot]], [[note-ginger|Ginger]], [[note-amalfi-lemon|Amalfi lemon]], [[note-brazilian-orange|Brazilian orange]]
- **Notas de Coração:** [[note-melon|Melon]], [[note-green-apple|Green apple]], [[note-pear|Pear]], [[note-cravo-especiaria|Cravo-da-índia]], [[note-guatemala-cardamom|Guatemala cardamom]], [[note-madagascan-cinnamon|Madagascan cinnamon]]
- **Notas de Fundo:** [[note-white-musk|White Musk]], [[note-ambar|Âmbar (Amber)]], [[note-bourbon-vanilla|Bourbon vanilla]], [[note-woods|Woods]]
