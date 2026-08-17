---
schema_version: 1
id: antiquario:fragrance:parfumo-lancome-la-vie-est-belle-leau-de-parfum
project: o-antiquario
type: fragrance
title: La Vie est Belle L'Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Lancome/La_Vie_est_Belle
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:lancome
- predicate: has-top-note
  target: antiquario:olfactory-note:blackcurrant
- predicate: has-top-note
  target: antiquario:olfactory-note:pear
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasmine
- predicate: has-heart-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-base-note
  target: antiquario:olfactory-note:praline
- predicate: has-base-note
  target: antiquario:olfactory-note:tonka-bean
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: created-by
  target: antiquario:perfumer:olivier-polge
- predicate: created-by
  target: antiquario:perfumer:dominique-ropion
- predicate: created-by
  target: antiquario:perfumer:anne-flipo
---

# La Vie est Belle L'Eau de Parfum

**Marca:** [[brand-lancome]]

## Pirâmide Olfativa

- **Saída:** [[note-blackcurrant]], [[note-pear]]
- **Coração:** [[note-iris]], [[note-jasmine]], [[note-orange-blossom]]
- **Fundo:** [[note-praline]], [[note-tonka-bean]], [[note-patchouli]], [[Baunilha]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-lancome|Lancôme]]
- **Perfumista(s):** [[olivier-polge|Olivier Polge]], [[dominique-ropion|Dominique Ropion]], [[anne-flipo|Anne Flipo]]
- **Acordes Principais:** [[doce|Doce]], [[floral|Floral]], [[gourmand|Gourmand]], [[frutado|Frutado]], [[Atalcado|Atalcado]]
- **Notas de Saída:** [[note-blackcurrant|Blackcurrant]], [[note-pear|Pear]]
- **Notas de Coração:** [[note-iris|Iris]], [[note-jasmine|Jasmine]], [[note-orange-blossom|Orange blossom]]
- **Notas de Fundo:** [[note-praline|Praline]], [[note-tonka-bean|Tonka bean]], [[note-patchouli|Patchouli]], [[Baunilha|Baunilha]]
