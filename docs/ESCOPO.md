# Escopo do projeto — O Antiquário

## 1. Resumo executivo

O Antiquário será um companion e consultor de perfumaria capaz de conhecer o gosto do usuário, interpretar o contexto de uso e recomendar fragrâncias com justificativas verificáveis. O produto deverá contemplar alta perfumaria, nicho, designer, perfumaria árabe, perfumaria brasileira, produtos de grande consumo e fragrâncias inspiradas.

O diferencial não será apenas listar notas. O sistema combinará perfil olfativo, evolução da fragrância, desempenho percebido, clima, ambiente, ocasião, duração desejada, orçamento, disponibilidade e histórico pessoal de uso.

O MVP será gratuito para construir e operar dentro das cotas escolhidas. Nenhuma funcionalidade essencial dependerá exclusivamente de uma API paga.

## 2. Problema

As informações de perfumaria estão fragmentadas entre fabricantes, bases comunitárias, publicações técnicas e relatos subjetivos. O usuário encontra dificuldade para:

- entender como notas, acordes e concentrações se traduzem em experiência real;
- escolher um perfume adequado ao clima, horário, ambiente e ocasião;
- comparar desempenho sem tratar opiniões subjetivas como fatos absolutos;
- encontrar alternativas acessíveis a fragrâncias caras;
- aprender com o próprio histórico de uso;
- distinguir informação declarada pelo fabricante, consenso comunitário e estimativa algorítmica.

## 3. Visão do produto

Criar um especialista pessoal que responda perguntas como:

- “Qual perfume da minha coleção funciona hoje à noite?”
- “Quero algo elegante para escritório, com pouca projeção e seis horas de duração.”
- “Gosto de Terre d’Hermès, mas quero uma alternativa mais barata e menos terrosa.”
- “Por que este perfume desaparece rápido na minha pele?”
- “Quais notas devo evitar em calor úmido e ambiente fechado?”
- “Compare estas três fragrâncias para um casamento ao ar livre.”
- “O que mudou entre a abertura, o coração e o dry-down que registrei?”

## 4. Objetivos

### 4.1 Objetivos do MVP

- Disponibilizar um catálogo inicial de 600 fragrâncias normalizadas.
- Cobrir pelo menos 200 fragrâncias brasileiras, 300 internacionais e 100 árabes, acessíveis ou inspiradas.
- Permitir busca por nome, marca, notas, acordes, segmento e concentração.
- Criar e manter um perfil olfativo local do usuário.
- Recomendar três opções para um contexto informado.
- Explicar recomendações em português natural usando Gemini Flash.
- Continuar recomendando quando o Gemini estiver indisponível.
- Registrar uso real, duração, projeção e impressão por fase.
- Exibir origem e confiança dos principais dados.

### 4.2 Objetivos posteriores

- Aprender pesos individuais a partir do diário de uso.
- Receber contribuições comunitárias moderadas.
- Criar comparações, alternativas e mapas de similaridade.
- Oferecer análise opcional de foto de frasco ou embalagem.
- Suportar outros idiomas e catálogos regionais.
- Disponibilizar o banco próprio por uma API aberta, respeitando as licenças de origem.

## 5. Não objetivos

Não fazem parte do MVP:

- copiar ou reproduzir a base, resenhas ou imagens da Fragrantica;
- usar cookies de sessão, automação stealth ou contornar Cloudflare;
- fornecer diagnóstico médico, dermatológico ou toxicológico;
- afirmar duração ou projeção como propriedades universais;
- comercializar perfumes ou operar marketplace;
- monitorar preços em tempo real;
- prometer cobertura equivalente a grandes bases comerciais no lançamento;
- produzir fórmulas comerciais ou revelar fórmulas proprietárias;
- depender de geração de imagens, voz em tempo real ou pesquisa web paga.

## 6. Público-alvo

### 6.1 Primário

- entusiastas iniciantes que precisam de orientação clara;
- colecionadores que desejam organizar e usar melhor a coleção;
- consumidores que buscam alternativas por faixa de preço;
- interessados em perfumaria brasileira, árabe, nicho e designer.

### 6.2 Secundário

- vendedores e consultores independentes;
- criadores de conteúdo;
- estudantes de perfumaria;
- perfumistas artesanais interessados em matérias-primas e conceitos, sem acesso a fórmulas proprietárias.

### 6.3 Restrição etária

Enquanto o plano gratuito do Gemini estiver em uso, o produto deverá ser direcionado a maiores de 18 anos, conforme os termos atuais do Gemini API.

## 7. Proposta de valor

