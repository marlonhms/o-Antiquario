# Taxonomias científicas olfativas — adoção no Antiquário

## Objetivo

Incorporar conhecimento linguístico, perceptivo e molecular ao grafo sem transformar inferências em pirâmides comerciais. Esta trilha complementa a taxonomia operacional existente; não substitui notas declaradas por fabricantes ou fontes factuais aprovadas.

## Estudos de referência

### ODEUROPA — léxico multilíngue e histórico

O trabalho [Building a Multilingual Taxonomy of Olfactory Terms with Timestamps](https://aclanthology.org/2022.lrec-1.429/) organiza termos olfativos em inglês, italiano, francês e alemão. O [recurso publicado](https://github.com/Odeuropa/multilingualTaxonomies) registra origem do termo, synset, primeira ocorrência, períodos históricos, categoria de fonte e categoria de qualidade.

Aplicações previstas:

- aliases multilíngues com rótulo original preservado;
- expansão de busca e recuperação semântica;
- distinção entre fonte de odor e qualidade percebida;
- análise histórica e cultural de vocabulário;
- geração de candidatos para revisão, nunca de notas de perfume.

### Taxonomia molecular especializada

O trabalho [Hierarchies of smell: structuring the molecular odor space using semantic taxonomies and machine learning](https://academic.oup.com/chemse/article/doi/10.1093/chemse/bjag020/8728262) apresenta uma taxonomia especializada e uma taxonomia baseada em coocorrência. O estudo trabalha com um conjunto consolidado de 6.711 moléculas e 146 descritores; a taxonomia especializada reúne 617 conceitos, sendo 557 descritores baseados em fonte e 60 qualidades.

Aplicações previstas:

- representação de moléculas odorantes;
- ligação rastreável entre molécula e descritor;
- famílias perceptivas de maior nível;
- comparação entre organização especializada e agrupamento calculado;
- validação futura de coerência por coocorrência e modelos interpretáveis.

Limites que devem permanecer visíveis:

- ausência de peso relativo dos descritores;
- concentração não modelada;
- foco em moléculas isoladas, não em misturas;
- desbalanceamento do corpus;
- percepção dependente de pessoa, cultura e contexto.

## Modelo conceitual

```text
fragrance
  └─ declaração factual → olfactory-note
                              └─ derived-from → raw-material
                                                    └─ contains-odorant → molecule
                                                                                └─ described-as → odor-descriptor
                                                                                                      └─ belongs-to-olfactory-family → olfactory-family

olfactory-note / raw-material / molecule / odor-descriptor
  └─ has-quality → odor-quality
```

`accord` continua representando uma impressão composta na fragrância. Ele não deve ser usado como sinônimo de família, descritor ou molécula.

## Entidades adicionadas ao Knowledge Core

| Tipo | ID de exemplo | Finalidade |
| --- | --- | --- |
| `molecule` | `antiquario:molecule:geraniol` | Composto químico odorante |
| `odor-descriptor` | `antiquario:odor-descriptor:floral` | Fonte ou caráter percebido |
| `odor-quality` | `antiquario:odor-quality:pungente` | Qualidade perceptiva, hedônica ou trigeminal |
| `olfactory-family` | `antiquario:olfactory-family:floral` | Agrupamento taxonômico amplo |

## Relações científicas

| Predicado | Origem | Destino |
| --- | --- | --- |
| `described-as` | nota, matéria-prima ou molécula | descritor |
| `has-quality` | nota, matéria-prima, molécula ou descritor | qualidade |
| `belongs-to-olfactory-family` | descritor | família |
| `broader-descriptor-than` | descritor | descritor |
| `broader-quality-than` | qualidade | qualidade |
| `derived-from` | nota | matéria-prima |
| `contains-odorant` | matéria-prima | molécula |

## Barreira entre ciência e catálogo

Relações científicas são candidatas até passarem pela política de fonte e pelo contrato do grafo. Nenhum processo dessa trilha pode criar:

- `has-note`;
- `has-top-note`;
- `has-heart-note`;
- `has-base-note`;
- qualquer relação `declares-*`.

Esses predicados exigem declaração explicitamente ligada ao perfume. Similaridade, coocorrência, embedding, taxonomia ou composição molecular não são evidência suficiente.

## Fases de implementação

### Fase 1 — contrato e proteção

- adicionar os quatro tipos ao schema;
- adicionar contratos de relações científicas;
- criar testes que impeçam relações científicas diretamente em fragrâncias;
- criar uma skill versionada para orientar agentes futuros;
- criar auditor determinístico de candidatos.

### Fase 2 — staging ODEUROPA

**Implementada em 17/08/2026.** O proprietário aprovou o recurso exclusivamente para staging com atribuição CC BY 4.0.

- fonte registrada como `allowed_staging`, com bloqueio estrutural de escrita no core;
- snapshot fixado no commit `7af2fc446c6c399bef601fc952429d34b3945ef4` e verificado por SHA-256;
- idioma, termo original, classe gramatical, método, synset, marca temporal, licença e localizador preservados;
- candidatos de descritor e qualidade separados da taxonomia canônica;
- colisões normalizadas, termos sem categoria e linhas malformadas isolados;
- categorias compostas preservadas literalmente, sem presumir uma hierarquia que a fonte não declarou;
- zero relações comerciais ou pirâmides geradas.

O snapshot atual contém 3.822 termos válidos nos quatro idiomas, 3.567 candidatos classificados, 125 grupos de colisão e 256 ocorrências em quarentena. As 421 anotações extras do TSV francês foram preservadas como avisos, não descartadas.

### Executar o importador

```powershell
npm run data:sync:odeuropa
```

O fluxo padrão baixa somente os quatro TSVs do commit fixado. Para reprocessar um checkout local auditado:

```powershell
npm run data:sync:odeuropa -- --source-dir "<pasta-do-repositorio>" --ref 7af2fc446c6c399bef601fc952429d34b3945ef4
```

Saídas locais:

```text
data/raw/odeuropa/<snapshot>/snapshot.json
data/raw/odeuropa/<snapshot>/taxonomies-v2/*.tsv
data/staging/odeuropa/<snapshot>/terms.jsonl
data/staging/odeuropa/<snapshot>/entity-candidates.jsonl
data/staging/odeuropa/<snapshot>/classification-candidates.jsonl
data/staging/odeuropa/<snapshot>/collisions.jsonl
data/staging/odeuropa/<snapshot>/quarantine.jsonl
data/staging/odeuropa/<snapshot>/warnings.jsonl
data/staging/odeuropa/<snapshot>/report.json
```

Arquivos brutos e de staging permanecem fora do Git. O manifesto, o importador, os testes e esta decisão de governança são versionados.

### Resolvedor ODEUROPA ↔ taxonomia canônica

**Implementado em 17/08/2026.** O resolvedor não trata igualdade textual como identidade ontológica. Ele produz pontes lexicais para o RAG em quatro grupos mutuamente exclusivos:

1. `resolved-retrieval-bridges`: rótulo inglês canônico exato, único e sem colisão no termo ODEUROPA;
2. `equivalence-candidates`: alias de idioma desconhecido ou propagação por synset compartilhado com uma âncora inglesa única;
3. `ambiguities`: múltiplos conceitos canônicos, homógrafo entre idiomas ou synset cruzando tipos ODEUROPA;
4. `unresolved`: sem evidência suportada ou já em quarentena na origem.

Mesmo uma ponte resolvida declara `scope: retrieval_only`, `semantic_identity: unverified`, `claim_nature: inferred` e `promotion_status: blocked`. Ela melhora recuperação e navegação, mas não cria `same-as`, não altera aliases canônicos e não produz relações de perfume.

```powershell
npm run data:resolve:odeuropa
```

Resultado do snapshot atual:

| Saída | Quantidade | Interpretação |
| --- | ---: | --- |
| Pontes resolvidas para recuperação | 98 | Correspondência inglesa exata e única |
| Candidatos | 17 | 13 por alias e 4 por synset |
| Ambiguidades | 62 | 10 colisões canônicas e 52 homógrafos entre idiomas |
| Sem resolução | 3.645 | Fora da cobertura segura atual |
| Cobertura recuperável | 115 termos / 3,42% | Reflexo do core ainda pequeno e majoritariamente PT/EN |

Saídas em `data/staging/odeuropa/<snapshot>/equivalence/`:

```text
resolved-retrieval-bridges.jsonl
equivalence-candidates.jsonl
ambiguities.jsonl
unresolved.jsonl
report.json
manifest.json
```

O auditor do resolvedor exige IDs únicos, alocação única de cada termo, destinos não comerciais, ausência de predicado de grafo e escopo estritamente voltado à recuperação. O processamento também revelou registros repetidos por métodos diferentes na fonte; os IDs do importador passaram a usar o localizador da linha para preservar cada evidência sem colisão.

### Índice de expansão e avaliação do RAG

**Implementado em 17/08/2026.** As 98 pontes resolvidas foram consolidadas em 97 entradas únicas e 194 chaves de consulta PT/EN. Duas evidências ODEUROPA para `musk` convergem na mesma entrada sem perder seus localizadores.

O índice:

- inclui zero dos 17 candidatos ainda pendentes;
- exige idioma explícito na consulta e separa a proveniência canônica da ODEUROPA;
- usa correspondência por tokens e frase mais longa, sem substring;
- agrega rótulos canônicos PT/EN sem declarar identidade semântica;
- registra o release e o hash do Knowledge Core usado;
- publica rota somente quando documento e chunks realmente existem;
- falha se encontrar predicado de grafo, destino comercial, chave duplicada ou bridge fora do contrato.

No estado atual, 67 dos 97 destinos possuem rota para 89 chunks do Knowledge Core: 49 por ID direto e 18 por reconciliação exata de rótulo e tipo. Os 30 restantes não possuem documento. A correspondência documental ambígua foi eliminada pela migração canônica de `carnation`, `clove` e `cravo`; nenhuma situação pendente cria uma rota artificial.

Avaliação no conjunto ouro de 19 casos naturais e de segurança em português e inglês:

| Métrica | Resultado |
| --- | ---: |
| Precisão micro lexical | 100% |
| Revocação micro lexical | 100% |
| Casos com resultado exato | 100% |
| Violações de segurança | 0 |
| Cobertura de rotas para chunks | 100% |

Esses números medem somente a regressão controlada atual. Não demonstram precisão geral em linguagem natural, outros idiomas ou uso real.

```powershell
npm run data:index:odeuropa
npm run data:query:odeuropa -- "sandalwood and patchouli" --language en
npm run data:backlog:odeuropa
```

Artefatos locais:

```text
data/staging/odeuropa/<snapshot>/equivalence/retrieval/index.json
data/staging/odeuropa/<snapshot>/equivalence/retrieval/evaluation.json
data/staging/odeuropa/<snapshot>/equivalence/retrieval/manifest.json
data/staging/odeuropa/<snapshot>/equivalence/retrieval/routing-gaps.jsonl
data/staging/odeuropa/<snapshot>/equivalence/retrieval/routing-backlog.jsonl
data/staging/odeuropa/<snapshot>/equivalence/retrieval/backlog-report.json
data/staging/odeuropa/<snapshot>/equivalence/retrieval/backlog-manifest.json
```

### Priorização das lacunas

**Implementado em 17/08/2026.** As 57 lacunas iniciais formaram um backlog determinístico e auditável: 1 item `P0` de identidade, 3 itens `P1` presentes no conjunto ouro, 4 itens `P2` usados pelo catálogo ativo, 19 documentos rasos `P3` e 30 documentos ausentes `P4` sem demanda observada nesses dois consumidores.

**Concluído em 17/08/2026.** A fila `P0/P1/P2` foi encerrada. `Cravo-flor` e `cravo-da-índia` agora são conceitos e documentos distintos; os sete conceitos prioritários ganharam conteúdo canônico independente da ODEUROPA.

**Concluído em 17/08/2026.** Os 18 itens `P3` foram enriquecidos por uma automação determinística com prévia, auditoria e precondição de hash. Ela reutilizou 96 relações de pirâmide já declaradas, promoveu 18 seções factuais, criou 36 chunks e zero relações. O backlog atual contém somente 30 itens `P4` sem documento.

O ranking usa demanda e conectividade apenas para ordenar trabalho. Ele não aumenta confiança, não promove equivalências e não gera relações protegidas.

### Fase 3 — piloto molecular

- selecionar um subconjunto pequeno e verificável do material do estudo de 2026;
- registrar moléculas por identificador químico estável;
- criar relações `described-as` com proveniência por claim;
- comparar hierarquia especializada e coocorrência sem fundi-las;
- impedir promoção de fontes ou subconjuntos não aprovados pelo proprietário.

### Fase 4 — recuperação e explicação

- incluir descritores e famílias na expansão de consulta do RAG;
- recuperar primeiro fatos específicos e depois conceitos amplos;
- mostrar ao usuário se a explicação é declarada, curada, inferida ou prevista;
- medir ganho de cobertura sem degradar precisão factual.

### Fase 5 — validação científica e sensorial

- criar cenários ouro de relações corretas e falsos positivos perigosos;
- medir cobertura, precisão de resolução, conflitos e nós órfãos;
- adicionar concentração, intensidade e mistura somente quando existirem dados adequados;
- manter observações pessoais e de painel em uma camada contextual separada.

## Critérios de aceite do piloto

- zero relações comerciais geradas pela trilha científica;
- 100% dos candidatos com fonte, localizador, método e confiança;
- aliases não apagam o rótulo e o idioma originais;
- colisões semânticas permanecem em quarentena;
- toda relação promovida respeita o contrato de origem e destino;
- reprocessar o mesmo snapshot produz a mesma saída.
