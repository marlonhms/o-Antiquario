# Roadmap de continuidade — O Antiquário

> **Estado consolidado em 22/07/2026.** Este é o documento de handoff para o próximo agente. Ele descreve a ordem de trabalho, os limites do projeto e os critérios de aceite; não autoriza decidir, em nome do proprietário do projeto, a permissão ou a licença de uma nova fonte.

## 1. Norte do produto

O Antiquário é um companion local-first de perfumaria. Ele deve recomendar e explicar escolhas com dados rastreáveis, sem transformar uma resposta de IA em fonte factual.

Princípios que não podem ser flexibilizados durante a continuidade:

- custo operacional zero no MVP;
- interface e recomendador continuam úteis sem IA ou rede;
- o motor determinístico escolhe os candidatos; a IA, futuramente, apenas conversa e explica;
- cada fato preserva fonte, data, método e localização da evidência;
- dado factual, interpretação editorial e memória pessoal ficam em camadas distintas;
- nenhuma automação autenticada, cookie de terceiros, bypass anti-bot ou scraping de fontes proibidas;
- o proprietário decide se uma fonte e seu uso são adequados. O agente registra opções, riscos técnicos e proveniência, mas não substitui essa decisão;
- não importar textos publicitários, reviews, imagens ou páginas inteiras como corpus do RAG.

## 2. Fotografia atual do repositório

### Entregue e publicado

| Área | Estado atual | Evidência no repositório |
|---|---|---|
| Interface local | PWA React/Vite com direção visual vinho e dourado, consulta em três etapas e layout responsivo | `apps/web/src/App.tsx`, `apps/web/src/styles.css` |
| Consulta reativa | Toda mudança na consulta recalcula o ranking imediatamente; o botão final apenas leva o usuário à curadoria | commit `10e1ee4` |
| Recomendador | Motor determinístico, filtros duros, score explicável, confiança, diversidade, histórico local e fallback textual | `src/recommender/` |
| Dados de demonstração | Perfumes usados no ranking atual são **fixtures sintéticas**, não produtos reais | `src/recommender/fixtures.ts` |
| Base factual | Release local Wikidata com 282 perfumes, 276 descritores e 251 claims semânticos | `apps/web/public/catalog/` |
| Biblioteca Olfativa | Busca e ficha factual de perfume, marca, perfumista, país, ano, descritores e claims | commit `775d61d` |
| Pipeline | Snapshot, staging, DuckDB, Parquet, release JSON, auditorias e fixture offline | `pipeline/antiquario_data/` |
| Knowledge Core | Vault Obsidian, vínculos tipados, evidência como nó, health gates e fila de curadoria | `knowledge/`, `src/knowledge/` |
| Curadoria | Gera rascunhos factuais em `00_Inbox`; nada dessa fila entra no core automaticamente | `pipeline/antiquario_data/curation_queue.py` |

### Limites atuais importantes

1. A Biblioteca Olfativa mostra dados reais, mas o ranking ainda usa somente fixtures sintéticas. Isso é intencional: a maior parte dos 282 perfumes ainda não possui notas em pirâmide, acordes, desempenho e contexto aprovados.
2. `P5872` do Wikidata significa **descritor olfativo factual**. Ele não autoriza classificá-lo como nota de topo, coração, fundo ou acorde.
3. Os claims `P1552`, `P2360`, `P366` e `P4543` também são dados brutos. Não promover seus significados a regras de ranking sem contrato editorial explícito.
4. O grafo possui muitos registros em `knowledge/vault/00_Inbox`. Isso é esperado: são identidades aguardando evidência e revisão, não nós quebrados do core.
5. Gemini ainda não está integrado. Não antecipar essa etapa antes de existir um conjunto real, aprovado e testável de candidatos.

### Situação do Git no handoff

- Branch de trabalho: `main`.
- Último commit publicado no momento deste roadmap: `10e1ee4 fix: update recommendations as consultation changes`.
- O arquivo `docs/Bases De Dados De Perfumaria.md` é uma pesquisa do proprietário, não rastreada. Não modificar, adicionar ou commitar esse arquivo sem pedido explícito.

