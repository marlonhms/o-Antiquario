---
schema_version: 1
id: antiquario:fragrance:parfumo-guerlain-lhomme-ideal-extreme
project: o-antiquario
type: fragrance
title: L'Homme Idéal Extrême
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
  locator: https://www.parfumo.com/Perfumes/Guerlain/l-homme-ideal-extreme
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:guerlain
- predicate: has-top-note
  target: antiquario:olfactory-note:almond
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-heart-note
  target: antiquario:olfactory-note:heliotrope
- predicate: has-heart-note
  target: antiquario:olfactory-note:ameixa
- predicate: has-base-note
  target: antiquario:olfactory-note:tobacco
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:cedar
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:couro
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: created-by
  target: antiquario:perfumer:thierry-wasser
---

# L'Homme Idéal Extrême

**Marca:** [[brand-guerlain]]

## Pirâmide Olfativa

- **Saída:** [[note-almond]], [[Bergamota]], [[note-pink-pepper]]
- **Coração:** [[note-canela]], [[note-heliotrope]], [[note-ameixa]]
- **Fundo:** [[note-tobacco]], [[note-leather]], [[note-patchouli]], [[note-cedar]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-guerlain|Guerlain]]
- **Perfumista(s):** [[thierry-wasser|Thierry Wasser]]
- **Acordes Principais:** [[doce|Doce]], [[especiado|Especiado]], [[frutado|Frutado]], [[antiquario:accord:couro|Couro]], [[gourmand|Gourmand]]
- **Notas de Saída:** [[note-almond|Almond]], [[Bergamota|Bergamota]], [[note-pink-pepper|Pink pepper]]
- **Notas de Coração:** [[note-canela|Canela]], [[note-heliotrope|Heliotrope]], [[note-ameixa|Ameixa (Plum)]]
- **Notas de Fundo:** [[note-tobacco|Tobacco]], [[note-leather|Leather]], [[note-patchouli|Patchouli]], [[note-cedar|Cedar]]
