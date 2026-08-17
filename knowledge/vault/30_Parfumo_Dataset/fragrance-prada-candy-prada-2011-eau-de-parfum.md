---
schema_version: 1
id: antiquario:fragrance:parfumo-prada-candy-prada-2011-eau-de-parfum
project: o-antiquario
type: fragrance
title: Candy Prada 2011 Eau de Parfum
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
  locator: https://www.parfumo.com/Perfumes/Prada/Candy_Eau_de_Parfum
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:prada
- predicate: has-top-note
  target: antiquario:olfactory-note:white-musk
- predicate: has-heart-note
  target: antiquario:olfactory-note:benzoin-siam
- predicate: has-base-note
  target: antiquario:olfactory-note:caramel
- predicate: has-concentration
  target: antiquario:concentration:eau-de-parfum
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:atalcado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: created-by
  target: antiquario:perfumer:daniela-andrier
---

# Candy Prada 2011 Eau de Parfum

**Marca:** [[brand-prada]]

## Pirâmide Olfativa

- **Saída:** [[note-white-musk]]
- **Coração:** [[note-benzoin-siam]]
- **Fundo:** [[note-caramel]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-prada|Prada]]
- **Perfumista(s):** [[daniela-andrier|Daniela Andrier]]
- **Concentração:** [[Eau-De-Parfum|Eau de Parfum]]
- **Acordes Principais:** [[doce|Doce]], [[gourmand|Gourmand]], [[Atalcado|Atalcado]], [[ambarado|Ambarado]]
- **Notas de Saída:** [[note-white-musk|White Musk]]
- **Notas de Coração:** [[note-benzoin-siam|Benzoin Siam]]
- **Notas de Fundo:** [[note-caramel|Caramel]]
