# Roadmap de produto B2C e B2B — O Antiquário

> **Direção definida em 31/07/2026.** Este roadmap começa somente depois que a base factual, o Knowledge Core e a memória RAG alcançarem o Gate de Confiança descrito abaixo. Ele não substitui o roadmap técnico atual: organiza a transformação do núcleo olfativo em produto, experiência e receita.

## 1. Tese do produto

O Antiquário não será apenas uma enciclopédia de perfumes. Seu valor será reduzir a incerteza entre intenção, fragrância, pele, ambiente e memória pessoal.

A mesma inteligência atenderá dois mercados com experiências diferentes:

- **B2C:** um companion privado que aprende com a pessoa e ajuda a escolher, experimentar, comprar e usar melhor suas fragrâncias;
- **B2B:** um consultor de vendas que interpreta a necessidade do cliente dentro do catálogo, estoque e políticas de cada loja ou profissional.

O banco bruto não é o produto comercial. O produto é a combinação de:

- identidade e proveniência confiáveis;
- grafo olfativo conectado;
- recomendação contextual reproduzível;
- memória pessoal ou comercial isolada;
- explicação sensorial clara;
- aprendizado a partir de experiências reais;
- interface premium e confiança editorial.

## 2. Contrato de experiência sensorial

O sistema não cheira, não conhece antecipadamente a química da pele e não pode prometer que duas pessoas perceberão a mesma fragrância da mesma forma. Para entregar experiências honestas, toda resposta deverá separar quatro camadas:

| Camada | Exemplo | Como apresentar |
|---|---|---|
| Fato declarado | notas, concentração, perfumista | “A marca declara…” |
| Curadoria olfativa | evolução provável e associação contextual | “Nossa curadoria interpreta…” |
| Estimativa do motor | adequação ao calor, ocasião ou projeção desejada | “Há boa compatibilidade porque…” |
| Memória pessoal | duração e percepção registradas pelo usuário | “Na sua pele, você observou…” |

Regras obrigatórias:

- nunca apresentar percepção subjetiva como propriedade universal;
- nunca inventar pirâmide, desempenho, matéria-prima ou disponibilidade;
- mostrar confiança e origem junto das afirmações relevantes;
- explicar conflitos entre fontes, em vez de escondê-los;
- usar a IA para linguagem e diálogo, não para criar fatos;
- convidar o usuário a confirmar a experiência na própria pele;
- permitir correção, exportação e exclusão da memória pessoal;
- evitar diagnóstico médico, dermatológico ou promessa de segurança clínica.

## 3. Gate de Confiança Olfativa

Nenhuma assinatura, recomendação comercial ou piloto com cliente deverá ser lançado enquanto este gate estiver bloqueado.

### 3.1 Base factual

- catálogo comercial mínimo definido no `ESCOPO.md` alcançado ou uma coleção menor formalmente aprovada para piloto;
- 100% das fragrâncias publicadas com identidade, marca, fonte, licença, data e hash rastreáveis;
- pelo menos 90% do catálogo elegível com família e informação olfativa suficiente para comparação;
- concentração, ano e perfumista preservados apenas quando conhecidos;
- nenhuma ambiguidade de identidade promovida silenciosamente ao core;
- conflitos e termos não resolvidos visíveis em relatórios de quarentena;
- builds determinísticos, versionados e reversíveis.

### 3.2 Grafo e RAG

- estado `core` aprovado no `graph-health.json`;
- zero wikilinks quebrados, IDs duplicados ou relações com origem/destino inválidos;
- perfumes elegíveis conectados a notas, acordes, evidências e entidades relevantes;
- cada trecho recuperado preserva documento, seção, fonte e escopo da evidência;
- recuperação factual avaliada por um conjunto ouro versionado;
- perguntas sem evidência retornam “não sei” ou pedem contexto, em vez de completar lacunas;
- nenhuma instrução encontrada no conteúdo recuperado pode substituir as regras do sistema;
- documentos privados, `00_Inbox` e fontes não aprovadas permanecem fora do índice publicado.

### 3.3 Recomendador

