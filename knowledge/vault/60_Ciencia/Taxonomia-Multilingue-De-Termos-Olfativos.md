---
schema_version: 1
id: antiquario:science:taxonomia-multilingue-termos-olfativos
project: o-antiquario
type: science
title: Taxonomia multilíngue de termos olfativos
aliases: [Menini 2022, Taxonomia ODEUROPA, Building a Multilingual Taxonomy of Olfactory Terms with Timestamps]
tags: [ciencia, taxonomia, linguagem-olfativa, multilingue, odeuropa, recuperacao]
source_ids: [menini_2022_olfactory_taxonomy]
license: CC-BY-NC-4.0
confidence: high
review_status: approved
updated_at: 2026-08-17
language: pt-BR
summary: Síntese científica do método, da estrutura, da avaliação e dos limites da taxonomia multilíngue e histórica de termos olfativos apresentada por Menini e colaboradores.
evidence:
  - source_id: menini_2022_olfactory_taxonomy
    kind: scientific
    license: CC-BY-NC-4.0
    confidence: high
    claim_scope: Objetivo, idiomas, caráter semiautomático e dimensão temporal descritos no resumo e na introdução.
    locator: https://aclanthology.org/2022.lrec-1.429.pdf#page=1
    retrieved_at: 2026-08-17
  - source_id: menini_2022_olfactory_taxonomy
    kind: scientific
    license: CC-BY-NC-4.0
    confidence: high
    claim_scope: Fluxo com sementes, WordNet, n-gramas, informação temporal, embeddings, agrupamento e revisão manual.
    locator: https://aclanthology.org/2022.lrec-1.429.pdf#page=3
    retrieved_at: 2026-08-17
  - source_id: menini_2022_olfactory_taxonomy
    kind: scientific
    license: CC-BY-NC-4.0
    confidence: high
    claim_scope: Categorias, avaliação por idioma, conteúdo publicado, conclusão e limitações metodológicas.
    locator: https://aclanthology.org/2022.lrec-1.429.pdf#page=6
    retrieved_at: 2026-08-17
relations: []
---

# Taxonomia multilíngue de termos olfativos

## Classificação documental

Este documento é uma síntese de metodologia científica. O artigo de Stefano Menini, Teresa Paccosi, Serra Sinem Tekiroğlu e Sara Tonelli foi publicado nos anais da LREC 2022, nas páginas 4030–4039. A síntese integra o Core Científico e segue a governança descrita em [[Fontes-De-Conhecimento|Fontes de conhecimento]].

O artigo e o recurso de dados têm papéis diferentes no Antiquário. Este documento registra o método e seus limites; os arquivos multilíngues ODEUROPA continuam em staging e são usados somente para expansão e roteamento de consultas.

## Questão de pesquisa declarada

Os autores partem da ausência de uma taxonomia sistemática e consistente para informação olfativa em perspectiva multilíngue. O trabalho descreve a construção semiautomática de uma taxonomia em inglês, francês, alemão e italiano e acrescenta marcas temporais para apoiar análise de conteúdo histórico.

## Método declarado

O fluxo começa com termos-semente definidos com apoio de especialistas em estudos olfativos e patrimônio cultural. Esses termos são expandidos por synsets do WordNet. Em seguida, o trabalho usa coocorrências extraídas de Google N-grams entre 1650 e 1925, informação temporal e embeddings de palavras para propor novos termos e agrupá-los.

O processo combina informação de domínio definida de cima para baixo com sinais distribucionais e de similaridade obtidos de baixo para cima. Cada etapa automática é seguida de avaliação e correção manual; termos sem associação suficiente ao domínio olfativo são descartados.

## Fontes de cheiro e qualidades

O artigo distingue duas classes linguísticas principais:

- substantivos associados a fontes de cheiro, como natureza, flores, plantas, solo, alimentos, bebidas, fumaça, tabaco, indústria e resíduos;
- adjetivos associados a qualidades percebidas, como fresco, pungente, doce, especiado, frutado, floral, amadeirado, terroso, mofado, químico, sintético, defumado, tostado e deteriorado.

Essa distinção é valiosa para o Antiquário porque impede que uma palavra sensorial seja tratada automaticamente como ingrediente, matéria-prima, nota de composição ou família olfativa.

## Avaliação e recurso publicado

Os termos candidatos foram classificados por proximidade com agrupamentos predefinidos e por limiares de similaridade distintos para fontes e qualidades. O procedimento foi repetido em duas iterações e avaliado manualmente por especialistas para selecionar o compromisso entre cobertura e precisão.

A taxonomia final reúne termos provenientes do WordNet e das coocorrências históricas, além de categoria, synset quando aplicável, primeira ocorrência e presença por períodos de cinquenta anos entre 1650 e 1925. O artigo relata resultados separados por idioma e informa que substantivos associados a fontes são mais numerosos do que adjetivos associados a qualidades.

## Aplicação curada no Antiquário

O uso permitido desta pesquisa no projeto é linguístico, histórico e de recuperação:

- ampliar consultas em idiomas diferentes sem alterar o termo canônico;
- distinguir `odor-descriptor` de `odor-quality` antes de criar candidatos;
- localizar sinônimos e variantes para busca;
- apoiar explicações sobre vocabulário olfativo;
- estudar a ocorrência histórica de categorias e termos;
- encaminhar termos sem correspondência segura para quarentena.

Essas aplicações são interpretação editorial do Antiquário, não resultados medidos pelo artigo.

## Limitações declaradas e operacionais

Os autores apontam limitações de cobertura quando recursos como WordNet ou Google N-grams não estão disponíveis ou possuem estrutura desigual entre idiomas. A abordagem usa coocorrência e embeddings para classificar linguagem; ela não mede composição química, presença de ingrediente, intensidade, concentração ou comportamento de uma fragrância acabada.

No Antiquário, similaridade lexical, synset ou categoria ODEUROPA produz no máximo uma rota de recuperação ou um candidato `inferred`. Não cria `same-as`, não promove automaticamente aliases e não altera o Knowledge Core sem validação independente.

## Derivações proibidas

Esta fonte não sustenta:

- `has-note`, `has-top-note`, `has-heart-note` ou `has-base-note` para qualquer perfume;
- identificação de matéria-prima ou molécula em uma composição;
- fixação, projeção, silagem, intensidade ou evolução temporal de perfume;
- equivalência química entre aliases linguísticos;
- classificação comercial automática de fragrâncias.

## Proveniência

Artigo: Menini, Stefano; Paccosi, Teresa; Tekiroğlu, Serra Sinem; Tonelli, Sara. *Building a Multilingual Taxonomy of Olfactory Terms with Timestamps*. LREC 2022, pp. 4030–4039.

O PDF local informa CC BY-NC 4.0. A página atual da ACL Anthology apresenta uma política geral CC BY 4.0 para materiais posteriores a 2016. O manifesto preserva a indicação mais restritiva do PDF até revisão específica. A licença do artigo não substitui a licença registrada separadamente para os arquivos do recurso ODEUROPA.

## Navegação

Retorne ao [[Antiquario-Index|índice principal]] para navegar pelos demais domínios do Knowledge Core.
