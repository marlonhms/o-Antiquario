---
schema_version: 1
id: antiquario:fragrance:parfumo-afnan-perfumes-supremacy-not-only-intense
project: o-antiquario
type: fragrance
title: Supremacy Not Only Intense
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
  locator: https://www.parfumo.com/Perfumes/Afnan_Perfumes/supremacy-not-only-intense
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:afnan-perfumes
- predicate: has-top-note
  target: antiquario:olfactory-note:blackcurrant
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:apple
- predicate: has-heart-note
  target: antiquario:olfactory-note:oakmoss
- predicate: has-heart-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-base-note
  target: antiquario:olfactory-note:saffron
- predicate: has-base-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:amadeirado
---

# Supremacy Not Only Intense

**Marca:** [[brand-afnan-perfumes]]

## Pirâmide Olfativa

- **Saída:** [[note-blackcurrant]], [[Bergamota]], [[note-apple]]
- **Coração:** [[note-oakmoss]], [[note-patchouli]], [[note-lavender]]
- **Fundo:** [[note-saffron]], [[note-ambergris]], [[note-musk]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-afnan-perfumes|Afnan Perfumes]]
- **Acordes Principais:** [[frutado|Frutado]], [[defumado|Defumado]], [[Fresco|Fresco]], [[Citricos|Cítricos]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-blackcurrant|Blackcurrant]], [[Bergamota|Bergamota]], [[note-apple|Apple]]
- **Notas de Coração:** [[note-oakmoss|Oakmoss]], [[note-patchouli|Patchouli]], [[note-lavender|Lavender]]
- **Notas de Fundo:** [[note-saffron|Saffron]], [[note-ambergris|Ambergris]], [[note-musk|Musk]]