## 3. Arquitetura de dados que deve ser preservada

```text
Wikidata / catálogo oficial em PDF / futura fonte aprovada
  → raw local imutável (quando aplicável)
  → staging com hash e proveniência
  → quarentena de ambiguidade e conflito
  → catálogo factual versionado
  → fila editorial no Obsidian
  → Knowledge Core aprovado
  → catálogo elegível para ranking
  → IA apenas recebe candidatos já selecionados
```

| Camada | Finalidade | Pode alimentar ranking? |
|---|---|---:|
| `data/raw` | Arquivo original local ou snapshot autorizado | Não |
| `data/staging` | Extração estruturada, fatos ainda não validados | Não |
| `data/catalog` e release web | Identidade factual e relações rastreáveis | Ainda não, sozinha |
| `knowledge/vault/00_Inbox` | Rascunho de curadoria | Não |
| `knowledge/vault/10_Perfumes` aprovado | Conhecimento editorial com evidências | Sim, após contrato de ranking |
| `src/recommender/fixtures.ts` | Laboratório de UX e lógica | Somente demonstração |

## 4. Próxima prioridade: conector de catálogos oficiais em PDF

### Objetivo

Criar uma fonte local e auditável para catálogos que o proprietário disponibilizar manualmente — por exemplo, O Boticário, Natura e Eudora. O conector deve extrair fatos declarados pelo documento e encaminhá-los para revisão, sem inferir atributos ausentes.

### Escopo da primeira versão

- Receber somente PDFs colocados manualmente no repositório local; não implementar downloader, scraper de site ou login.
- Calcular SHA-256 do arquivo e registrar marca, edição, caminho local, data de ingestão e páginas processadas.
- Extrair texto por página quando o PDF contiver camada textual.
- Produzir uma saída estruturada de candidatos a produto e claims com referência de página.
- Reconhecer apenas campos declarados: nome, marca, linha, concentração, volume, notas, família, pirâmide e data/edição quando estiverem explícitos.
- Separar notas de topo/coração/fundo apenas quando o catálogo declarar a camada. Uma lista sem camada vira `declared_notes_unlayered`.
- Resolver nomes de notas contra a taxonomia local; nomes desconhecidos entram na quarentena de vocabulário.
- Fazer matching conservador com Wikidata por nome normalizado + marca. Empates, colisões e ausência de match permanecem pendentes.
- Gerar uma fila editorial para aprovação humana, sem escrita direta no Knowledge Core ou no ranking.

### Não escopo da primeira versão

- OCR obrigatório: será uma capacidade opcional, acionada somente se um catálogo real for imagem e o proprietário aprovar a dependência local necessária.
- Extração de preço como verdade universal, cálculo de desempenho, família inferida por IA ou acorde deduzido por notas.
- Armazenar um corpus de texto comercial. A saída deve conter fatos normalizados e localizadores de página; o PDF original continua local.
- Baixar ou reutilizar imagens, logos ou materiais promocionais.
- Automatizar qualquer acesso a sites de terceiros.

### Contrato de entrada proposto

```text
data/raw/official-catalogs/
  <marca>/
    <edicao-ou-ano>.pdf
```

Os PDFs não devem entrar no Git por padrão. Antes de implementar, atualizar `.gitignore` para cobrir `data/raw/official-catalogs/**/*.pdf` e criar um `README.md` pequeno nesse diretório explicando a convenção. Somente fixtures sintéticas ou documentos cujo versionamento tenha sido explicitamente autorizado podem ser usados em testes.

### Contrato de saída proposto

```text
data/staging/official-pdf/
  <sha256>/
    document.json          # metadados, hash, fonte, versão do extrator
    pages.jsonl            # página, sucesso de extração e hash de texto
    claims.jsonl           # valor normalizado + página + método
    candidates.jsonl       # perfume candidato + status de matching
    quarantine.jsonl       # campos ambíguos ou termos desconhecidos
    report.json            # cobertura e erros por documento
```

