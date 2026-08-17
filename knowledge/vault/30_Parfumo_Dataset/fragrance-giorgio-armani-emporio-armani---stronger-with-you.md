---
schema_version: 1
id: antiquario:fragrance:parfumo-giorgio-armani-emporio-armani---stronger-with-you
project: o-antiquario
type: fragrance
title: Emporio Armani - Stronger With You
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
  locator: https://www.parfumo.com/Perfumes/Giorgio_Armani/Emporio_Armani_Stronger_With_You
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:giorgio-armani
- predicate: has-top-note
  target: antiquario:olfactory-note:cardamom
- predicate: has-top-note
  target: antiquario:olfactory-note:pink-pepper
- predicate: has-top-note
  target: antiquario:olfactory-note:violet-leaf
- predicate: has-heart-note
  target: antiquario:olfactory-note:sage
- predicate: has-base-note
  target: antiquario:olfactory-note:baunilha
- predicate: has-base-note
  target: antiquario:olfactory-note:marron-glace
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:gourmand
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: created-by
  target: antiquario:perfumer:cecile-matton
- predicate: created-by
  target: antiquario:perfumer:mane
---

# Emporio Armani - Stronger With You

**Marca:** [[brand-giorgio-armani]]

## Pirâmide Olfativa

- **Saída:** [[note-cardamom]], [[note-pink-pepper]], [[note-violet-leaf]]
- **Coração:** [[note-sage]]
- **Fundo:** [[Baunilha]], [[note-marron-glace]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-giorgio-armani|Giorgio Armani]]
- **Perfumista(s):** [[cecile-matton|Cécile Matton]], [[mane|Mane]]
- **Acordes Principais:** [[doce|Doce]], [[especiado|Especiado]], [[gourmand|Gourmand]], [[Amadeirado|Amadeirado]]
- **Notas de Saída:** [[note-cardamom|Cardamom]], [[note-pink-pepper|Pink pepper]], [[note-violet-leaf|Violet leaf]]
- **Notas de Coração:** [[note-sage|Sage]]
- **Notas de Fundo:** [[Baunilha|Baunilha]], [[note-marron-glace|Marron glacé]]
