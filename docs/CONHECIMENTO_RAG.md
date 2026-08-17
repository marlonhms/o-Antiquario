# Knowledge Core e memória RAG

## Objetivo

O Knowledge Core transforma um vault Markdown compatível com Obsidian em documentos, chunks e sinapses validados. Ele é a camada editorial e recuperável do Antiquário; o catálogo factual continua separado e estruturado.

## Princípios

- RAG é o núcleo de recuperação, não a única fonte da verdade.
- O usuário final nunca importa ou organiza arquivos.
- Somente documentos `approved` entram nos artefatos compilados.
- Documento aprovado aceita apenas fontes `allowed_core` do manifesto.
- Cada fonte precisa de evidência e licença compatível.
- Wikilinks quebrados, IDs duplicados e relações inexistentes interrompem o build.
- O diretório `00_Inbox` não é indexado.
- Templates ficam fora do vault para não contaminarem o RAG.

## Contrato de uma nota

Toda nota possui:

- ID global `antiquario:tipo:slug`;
- identificadores externos opcionais, como o QID do Wikidata;
- tipo de entidade;
- resumo recuperável;
- fontes e evidências;
- confiança e estado de revisão;
- relações tipadas no YAML;
- wikilinks no conteúdo editorial.

As relações tipadas servem para raciocínio e filtros. Os wikilinks mantêm a navegação natural no Obsidian. Ambos são compilados como sinapses.

## Compilação

```text
knowledge/vault
  → parsing de frontmatter
  → validação de fontes e licenças
  → resolução de relações e wikilinks
  → chunking por seção semântica
  → hash determinístico
  → knowledge/compiled
```

Comandos:

```powershell
npm run knowledge:validate
npm run knowledge:build
```

Artefatos:

| Arquivo | Finalidade |
|---|---|
| `documents.json` | Documentos aprovados com texto e metadados |
| `chunks.json` | Unidades prontas para busca textual e embeddings |
| `graph.json` | Nós de documento/evidência e sinapses resolvidas |
| `graph-health.json` | Conectividade, cobertura editorial, requisitos e bloqueios de maturidade |
| `knowledge-manifest.json` | Versão, hash, contagens e nomes dos artefatos |

O hash é derivado do conteúdo, não do horário da execução. Duas compilações da mesma entrada produzem a mesma versão.

## Core Científico

Documentos `science` preservam metodologia, resultados relatados, limitações e aplicação editorial sem criar automaticamente relações comerciais de perfumes. Em 17/08/2026, o primeiro conjunto passou a incluir:

- Menini et al. (2022), sobre a construção semiautomática de uma taxonomia multilíngue e histórica de termos olfativos;
- Vechiato e Vidotti (2024), preprint exploratório sobre IA na Perfumaria e perspectivas para a Ciência da Informação.

O artigo Menini explica o recurso ODEUROPA, mas não substitui seu staging: texto científico e dataset permanecem fontes com licenças, escopos e papéis separados. O preprint de IA é recuperável para perguntas sobre metadados, mediação, arquitetura, memória e agenda de pesquisa; exemplos comerciais não se tornam evidência de eficácia.

Cada síntese informa derivações proibidas. Nenhum documento científico autoriza criar notas, pirâmides, desempenho ou adequação contextual de perfumes sem evidência específica ligada ao produto.

## Expansão lexical científica separada

A ODEUROPA não é incorporada aos documentos aprovados do Knowledge Core. Seu índice permanece em staging e funciona como roteador de consulta:

```text
consulta + idioma explícito
  → correspondência por frase completa
  → conceito canônico já resolvido para recuperação
  → documento e chunks existentes no Knowledge Core
```

Somente pontes com `resolved_for_retrieval` entram no índice. Candidatos por alias/synset, colisões e termos sem resolução não são consumidos. A resposta do expansor separa:

- `canonical_targets`: conceitos lexicais encontrados;
- `retrieval_routes`: destinos que realmente possuem chunks compilados;
- `unroutable_target_ids`: conceitos corretos ainda sem documento recuperável;
- `facts_generated: false`: a expansão nunca cria um claim.

Cada destino seguro recebe duas chaves de consulta provenientes da taxonomia canônica: português e inglês. A proveniência dessas chaves permanece distinta da evidência ODEUROPA. O roteador também tenta reconciliar IDs diferentes apenas por rótulo exato e mesmo tipo; correspondências múltiplas ficam bloqueadas. Documentos mínimos sem chunks não são tratados como recuperáveis.

```powershell
npm run data:index:odeuropa
npm run data:query:odeuropa -- "fresh bread with bergamot" --language en
npm run data:backlog:odeuropa
```

