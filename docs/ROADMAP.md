# Roadmap detalhado — O Antiquário

## 1. Premissas

- Roadmap organizado em sprints de uma semana, ajustável à capacidade disponível.
- Uma entrega só é considerada concluída quando código, testes e documentação estão presentes.
- Nenhuma fonte entra no catálogo sem revisão de licença e proveniência.
- A integração do Gemini ocorre depois do recomendador determinístico.
- Datas são estimativas; os critérios de aceite têm prioridade.

## 2. Marcos

| Marco | Horizonte estimado | Resultado |
|---|---:|---|
| M0 — Fundação | Semana 1 | Repositório, decisões, licenças e contratos de dados |
| M1 — Catálogo mínimo | Semanas 2–3 | Pipeline e 150 fragrâncias válidas |
| M2 — Recomendador | Semanas 4–5 | Busca, filtros, ranking e explicação local |
| M3 — Companion | Semana 6 | Gemini protegido por Worker e fallback |
| M4 — MVP fechado | Semanas 7–8 | PWA completa, diário e 600 fragrâncias |
| M5 — Beta público | Semanas 9–11 | Qualidade, acessibilidade e contribuições controladas |
| M6 — Versão 1.0 | Semanas 12–14 | Personalização validada e lançamento estável |

## 3. Fase 0 — Fundação e governança

### Sprint 1

> **Progresso em 22/07/2026:** manifesto de fontes, classificação jurídica/técnica, schema, auditoria automática e testes concluídos. Permanecem pendentes CI, lint, formatação, ADRs e política de privacidade preliminar.

#### Entregas

- Inicializar monorepo TypeScript.
- Definir convenções de código e branches.
- Criar contratos de domínio para perfume, nota, evidência, perfil e recomendação.
- Criar `data-sources.yml` com licença, URL, responsável e uso permitido.
- Configurar lint, formatação, testes e verificação de tipos.
- Criar registro de decisões arquiteturais.
- Definir política de privacidade preliminar e aviso do Gemini gratuito.

#### Critérios de aceite

- Instalação reproduzível com um comando.
- CI executando lint, tipos e testes.
- Nenhum segredo versionado.
- Toda fonte planejada classificada como permitida, isolada, pendente ou proibida.
- Esquemas validados automaticamente.

## 4. Fase 1 — Dados e taxonomia

### Sprint 2: taxonomia olfativa

> **Progresso em 22/07/2026:** taxonomia v1, glossário português/inglês, aliases, normalização de acentos, IDs estáveis, validação de referências e 214 notas concluídos. O Knowledge Core v1 foi implementado com vault Obsidian, contrato validado, chunking semântico, grafo de sinapses e artefatos determinísticos. O conector Wikidata e a publicação DuckDB/Parquet também estão implementados com cache e fixture offline; resta validar uma sincronização real, evoluir a resolução entre fontes e emitir o relatório de itens externos sem licença.

#### Entregas

- Criar famílias e subfamílias olfativas.
- Criar glossário português/inglês de notas e acordes.
- Definir sinônimos e normalização de acentos.
- Definir volatilidade relativa, persistência e descritores das notas quando houver fonte válida.
- Implementar importador do Wikidata.
- Criar validação de duplicatas e identificadores estáveis.

#### Critérios de aceite

- Pelo menos 150 notas normalizadas.
- Todas as notas com identificador estável e nome em português.
- Importação idempotente: duas execuções produzem o mesmo resultado.
- Relatório automático de itens sem fonte ou licença.

### Sprint 3: catálogo inicial

> **Progresso em 22/07/2026:** sincronização real validada com 85 fragrâncias aceitas e 3 quarentenadas. O Catalog Compiler publica JSON determinístico, entidades deduplicadas, índice de busca local e relatório de ambiguidades; a PWA já detecta a release factual. A meta de 150 registros e a cobertura editorial de família, notas, segmentos brasileiro e árabe permanecem pendentes.

#### Entregas

- Curar 150 fragrâncias representativas.
- Incluir pelo menos 50 brasileiras e 25 árabes/acessíveis.
- Implementar separação lógica de dados ODbL.
- Gerar artefatos JSON versionados para o frontend.
- Criar relatório de cobertura por campo, marca e segmento.

#### Critérios de aceite

- Cem por cento dos registros com proveniência.
- Nenhuma imagem sem licença explícita.
- Pelo menos 90% dos registros com família e notas.
- Zero IDs duplicados ou referências quebradas.
- Build de dados menor que o limite definido para a PWA.

## 5. Fase 2 — Busca e recomendador determinístico

### Sprint 4: busca e filtros

#### Entregas

- Índice local por nome, marca, nota e acorde.
- Busca tolerante a acentos e pequenas variações.
- Filtros positivos e negativos.
- Comparação de até quatro perfumes.
- Testes de desempenho com catálogo ampliado artificialmente.

#### Critérios de aceite

- p95 da busca abaixo de 200 ms no conjunto de referência.
- Resultados iguais offline e online.
- Filtros combinados com testes de regressão.
- Busca por nomes em português ou inglês quando houver sinônimo.

### Sprint 5: ranking contextual

#### Entregas

