---
schema_version: 1
id: antiquario:fragrance:parfumo-lalique-encre-noire-a-lextreme
project: o-antiquario
type: fragrance
title: Encre Noire à L'Extrême
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
  locator: https://www.parfumo.com/Perfumes/Lalique/Encre_Noire__L_Extrme
  retrieved_at: '2026-08-17'
relations:
- predicate: belongs-to-brand
  target: antiquario:brand:lalique
- predicate: has-top-note
  target: antiquario:olfactory-note:cypress
- predicate: has-top-note
  target: antiquario:olfactory-note:elemi-resin
- predicate: has-top-note
  target: antiquario:olfactory-note:bergamota
- predicate: has-heart-note
  target: antiquario:olfactory-note:haitian-vetiver
- predicate: has-heart-note
  target: antiquario:olfactory-note:java-vetiver
- predicate: has-heart-note
  target: antiquario:olfactory-note:frankincense
- predicate: has-heart-note
  target: antiquario:olfactory-note:iris
- predicate: has-base-note
  target: antiquario:olfactory-note:benzoin
- predicate: has-base-note
  target: antiquario:olfactory-note:patchouli
- predicate: has-base-note
  target: antiquario:olfactory-note:sandalo
- predicate: has-accord
  target: antiquario:accord:amadeirado
- predicate: has-accord
  target: antiquario:accord:terroso
- predicate: has-accord
  target: antiquario:accord:defumado
- predicate: has-accord
  target: antiquario:accord:resinoso
- predicate: has-accord
  target: antiquario:accord:especiado
- predicate: created-by
  target: antiquario:perfumer:nathalie-lorson
---

# Encre Noire à L'Extrême

**Marca:** [[brand-lalique]]

## Pirâmide Olfativa

- **Saída:** [[note-cypress]], [[note-elemi-resin]], [[Bergamota]]
- **Coração:** [[note-haitian-vetiver]], [[note-java-vetiver]], [[note-frankincense]], [[note-iris]]
- **Fundo:** [[note-benzoin]], [[note-patchouli]], [[note-sandalo]]

## Conexões do Grafo

- **Casa / Marca:** [[brand-lalique|Lalique]]
- **Perfumista(s):** [[nathalie-lorson|Nathalie Lorson]]
- **Acordes Principais:** [[Amadeirado|Amadeirado]], [[terroso|Terroso]], [[defumado|Defumado]], [[resinoso|Resinoso]], [[especiado|Especiado]]
- **Notas de Saída:** [[note-cypress|Cypress]], [[note-elemi-resin|Elemi resin]], [[Bergamota|Bergamota]]
- **Notas de Coração:** [[note-haitian-vetiver|Haitian vetiver]], [[note-java-vetiver|Java vetiver]], [[note-frankincense|Frankincense]], [[note-iris|Iris]]
- **Notas de Fundo:** [[note-benzoin|Benzoin]], [[note-patchouli|Patchouli]], [[note-sandalo|Sândalo (Sandalwood)]]
