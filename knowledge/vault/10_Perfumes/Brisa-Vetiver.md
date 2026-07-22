---
schema_version: 1
id: antiquario:fragrance:brisa-vetiver
project: o-antiquario
type: fragrance
title: Brisa Vetiver
aliases: [Brisa-Vetiver]
tags: [perfume, fixture, citrico, amadeirado]
source_ids: [internal_curated]
license: CC0-1.0
confidence: high
review_status: approved
updated_at: 2026-07-22
language: pt-BR
summary: Fragrância fictícia de referência usada para validar recomendação, conhecimento e recuperação local.
evidence:
  - source_id: internal_curated
    kind: curated
    license: CC0-1.0
    confidence: high
    claim_scope: Fixture original criada exclusivamente para testes do projeto.
relations:
  - predicate: has-note
    target: antiquario:olfactory-note:bergamota
  - predicate: has-note
    target: antiquario:olfactory-note:vetiver
  - predicate: has-accord
    target: antiquario:accord:citricos
  - predicate: has-accord
    target: antiquario:accord:amadeirado
  - predicate: suited-to
    target: antiquario:context:calor-umido
  - predicate: suited-to
    target: antiquario:context:escritorio
---

# Brisa Vetiver

Brisa Vetiver é uma fragrância fictícia da Casa Aurora. Ela existe para testar o motor sem atribuir características inventadas a um produto comercial real.

## Estrutura

A abertura combina [[Bergamota]] e limão. O coração contém chá verde e lavanda; a base combina [[Vetiver]] e cedro.

## Acordes

O perfil conecta [[Citricos|Cítricos]] e [[Amadeirado]], com uma faceta verde secundária.

## Contextos de teste

Sua ficha determinística favorece [[Calor-Umido|calor úmido]] e [[Escritorio|escritório]], sempre respeitando o teto de projeção informado pelo usuário.
