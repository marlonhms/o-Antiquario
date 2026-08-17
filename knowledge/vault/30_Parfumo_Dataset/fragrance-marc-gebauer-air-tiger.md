---
schema_version: 1
id: antiquario:fragrance:parfumo-marc-gebauer-air-tiger
project: o-antiquario
type: fragrance
title: Air Tiger
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
  locator: https://www.parfumo.com/Perfumes/marc-gebauer/air-tiger
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:marc-gebauer
- predicate: has-top-note
  target: antiquario:olfactory-note:zimbro
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:limao-siciliano
- predicate: has-heart-note
  target: antiquario:olfactory-note:leather
- predicate: has-heart-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedar
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-base-note
  target: antiquario:olfactory-note:labdanum
- predicate: has-base-note
  target: antiquario:olfactory-note:woods
- predicate: has-base-note
  target: antiquario:olfactory-note:ambar
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:christian-carbonnel-aka-chris-maurice
---

# Air Tiger

**Marca:** [[brand-marc-gebauer]]

## Pirâmide Olfativa

- **Saída:** [[note-zimbro]], [[note-cardamom]], [[note-limao-siciliano]]
- **Coração:** [[note-leather]], [[note-patchouli]], [[note-cedar]], [[note-iris]]
- **Fundo:** [[note-labdanum]], [[note-woods]], [[note-ambar]], [[note-benzoin]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-marc-gebauer|Marc Gebauer]]
- **Perfumista(s):** [[christian-carbonnel-aka-chris-maurice|Christian Carbonnel a.k.a. Chris Maurice]]
- **Acordes Principais:** [[especiado|Especiado]], [[Amadeirado|Amadeirado]], [[antiquario:accord:couro|Couro]], [[defumado|Defumado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-zimbro|Zimbro (Juniper Berry)]], [[note-cardamom|Cardamom]], [[note-limao-siciliano|Limão Siciliano]]
- **Notas de Coração:** [[note-leather|Leather]], [[note-patchouli|Patchouli]], [[note-cedar|Cedar]], [[note-iris|Iris]]
- **Notas de Fundo:** [[note-labdanum|Labdanum]], [[note-woods|Woods]], [[note-ambar|Âmbar (Amber)]], [[note-benzoin|Benzoin]]