- no mínimo 60 cenários ouro cobrindo clima, ambiente, ocasião, orçamento, intensidade e rejeições;
- zero fragrâncias inexistentes ou fora da lista de candidatos nas respostas;
- filtros duros respeitados em 100% dos testes;
- justificativa rastreável aos fatores que realmente alteraram o score;
- fallback local funcional em 100% dos testes sem IA;
- avaliação humana considera coerentes pelo menos 80% dos top 3 no beta interno;
- diferenças entre dado declarado, curadoria e estimativa aparecem na interface.

### 3.4 Segurança e privacidade

- chave de IA ausente do bundle e protegida por Worker;
- payloads validados, limitados e anonimizados;
- logs sem prompts integrais, diário privado, credenciais ou identificação pessoal;
- consentimento explícito antes da primeira chamada à IA;
- exportação e exclusão verificadas por testes;
- isolamento entre memória pessoal, catálogo público e futuros tenants B2B;
- rate limit, timeout, circuit breaker e fallback testados.

### 3.5 Validação na vida real

- grupo piloto usa as recomendações na pele e registra abertura, evolução, duração e adequação ao contexto;
- o sistema mede diferença entre previsão e percepção, sem apagar a subjetividade;
- feedback pessoal recalibra apenas o perfil daquele usuário;
- agregações futuras exigem consentimento, anonimização e amostra mínima;
- linguagem sensorial é compreensível, útil e não induz certeza falsa.

### 3.6 Saída do gate

O gate só muda para `ready_for_product_pilot` quando um relatório versionado confirmar todos os requisitos. Qualquer regressão crítica volta o estado para `blocked` e impede a publicação de uma nova release comercial.

## 4. Sequência integrada

```text
Base factual + Knowledge Core + RAG seguro
  → Gate de Confiança Olfativa
  → Beta B2C fechado + descoberta B2B
  → Passaporte Olfativo + Antiquário Pro piloto
  → Privé + Pro pago
  → Afiliados independentes + Maison white-label
  → Comunidade moderada + inteligência comercial agregada
```

As trilhas B2C e B2B podem avançar em paralelo depois do gate, mas compartilham o mesmo catálogo público, taxonomia, recomendador e contrato de confiança.

## 5. Roadmap B2C

### B2C 1 — Beta sensorial fechado

**Objetivo:** provar que o sistema compreende intenção e contexto antes de cobrar.

**Escopo:**

- 30 a 100 participantes convidados;
- onboarding olfativo progressivo;
- consulta por momento, ambiente, clima e intenção;
- três recomendações com força, ressalva e confiança;
- comparação entre previsão e experiência após o uso;
- coleção, lista de desejos e diário local;
- botão claro para corrigir uma percepção;
- explicação por fallback e por IA sob o mesmo contrato factual.

**Métricas de saída:**

- pelo menos 70% concluem a primeira consulta;
- pelo menos 50% salvam, comparam ou sinalizam desejo de experimentar uma opção;
- pelo menos 30% retornam para registrar uma experiência;
- pelo menos 80% consideram uma recomendação do top 3 coerente;
- taxa de afirmação factual sem suporte igual a zero nas auditorias;
- incidentes críticos de privacidade iguais a zero.

**Não inclui:** cobrança, publicidade, ranking patrocinado ou recomendação baseada em comissão.

### B2C 2 — Antiquário Essencial público

**Objetivo:** criar utilidade recorrente e aprender quais jornadas geram confiança.

**Entrega gratuita:**

- consulta contextual;
- biblioteca olfativa e comparação;
- perfil inicial;
- coleção e diário básicos;
- explicações determinísticas offline;
- transparência de fontes e confiança;
- instalação como PWA;
- exportação e exclusão de dados.

**Métricas principais:** ativação, conclusão da consulta, itens salvos, retorno em 7/30 dias, uso do diário, correções do usuário e falhas de recomendação.

**Gate para monetização:** não cobrar assinatura até existir evidência de retorno recorrente e de valor além da primeira curiosidade.

### B2C 3 — Passaporte Olfativo

**Objetivo:** validar disposição de pagamento com uma compra avulsa de baixo risco.

**Produto:**

