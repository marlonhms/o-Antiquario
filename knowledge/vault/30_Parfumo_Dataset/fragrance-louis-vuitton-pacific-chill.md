---
schema_version: 1
id: antiquario:fragrance:parfumo-louis-vuitton-pacific-chill
project: o-antiquario
type: fragrance
title: Pacific Chill
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
  locator: https://www.parfumo.com/Perfumes/Louis_Vuitton/pacific-chill
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:louis-vuitton
- predicate: has-top-note
  target: antiquario:olfactory-note:citron
- predicate: has-top-note
  target: antiquario:olfactory-note:laranja
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:mint
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: created-by
  target: antiquario:perfumer:jacques-cavallier-belletrud
---

# Pacific Chill

**Marca:** [[brand-louis-vuitton]]

## Pirâmide Olfativa

- **Saída:** [[note-citron]], [[note-laranja]], [[note-limao-siciliano]], [[note-mint]]
- **Coração:** N/A
- **Fundo:** N/A

## Conexões do Grafo

- **Casa / Marca:** [[brand-louis-vuitton|Louis Vuitton]]
- **Perfumista(s):** [[jacques-cavallier-belletrud|Jacques Cavallier-Belletrud]]
- **Acordes Principais:** [[frutado|Frutado]], [[Fresco|Fresco]], [[Citricos|Cítricos]], [[doce|Doce]], [[verde|Verde]]
- **Notas de Saída:** [[note-citron|Citron]], [[note-laranja|Laranja (Orange)]], [[note-limao-siciliano|Limão Siciliano]], [[note-mint|Mint]]