- Recomendações contextuais, não rankings genéricos.
- Explicações ligadas aos dados exibidos.
- Inclusão de perfumes brasileiros e acessíveis desde o início.
- Aprendizado baseado na experiência real do usuário.
- Transparência sobre incerteza e origem.
- Funcionamento local e gratuito mesmo sem IA em nuvem.

## 8. Escopo funcional

### 8.1 Onboarding olfativo

O usuário informa:

- perfumes que ama, gosta, tolera e evita;
- notas e acordes preferidos ou rejeitados;
- intensidade e projeção desejadas;
- preferência por masculino, feminino, compartilhável ou sem classificação;
- segmentos e orçamento habituais;
- sensibilidade a doçura, couro, notas animais, oud, fumaça, especiarias e florais intensos;
- ambientes e ocasiões mais frequentes.

**Resultado:** vetor inicial de preferências com indicação de que é provisório.

### 8.2 Catálogo

Cada fragrância poderá conter:

- nome, marca, ano e país;
- concentração e segmento;
- perfumista, quando conhecido;
- notas de topo, coração e base;
- acordes normalizados;
- família olfativa;
- desempenho declarado, comunitário ou estimado;
- adequação a clima, estação, horário e ocasião;
- faixa de preço relativa, sem preço em tempo real;
- perfumes relacionados;
- fontes, licenças e confiança por campo;
- data da última revisão.

### 8.3 Busca e exploração

- Busca tolerante a acentos e pequenas variações.
- Filtros combináveis.
- Exclusão explícita de notas ou acordes.
- Comparação de até quatro fragrâncias.
- Navegação por famílias, notas, marcas e segmentos.
- Glossário olfativo bilíngue português/inglês.

### 8.4 Recomendação contextual

Entradas possíveis:

- data, horário e duração;
- temperatura e umidade informadas manualmente;
- ambiente interno ou externo;
- ventilação e densidade de pessoas;
- ocasião e formalidade;
- projeção desejada;
- orçamento e disponibilidade na coleção;
- preferências e rejeições do usuário.

Saída mínima:

- três recomendações ordenadas;
- motivo principal de cada escolha;
- modo de uso conservador, sem prescrição médica;
- possíveis conflitos com contexto ou preferências;
- nível de confiança;
- indicação de quais dados são estimados.

### 8.5 Companion conversacional

O Gemini será responsável por:

- interpretar linguagem natural;
- solicitar apenas os esclarecimentos indispensáveis;
- transformar a saída estruturada do recomendador em explicação;
- comparar candidatos fornecidos pelo sistema;
- explicar conceitos de perfumaria com base na base interna.

O Gemini não poderá:

- inventar perfumes fora da lista de candidatos;
- alterar notas, marcas ou métricas recebidas;
- apresentar estimativas como fatos;
- receber dados pessoais identificáveis;
- funcionar como única fonte de uma recomendação.

### 8.6 Coleção e diário de uso

- Adicionar fragrância à coleção, amostras e lista de desejos.
- Registrar data, contexto, borrifadas, local de aplicação e clima percebido.
- Avaliar abertura, coração, base, projeção e duração.
- Registrar “usaria novamente” e adequação à ocasião.
- Recalcular preferências a partir do histórico.
- Exportar e apagar todos os dados locais.

### 8.7 Proveniência e confiança

Todo campo relevante deverá indicar uma destas origens:

- `fabricante`: informação factual declarada pela marca;
- `fonte_aberta`: informação importada de base licenciada;
- `curadoria`: informação revisada pela equipe;
- `comunidade`: agregação de votos próprios;
- `estimativa`: resultado de regra ou modelo;
- `usuario`: observação pessoal.

Níveis de confiança: `alta`, `média`, `baixa` e `desconhecida`.

## 9. Fontes de dados permitidas

### 9.1 Núcleo

- Wikidata CC0 para entidades e relacionamentos.
- Dados próprios inseridos com fonte e trilha de revisão.
- Conjuntos CC0 cuja procedência seja auditada antes da importação.

### 9.2 Enriquecimento separado

- Open Beauty Facts/Open Database License para código de barras, embalagem e ingredientes declarados. Seus dados devem permanecer em camada separada para respeitar obrigações de atribuição e compartilhamento.
- Pyrfume para ciência olfativa, validando a licença de cada arquivo; a licença do código do repositório não torna automaticamente todas as fontes comerciais ou redistribuíveis.
- PubChem para propriedades de moléculas e identificadores químicos.
- IFRA como referência técnica pública, sem apresentar o sistema como certificador de segurança.