- identidade olfativa explicada;
- afinidades, rejeições e zonas de exploração;
- recomendações por trabalho, calor, encontros, eventos e assinatura;
- análise de redundância da coleção;
- sequência de experimentação antes da compra;
- relatório digital compartilhável com versão da base e data;
- ressalvas e perguntas ainda não respondidas.

**Hipótese comercial:** testar faixas como R$ 29, R$ 39 e R$ 59, sem assumir preço definitivo.

**Métricas de saída:** conversão da oferta, conclusão, satisfação, pedido de reembolso, recomendação a terceiros e uso real das sugestões.

### B2C 4 — Antiquário Privé

**Objetivo:** cobrar pela continuidade da memória, não por esconder a recomendação básica.

**Recursos premium candidatos:**

- memória olfativa longitudinal;
- guarda-roupa e rotação semanal/sazonal;
- análise de redundâncias e lacunas da coleção;
- aprendizado por abertura, coração e dry-down percebidos;
- planejamento para viagens e eventos;
- relatórios de evolução do gosto;
- alertas de desejo, experimentação e reposição;
- consultas conversacionais ampliadas;
- sincronização opcional e criptografada entre dispositivos.

**Hipótese comercial:** R$ 14,90 a R$ 29,90 por mês, com plano anual testado depois da retenção mensal.

**Gate de saída:** retenção suficiente para demonstrar uso contínuo; se a assinatura servir apenas para uma consulta, retornar ao modelo avulso.

### B2C 5 — Comércio assistido e afiliados

**Objetivo:** monetizar intenção de compra sem corromper a recomendação.

**Recursos:**

- “onde experimentar” e “onde comprar” após o ranking;
- parceiros oficiais e lojas identificadas;
- diferentes volumes e faixas de preço;
- alerta de disponibilidade ou promoção quando houver fonte válida;
- registro de clique e conversão com consentimento apropriado;
- disclosure claro de comissão.

**Firewall de independência:**

- comissão, margem e patrocínio nunca entram no score olfativo;
- opção sem parceiro continua visível;
- resultados patrocinados ficam separados e rotulados;
- indisponibilidade comercial não altera fatos do perfume;
- cada integração tem política de atualização e desligamento.

### B2C 6 — Comunidade moderada

**Objetivo:** transformar vivências individuais em padrões úteis sem criar uma base de boatos.

**Pré-requisitos:** identidade/antiabuso, moderação, consentimento, direito de exclusão e modelo de reputação.

**Escopo:**

- avaliações estruturadas, não cópia de resenhas externas;
- percepção por contexto e fase;
- agregação somente com amostra mínima;
- separação entre média comunitária e experiência pessoal;
- detecção de spam, campanha coordenada e conflito de interesse;
- contribuição nunca sobrescreve dado factual.

## 6. Roadmap B2B

### B2B 1 — Descoberta e codesign

**Objetivo:** confirmar os fluxos comerciais antes de construir uma plataforma multiempresa.

**Participantes:** três a cinco consultores independentes e duas a três lojas ou operações digitais de perfis distintos.

**Perguntas que o piloto deve responder:**

- como o profissional recebe e atualiza o catálogo;
- quais dados de estoque e preço existem;
- como ele entende a necessidade do cliente hoje;
- onde perde vendas por excesso de opções;
- quais explicações aumentam confiança sem pressionar;
- como compartilha recomendações pelo WhatsApp ou no balcão;
- quais dados podem ser armazenados com consentimento.

**Saída:** mapa de jornadas, contrato de catálogo B2B e lista priorizada de problemas comprovados.

### B2B 2 — Fundação multi-tenant

**Objetivo:** permitir que cada negócio use sua própria realidade comercial sem contaminar o core.

**Arquitetura obrigatória:**

- tenant, usuário, papel e permissões;
- catálogo público referenciado por IDs estáveis;
- catálogo privado, preço e estoque isolados por tenant;
- pipeline de PDF/CSV com relatório de qualidade;
- matching conservador com o catálogo factual;
- itens não resolvidos em quarentena;
- trilha de auditoria de importação e publicação;
- exclusão completa do tenant;
- nenhuma informação privada enviada ao RAG público;
- ambientes de demonstração com dados sintéticos.

