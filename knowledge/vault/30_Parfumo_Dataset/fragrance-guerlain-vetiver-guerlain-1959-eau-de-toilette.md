---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-vetiver-guerlain-1959-eau-de-toilette
project: o-antiquario
type: fragrance
title: Vetiver Guerlain 1959 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Guerlain/Vetiver
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:guerlain
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-heart-note
  target: antiquario:olfactory-note:pepper
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:tobacco
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: created-by
  target: antiquario:perfumer:jean-paul-guerlain
---

# Vetiver Guerlain 1959 Eau de Toilette

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[Bergamota]], [[note-limao-siciliano]], [[note-laranja]]
- **Coração:** [[note-nutmeg]], [[note-pepper]]
- **Fundo:** [[Vetiver]], [[note-tobacco]], [[note-tonka-bean]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-guerlain|Guerlain]]
- **Perfumista(s):** [[jean-paul-guerlain|Jean-Paul Guerlain]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[verde|Verde]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[Fresco|Fresco]], [[Citricos|Cítricos]]
- **Notas de Saída:** [[Bergamota|Bergamota]], [[note-limao-siciliano|Limão Siciliano]], [[note-laranja|Laranja (Orange)]]
- **Notas de Coração:** [[note-nutmeg|Nutmeg]], [[note-pepper|Pepper]]
- **Notas de Fundo:** [[note-vetiver|Vetiver]], [[note-tobacco|Tobacco]], [[note-tonka-bean|Tonka bean]]
