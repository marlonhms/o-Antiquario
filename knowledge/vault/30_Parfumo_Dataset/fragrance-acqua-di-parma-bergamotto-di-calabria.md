---
schema_version: 1
id: antiquario:fragrance:parfumo-acqua-di-parma-bergamotto-di-calabria
project: o-antiquario
type: fragrance
title: Bergamotto di Calabria
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
  locator: https://www.parfumo.com/Perfumes/Acqua_di_Parma/bergamotto-di-calabria
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:acqua-di-parma
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-heart-note
  target: antiquario:olfactory-note:red-ginger
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:shyamala-maisondieu
---

# Bergamotto di Calabria

**Marca:** [[brand-acqua-di-parma]]

## Pirâmide Olfativa

- **Saída:** [[note-limao-siciliano]], [[note-calabrian-bergamot]]
- **Coração:** [[note-cedarwood]], [[note-red-ginger]]
- **Fundo:** [[note-musk]], [[note-benzoin]], [[Vetiver]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-acqua-di-parma|Acqua di Parma]]
- **Perfumista(s):** [[shyamala-maisondieu|Shyamala Maisondieu]]
- **Acordes Principais:** [[Citricos|Cítricos]], [[Fresco|Fresco]], [[frutado|Frutado]], [[verde|Verde]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-limao-siciliano|Limão Siciliano]], [[note-calabrian-bergamot|Calabrian bergamot]]
- **Notas de Coração:** [[note-cedarwood|Cedarwood]], [[note-red-ginger|Red ginger]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-benzoin|Benzoin]], [[note-vetiver|Vetiver]]
