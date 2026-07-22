# Fontes e licenças — O Antiquário

## Objetivo

Toda fonte usada pelo projeto deve estar registrada em `data/sources.yml` antes de qualquer importação. O manifesto funciona como uma lista de permissão: fontes desconhecidas são rejeitadas, e nenhuma classificação é inferida automaticamente.

Esta documentação registra decisões técnicas de governança; não substitui aconselhamento jurídico.

## Classificações

| Classificação | Significado |
| --- | --- |
| `allowed_core` | Pode alimentar o catálogo principal redistribuível. |
| `allowed_isolated` | Pode ser usada apenas em artefato separado, preservando obrigações próprias. |
| `reference_only` | Pode orientar revisão humana, mas não alimentar importação em massa. |
| `pending_review` | Não entra em produção até revisão adicional da fonte ou do conjunto específico. |
| `prohibited` | Não pode ser ingerida nem acessada automaticamente pelo pipeline. |

## Decisões iniciais

### Wikidata — core permitido

Os dados estruturados relevantes são publicados sob CC0. O importador deverá respeitar as boas práticas de acesso e não presumir que imagens do Wikimedia Commons compartilhem a mesma licença do dado estruturado.

### Open Beauty Facts — camada ODbL isolada

O banco está sob ODbL e seus conteúdos individuais sob Database Contents License. Dados derivados dessa fonte não serão fundidos fisicamente ao catálogo core. Imagens ficam fora do MVP.

### Pyrfume — revisão por conjunto

O repositório declara licença MIT, mas agrega conjuntos científicos de múltiplas origens. Cada arquivo lógico deverá ser aprovado com sua fonte primária antes de uso.

### PubChem — revisão por registro e provedor

O PubChem agrega centenas de contribuidores e informa que licenças podem variar. Somente valores acompanhados de proveniência compatível poderão avançar do staging.

### IFRA — referência

Os materiais servem para conferência técnica e links oficiais. O glossário declara proteção autoral e requisitos de crédito; ele não será convertido em dataset do produto.

### Granado e Phebo — pendente e manual

O site oficial é uma referência importante para a cobertura brasileira, mas não concede uma licença aberta de redistribuição em massa. Até nova autorização, será usado apenas em revisão humana. Outros fabricantes só poderão entrar após receberem um registro próprio no manifesto. Textos publicitários, imagens, logotipos e material editorial não serão copiados.

### Fragrantica — proibida para ingestão

O projeto não fará scraping, agregação, espelhamento, criação de dataset, reutilização de cookies ou contorno de mecanismos anti-bot. Uma mudança dessa classificação exige autorização escrita separada e nova revisão.

## Regras operacionais

1. Um importador recebe um `sourceId` existente no manifesto.
2. A classificação da fonte determina a camada de saída.
3. Fonte pendente, de referência ou proibida nunca grava no catálogo core.
4. Cada valor importado preserva origem, licença e data de consulta.
5. Conflitos e licenças ausentes geram rejeição, nunca correção silenciosa.
6. Imagens passam por uma revisão independente do registro textual.
7. O manifesto é revisto periodicamente e sempre que os termos de uma fonte mudarem.

## Validação

```bash
npm run sources:validate
```

O comando verifica schema, URLs HTTPS, IDs únicos, datas de revisão e coerência entre classificação, licença, automação, redistribuição e camada de armazenamento.

## Evidências oficiais consultadas

- [Licenciamento do Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing)
- [Acesso e boas práticas do Wikidata](https://www.wikidata.org/wiki/Help:Data_access)
- [Licenças do ecossistema Open Food Facts](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorials/license-be-on-the-legal-side/)
- [API do Open Beauty Facts](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorials/scanning-cosmetics-pet-food-and-other-products/)
- [Repositório Pyrfume Data](https://github.com/pyrfume/pyrfume-data)
- [Política de downloads e proveniência do PubChem](https://pubchem.ncbi.nlm.nih.gov/docs/downloads)
- [Glossário de ingredientes da IFRA](https://ifrafragrance.org/docs/default-source/glossary/ifra-fragrance-ingredient-glossary---april-2020.pdf)
- [Termos de uso da Granado e Phebo](https://www.granado.com.br/granado/termos-de-uso)
- [Termos de serviço do Fragrantica](https://www.fragrantica.com/terms-of-service.phtml)
