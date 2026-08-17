---
schema_version: 1
id: antiquario:fragrance:parfumo-amouage-lyric-man
project: o-antiquario
type: fragrance
title: Lyric Man
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
  locator: https://www.parfumo.com/Perfumes/Amouage/Lyric_Man
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:amouage
- predicate: has-top-note
  target: antiquario:olfactory-note:lime
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose
- predicate: has-heart-note
  target: antiquario:olfactory-note:angelica
- predicate: has-heart-note
  target: antiquario:olfactory-note:galbanum
- predicate: has-heart-note
  target: antiquario:olfactory-note:laranja-blossom
- predicate: has-heart-note
  target: antiquario:olfactory-note:ginger
- predicate: has-heart-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-heart-note
  target: antiquario:olfactory-note:saffron
- predicate: has-base-note
  target: antiquario:olfactory-note:musk
- predicate: has-base-note
  target: antiquario:olfactory-note:pine
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:daniel-visentin
---

# Lyric Man

**Marca:** [[brand-amouage]]

## Pirâmide Olfativa

- **Saída:** [[note-lime]], [[Bergamota]]
- **Coração:** [[note-rose]], [[note-angelica]], [[note-galbanum]], [[note-orange-blossom]], [[note-ginger]], [[note-nutmeg]], [[note-saffron]]
- **Fundo:** [[note-musk]], [[note-pine]], [[note-sandalo]], [[note-frankincense]], [[Baunilha]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-amouage|Amouage]]
- **Perfumista(s):** [[daniel-visentin|Daniel Visentin]]
- **Acordes Principais:** [[floral|Floral]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[Fresco|Fresco]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-lime|Lime]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-rose|Rose]], [[note-angelica|Angelica]], [[note-galbanum|Galbanum]], [[note-orange-blossom|Orange blossom]], [[note-ginger|Ginger]], [[note-nutmeg|Nutmeg]], [[note-saffron|Saffron]]
- **Notas de Fundo:** [[note-musk|Musk]], [[note-pine|Pine]], [[note-sandalo|Sândalo (Sandalwood)]], [[note-frankincense|Frankincense]], [[Baunilha|Baunilha]]