**Gate de segurança:** testes de isolamento provam que uma empresa não consegue consultar dados de outra.

### B2B 3 — Antiquário Pro piloto

**Objetivo:** ajudar o vendedor a escolher produtos disponíveis, explicar a seleção e conduzir o cliente à experimentação.

**Fluxo principal:**

1. vendedor registra intenção, contexto, preferências e orçamento;
2. motor filtra apenas o catálogo e estoque permitidos;
3. sistema sugere até três produtos;
4. explicação separa dado, curadoria e estimativa;
5. vendedor apresenta, testa e registra reação estruturada;
6. sistema gera um cartão compartilhável sem dado sensível;
7. resultado da interação alimenta apenas a memória autorizada daquele tenant/cliente.

**Recursos:**

- modo balcão e modo WhatsApp;
- busca por linguagem natural;
- alternativas por orçamento;
- comparação e tratamento de objeções factuais;
- aviso de indisponibilidade;
- favoritos e histórico consentido;
- painel de cobertura e itens sem informação suficiente.

**Métricas:** tempo até recomendação, produtos experimentados, conversão assistida, ticket, devolução, satisfação do cliente e uso semanal pelo profissional.

### B2B 4 — Piloto pago

**Objetivo:** confirmar retorno econômico e disposição de pagamento.

**Hipóteses:**

- plano individual entre R$ 79 e R$ 199/mês;
- plano de pequena loja entre R$ 399 e R$ 999/mês;
- implantação cobrada apenas quando houver trabalho real de catálogo ou integração;
- período piloto com objetivo e métrica definidos, não gratuidade indefinida.

**Critérios de continuação:**

- profissionais ativos semanalmente;
- economia mensurável de tempo;
- melhora de conversão ou qualidade percebida;
- importação de catálogo reproduzível;
- suporte operacional sustentável;
- margem positiva sem depender de uso ilimitado de IA paga.

### B2B 5 — Antiquário Maison

**Objetivo:** oferecer experiência white-label para lojas, redes e marcas.

**Produtos possíveis:**

- consultor incorporado ao e-commerce;
- QR code de descoberta no ponto de venda;
- modo tablet para equipe;
- landing pages de campanha;
- API de recomendação com IDs permitidos;
- personalização visual e editorial;
- integração de estoque, preço e CRM por contratos explícitos;
- painel operacional e relatório de qualidade do catálogo.

**Requisitos adicionais:** SLA, limites por plano, rotação de segredos, webhooks idempotentes, sandbox, versionamento de API e processo de incidentes.

### B2B 6 — Inteligência comercial responsável

**Objetivo:** mostrar padrões de demanda sem vender ou expor pessoas.

**Indicadores permitidos:**

- ocasiões mais consultadas;
- faixas de orçamento;
- acordes desejados;
- produtos muito recomendados e pouco disponíveis;
- lacunas do catálogo;
- razões agregadas de rejeição;
- cobertura e confiança dos dados.

**Limites:**

- sem perfis individuais comercializados;
- sem texto privado nos painéis;
- amostra mínima para agregação;
- opt-out e retenção definidos;
- dados de uma empresa não compõem benchmark de outra sem contrato e anonimização;
- análise comercial não altera o ranking olfativo individual.

### B2B 7 — Escala e ecossistema

Somente depois de retenção e unit economics comprovados:

- conectores configuráveis de catálogo e estoque;
- onboarding self-service;
- parceiros de implementação;
- API/SDK documentados;
- idiomas e taxonomias regionais;
- biblioteca de experiências por segmento;
- marketplace de integrações, não de perfumes;
- expansão para outros mercados com revisão de fontes, idioma e legislação.

## 7. Capacidades compartilhadas

| Capacidade | B2C | B2B |
|---|---|---|
| Catálogo factual e taxonomia | Público e versionado | Referenciado pelo tenant |
| Recomendador | Perfil e contexto pessoal | Perfil, contexto, catálogo e estoque |
| RAG | Conhecimento aprovado | Core aprovado + documentos privados isolados |
| Memória | Local por padrão | Consentida e vinculada ao tenant |
| IA | Explica candidatos | Auxilia o profissional, sem escolher fora do estoque |
| Analytics | Local/consentido | Agregado, isolado e auditável |
| Monetização | Avulso, assinatura, afiliado | Licença, implantação, uso e white-label |