Todo claim deve conter, no mínimo:

```json
{
  "document_hash": "sha256…",
  "source_id": "official_catalog_<marca>",
  "page": 12,
  "field": "top_note",
  "value": "bergamota",
  "extraction_method": "text-layer",
  "confidence": "declared",
  "review_status": "pending"
}
```

`source_id` só pode ser registrado depois da direção explícita do proprietário sobre a fonte e o uso pretendido. O agente pode criar a estrutura técnica e um perfil de parser, mas não deve afirmar que o material é permitido para redistribuição ou para o core.

### Implementação sugerida

1. Adicionar dependência Python mínima para leitura de PDF com texto (preferência: `pypdf`) ao `pyproject.toml` e ao lockfile.
2. Criar `pipeline/antiquario_data/official_pdf.py` com funções puras para hash, leitura por página, normalização e escrita de staging.
3. Criar perfis de extração configuráveis por marca em YAML/JSON; o núcleo não deve depender de regexes fixas para uma única diagramação.
4. Adicionar o subcomando `official-pdf` à CLI, inicialmente com `--input`, `--brand`, `--edition`, `--source-id` e `--dry-run`.
5. Implementar matching conservador e quarentena; não reutilizar o resolvedor para “adivinhar” identidade.
6. Criar testes com fixture sintética gerada localmente, incluindo: pirâmide explícita, lista sem camada, nota desconhecida, produto ambíguo e página sem texto.
7. Adicionar `npm run data:ingest:official-pdf` e documentação de execução local.
8. Só depois de validar 1–3 catálogos reais, adicionar OCR opcional e perfis por marca.

### Critérios de aceite

- Reexecutar o mesmo PDF produz o mesmo `document_hash` e a mesma saída normalizada.
- Cada campo extraído aponta para arquivo e página.
- Nenhuma nota sem camada declarada aparece como topo/coração/fundo.
- Nenhum match ambíguo cria ou altera registro factual automaticamente.
- Nenhum PDF bruto ou texto publicitário é enviado para a PWA, Gemini ou Git sem autorização explícita.
- `npm run data:test`, `npm test`, `npm run typecheck` e `npm run build` continuam verdes.

## 5. Prioridade seguinte: resolver termos e conectar o grafo

O PDF será valioso quando suas notas puderem criar relações confiáveis, e não apenas mais arquivos. Após o conector mínimo:

1. Criar um vocabulário de aliases por fonte, separado da taxonomia canônica.
2. Resolver cada termo de nota para um ID canônico ou quarentena.
3. Gerar relações factuais tipadas:
   - `declares-top-note`;
   - `declares-heart-note`;
   - `declares-base-note`;
   - `declares-unlayered-note`;
   - `declares-concentration`;
   - `declares-family`.
4. Criar rascunho em `00_Inbox` que cite a evidência do catálogo oficial.
5. Após revisão humana, mover somente o registro aprovado a `knowledge/vault/10_Perfumes` e executar `npm run knowledge:build`.
6. Acompanhar no relatório do grafo: percentual de perfumes conectados a notas, notas por camada, entidades em quarentena e cobertura por marca/região.

Meta inicial útil: aprovar 20 perfumes reais com ao menos uma evidência de identidade e uma relação olfativa declarada. A meta não é volume; é validar a cadeia completa de confiança.

## 6. Transição do ranking: fixtures → perfumes reais aprovados

Isso só começa quando houver um subconjunto editorialmente completo. Não misturar registros factuais incompletos ao ranking apenas para aumentar a quantidade.

### Etapas

