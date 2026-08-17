---
name: antiquario-taxonomia-olfativa
description: Modelar, normalizar e auditar conhecimento olfativo no projeto O Antiquário. Usar ao trabalhar com taxonomias, descritores, qualidades, famílias, notas de perfume, matérias-primas, moléculas odorantes, aliases multilíngues, relações do grafo, candidatos vindos de ODEUROPA/Pyrfume ou pesquisas científicas, e ao investigar conexões ou pontas soltas no RAG olfativo.
---

# Taxonomia Olfativa do Antiquário

## Objetivo

Estruturar conhecimento olfativo com proveniência sem confundir declaração comercial, percepção, matéria e inferência científica. Manter o grafo como fonte de verdade e produzir relações automáticas somente como candidatos em quarentena.

## Preparação

1. Ler `references/contrato-antiquario.md` antes de alterar schema, grafo, taxonomia, vault ou pipeline.
2. Ler `references/fontes-cientificas.md` ao usar ODEUROPA, taxonomias moleculares, Pyrfume, OpenPOM ou literatura científica.
3. Inspecionar `data/sources.yml` antes de importar dados. Apresentar fatos sobre licença e proveniência; deixar a decisão de uso de uma nova fonte para o proprietário.
4. Preservar alterações locais não relacionadas e verificar o estado do Git antes de editar.

## Classificar antes de conectar

Classificar cada conceito em exatamente um tipo primário:

- `fragrance`: produto comercial acabado;
- `olfactory-note`: termo declarado ou curado como nota de composição;
- `accord`: impressão composta percebida;
- `raw-material`: matéria-prima natural, extrato ou base;
- `molecule`: composto químico odorante identificável;
- `odor-descriptor`: referência à fonte ou caráter percebido do odor;
- `odor-quality`: qualidade hedônica, trigeminal, emocional, textura ou intensidade;
- `olfactory-family`: agrupamento amplo de descritores.

Não resolver uma ambiguidade mudando silenciosamente o tipo. Registrar o termo como candidato ambíguo quando a evidência não permitir escolher.

## Separar a natureza da afirmação

Usar uma destas classes antes de criar qualquer relação:

1. `declared`: informação explicitamente declarada para o perfume por uma fonte adequada;
2. `observed`: percepção registrada por pessoa ou painel, com contexto;
3. `curated`: interpretação editorial identificada como tal;
4. `inferred`: relação calculada, linguística, taxonômica ou molecular;
5. `predicted`: saída de modelo, nunca tratada como fato.

Somente `declared` pode propor pirâmide ou nota declarada para uma fragrância. Relações `inferred` e `predicted` devem permanecer em staging ou quarentena.

## Fluxo de trabalho

1. Identificar o conceito, o claim exato e o localizador da evidência.
2. Normalizar Unicode, caixa, hífens e espaços sem apagar o rótulo original.
3. Resolver aliases apenas quando representarem o mesmo conceito; não fundir termos somente por proximidade vetorial ou distância ortográfica.
4. Escolher a relação permitida no contrato do projeto.
5. Registrar fonte, licença informada pela fonte, localizador, método, confiança e natureza da afirmação.
6. Produzir relações científicas como candidatos com `status: candidate`.
7. Executar `scripts/audit_candidates.py <arquivo.json-ou-jsonl>` antes de propor promoção.
8. Promover ao core apenas quando a política de fontes e as validações existentes aceitarem o documento.
9. Executar os testes proporcionais à alteração: `npm run typecheck`, `npm test`, `npm run knowledge:build` e, quando aplicável, `npm run build`.

## Barreiras obrigatórias

- Nunca derivar `has-note`, `has-top-note`, `has-heart-note`, `has-base-note` ou relações `declares-*` de semelhança, coocorrência, embedding, molécula ou taxonomia.
- Nunca assumir que uma molécula isolada reproduz o comportamento de uma mistura ou perfume acabado.
- Nunca inferir intensidade, concentração, fixação, projeção ou evolução temporal quando a fonte não medir o atributo.
- Nunca transformar alias linguístico em identidade química.
- Nunca promover automaticamente um candidato que contenha conflito, tipo ambíguo ou fonte ainda não aprovada pelo projeto.
- Preservar múltiplas rotas taxonômicas quando um descritor pertencer legitimamente a mais de uma família.

## Saída esperada

Ao modelar um termo ou lote, entregar:

1. entidades reconhecidas e tipos escolhidos;
2. relações factuais separadas das inferidas;
3. candidatos rejeitados ou em quarentena com motivo;
4. proveniência por claim;
5. impacto esperado na conectividade do grafo;
6. comandos de validação executados e resultados.

Preferir pequenas mudanças auditáveis. Não importar um corpus inteiro para testar o modelo conceitual.
