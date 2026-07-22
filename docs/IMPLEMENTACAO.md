# Arquitetura e plano de implementação — O Antiquário

## 1. Decisões arquiteturais

### 1.1 Local-first

Catálogo, perfil, coleção, diário, busca e recomendação básica executam no dispositivo. Isso reduz custo, latência, exposição de dados e dependência de serviços externos.

### 1.2 IA como camada de linguagem

O Gemini interpreta a solicitação e explica resultados. A seleção dos perfumes acontece no motor local. Se o Gemini falhar, templates produzem uma resposta funcional.

### 1.3 Dados como produto versionado

O catálogo será compilado durante o build para arquivos estáticos versionados. Cada registro carregará proveniência e confiança. Dados com obrigações incompatíveis permanecerão fisicamente separados.

### 1.4 Backend mínimo

O único backend obrigatório do MVP será um Cloudflare Worker para proteger a chave do Gemini, validar entradas e controlar abuso. Perfil e diário não serão enviados ao servidor como registros persistentes.

## 2. Stack proposta

| Camada | Tecnologia | Motivo |
|---|---|---|
| Monorepo | pnpm workspaces | Simples, gratuito e eficiente |
| Linguagem | TypeScript | Tipos compartilhados entre app, Worker e dados |
| Frontend | React + Vite | PWA leve e ecossistema estável |
| UI | CSS Modules ou Tailwind | Escolha final após protótipo visual |
| Estado remoto | TanStack Query | Controle de chamadas e erros do companion |
| Estado local | Zustand | Estado de sessão simples |
| Persistência | IndexedDB com Dexie | Perfil, coleção e diário locais |
| Validação | Zod | Mesmo contrato no frontend, Worker e pipeline |
| Busca | MiniSearch ou índice próprio | Pesquisa offline no catálogo inicial |
| Worker | Cloudflare Workers + Hono | Proxy pequeno, validação e streaming |
| IA | Google Gen AI SDK | SDK oficial do Gemini API |
| Testes | Vitest + Testing Library + Playwright | Unidade, componente e ponta a ponta |
| Qualidade | ESLint + Prettier + TypeScript strict | Consistência e segurança |
| CI | Pipeline compatível com provedor Git | Verificações reproduzíveis |

As bibliotecas serão confirmadas durante a Sprint 1 para evitar dependências desnecessárias.

## 3. Estrutura esperada do repositório

```text
o-antiquario/
├─ apps/
│  ├─ web/                    # PWA React
│  └─ worker/                 # Proxy seguro do Gemini
├─ packages/
│  ├─ domain/                 # Tipos, schemas e regras centrais
│  ├─ recommender/            # Filtros, score e explicações locais
│  ├─ data-pipeline/          # Importadores e normalização
│  ├─ catalog/                # Artefatos compilados e índices
│  └─ ui/                     # Componentes compartilhados
├─ data/
│  ├─ core/                   # CC0 e curadoria própria
│  ├─ obf/                    # ODbL isolado
│  ├─ sources/                # Manifestos de proveniência
│  ├─ staging/                # Entrada ainda não aprovada
│  └─ rejected/               # Registro do que não pode ser usado
├─ scripts/
│  ├─ ingest/
│  ├─ normalize/
│  ├─ validate/
│  └─ report/
├─ tests/
│  ├─ fixtures/
│  └─ golden-scenarios/
├─ docs/
│  ├─ adr/
│  ├─ ESCOPO.md
│  ├─ ROADMAP.md
│  └─ IMPLEMENTACAO.md
└─ README.md
```

## 4. Modelo de domínio

### 4.1 Fragrância

```ts
type Confidence = "high" | "medium" | "low" | "unknown";
type EvidenceKind =
  | "manufacturer"
  | "open_source"
  | "curated"
  | "community"
  | "estimated"
  | "user";

interface Evidence {
  sourceId: string;
  sourceUrl?: string;
  kind: EvidenceKind;
  license: string;
  retrievedAt: string;
  confidence: Confidence;
  method?: string;
}

interface SourcedValue<T> {
  value: T;
  evidence: Evidence[];
}

interface Fragrance {
  id: string;
  name: SourcedValue<string>;
  brand: SourcedValue<string>;
  year?: SourcedValue<number>;
  country?: SourcedValue<string>;
  concentrations: SourcedValue<string[]>;
  segments: SourcedValue<string[]>;
  perfumers: SourcedValue<string[]>;
  family?: SourcedValue<string>;
  topNotes: SourcedValue<string[]>;
  heartNotes: SourcedValue<string[]>;
  baseNotes: SourcedValue<string[]>;
  accords: SourcedValue<WeightedTag[]>;
  performance: PerformanceProfile;
  suitability: SuitabilityProfile;
  priceTier?: SourcedValue<1 | 2 | 3 | 4 | 5>;
  lastReviewedAt: string;
}
```

