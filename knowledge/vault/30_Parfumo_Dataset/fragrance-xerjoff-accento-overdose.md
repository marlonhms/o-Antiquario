---
schema_version: 1
id: antiquario:fragrance:parfumo-xerjoff-accento-overdose
project: o-antiquario
type: fragrance
title: Accento Overdose
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
  locator: https://www.parfumo.com/Perfumes/Xerjoff/accento-overdose
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:xerjoff
- predicate: has-top-note
  target: antiquario:olfactory-note:fruity-notes
- predicate: has-top-note
  target: antiquario:olfactory-note:green-notes
- predicate: has-heart-note
  target: antiquario:olfactory-note:eucalyptus
- predicate: has-heart-note
  target: antiquario:olfactory-note:stone-pine
- predicate: has-base-note
  target: antiquario:olfactory-note:egyptian-jasmine
- predicate: has-base-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-base-note
  target: antiquario:olfactory-note:bulgarian-rose
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:verde
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: created-by
  target: antiquario:perfumer:christian-carbonnel-aka-chris-maurice
---

# Accento Overdose

**Marca:** [[brand-xerjoff]]

## Pirâmide Olfativa

- **Saída:** [[note-fruity-notes]], [[note-green-notes]]
- **Coração:** [[note-eucalyptus]], [[note-stone-pine]]
- **Fundo:** [[note-egyptian-jasmine]], [[note-lily-of-the-valley]], [[note-bulgarian-rose]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-xerjoff|XerJoff]]
- **Perfumista(s):** [[christian-carbonnel-aka-chris-maurice|Christian Carbonnel a.k.a. Chris Maurice]]
- **Acordes Principais:** [[floral|Floral]], [[frutado|Frutado]], [[doce|Doce]], [[verde|Verde]], [[Fresco|Fresco]]
- **Notas de Saída:** [[note-fruity-notes|Fruity notes]], [[note-green-notes|Green notes]]
- **Notas de Coração:** [[note-eucalyptus|Eucalyptus]], [[note-stone-pine|Stone pine]]
- **Notas de Fundo:** [[note-egyptian-jasmine|Egyptian jasmine]], [[note-lily-of-the-valley|Lily of the valley]], [[note-bulgarian-rose|Bulgarian rose]]