1. Definir contrato `EligibleForRecommendation` com identidade, concentração, notas/acordes aprovados, contexto mínimo, desempenho/confiança e evidências.
2. Criar compilador que publica um catálogo de recomendação separado do catálogo factual.
3. Adaptar o recomendador para receber esse catálogo por injeção de dependência, mantendo fixtures nos testes.
4. Criar cenários ouro usando somente fragrâncias aprovadas.
5. Exibir na interface a distinção entre “dado declarado”, “curadoria editorial” e “estimativa”.
6. Remover o aviso de catálogo sintético somente quando a tela principal estiver realmente usando o catálogo aprovado.

### Gate de aceite

Não ligar a PWA ao ranking factual até haver, no mínimo, 20 perfumes aprovados e testes que provem exclusões, explicações, diversidade e fallback nesse conjunto.

## 7. IA Gemini Flash — somente após o gate do ranking factual

Quando o gate anterior passar:

1. Criar Worker/proxy com chave fora do bundle.
2. Enviar ao modelo somente contexto anônimo e candidatos já selecionados.
3. Validar a resposta em JSON Schema; a IA não pode introduzir perfume, nota ou afirmação factual fora do contexto fornecido.
4. Implementar limite de uso, timeout, retry curto, circuit breaker e templates locais de fallback.
5. Incluir consentimento e controle para desativar IA.
6. Verificar os limites e preços atuais diretamente na documentação oficial do Gemini antes de escolher o modelo.

## 8. Qualidade, operação e documentação

Essas tarefas podem seguir em paralelo às fases de dados, desde que não alterem os limites acima:

- adicionar CI para `typecheck`, testes TypeScript, testes Python e build;
- adicionar formatter/lint somente com configuração pequena e sem reformatação massiva do repositório;
- documentar ADRs já praticados: local-first, Cerberus separado, fontes e camadas de dados;
- adicionar testes de componente/e2e para a consulta reativa e Biblioteca Olfativa;
- medir tamanho da release e tempo de busca com catálogo maior;
- tornar o catálogo factual mais navegável: filtros por marca, ano, país e descritor, sem usá-los como score;
- implementar PWA offline, perfil, coleção e diário somente depois de estabilizar o modelo de dados elegível.

## 9. Primeira sessão recomendada para o próximo agente

1. Ler este roadmap, `docs/PLATAFORMA_DADOS.md`, `docs/CURADORIA_EDITORIAL.md`, `docs/FONTES_E_LICENCAS.md` e `data/sources.yml` por completo.
2. Confirmar o estado do Git e preservar `docs/Bases De Dados De Perfumaria.md` como arquivo do proprietário.
3. Rodar a baseline:

   ```powershell
   npm run typecheck
   npm test
   npm run data:test
   npm run build
   ```

4. Se houver PDF(s) de exemplo fornecido(s), iniciar a fase 4 exatamente pela estrutura de entrada, hash, saída de staging e fixture sintética. Se não houver, preparar apenas o conector genérico e seus testes — não baixar documentos por conta própria.
5. Após cada mudança no pipeline, testar a idempotência e atualizar a documentação operacional.
6. Antes de conectar qualquer dado novo ao ranking, parar no gate da seção 6 e pedir confirmação/direção ao proprietário.

## 10. Comandos úteis

```powershell
# Interface local
npm run dev

# Qualidade
npm run typecheck
npm test
npm run data:test
npm run build

# Pipeline factual existente
npm run data:sync:wikidata
npm run data:build
npm run knowledge:build
npm run catalog:compile
npm run curation:queue

# Auditoria do Wikidata
npm run data:audit:wikidata
npm run data:audit:values
```

## 11. Definição de pronto para a próxima entrega

A próxima entrega deve ser considerada pronta somente se:

- o extrator de PDF (ou sua primeira etapa) tiver testes reproduzíveis;
- a saída preservar hash, fonte e página;
- ambiguidades estiverem visíveis em quarentena, não ocultas por heurística;
- nenhum dado tiver sido promovido a pirâmide, acorde, desempenho ou ranking sem evidência e revisão apropriadas;
- a PWA continuar carregando localmente e os quatro comandos de qualidade passarem;
- documentação, changelog/commit e instruções de execução forem atualizados.
