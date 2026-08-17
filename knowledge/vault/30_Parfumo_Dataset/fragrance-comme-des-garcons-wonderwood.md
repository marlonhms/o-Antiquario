---
schema_version: 1
id: antiquario:fragrance:parfumo-comme-des-garcons-wonderwood
project: o-antiquario
type: fragrance
title: Wonderwood
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
  locator: https://www.parfumo.com/Perfumes/Comme_des_Garons/Wonderwood
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:comme-des-garcons
- predicate: has-top-note
  target: antiquario:olfactory-note:madagascan-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:somalian-frankincense
- predicate: has-top-note
  target: antiquario:olfactory-note:nutmeg
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:cashmeran
- predicate: has-heart-note
  target: antiquario:olfactory-note:cedarwood
- predicate: has-heart-note
  target: antiquario:olfactory-note:gaiac-wood
- predicate: has-heart-note
  target: antiquario:olfactory-note:caraway
- predicate: has-heart-note
  target: antiquario:olfactory-note:christalon
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-base-note
  target: antiquario:olfactory-note:javanol
- predicate: has-base-note
  target: antiquario:olfactory-note:vetiver
- predicate: has-base-note
  target: antiquario:olfactory-note:oud
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:terroso
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: created-by
  target: antiquario:perfumer:antoine-lie
---

# Wonderwood

**Marca:** [[brand-comme-des-garcons]]

## Pirâmide Olfativa

- **Saída:** [[note-madagascan-pepper]], [[note-somalian-frankincense]], [[note-nutmeg]], [[Bergamota]]
- **Coração:** [[note-cashmeran]], [[note-cedarwood]], [[note-gaiac-wood]], [[note-caraway]], [[note-christalon]]
- **Fundo:** [[note-sandalo]], [[note-javanol]], [[Vetiver]], [[note-oud]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-comme-des-garcons|Comme des Garçons]]
- **Perfumista(s):** [[antoine-lie|Antoine Lie]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[especiado|Especiado]], [[defumado|Defumado]], [[terroso|Terroso]], [[resinoso|Resinoso]]
- **Notas de Saída:** [[note-madagascan-pepper|Madagascan pepper]], [[note-somalian-frankincense|Somalian frankincense]], [[note-nutmeg|Nutmeg]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-cashmeran|Cashmeran]], [[note-cedarwood|Cedarwood]], [[note-gaiac-wood|Gaiac wood]], [[note-caraway|Caraway]], [[note-christalon|Christalon]]
- **Notas de Fundo:** [[note-sandalo|Sândalo (Sandalwood)]], [[note-javanol|Javanol]], [[note-vetiver|Vetiver]], [[note-oud|Oud]]
