# Referências científicas e limites de aplicação

## Menini et al. (2022)

**Fonte:** Stefano Menini, Teresa Paccosi, Serra Sinem Tekiroğlu e Sara Tonelli. “Building a Multilingual Taxonomy of Olfactory Terms with Timestamps.” LREC 2022.

- Artigo: https://aclanthology.org/2022.lrec-1.429/
- Recurso: https://github.com/Odeuropa/multilingualTaxonomies

### Contribuição útil

- léxico olfativo em inglês, italiano, francês e alemão;
- separação entre substantivos associados a fontes de cheiro e adjetivos associados a qualidades;
- expansão a partir de WordNet, coocorrência histórica e embeddings FastText;
- marcação de primeira ocorrência e períodos entre 1650 e 1925;
- candidatos para aliases, busca multilíngue e análise cultural.

### Limite

Usar como recurso linguístico e histórico. Não interpretar os termos como pirâmide de perfume, composição química, intensidade ou desempenho.

## Sajan et al. (2026)

**Fonte:** Akshay Sajan et al. “Hierarchies of smell: structuring the molecular odor space using semantic taxonomies and machine learning.” Chemical Senses 51, 2026, bjag020.

- Artigo: https://academic.oup.com/chemse/article/doi/10.1093/chemse/bjag020/8728262
- Vocabulário especializado: https://vocab.odeuropa.eu/en/

### Contribuição útil

- conjunto molecular consolidado com 6.711 moléculas e 146 descritores para as tarefas publicadas;
- taxonomia especializada com 617 conceitos: 557 descritores baseados em fonte e 60 qualidades;
- 16 famílias e 31 subclasses na taxonomia especializada;
- comparação entre taxonomia especializada, agrupamento por coocorrência e grupos aleatórios;
- validação por modelos interpretáveis e OpenPOM;
- base para representar `molecule -> odor-descriptor -> olfactory-family`.

### Limites declarados

- descritores sem pesos relativos;
- concentração não considerada;
- dados desbalanceados em direção a odores valorizados por alimentação e perfumaria;
- foco em moléculas isoladas, não em misturas;
- estrutura 2D não representa toda a conformação e interação biológica;
- diferenças sociais, linguísticas e culturais continuam relevantes.

## Uso conjunto no Antiquário

Usar Menini et al. para o eixo linguagem–tempo–cultura. Usar Sajan et al. para o eixo molécula–descritor–hierarquia. Conectar os eixos por IDs e evidência, sem colapsá-los em uma única lista de “notas”.

## Política operacional

Tratar licença do artigo, licença do repositório e licença de cada dataset de origem como registros distintos. Consultar `data/sources.yml` e apresentar a avaliação ao proprietário antes de importar qualquer dataset novo para o core.