### 4.2 Desempenho

```ts
interface MetricEstimate {
  value: number;            // normalizado de 0 a 1
  sampleSize?: number;
  confidence: Confidence;
  evidence: Evidence[];
}

interface PerformanceProfile {
  longevity: MetricEstimate;
  projection: MetricEstimate;
  sillage: MetricEstimate;
}
```

Desempenho pessoal ficará separado do desempenho agregado para não sobrescrever a experiência individual.

### 4.3 Perfil e diário

```ts
interface UserProfile {
  schemaVersion: number;
  likedFragranceIds: string[];
  dislikedFragranceIds: string[];
  preferredNotes: WeightedTag[];
  avoidedNotes: WeightedTag[];
  preferredAccords: WeightedTag[];
  desiredProjection: number;
  budgetTier?: number;
  settings: {
    aiEnabled: boolean;
    aiConsentAt?: string;
    language: "pt-BR" | "en";
  };
}

interface WearLog {
  id: string;
  fragranceId: string;
  wornAt: string;
  sprays?: number;
  applicationAreas?: string[];
  context: RecommendationContext;
  openingRating?: number;
  heartRating?: number;
  drydownRating?: number;
  longevityHours?: number;
  projectionRating?: number;
  wouldWearAgain?: boolean;
  privateNotes?: string;    // nunca enviado ao Gemini por padrão
}
```

## 5. Pipeline de dados

### 5.1 Fluxo

```text
Fonte permitida
  → download/importação reproduzível
  → staging
  → validação de licença e schema
  → normalização de nomes e notas
  → deduplicação
  → revisão de conflitos
  → catálogo core ou camada isolada
  → relatório de cobertura
  → artefatos estáticos versionados
```

### 5.2 Manifesto de fonte

Cada fonte terá um manifesto semelhante a:

```yaml
id: wikidata
name: Wikidata
url: https://www.wikidata.org/
license: CC0-1.0
usage: core
redistribution: allowed
attribution_required: false
commercial_use: allowed
reviewed_at: 2026-07-22
notes: Structured data only; media licenses are evaluated separately.
```

### 5.3 Regras de importação

- Importadores nunca publicam diretamente no catálogo.
- Todo registro deve ter `sourceId` e `retrievedAt`.
- Conflitos geram relatório; não são resolvidos silenciosamente.
- Texto editorial de terceiros não é importado.
- URLs de imagem passam por validação de licença independente.
- Dados ODbL não são fundidos ao artefato `core`; a associação acontece por referência.
- Datasets derivados de scraping são rejeitados mesmo quando republicados com rótulo CC0 sem prova de origem compatível.

### 5.4 Knowledge Core e vault editorial

O conhecimento narrativo vive em `knowledge/vault`, separado do catálogo factual. Cada nota possui ID global, proveniência, confiança, estado de revisão, relações tipadas e wikilinks compatíveis com Obsidian.

O compilador em `src/knowledge` executa:

```text
Markdown + YAML
  → validação Zod
  → conferência no manifesto de fontes
  → resolução de relações e wikilinks
  → chunking por seção semântica
  → documentos + chunks + grafo + manifesto
```

Somente documentos aprovados com fontes `allowed_core` entram na release. O diretório `00_Inbox`, templates e itens rejeitados não são indexados. A versão é derivada de SHA-256 do conteúdo, permitindo builds idempotentes.

O Cerberus permanece separado conforme o ADR 0001. Uma ponte futura exportará apenas decisões, arquitetura e aprendizados consolidados, nunca todo o catálogo ou memória privada.

## 6. Motor de recomendação

### 6.1 Etapas

1. Normalizar o pedido do usuário.
2. Aplicar regras duras de exclusão.
3. Gerar candidatos por preferências, notas e coleção.
4. Calcular componentes de pontuação.
5. Penalizar dados de baixa confiança.
6. Aplicar diversidade para evitar três opções quase idênticas.
7. Retornar top 10 com rastreamento dos fatores.
8. Selecionar top 3 para apresentação.