- Implementar regras de exclusão.
- Implementar componentes de pontuação e pesos configuráveis.
- Gerar rastreamento dos fatores que formaram a nota final.
- Criar explicação por templates para operação sem IA.
- Criar conjunto ouro de 30 cenários.

#### Critérios de aceite

- Mesma entrada produz o mesmo ranking.
- Cada recomendação explica ao menos três fatores.
- Nenhuma fragrância rejeitada por regra dura aparece no resultado.
- Fallback cobre todos os cenários do conjunto ouro.
- Pesos totalizam 100% e são versionados.

## 6. Fase 3 — Experiência e companion

### Sprint 6: Gemini Flash

#### Entregas

- Criar Worker como proxy seguro.
- Integrar SDK oficial do Google Gen AI.
- Usar modelo configurável por ambiente, inicialmente `gemini-3.5-flash-lite`.
- Definir JSON Schema da resposta.
- Limitar Gemini aos candidatos fornecidos.
- Implementar timeout, retry curto, circuit breaker e fallback.
- Aplicar CORS, rate limit, limite de payload e sanitização.
- Implementar consentimento e aviso de privacidade.

#### Critérios de aceite

- Chave ausente no bundle e nos logs.
- Resposta inválida do modelo não quebra o fluxo.
- Erros `429`, timeout e `5xx` ativam fallback.
- Teste adversarial não consegue introduzir perfume fora dos candidatos.
- Nenhum dado pessoal identificável é enviado pelo contrato normal.

### Sprint 7: PWA e perfil

#### Entregas

- Onboarding olfativo.
- Tela inicial contextual.
- Busca, detalhes, comparação e recomendações.
- Armazenamento local de perfil e coleção.
- Instalação PWA e modo offline para catálogo/recomendador.
- Estados de carregamento, erro e cota esgotada.

#### Critérios de aceite

- Fluxos principais utilizáveis em tela móvel.
- Aplicação reabre offline após primeira visita.
- Preferências permanecem no dispositivo.
- Usuário consegue desativar IA e continuar usando o produto.
- Auditoria inicial de acessibilidade sem erros críticos.

## 7. Fase 4 — Diário, catálogo completo e MVP fechado

### Sprint 8

#### Entregas

- Diário de uso com evolução por fases.
- Exportação e exclusão local.
- Ajuste de perfil a partir do histórico.
- Ampliar catálogo para 600 fragrâncias.
- Revisão específica da cobertura brasileira.
- Painel interno de qualidade dos dados.

#### Critérios de aceite

- Usuário exporta todos os dados em JSON.
- Exclusão remove perfil, coleção e diário.
- Ajuste automático pode ser desfeito.
- Metas 300/200/100 de cobertura atingidas.
- Todos os registros passam pela auditoria de origem.

## 8. Fase 5 — Beta público

### Sprints 9 a 11

#### Entregas

- Teste com 20 a 50 usuários maiores de 18 anos.
- Coleta anônima e opcional de qualidade das recomendações.
- Melhorias de linguagem e acessibilidade.
- Formulário de sugestão de fragrância com URL da fonte.
- Fila de moderação, sem publicação automática.
- Proteção antiabuso e limites visíveis.
- Documentação de contribuição e licenciamento.

#### Critérios de aceite

- Pelo menos 70% das avaliações classificam o top 3 como coerente.
- Nenhum incidente de vazamento de chave ou dado pessoal.
- Sugestões sem fonte são rejeitadas pelo fluxo.
- Principais jornadas atendem WCAG 2.2 AA.
- Relatório de beta com problemas priorizados.

## 9. Fase 6 — Versão 1.0

### Sprints 12 a 14

#### Entregas

- Calibração dos pesos com dados agregados do beta.
- Métrica bayesiana para desempenho comunitário.
- Mapa de similaridade explicável.
- Melhorias de cache e tamanho do catálogo.
- Política pública de dados e privacidade.
- Runbook de indisponibilidade do Gemini.
- Release estável e changelog.

#### Critérios de aceite

- Recomendador calibrado sem reduzir a diversidade do catálogo.
- Perfumes com pouca evidência exibem baixa confiança.
- Aplicação permanece útil com Gemini desativado por 24 horas.
- Restore testado a partir dos artefatos versionados.
- Documentação de operação e manutenção aprovada.

## 10. Backlog pós-1.0

- Entrada opcional de clima por provedor compatível com o requisito de custo/licença.
- Reconhecimento de frasco e código de barras.
- Importação de coleção por arquivo.
- Múltiplos perfis no mesmo dispositivo.
- Recomendações de layering com regras conservadoras.
- Grafo de perfumistas, casas e linhagens olfativas.
- API aberta para o núcleo de dados próprios.
- Internacionalização.
- Sincronização criptografada opcional.
- Aplicativo móvel empacotado a partir da PWA.

## 11. Gates de continuidade

### Gate A — após Sprint 3

Continuar somente se a auditoria confirmar que o catálogo pode ser redistribuído e mantido legalmente.

### Gate B — após Sprint 5

Continuar somente se o recomendador produzir resultados coerentes sem IA.

### Gate C — após Sprint 8

Abrir beta somente se privacidade, fallback, rate limit e remoção de dados estiverem testados.

### Gate D — antes da versão 1.0

Lançar somente com processo claro de atualização das fontes e resposta a mudanças de cota/licença.
