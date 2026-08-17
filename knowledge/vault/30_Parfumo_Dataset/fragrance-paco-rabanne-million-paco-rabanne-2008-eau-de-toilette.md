---
schema_version: 1
id: antiquario:fragrance:parfumo-paco-rabanne-million-paco-rabanne-2008-eau-de-toilette
project: o-antiquario
type: fragrance
title: Million Paco Rabanne 2008 Eau de Toilette
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
  locator: https://www.parfumo.com/Perfumes/Paco_Rabanne/1_Million_Eau_de_Toilette
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:paco-rabanne
- predicate: has-top-note
  target: antiquario:olfactory-note:red-mandarin-orange
- predicate: has-top-note
  target: antiquario:olfactory-note:peppermint
- predicate: has-heart-note
  target: antiquario:olfactory-note:canela
- predicate: has-heart-note
  target: antiquario:olfactory-note:rose-absolute
- predicate: has-base-note
  target: antiquario:olfactory-note:amberketal
- predicate: has-base-note
  target: antiquario:olfactory-note:leather
- predicate: has-concentration
  target: antiquario:concentration:eau-de-toilette
- predicate: has-accord
  target: antiquario:accord:doce
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: has-accord
  target: antiquario:accord:ambarado
- predicate: has-accord
  target: antiquario:accord:frutado
- predicate: created-by
  target: antiquario:perfumer:christophe-raynaud
- predicate: created-by
  target: antiquario:perfumer:olivier-pescheux
- predicate: created-by
  target: antiquario:perfumer:michel-girard
---

# Million Paco Rabanne 2008 Eau de Toilette

**Marca:** [[brand-paco-rabanne]]

## Pirâmide Olfativa

- **Saída:** [[note-red-mandarin-orange]], [[note-peppermint]]
- **Coração:** [[note-canela]], [[note-rose-absolute]]
- **Fundo:** [[note-amberketal]], [[note-leather]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-paco-rabanne|Paco Rabanne]]
- **Perfumista(s):** [[christophe-raynaud|Christophe Raynaud]], [[olivier-pescheux|Olivier Pescheux]], [[michel-girard|Michel Girard]]
- **Concentração:** [[eau-de-toilette|Eau de Toilette]]
- **Acordes Principais:** [[doce|Doce]], [[especiado|Especiado]], [[ambarado|Ambarado]], [[frutado|Frutado]]
- **Notas de Saída:** [[note-red-mandarin-orange|Red mandarin orange]], [[note-peppermint|Peppermint]]
- **Notas de Coração:** [[note-canela|Canela]], [[note-rose-absolute|Rose absolute]]
- **Notas de Fundo:** [[note-amberketal|Amberketal]], [[note-leather|Leather]]
