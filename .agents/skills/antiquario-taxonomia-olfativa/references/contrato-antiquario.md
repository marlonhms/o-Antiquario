# Contrato conceitual do Antiquário

## Regra central

Separar o que o perfume declara, o que uma pessoa percebe, o que uma taxonomia organiza e o que um modelo prevê. Uma relação entre molécula e descritor não comprova uma nota na pirâmide de um perfume.

## Camadas

| Tipo | Representa | Não representa automaticamente |
| --- | --- | --- |
| `fragrance` | Produto comercial acabado | Fórmula química completa |
| `olfactory-note` | Nota declarada ou curada para uma composição | Ingrediente físico comprovado |
| `accord` | Impressão composta da fragrância | Molécula isolada |
| `raw-material` | Matéria natural, extrato, base ou ingrediente | Nota declarada em qualquer perfume |
| `molecule` | Composto químico odorante | Cheiro invariável em toda concentração |
| `odor-descriptor` | Fonte ou caráter percebido, como floral ou pera | Ingrediente ou posição da pirâmide |
| `odor-quality` | Qualidade como fresco, pungente ou agradável | Fonte material do cheiro |
| `olfactory-family` | Categoria ampla de navegação | Verdade exclusiva ou universal |

## Relações científicas permitidas

| Predicado | Origem | Destino | Uso |
| --- | --- | --- | --- |
| `described-as` | nota, matéria-prima ou molécula | descritor | Associação perceptiva com evidência |
| `has-quality` | nota, matéria-prima, molécula ou descritor | qualidade | Qualidade perceptiva ou hedônica |
| `belongs-to-olfactory-family` | descritor | família | Rota taxonômica não exclusiva |
| `broader-descriptor-than` | descritor | descritor | Hierarquia entre descritores |
| `broader-quality-than` | qualidade | qualidade | Hierarquia entre qualidades |
| `derived-from` | nota | matéria-prima | Origem material documentada |
| `contains-odorant` | matéria-prima | molécula | Composição química documentada |

## Relações comerciais protegidas

`has-note`, `has-top-note`, `has-heart-note`, `has-base-note` e quaisquer predicados `declares-*` exigem evidência explícita ligada ao perfume. Não gerar essas relações a partir de taxonomia, modelo, similaridade ou molécula.

## Proveniência mínima

Cada candidato deve conter:

- `source_id`;
- `locator` verificável;
- `license` tal como informada pela fonte;
- `claim_scope` específico;
- `confidence`;
- `claim_nature`;
- método que produziu a relação;
- rótulo original quando houve normalização ou tradução.

## Promoção

Manter `status: candidate` durante a geração automática. Promover somente por um pipeline explícito que confirme contrato de tipos, política de fonte, destinos existentes, ausência de conflito e evidência suficiente.

## Arquivos do projeto a consultar

- `src/knowledge/schema.ts`: tipos e frontmatter do Knowledge Core;
- `src/knowledge/graph.ts`: contratos de relações;
- `src/knowledge/validation.ts`: política de promoção;
- `data/sources.yml`: estado e condições das fontes;
- `data/taxonomy/taxonomy.yml`: vocabulário operacional atual;
- `docs/TAXONOMIA.md`: documentação humana;
- `docs/CONHECIMENTO_RAG.md`: arquitetura do grafo e RAG.
