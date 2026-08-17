---
schema_version: 1
id: antiquario:fragrance:parfumo-tiziana-terenzi-rosso-pompei
project: o-antiquario
type: fragrance
title: Rosso Pompei
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
  locator: https://www.parfumo.com/Perfumes/Tiziana_Terenzi/rosso-pompei
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:tiziana-terenzi
- predicate: has-top-note
  target: antiquario:olfactory-note:sicilian-grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-grapefruit
- predicate: has-top-note
  target: antiquario:olfactory-note:italian-lemon
- predicate: has-heart-note
  target: antiquario:olfactory-note:ambergris
- predicate: has-heart-note
  target: antiquario:olfactory-note:jasminum-grandiflorum
- predicate: has-heart-note
  target: antiquario:olfactory-note:mexican-tuberose
- predicate: has-heart-note
  target: antiquario:olfactory-note:lily-of-the-valley
- predicate: has-heart-note
  target: antiquario:olfactory-note:magnolia
- predicate: has-base-note
  target: antiquario:olfactory-note:indian-sandalwood
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:lebanon-cedar
- predicate: has-base-note
  target: antiquario:olfactory-note:neapolitan-maple
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: has-accord
  target: antiquario:accord:citricos
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: created-by
  target: antiquario:perfumer:paolo-terenzi
---

# Rosso Pompei

**Marca:** [[brand-tiziana-terenzi]]

## Pirâmide Olfativa

- **Saída:** [[note-sicilian-grapefruit]], [[note-pink-grapefruit]], [[note-italian-lemon]]
- **Coração:** [[note-ambergris]], [[note-jasminum-grandiflorum]], [[note-mexican-tuberose]], [[note-lily-of-the-valley]], [[note-magnolia]]
- **Fundo:** [[note-indian-sandalwood]], [[note-patchouli]], [[note-lebanon-cedar]], [[note-neapolitan-maple]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-tiziana-terenzi|Tiziana Terenzi]]
- **Perfumista(s):** [[paolo-terenzi|Paolo Terenzi]]
- **Acordes Principais:** [[frutado|Frutado]], [[Citricos|Cítricos]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]], [[doce|Doce]]
- **Notas de Saída:** [[note-sicilian-grapefruit|Sicilian grapefruit]], [[note-pink-grapefruit|Pink grapefruit]], [[note-italian-lemon|Italian lemon]]
- **Notas de Coração:** [[note-ambergris|Ambergris]], [[note-jasminum-grandiflorum|Jasminum grandiflorum]], [[note-mexican-tuberose|Mexican tuberose]], [[note-lily-of-the-valley|Lily of the valley]], [[note-magnolia|Magnólia]]
- **Notas de Fundo:** [[note-indian-sandalwood|Indian sandalwood]], [[note-patchouli|Patchouli]], [[note-lebanon-cedar|Lebanon cedar]], [[note-neapolitan-maple|Neapolitan maple]]