### 6.2 Fórmula inicial

```text
score =
  preferenceMatch  * 0.30 +
  contextFit       * 0.25 +
  performanceFit   * 0.15 +
  personalHistory  * 0.10 +
  budgetFit        * 0.10 +
  dataConfidence   * 0.05 +
  controlledNovelty* 0.05
```

Todos os componentes ficam entre 0 e 1. A versão dos pesos será incluída no resultado para permitir reprodução.

### 6.3 Contexto climático sem API obrigatória

O MVP recebe temperatura e umidade manualmente ou usa valores aproximados escolhidos pelo usuário. Dessa forma, nenhuma API climática é requisito. Uma integração automática poderá ser adicionada apenas se a licença e a gratuidade forem compatíveis.

### 6.4 Explicação determinística

O motor produz fatos explicativos estruturados:

```json
{
  "fragranceId": "example-id",
  "score": 0.82,
  "strengths": [
    { "factor": "context", "messageKey": "good_for_warm_indoor" },
    { "factor": "preference", "messageKey": "matches_citrus_woody" }
  ],
  "tradeoffs": [
    { "factor": "performance", "messageKey": "may_need_reapplication" }
  ],
  "confidence": "medium"
}
```

Templates localizados transformam isso em resposta mesmo sem Gemini.

## 7. Integração Gemini

### 7.1 Responsabilidade

O Gemini recebe um pacote pequeno e anônimo:

- intenção normalizada;
- contexto em categorias, não coordenadas;
- preferências relevantes, sem identificação;
- até dez candidatos com campos necessários;
- explicações calculadas pelo motor;
- contrato da resposta.

### 7.2 Modelo configurável

```env
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_API_KEY=secret
GEMINI_TIMEOUT_MS=8000
GEMINI_MAX_OUTPUT_TOKENS=700
```

O código não dependerá de aliases como `latest`. Uma troca de modelo exigirá apenas configuração e testes de contrato.

### 7.3 Contrato da resposta

```ts
const CompanionResponse = z.object({
  summary: z.string().max(600),
  recommendations: z.array(z.object({
    fragranceId: z.string(),
    explanation: z.string().max(500),
    caveat: z.string().max(300).optional(),
  })).min(1).max(3),
  confidenceNote: z.string().max(300),
  followUpQuestion: z.string().max(240).optional(),
});
```

Após validar o schema, o Worker também confirma que todos os IDs retornados pertencem à lista enviada. Qualquer violação aciona fallback.

### 7.4 Prompt de sistema

Regras centrais:

- atuar como consultor de perfumaria, não como banco de dados autônomo;
- usar somente os candidatos e fatos fornecidos;
- não inventar notas, desempenho, preço ou disponibilidade;
- indicar incerteza;
- não oferecer diagnóstico médico;
- responder em português claro;
- devolver somente JSON compatível com o schema.

### 7.5 Controle de custo e cota

- Nenhum projeto com faturamento habilitado será requisito do MVP.
- Limite de chamadas por IP/usuário e janela de tempo.
- Uma chamada por recomendação concluída; digitação não dispara o modelo.
- Contexto e saída limitados.
- Cache apenas de respostas anônimas e genéricas.
- Erro `429` abre circuit breaker temporário.
- Estado da IA exibido na interface sem impedir o uso local.

## 8. Worker e segurança

### 8.1 Endpoint

`POST /api/companion/recommend`

Fluxo:

1. Verificar método, origem e tamanho.
2. Validar token antiabuso, quando habilitado.
3. Aplicar rate limit.
4. Validar payload com Zod.
5. Remover campos não permitidos.
6. Chamar Gemini com timeout.
7. Validar resposta e IDs.
8. Retornar resposta ou erro tipado para fallback.

### 8.2 Proteções

- `GEMINI_API_KEY` em secret binding.
- CORS limitado aos domínios do projeto.
- Payload máximo inicial de 32 KB.
- Sem proxy genérico de prompts.
- Sem persistência de texto livre.
- Logs com request ID, latência, status e contagem aproximada, nunca conteúdo integral.
- Rate limit com armazenamento compatível com a camada gratuita.
- Headers de segurança e política de conteúdo no frontend.

## 9. Privacidade

### 9.1 Classificação

