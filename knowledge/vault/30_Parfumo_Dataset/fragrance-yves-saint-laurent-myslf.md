---
schema_version: 1
id: antiquario:fragrance:parfumo-yves-saint-laurent-myslf
project: o-antiquario
type: fragrance
title: Myslf
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
  locator: https://www.parfumo.com/Perfumes/Yves_Saint_Laurent/myslf
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:yves-saint-laurent
- predicate: has-top-note
  target: antiquario:olfactory-note:calabrian-bergamot
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamot-leaf
- predicate: has-heart-note
  target: antiquario:olfactory-note:tunisian-orange-blossom-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:ambrofix
- predicate: has-base-note
  target: antiquario:olfactory-note:woods
- predicate: has-base-note
  target: antiquario:olfactory-note:indonesian-patchouli
- predicate: has-accord
  target: antiquario:accord:fresco
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:floral
- predicate: created-by
  target: antiquario:perfumer:christophe-raynaud
- predicate: created-by
  target: antiquario:perfumer:daniela-andrier
- predicate: created-by
  target: antiquario:perfumer:antoine-maisondieu
---

# Myslf

**Marca:** [[brand-yves-saint-laurent]]

## Pirâmide Olfativa

- **Saída:** [[note-calabrian-bergamot]], [[note-bergamot-leaf]]
- **Coração:** [[note-tunisian-orange-blossom-absolute]]
- **Fundo:** [[note-ambrofix]], [[note-woods]], [[note-indonesian-patchouli]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-yves-saint-laurent|Yves Saint Laurent]]
- **Perfumista(s):** [[christophe-raynaud|Christophe Raynaud]], [[daniela-andrier|Daniela Andrier]], [[antoine-maisondieu|Antoine Maisondieu]]
- **Acordes Principais:** [[Fresco|Fresco]], [[Amadeirado|Amadeirado]], [[doce|Doce]], [[floral|Floral]]
- **Notas de Saída:** [[note-calabrian-bergamot|Calabrian bergamot]], [[note-bergamot-leaf|Bergamot leaf]]
- **Notas de Coração:** [[note-tunisian-orange-blossom-absolute|Tunisian orange blossom absolute]]
- **Notas de Fundo:** [[note-ambrofix|Ambrofix]], [[note-woods|Woods]], [[note-indonesian-patchouli|Indonesian patchouli]]
