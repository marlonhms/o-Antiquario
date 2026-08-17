---
schema_version: 1
id: antiquario:fragrance:parfumo-versace-versace-pour-homme-oud-noir
project: o-antiquario
type: fragrance
title: Versace pour Homme Oud Noir
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
  locator: https://www.parfumo.com/Perfumes/Versace/Versace_pour_Homme_Oud_Noir
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:versace
- predicate: has-top-note
  target: antiquario:olfactory-note:pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:bitter-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:neroli
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-heart-note
  target: antiquario:olfactory-note:saffron
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:leatherwood
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:resinoso
---

# Versace pour Homme Oud Noir

**Marca:** [[brand-versace]]

## Pirâmide Olfativa

- **Saída:** [[note-pepper]], [[note-bitter-orange]], [[note-neroli]]
- **Coração:** [[note-frankincense]], [[note-cardamom]], [[note-saffron]]
- **Fundo:** [[note-oud]], [[note-patchouli]], [[note-leatherwood]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-versace|Versace]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[defumado|Defumado]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-pepper|Pepper]], [[note-bitter-orange|Bitter orange]], [[note-neroli|Neroli]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[note-cardamom|Cardamom]], [[note-saffron|Saffron]]
- **Notas de Fundo:** [[note-oud|Oud]], [[note-patchouli|Patchouli]], [[note-leatherwood|Leatherwood]]
