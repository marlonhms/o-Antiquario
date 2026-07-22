---
schema_version: 1
id: antiquario:context:calor-umido
project: o-antiquario
type: context
title: Calor úmido
aliases: [Calor-Umido]
tags: [contexto, clima, calor, umidade]
source_ids: [internal_curated]
license: CC0-1.0
confidence: medium
review_status: approved
updated_at: 2026-07-22
language: pt-BR
summary: Contexto climático que favorece avaliação conservadora de densidade, doçura e projeção percebida.
evidence:
  - source_id: internal_curated
    kind: curated
    license: CC0-1.0
    confidence: medium
    claim_scope: Heurística contextual original usada pelo recomendador inicial.
relations:
  - predicate: favors
    target: antiquario:accord:citricos
  - predicate: compatible-example
    target: antiquario:fragrance:brisa-vetiver
---

# Calor úmido

No calor úmido, o Antiquário reduz a preferência por combinações muito densas quando o usuário deseja discrição. Isso é uma heurística contextual, não uma regra universal.

## Perfis úteis

Estruturas [[Citricos|cítricas]] e amadeiradas transparentes podem oferecer sensação de luminosidade. [[Bergamota]] é um possível indicador, mas não substitui dados de performance.

## Aplicação

Quantidade aplicada, ventilação e proximidade entre pessoas alteram a experiência. [[Brisa-Vetiver|Brisa Vetiver]] é o exemplo sintético inicial deste contexto.
