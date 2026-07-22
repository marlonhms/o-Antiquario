# Taxonomia olfativa — O Antiquário

## Objetivo

A taxonomia oferece um vocabulário estável para busca, catálogo e recomendação. Ela separa três conceitos:

- **família:** agrupamento amplo usado para classificação;
- **acorde:** impressão olfativa percebida na composição;
- **nota:** matéria-prima, referência natural, molécula ou efeito descrito na pirâmide.

Esses conceitos não são tratados como equivalentes. Uma fragrância pode pertencer a uma família amadeirada, ter acorde cítrico e apresentar bergamota como nota.

## Cobertura da versão 1

- 15 famílias;
- 33 acordes;
- 214 notas;
- nomes em português e inglês;
- 129 aliases explícitos;
- IDs estáveis em ASCII e `kebab-case`;
- proveniência por termo;
- dedicação CC0 para a curadoria original.

O artefato fica em `data/taxonomy/taxonomy.yml`.

## Normalização

A função `normalizeOlfactiveText` aplica a mesma transformação a consultas e termos indexados:

1. normalização Unicode NFKD;
2. remoção de marcas diacríticas;
3. conversão para minúsculas em português;
4. equivalência entre hífen, underscore e espaço;
5. remoção de pontuação;
6. compactação de espaços.

Exemplos:

| Entrada | Forma normalizada | ID resolvido |
| --- | --- | --- |
| `NÉROLI` | `neroli` | `neroli` |
| `limão` | `limao` | `limao-siciliano` |
| `LEMON` | `lemon` | `limao-siciliano` |
| `terra molhada` | `terra molhada` | `petricor` |
| `fresh spicy` | `fresh spicy` | `especiado-fresco` |

## Regras de integridade

- IDs não podem se repetir dentro de uma coleção.
- Dois termos do mesmo tipo não podem disputar o mesmo nome normalizado.
- Acordes e notas só podem referenciar famílias existentes.
- Todo termo deve indicar ao menos uma fonte.
- Apenas fontes classificadas como `allowed_core` podem alimentar esta taxonomia.
- A taxonomia precisa manter pelo menos 150 notas para satisfazer o marco atual.
- Volatilidade e persistência continuam opcionais até existir fonte técnica licenciada e aprovada.

## Uso no código

```ts
const taxonomy = await loadTaxonomy();
const index = buildTaxonomyIndex(taxonomy);

resolveNote(index, "orris");
resolveAccord(index, "cítrico");
```

As resoluções são determinísticas e não fazem aproximação difusa. Tolerância a erros de digitação será implementada junto ao índice de busca, com limiar explícito e testes de falsos positivos.

## Validação

```bash
npm run taxonomy:validate
npm test
```

Além do schema, os testes confirmam que todas as notas e acordes presentes no catálogo sintético atual são reconhecidos.

## Próximas ampliações

1. Importador idempotente do Wikidata.
2. Associação opcional de QIDs aos termos aprovados.
3. Relatório de termos sem tradução ou com conflito.
4. Revisão editorial especializada da classificação.
5. Inclusão de volatilidade e persistência somente com evidência compatível.
