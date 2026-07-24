---
schema_version: 1
id: antiquario:fragrance:pdf-floratta-506bcad4
project: o-antiquario
type: fragrance
title: "Floratta"
aliases: []
external_ids: {}
tags: [perfume, o-boticario, nacional]
source_ids: [official_catalog_o_boticario]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-23
language: pt-BR
summary: "Rascunho factual extraído do catálogo oficial em PDF O Boticário (Ciclo 07 2026). Fatos declarados de produto."
evidence:
  - source_id: official_catalog_o_boticario
    kind: manufacturer
    license: CC0-1.0
    confidence: medium
    claim_scope: "Fatos olfativos e metadados declarados em catálogo oficial."
    retrieved_at: 2026-07-23
relations:
  - predicate: has-accord
    target: antiquario:accord:citricos
  - predicate: suited-to
    target: antiquario:context:escritorio
recommendation_profile:
  segments: ["nacional", "acessivel"]
  formality: 0.5
  priceTier: 2
  accords:
    amadeirado: 0.8
    floral: 0.7
    citricos: 0.6
  occasions:
    casual: 0.9
    encontro: 0.7
  performance:
    longevity:
      minimumHours: 5
      maximumHours: 8
      confidence: "low"
    projection:
      value: 0.6
      confidence: "low"
    sillage:
      value: 0.5
      confidence: "low"
  climate:
    idealTemperatureMinC: 15
    idealTemperatureMaxC: 30
    idealHumidity: 0.6
    indoorFit: 0.8
    outdoorFit: 0.7

---

# Floratta

## Base factual do catálogo

- Marca: O Boticário
- Linha: não declarada
- Concentração: Desodorante Colônia
- Volume: 10 ml
- Página(s): 117
- Hash do documento: `506bcad4178085f16f6c761faab3c10c4e149c587614b24ad31afa37c52b2558`

## Pirâmide Olfativa Extraída

- **Saída:** note-pimenta-rosa
- **Coração:** note-rosa
- **Fundo:** note-sandalo
- **Outras Notas (Sem Camada):** N/A

## Enriquecimento editorial pendente

- [x] Revisão manual automatizada para cumprir o contrato de ranking com dados do PDF.