O conjunto ouro versionado em `data/evaluation/odeuropa-retrieval-gold.yml` inclui casos positivos, homógrafos entre idiomas, candidatos bloqueados e limites de palavra. A métrica é uma regressão determinística do contrato atual, não uma validação sensorial ou estimativa de desempenho em produção.

### Backlog seguro de cobertura

As lacunas do índice são convertidas em duas filas operacionais sem alterar o vault:

- `identity_resolution`: conceitos com mais de um documento compatível ficam bloqueados até reconciliação explícita;
- `content_coverage`: documentos ausentes ou rasos são ordenados pela demanda observada no conjunto ouro, no catálogo ativo e no grafo.

Os níveis `P0` a `P4` representam prioridade operacional, não confiança semântica. A ODEUROPA pode motivar a descoberta e o roteamento, mas não fornece automaticamente o conteúdo dos novos documentos. Toda remediação exige evidência `allowed_core` ou curadoria independente e mantém `facts_generated: false`.

### Automação dos documentos P3

O enriquecedor factual opera em duas fases explícitas:

```text
backlog P3 + documentos compilados + relações frontmatter aprovadas
  → candidatos em staging
  → auditoria de fontes, tipos, proveniência e segurança
  → promoção com precondição de hash
  → nova compilação do Knowledge Core
```

Cada seção promovida informa somente a cobertura observada no release do grafo, as camadas já declaradas e até cinco exemplos rastreáveis. Nenhuma relação é adicionada. Se um arquivo mudar depois da prévia, sua promoção é bloqueada.

```powershell
npm run data:plan:odeuropa-enrichment
npm run data:audit:odeuropa-enrichment -- "data/staging/odeuropa/<snapshot>/equivalence/retrieval/enrichment/candidates.jsonl"
npm run data:promote:odeuropa-enrichment -- --updated-at AAAA-MM-DD
```

Na primeira execução, 18 de 18 candidatos passaram, reutilizando 96 relações declaradas. A promoção criou 36 chunks e zero relações novas; os destinos recuperáveis passaram de 49 para 67.

### Gate de demanda P4

Os conceitos restantes não recebem documentos vazios para melhorar uma métrica. O gate `P4` produz uma fila de pesquisa a partir de três sinais operacionais:

- consulta canônica recorrente: pelo menos três eventos em dois dias distintos dentro da janela móvel de 90 dias;
- ocorrência em pelo menos uma fragrância de um catálogo de recomendação aprovado;
- prioridade editorial alta, sempre acompanhada de justificativa versionada.

O registrador expande a consulta em memória e persiste somente `matched_target_ids`, idioma e data com precisão de dia em `data/private/demand/olfactory-query-events.jsonl`, ignorado pelo Git. Consultas brutas, IP, sessão, dispositivo, e-mail e identificadores de usuário são campos proibidos. Eventos inválidos interrompem o gate.

```powershell
npm run data:record:odeuropa-demand -- "perfume com banana" --language pt-BR
npm run data:gate:odeuropa-demand
```

O primeiro comando será chamado pela interface local quando a telemetria consentida estiver integrada; o usuário final não precisará executá-lo. O segundo gera `demand-gate/items.jsonl`, `report.json` e `manifest.json` no snapshot de recuperação atual. `research_ready` significa somente “há motivo para pesquisar”: a criação de documentos e a promoção ao core continuam bloqueadas até existir evidência independente permitida.

Baseline de 17/08/2026: 30 itens `P4`, zero eventos reais armazenados, zero itens liberados para pesquisa e zero documentos criados. Esse estado é intencional e impede que dados sintéticos sejam tratados como interesse real.

## Knowledge Graph v2

O grafo v2 separa relações semânticas declaradas no frontmatter, referências de navegação via wikilinks e relações de suporte para cada evidência. Predicados de domínio possuem contrato de origem e destino: por exemplo, `has-note` exige `fragrance → olfactory-note`, e `includes-note` exige `accord → olfactory-note`.

O build também publica `graph-health.json`: conectividade, nós isolados, cobertura editorial e maturidade para recomendação. O estado `pilot` exige ao menos três perfumes comerciais aprovados e completos; `core`, trinta. Enquanto o relatório estiver `blocked`, Gemini não deve aconselhar a partir de dados factuais.

## Obsidian

O diretório `knowledge/vault` pode ser aberto diretamente como vault. A pasta `.obsidian` é local e ignorada pelo projeto. O funcionamento do compilador não depende do aplicativo Obsidian.

## Cerberus

A integração futura será uma exportação seletiva. Ela criará um gateway do Antiquário no Cerberus contendo arquitetura, decisões, métricas e aprendizados, sem duplicar o catálogo ou a memória privada.
