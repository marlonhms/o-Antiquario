# Catálogo Web e resolução de entidades

## Objetivo

O Catalog Compiler transforma o catálogo factual e o Knowledge Core em uma release pequena, determinística e pronta para consumo local pela PWA. Ele é infraestrutura interna: o usuário final recebe apenas os arquivos publicados em `apps/web/public/catalog`.

## Fluxo

```text
Wikidata → DuckDB/Parquet ─┐
                           ├→ resolução de entidades → release JSON versionada → PWA
Knowledge Core/Obsidian ───┘
```

O comando completo é:

```powershell
npm run catalog:compile
```

Ele valida e compila o Knowledge Core antes de gerar o catálogo web.

## Identidade e resolução

A prioridade de identidade é:

1. identificador externo estável, atualmente o QID do Wikidata;
2. chave normalizada de nome, marca e ano;
3. revisão humana quando a chave normalizada encontra mais de um candidato.

Uma nota editorial do tipo `perfume` pode declarar:

```yaml
external_ids:
  wikidata: Q123
```

O compilador liga essa nota ao registro factual correspondente. Colisões de impressão digital nunca são mescladas automaticamente; entram em `resolution-report.json` com a ação `manual_review`.

## Artefatos públicos

- `manifest.json`: versão, hash, contagens e nomes dos arquivos.
- `fragrances.json`: registros factuais compactos e suas ligações editoriais.
- `entities.json`: dicionários deduplicados de marcas, perfumistas e países.
- `search-index.json`: índice invertido tolerante a acentos e prefixos.
- `resolution-report.json`: ligações realizadas e ambiguidades pendentes.

O mesmo conjunto é preservado em `data/releases/<releaseId>`. `data/releases/latest.json` aponta para a release atual, enquanto `apps/web/public/catalog` é o endereço estável usado pela interface.

## Release atual

A primeira release factual é `catalog-web-v1-0c2fb85e6ff6`, com 85 fragrâncias, 38 marcas, 49 perfumistas, 8 países e 464 termos de busca. Existe uma colisão ambígua encaminhada para revisão humana e nenhuma fusão automática.

As recomendações da tela continuam usando o catálogo sintético de laboratório até que uma amostra factual tenha cobertura editorial suficiente de notas, acordes e desempenho. A interface mostra essa separação explicitamente.

## Qualidade e reprodutibilidade

- A versão deriva do conteúdo, não do relógio.
- A mesma entrada produz bytes e `releaseId` iguais.
- A ordem de registros e entidades é estável.
- O manifesto e os índices são validados por testes Python e TypeScript.
- A busca roda inteiramente no dispositivo, sem chamadas externas.
