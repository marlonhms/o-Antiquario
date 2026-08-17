---
schema_version: 1
id: antiquario:fragrance:parfumo-creed-bois-du-portugal
project: o-antiquario
type: fragrance
title: Bois du Portugal
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
  locator: https://www.parfumo.com/Perfumes/Creed/Bois_du_Portugal
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:creed
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:basil
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:lime
- predicate: has-top-note
  target: antiquario:olfactory-note:mandarin-orange
- predicate: has-heart-note
  target: antiquario:olfactory-note:lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:coriander
- predicate: has-heart-note
  target: antiquario:olfactory-note:cravo-especiaria
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-heart-note
  target: antiquario:olfactory-note:pimento
- predicate: has-base-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:leathery-notes
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
---

# Bois du Portugal

**Marca:** [[brand-creed]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]], [[note-basil]], [[note-limao-siciliano]], [[note-lime]], [[note-mandarin-orange]]
- **Coração:** [[note-lavender]], [[note-coriander]], [[note-cravo-especiaria]], [[note-nutmeg]], [[note-pimento]]
- **Fundo:** [[note-cedarwood]], [[note-sandalo]], [[note-patchouli]], [[Vetiver]], [[note-leathery-notes]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-creed|Creed]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[verde|Verde]], [[Citricos|Cítricos]], [[Fresco|Fresco]]
- **Notas de Saída:** [[Bergamota|Bergamota]], [[note-basil|Basil]], [[note-limao-siciliano|Limão Siciliano]], [[note-lime|Lime]], [[note-mandarin-orange|Mandarin orange]]
- **Notas de Coração:** [[note-lavender|Lavender]], [[note-coriander|Coriander]], [[note-cravo-especiaria|Cravo-da-índia]], [[note-nutmeg|Nutmeg]], [[note-pimento|Pimento]]
- **Notas de Fundo:** [[note-cedarwood|Cedarwood]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-patchouli|Patchouli]], [[note-vetiver|Vetiver]], [[note-leathery-notes|Leathery notes]]
