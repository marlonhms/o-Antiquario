# O Antiquário

Companion e consultor digital especializado em perfumaria mundial, da perfumaria acessível à alta perfumaria, construído com dados abertos, curadoria própria e uma camada conversacional baseada no plano gratuito do Gemini.

## Princípios do projeto

- Custo operacional obrigatório igual a zero no MVP.
- Nenhum scraping autenticado, uso de cookies de terceiros ou tentativa de contornar proteções anti-bot.
- Recomendação calculada por um motor determinístico e explicada pela IA; a IA não é a fonte dos fatos.
- Funcionamento degradado sem Gemini quando a cota gratuita estiver indisponível.
- Dados acompanhados de origem, licença, data de consulta e nível de confiança.
- Privacidade por padrão: o Gemini recebe apenas contexto anônimo e candidatos já selecionados.
- Experiência principal em português do Brasil, com taxonomia preparada para múltiplos idiomas.

## Documentação

- [Escopo do produto](docs/ESCOPO.md)
- [Roadmap detalhado](docs/ROADMAP.md)
- [Arquitetura e implementação](docs/IMPLEMENTACAO.md)
- [Direção visual](docs/DIRECAO_VISUAL.md)
- [Fontes e licenças](docs/FONTES_E_LICENCAS.md)
- [Taxonomia olfativa](docs/TAXONOMIA.md)
- [Knowledge Core e memória RAG](docs/CONHECIMENTO_RAG.md)
- [Plataforma de dados](docs/PLATAFORMA_DADOS.md)
- [Catálogo Web e resolução de entidades](docs/CATALOGO_WEB.md)
- [Curadoria Editorial](docs/CURADORIA_EDITORIAL.md)

## Estado

O núcleo determinístico e a primeira interface local estão funcionais. A versão atual contém regras de exclusão, pontuação explicável, confiança, histórico pessoal, diversidade do top 3, fallback sem IA e um formulário React responsivo ligado diretamente ao recomendador.

## Interface local

```bash
npm install
npm run dev
```

Abra `http://127.0.0.1:5173/`. Os dados do formulário ficam somente no navegador e o catálogo exibido nesta etapa é sintético.

## Desenvolvimento do núcleo

Requer Node.js 24 ou superior.

```bash
npm install
npm run typecheck
npm test
npm run demo
npm run knowledge:validate
npm run knowledge:build
npm run catalog:compile
```

O catálogo presente em `src/recommender/fixtures.ts` é inteiramente sintético e existe apenas para testes; não será publicado como dado real.

O vault editorial compatível com Obsidian vive em `knowledge/vault`. O build valida proveniência, resolve sinapses e publica artefatos determinísticos em `knowledge/compiled`.

## Pipeline de dados

O importador é uma ferramenta interna. Ele salva snapshots imutáveis do Wikidata, normaliza entidades em staging e publica DuckDB e Parquet; o usuário final nunca executa essa rotina.

```powershell
# em uma máquina nova
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c requirements-data.lock -e .

npm run data:test
npm run data:demo
npm run data:sync:wikidata
npm run data:build
npm run catalog:compile
npm run curation:queue
```

O compilador publica uma release JSON determinística em `data/releases` e a cópia estável consumida pela PWA em `apps/web/public/catalog`. A interface identifica quando essa base factual está pronta, mas o ranking permanece ligado ao catálogo sintético até que os registros reais tenham notas, acordes e desempenho curados.

## Restrições externas relevantes

As cotas gratuitas de serviços externos podem mudar. O projeto deverá consultar os limites ativos do Gemini no Google AI Studio e manter alternativas configuráveis. Em 22 de julho de 2026, a documentação oficial informa gratuidade de entrada e saída para modelos Flash selecionados, mas não garante capacidade fixa.

- [Preços do Gemini API](https://ai.google.dev/gemini-api/docs/pricing)
- [Limites do Gemini API](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Termos adicionais do Gemini API](https://ai.google.dev/gemini-api/terms)
- [Licenciamento do Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing)
- [Documentação do Open Beauty Facts](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorials/scanning-cosmetics-pet-food-and-other-products/)
- [Pyrfume](https://pyrfume.org/)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
- [Biblioteca de padrões IFRA](https://ifrafragrance.org/standards-library)