### 9.3 Fontes proibidas

- bancos obtidos por scraping sem licença clara;
- resenhas copiadas de terceiros;
- imagens sem licença de reutilização;
- datasets que apenas declaram uma licença aberta, mas têm origem incompatível;
- credenciais, cookies ou sessões fornecidos por usuários.

## 10. Modelo de recomendação

A pontuação inicial, calibrável, será:

| Componente | Peso inicial |
|---|---:|
| Compatibilidade com preferências | 30% |
| Adequação ao contexto | 25% |
| Desempenho desejado | 15% |
| Histórico pessoal | 10% |
| Orçamento e disponibilidade | 10% |
| Confiança dos dados | 5% |
| Diversidade/novidade controlada | 5% |

Regras de exclusão, como nota rejeitada ou projeção inadequada para ambiente sensível, serão aplicadas antes da pontuação.

## 11. Requisitos não funcionais

### 11.1 Custo

- Nenhum cartão ou faturamento será necessário para executar o MVP.
- O produto deverá interromper ou degradar funcionalidades antes de gerar cobrança.
- As cotas externas serão tratadas como recursos instáveis.

### 11.2 Desempenho

- Busca local: p95 abaixo de 200 ms com o catálogo inicial.
- Geração da lista determinística: p95 abaixo de 500 ms.
- Primeira resposta do companion: alvo de até 8 segundos, sem garantia por depender do provedor.
- Aplicação utilizável em conexão móvel e instalável como PWA.

### 11.3 Privacidade

- Perfil e diário armazenados localmente por padrão.
- Nenhum nome, e-mail, coordenada exata ou texto privado integral enviado ao Gemini.
- Consentimento específico antes da primeira chamada à IA.
- Aviso de que conteúdo do plano gratuito pode ser usado pelo Google para melhoria de produtos e revisado por humanos.
- Função de exportação e eliminação de dados.

### 11.4 Segurança

- Chave do Gemini somente no backend/Worker.
- Validação de esquema, tamanho máximo de entrada e lista permitida de origens.
- Rate limit por usuário ou IP e proteção contra automação abusiva.
- Logs sem prompts completos e sem credenciais.
- Dependências auditadas e atualizadas.

### 11.5 Qualidade e acessibilidade

- Interface alvo WCAG 2.2 AA.
- Navegação por teclado e compatibilidade com leitores de tela.
- Testes unitários do recomendador e testes ponta a ponta dos fluxos críticos.
- Respostas sempre distinguindo fato, consenso e estimativa.

## 12. Métricas de sucesso do MVP

- 600 fragrâncias publicadas, todas com licença e origem registradas.
- Pelo menos 90% com marca, nome, segmento, família e conjunto de notas.
- Pelo menos 80% com concentração e ano quando publicamente conhecidos.
- Trinta cenários de recomendação revisados manualmente.
- Nenhuma recomendação contendo fragrância inexistente na lista de candidatos.
- Fallback funcionando em 100% dos testes simulando indisponibilidade do Gemini.
- Pelo menos 70% dos testadores considerando as três recomendações coerentes.
- Nenhuma chave, cookie ou dado pessoal identificável no bundle ou nos logs.

## 13. Riscos e respostas

| Risco | Impacto | Resposta |
|---|---|---|
| Mudança na cota gratuita do Gemini | Alto | Modelo configurável, fallback determinístico e opção BYOK futura |
| Cobertura inicial pequena | Médio | Curadoria focada, contribuições e prioridade para Brasil/acessíveis |
| Licença inadequada de dataset | Alto | Registro de proveniência e bloqueio de importação sem auditoria |
| Dados subjetivos tratados como fatos | Alto | Tipos de evidência, confiança e amostra mínima |
| Abuso da chave pública indireta | Alto | Worker, rate limit, validação e proteção anti-bot |
| Recomendações genéricas | Médio | Diário, explicação por fatores e diversidade controlada |
| Dependência excessiva do LLM | Alto | Recomendador e templates executados sem IA |
| Informações de segurança mal interpretadas | Alto | Referências oficiais, linguagem não clínica e limites explícitos |

## 14. Critério de conclusão do MVP

O MVP estará concluído quando uma pessoa maior de 18 anos puder, sem pagar e sem criar infraestrutura própria:

1. configurar preferências;
2. pesquisar o catálogo;
3. informar um contexto;
4. receber três recomendações reproduzíveis;
5. obter uma explicação do Gemini ou fallback equivalente;
6. registrar o uso;
7. visualizar a origem e a confiança dos dados;
8. exportar ou apagar seu perfil.