| Dado | Armazenamento | Envio ao Gemini |
|---|---|---|
| Preferências normalizadas | IndexedDB | Apenas subconjunto anônimo |
| Coleção | IndexedDB | Apenas IDs candidatos |
| Diário e texto privado | IndexedDB | Não |
| Temperatura/faixa de umidade | Sessão/IndexedDB | Sim, categorizada |
| Localização exata | Não coletada | Não |
| Nome/e-mail | Não exigidos no MVP | Não |
| IP | Infraestrutura transitória | Não incluído no prompt |

### 9.2 Consentimento

Antes da primeira chamada, a interface explica:

- que a funcionalidade usa o Gemini API gratuito;
- que prompts e respostas podem ser usados pelo Google para melhoria e revisão humana;
- quais dados serão enviados;
- que a IA pode ser desativada;
- que o produto é destinado a maiores de 18 anos.

## 10. PWA e armazenamento local

### 10.1 IndexedDB

Stores propostas:

- `profile`
- `collection`
- `wearLogs`
- `settings`
- `catalogMetadata`
- `genericResponseCache`

Cada store terá `schemaVersion` e migração testada.

### 10.2 Offline

- Shell da aplicação e catálogo core armazenados pelo service worker.
- Busca, detalhes, coleção, diário e recomendação determinística funcionam offline.
- O companion informa claramente quando a explicação de IA não está disponível.
- Atualizações de catálogo usam manifesto com versão e hash.

## 11. Testes

### 11.1 Unidade

- normalização de notas e marcas;
- filtros e exclusões;
- cada componente do score;
- diversidade do top 3;
- confiança por tamanho de amostra;
- templates de fallback;
- migrações do armazenamento local.

### 11.2 Contrato

- payload frontend → Worker;
- Worker → Gemini simulado;
- validação e rejeição de IDs estranhos;
- respostas truncadas ou JSON inválido;
- mudanças de modelo.

### 11.3 Integração

- importação e compilação do catálogo;
- recomendação com perfil e contexto;
- consentimento e ativação da IA;
- `429`, timeout, `5xx` e rede offline;
- exportação e exclusão do perfil.

### 11.4 Ponta a ponta

- onboarding → recomendação → diário;
- pesquisa → comparação → coleção;
- modo offline;
- teclado e leitor de tela nos fluxos críticos.

### 11.5 Conjunto ouro

Trinta cenários versionados cobrirão:

- calor úmido e frio seco;
- escritório, encontro, festa e ar livre;
- alta e baixa projeção;
- nicho, designer, brasileiro, árabe e acessível;
- preferências conflitantes;
- dados de baixa confiança;
- ausência completa do Gemini.

## 12. Observabilidade gratuita

- Métricas agregadas no Worker: status, latência e fallback.
- Logs sem conteúdo de prompt.
- Painel local do pipeline: cobertura, conflitos e fontes vencidas.
- Relatório de bundle e desempenho no CI.
- Nenhuma ferramenta paga obrigatória.

## 13. Deploy

### 13.1 Ambientes

- `local`: catálogo e Worker local com Gemini opcional.
- `preview`: dados sintéticos ou chave de teste com cota restrita.
- `production`: domínio permitido, secrets e limites conservadores.

### 13.2 Processo

1. Validar dados e licenças.
2. Executar lint, tipos e testes.
3. Compilar catálogo e verificar hashes.
4. Gerar PWA.
5. Publicar Worker com secret binding.
6. Executar smoke tests com IA ativa e desativada.
7. Publicar frontend estático.
8. Registrar versão do catálogo, recomendador e prompt.

## 14. Ordem recomendada de implementação

1. Criar monorepo e contratos Zod.
2. Criar manifesto de fontes.
3. Implementar catálogo manual mínimo de 20 fragrâncias.
4. Implementar busca e recomendador contra esse catálogo.
5. Criar conjunto ouro e fallback.
6. Montar PWA com onboarding e recomendação.
7. Integrar Worker e Gemini.
8. Implementar coleção e diário.
9. Automatizar importações e ampliar catálogo.
10. Concluir segurança, acessibilidade e beta.

Essa ordem permite validar o valor do produto antes de investir tempo em volume de dados ou acabamento.

## 15. Definição de pronto por funcionalidade

Uma funcionalidade está pronta somente quando:

- comportamento e limites estão documentados;
- tipos e validação existem;
- caminhos feliz, vazio e de erro foram implementados;
- testes relevantes passam;
- funciona sem Gemini quando aplicável;
- acessibilidade foi verificada;
- não introduz segredo ou dado pessoal nos logs;
- dados exibidos têm proveniência e confiança;
- a mudança aparece no changelog.
