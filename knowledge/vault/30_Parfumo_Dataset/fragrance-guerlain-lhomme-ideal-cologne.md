---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-lhomme-ideal-cologne
project: o-antiquario
type: fragrance
title: L'Homme Idéal Cologne
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
  locator: https://www.parfumo.com/Perfumes/Guerlain/L_Homme_Ideal_Cologne
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:guerlain
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-heart-note
  target: antiquario:olfactory-note:almond
- predicate: has-heart-note
  target: antiquario:olfactory-note:neroli
- predicate: has-base-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-base-note
  target: antiquario:olfactory-note:indian-vetiver
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:thierry-wasser
---

# L'Homme Idéal Cologne

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[note-grapefruit]], [[Bergamota]], [[note-laranja]]
- **Coração:** [[note-almond]], [[note-neroli]]
- **Fundo:** [[note-white-musk]], [[note-indian-vetiver]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-guerlain|Guerlain]]
- **Perfumista(s):** [[thierry-wasser|Thierry Wasser]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[doce|Doce]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-grapefruit|Grapefruit]], [[Bergamota|Bergamota]], [[note-laranja|Laranja (Orange)]]
- **Notas de Coração:** [[note-almond|Almond]], [[note-neroli|Neroli]]
- **Notas de Fundo:** [[note-white-musk|White Musk]], [[note-indian-vetiver|Indian vetiver]]
