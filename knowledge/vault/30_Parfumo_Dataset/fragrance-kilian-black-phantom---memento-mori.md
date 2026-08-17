---
schema_version: 1
id: antiquario:fragrance:parfumo-kilian-black-phantom---memento-mori
project: o-antiquario
type: fragrance
title: Black Phantom - Memento Mori
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
  locator: https://www.parfumo.com/Perfumes/Kilian/black-phantom-memento-mori
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:kilian
- predicate: has-heart-note
  target: antiquario:olfactory-note:dark-chocolate
- predicate: has-heart-note
  target: antiquario:olfactory-note:coffee
- predicate: has-heart-note
  target: antiquario:olfactory-note:almond
- predicate: has-heart-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-heart-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-heart-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:caramel
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:sidonie-lancesseur
---

# Black Phantom - Memento Mori

**Marca:** [[brand-kilian]]

## Pirâmide Olfativa

- **Saída:** N/A
- **Coração:** [[note-dark-chocolate]], [[note-coffee]], [[note-almond]], [[note-sandalo]], [[Baunilha]], [[note-tonka-bean]]
- **Fundo:** [[note-caramel]], [[note-sandalo]], [[Baunilha]], [[note-tonka-bean]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-kilian|Kilian]]
- **Perfumista(s):** [[sidonie-lancesseur|Sidonie Lancesseur]]
- **Acordes Principais:** [[gourmand|Gourmand]], [[doce|Doce]], [[especiado|Especiado]], [[Amadeirado|Amadeirado]]
- **Notas de Coração:** [[note-dark-chocolate|Dark chocolate]], [[note-coffee|Coffee]], [[note-almond|Almond]], [[note-sandalo|Sândalo (Sandalwood)]], [[Baunilha|Baunilha]], [[note-tonka-bean|Tonka bean]]
- **Notas de Fundo:** [[note-caramel|Caramel]], [[note-sandalo|Sândalo (Sandalwood)]], [[Baunilha|Baunilha]], [[note-tonka-bean|Tonka bean]]
