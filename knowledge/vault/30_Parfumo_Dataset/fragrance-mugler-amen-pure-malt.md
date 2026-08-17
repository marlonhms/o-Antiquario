---
schema_version: 1
id: antiquario:fragrance:parfumo-mugler-amen-pure-malt
project: o-antiquario
type: fragrance
title: A*Men Pure Malt
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
  locator: https://www.parfumo.com/Perfumes/mugler/AMen_Pure_Malt
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:mugler
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:coffee
- predicate: has-base-note
  target: antiquario:olfactory-note:cocoa
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:licorice
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:jacques-huclier
---

# A*Men Pure Malt

**Marca:** [[brand-mugler]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** N/A
- **Fundo:** [[note-tonka-bean]], [[note-coffee]], [[note-cocoa]], [[Baunilha]], [[note-licorice]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-mugler|Mugler]]
- **Perfumista(s):** [[jacques-huclier|Jacques Huclier]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[ambarado|Ambarado]]
- **Notas de Fundo:** [[note-tonka-bean|Tonka bean]], [[note-coffee|Coffee]], [[note-cocoa|Cocoa]], [[Baunilha|Baunilha]], [[note-licorice|Licorice]]
