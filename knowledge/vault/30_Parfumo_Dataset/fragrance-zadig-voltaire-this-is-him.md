---
schema_version: 1
id: antiquario:fragrance:parfumo-zadig-voltaire-this-is-him
project: o-antiquario
type: fragrance
title: This Is Him!
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
  locator: https://www.parfumo.com/Perfumes/Zadig__Voltaire/This_is_Him
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:zadig-voltaire
- predicate: has-top-note
  target: antiquario:olfactory-note:black-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:grapefruit
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: created-by
  target: antiquario:perfumer:nathalie-lorson
- predicate: created-by
  target: antiquario:perfumer:aurelien-guichard
- predicate: created-by
  target: antiquario:perfumer:firmenich
---

# This Is Him!

**Marca:** [[brand-zadig-voltaire]]

## Pirâmide Olfativa

- **Saída:** [[note-black-pepper]], [[note-grapefruit]]
- **Coração:** [[note-frankincense]], [[Baunilha]]
- **Fundo:** [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-zadig-voltaire|Zadig & Voltaire]]
- **Perfumista(s):** [[nathalie-lorson|Nathalie Lorson]], [[aurelien-guichard|Aurélien Guichard]], [[firmenich|Firmenich]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[defumado|Defumado]], [[doce|Doce]]
- **Notas de Saída:** [[note-black-pepper|Black pepper]], [[note-grapefruit|Grapefruit]]
- **Notas de Coração:** [[note-frankincense|Frankincense]], [[Baunilha|Baunilha]]
- **Notas de Fundo:** [[note-sandalo|Sândalo (Sandalwood)]]
