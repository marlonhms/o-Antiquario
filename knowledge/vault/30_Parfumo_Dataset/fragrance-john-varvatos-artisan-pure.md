---
schema_version: 1
id: antiquario:fragrance:parfumo-john-varvatos-artisan-pure
project: o-antiquario
type: fragrance
title: Artisan Pure
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
  locator: https://www.parfumo.com/Perfumes/John_Varvatos/Artisan_Pure
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:john-varvatos
- predicate: has-top-note
  target: antiquario:olfactory-note:clementine
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:rodrigo-flores-roux
---

# Artisan Pure

**Marca:** [[brand-john-varvatos]]

## Pirâmide Olfativa

- **Saída:** [[note-clementine]]
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-john-varvatos|John Varvatos]]
- **Perfumista(s):** [[rodrigo-flores-roux|Rodrigo Flores-Roux]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]], [[floral|Floral]]
- **Notas de Saída:** [[note-clementine|Clementine]]
