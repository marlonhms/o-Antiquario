---
schema_version: 1
id: antiquario:fragrance:parfumo-lalique-encre-noire-sport
project: o-antiquario
type: fragrance
title: Encre Noire Sport
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
  locator: https://www.parfumo.com/Perfumes/Lalique/Encre_Noire_Sport
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:lalique
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:cypress
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:provencal-lavender
- predicate: has-heart-note
  target: antiquario:olfactory-note:bourbon-vetiver
- predicate: has-heart-note
  target: antiquario:olfactory-note:haitian-vetiver
- predicate: has-heart-note
  target: antiquario:olfactory-note:aquatic-notes
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-base-note
  target: antiquario:olfactory-note:cashmere-wood
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:terroso
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: created-by
  target: antiquario:perfumer:nathalie-lorson
---

# Encre Noire Sport

**Marca:** [[brand-lalique]]

## Pirâmide Olfativa

- **Saída:** [[note-grapefruit]], [[note-cypress]], [[Bergamota]], [[note-provencal-lavender]]
- **Coração:** [[note-bourbon-vetiver]], [[note-haitian-vetiver]], [[note-aquatic-notes]], [[note-nutmeg]]
- **Fundo:** [[note-cashmere-wood]], [[note-musk]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-lalique|Lalique]]
- **Perfumista(s):** [[nathalie-lorson|Nathalie Lorson]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[Fresco|Fresco]], [[verde|Verde]], [[terroso|Terroso]], [[Citricos|Cítricos]]
- **Notas de Saída:** [[note-grapefruit|Grapefruit]], [[note-cypress|Cypress]], [[Bergamota|Bergamota]], [[note-provencal-lavender|Provençal lavender]]
- **Notas de Coração:** [[note-bourbon-vetiver|Bourbon vetiver]], [[note-haitian-vetiver|Haitian vetiver]], [[note-aquatic-notes|Aquatic notes]], [[note-nutmeg|Nutmeg]]
- **Notas de Fundo:** [[note-cashmere-wood|Cashmere wood]], [[note-musk|Musk]]
