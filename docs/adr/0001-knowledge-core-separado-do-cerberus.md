# ADR 0001 — Knowledge Core separado do Cerberus

- Status: aceito
- Data: 2026-07-22

## Contexto

O Cerberus é o segundo cérebro geral de Marlon e conecta decisões, projetos e aprendizados. O Antiquário precisa de uma memória operacional própria, potencialmente formada por milhares de perfumes, notas, evidências e chunks.

Compartilhar o mesmo vault ou índice vetorial misturaria ciclos de publicação, regras de licença, privacidade e objetivos de recuperação distintos.

## Decisão

O Antiquário mantém seu próprio vault, grafo e índice RAG. Ele reutiliza as convenções valiosas do Cerberus — Markdown, frontmatter, wikilinks, hubs, proveniência e segurança — através de um contrato explícito e validado.

Uma ponte futura publicará no Cerberus apenas conhecimento estratégico aprovado: índice do projeto, decisões, arquitetura, métricas e aprendizados. O catálogo e a memória dos usuários nunca serão copiados integralmente.

## Consequências

- O produto pode reconstruir seu RAG sem depender do Cerberus.
- O Cerberus permanece denso em conhecimento estratégico.
- A integração exige um gateway explícito, versionado e sanitizado.
- Mudanças no contrato devem preservar IDs globais ou oferecer migração.
