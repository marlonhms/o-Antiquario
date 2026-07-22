# Plataforma de dados v1

## Objetivo

O pipeline Python transforma fontes permitidas em staging rastreável e depois publica um catálogo DuckDB/Parquet. Ele é uma ferramenta de manutenção; o usuário final recebe somente releases prontas.

## Ambiente

Requisitos:

- Python 3.12 ou superior;
- uma virtualenv local `.venv`;
- DuckDB instalado conforme `pyproject.toml`.

O launcher `scripts/run-python.mjs` encontra a virtualenv no Windows, Linux ou macOS. Também aceita o caminho explícito em `ANTIQUARIO_PYTHON`.

Preparação em uma máquina nova:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c requirements-data.lock -e .
```

O projeto declara a faixa compatível no `pyproject.toml` e registra a versão verificada em `requirements-data.lock`.

## Fluxo

```text
Wikidata SPARQL
  → snapshot bruto imutável por hash
  → normalização e deduplicação por QID
  → data/staging/wikidata/fragrances.jsonl + olfactory-descriptors.jsonl
  → quarentena + relatório de qualidade
  → validação e tabelas relacionais
  → data/catalog/catalog.duckdb
  → Parquet + catalog-manifest.json
  → resolução com o Knowledge Core
  → release JSON versionada para a PWA
```

O conector utiliza a classe `perfume (Q131746)`, marca/fabricante, país de origem, perfumista, datas e site oficial. Quando declarado, também importa `cheira a` (`P5872`) como **descritor olfativo factual**. Esse campo não é tratado como nota nem como camada de pirâmide: a classificação topo/coração/fundo continua editorial e verificável.

## Comandos

Teste totalmente offline:

```powershell
npm run data:test
npm run data:demo
```

Sincronização real e publicação:

```powershell
npm run data:sync:wikidata
npm run data:build
npm run data:status
npm run catalog:compile
npm run curation:queue
```

`catalog:compile` gera os arquivos públicos compactos, o índice de busca local e o relatório de resolução de entidades. O contrato completo está em [Catálogo Web e resolução de entidades](CATALOGO_WEB.md).

`curation:queue` cria rascunhos internos a partir do catálogo factual, sem inserir inferências olfativas no core. Veja [Curadoria Editorial](CURADORIA_EDITORIAL.md).

## Auditoria de propriedades

Antes de adicionar novos campos ao catálogo, a auditoria consulta quais propriedades estruturadas realmente aparecem nos QIDs de fragrância já importados. Ela não altera o catálogo nem infere pirâmide olfativa.

```powershell
npm run data:audit:wikidata
```

O relatório sai em `data/staging/wikidata/property-audit.json`, com cobertura por propriedade e uma lista explícita de propriedades ainda não mapeadas pelo pipeline. Atualmente `P5872` (`cheira a`) é mapeada como descritor factual; não como pirâmide.

Na importação atual, há 1.110 relações `cheira a` distribuídas por 132 das 282 fragrâncias factuais. Elas tornam a descoberta e a fila de curadoria mais conectadas, mas não são suficientes para afirmar topo, coração, fundo, acorde, desempenho ou contexto de uso.

## Descoberta regional no Wikidata

A consulta principal é ampla. Para aumentar a chance de cobertura específica sem substituir o catálogo existente, a sincronização pode acrescentar buscas por país de origem (`P495`) e mesclar os resultados pelo QID:

```powershell
npm run data:sync:wikidata -- --discovery-country Q155 --discovery-country Q878
npm run data:build
npm run catalog:compile
npm run curation:queue
```

`Q155` é Brasil e `Q878` são Emirados Árabes Unidos. O filtro é estrito: ele só seleciona fragrâncias cujo país de origem esteja declarado no Wikidata; país da marca não é inferido como país da fragrância.

## Idempotência

O snapshot usa o hash da consulta e do payload. Se o mesmo conteúdo reaparecer, a primeira data de recuperação é preservada. Staging, hashes de registro e versão do catálogo permanecem iguais.

## Governança

- O User-Agent identifica o projeto.
- HTTP 429 e falhas temporárias acionam espera exponencial limitada.
- Apenas dados estruturados CC0 do Wikidata entram no core.
- IDs externos são preservados.
- Rótulos ausentes e materiais genéricos detectáveis são enviados à quarentena.
- O relatório registra cobertura de marca, perfumista, país, ano e site oficial.
- O catálogo não importa textos editoriais, avaliações ou imagens.
- A fixture offline é sintética e nunca representa produtos comerciais reais.