Componentes compartilhados devem viver em contratos de domínio comuns. Regras específicas de comércio, tenant ou assinatura não entram no Knowledge Core.

## 8. Ordem de implementação recomendada

### Marco 0 — Confiança

- concluir base, grafo, RAG, conjunto ouro e segurança;
- emitir o relatório `ready_for_product_pilot`.

### Marco 1 — Aprendizado

- iniciar beta B2C fechado;
- executar descoberta B2B;
- instrumentar métricas sem conteúdo privado.

### Marco 2 — Primeira receita

- lançar Passaporte Olfativo;
- entregar Antiquário Pro a parceiros piloto;
- medir valor antes de ampliar infraestrutura.

### Marco 3 — Recorrência

- testar Privé com usuários recorrentes;
- converter Pro em piloto pago;
- implantar autenticação e billing somente para os fluxos validados.

### Marco 4 — Distribuição

- integrar afiliados com firewall de independência;
- lançar Maison para um primeiro parceiro;
- publicar contratos de integração e operação.

### Marco 5 — Escala responsável

- comunidade moderada;
- inteligência comercial agregada;
- onboarding B2B self-service;
- expansão de catálogo, regiões e idiomas.

## 9. Métricas norteadoras

### Confiança

- taxa de claims sustentados;
- conflitos e ambiguidades por release;
- precisão da recuperação;
- violações de filtros duros;
- fallback e disponibilidade;
- incidentes de privacidade.

### Valor B2C

- conclusão de consulta;
- desejo de experimentar;
- registro após uso;
- coerência percebida;
- retorno em 7/30/90 dias;
- conversão de Passaporte e Privé;
- cancelamento e reembolso.

### Valor B2B

- ativação de profissionais;
- tempo para recomendar;
- uso semanal;
- conversão assistida;
- ticket e devolução;
- qualidade da importação;
- retenção de tenants;
- custo de suporte e margem.

Métricas de receita nunca substituem métricas de confiança. Crescimento com aumento de recomendação inadequada bloqueia a próxima fase.

## 10. Modelo de decisão por fase

Cada fase termina com uma das decisões:

- **avançar:** critérios de confiança e valor atingidos;
- **iterar:** valor existe, mas há fricção ou cobertura insuficiente;
- **reduzir escopo:** apenas uma persona ou jornada funciona;
- **interromper:** risco, custo ou ausência de valor não justificam continuar.

Nenhuma fase avança somente porque o código está pronto. É necessário demonstrar comportamento seguro e valor observado.

## 11. Fora de escopo até validação posterior

- ranking influenciado por patrocínio;
- marketplace próprio ou estoque do Antiquário;
- fracionamento e venda direta de perfumes/decants;
- compartilhamento de memória pessoal entre empresas;
- treinamento de modelos com conteúdo privado sem consentimento específico;
- previsão química ou dermatológica individual;
- promessa de duração, elogios ou reação emocional garantida;
- autonomia da IA para publicar fatos ou alterar o catálogo;
- venda ou sublicenciamento indiscriminado do banco bruto.

## 12. Definição de pronto comercial

O Antiquário estará pronto para uma operação comercial inicial quando:

1. o Gate de Confiança Olfativa estiver aprovado e versionado;
2. uma pessoa conseguir entender por que recebeu cada recomendação;
3. a experiência funcionar com IA ativa, indisponível ou desativada;
4. feedback de pele melhorar a memória pessoal sem virar verdade coletiva automaticamente;
5. dados B2C e B2B estiverem isolados e apagáveis;
6. ranking e monetização estiverem tecnicamente separados;
7. um fluxo B2C e um fluxo B2B tiverem valor validado com pessoas reais;
8. cobrança, suporte, reembolso e incidentes tiverem responsáveis e procedimentos;
9. cada release puder ser auditada e revertida;
10. a promessa comercial permanecer menor ou igual ao que a evidência permite entregar.
