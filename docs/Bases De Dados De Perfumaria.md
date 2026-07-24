# **Relatório de Inteligência de Dados: Mineração OSINT e Estruturação de Bases de Conhecimento em Perfumaria**

A construção de um banco de conhecimento unificado sobre perfumaria, destinado a alimentar arquiteturas de Inteligência Artificial baseadas em Grafos de Conhecimento (Knowledge Graphs) e Geração Aumentada por Recuperação (RAG), exige a consolidação de dados heterogéneos dispersos em múltiplos vetores digitais. A complexidade deste domínio reside na necessidade de mapear não apenas metadados comerciais, mas a taxonomia estrutural exata da fragrância. Isto compreende as famílias olfativas, os acordes principais e a pirâmide olfativa completa, rigorosamente dividida em notas de saída (topo), corpo (coração) e fundo (base).  
Este documento apresenta um mapeamento exaustivo de vetores de extração de dados não convencionais através de metodologias OSINT (Open Source Intelligence). A análise avalia repositórios públicos, sistemas de engenharia reversa em APIs de comércio eletrónico, raspadores de código aberto e consultas à Web Semântica. A investigação foca-se em contornar as restrições impostas por arquiteturas de cibersegurança modernas e em priorizar fontes de integração ágil, livres de custos de licenciamento, para a rápida prototipagem de sistemas de IA.

## **1\. Mapeamento de Datasets Públicos e Corpus Estruturados**

A exploração exaustiva de catálogos abertos no Kaggle, Hugging Face e no Google Dataset Search revela uma segmentação clara. A maioria das bases divide-se entre análises de mercado focadas em preços e corpus textuais desenhados para o Processamento de Linguagem Natural (NLP). Para a construção de um grafo de conhecimento olfativo, é imperativo extrair entidades relacionais. A representação num Grafo de Conhecimento exige que cada "Nota Olfativa" seja um nó independente (Node), conectado ao nó da "Fragrância" através de arestas direcionais (Edges) como HAS\_TOP\_NOTE ou BELONGS\_TO\_FAMILY.

### **1.1. O Ecossistema Hugging Face e Bases Multilingues**

O ecossistema do Hugging Face oferece ficheiros formatados para o treino direto de Modelos de Linguagem de Grande Escala (LLMs), frequentemente armazenados no formato Apache Parquet para otimizar a leitura colunar.  
O recurso mais abrangente e estruturalmente preparado para este fim é o **FragDB (Fragrance Database)**, operado pela rede Fragrantika1. O repositório oficial pode ser acedido através do link direto https://github.com/FragDB/fragrance-database ou no Hugging Face em https://huggingface.co/datasets/FragDBnet/fragrance-database1. Embora o acesso à totalidade dos mais de 134.000 registos de perfumes exija um licenciamento comercial na plataforma principal fragdb.net, a organização disponibiliza amostras substanciais gratuitas que servem como *schema* fundamental para a modelação de grafos1.  
A estrutura do FragDB é distribuída em seis ficheiros CSV relacionais. O ficheiro fragrances.csv contém campos como ano, género, acordes e a crucial pirâmide de notas (notes\_pyramid)4. Adicionalmente, o ficheiro notes.csv lista mais de 2.500 notas olfativas individuais, incluindo os seus nomes latinos, grupos químicos e perfis de odor1. Para a arquitetura RAG, o verdadeiro valor reside nos ficheiros Parquet complementares, como o comments.parquet, que contém mais de 4,6 milhões de avaliações de utilizadores em 23 idiomas1. A integração destes ficheiros exige a utilização da biblioteca pandas ou polars em Python. O planeamento de integração dita que as notas sejam ingeridas primeiro para criar o vocabulário base do grafo, seguidas pelas fragrâncias que farão referência aos IDs únicos (PIDs) destas notas.  
Outro repositório de alto valor tático no Hugging Face é o **Perfume Description Dataset** alojado pelo utilizador MrBob23, acessível em https://huggingface.co/datasets/MrBob23/perfume-description/blob/main/perfume\_metadata.csv5. Ao contrário de descrições em texto livre, este ficheiro CSV categoriza a pirâmide olfativa em colunas rigorosas. O registo de um perfume evidencia a separação semântica: a coluna de notas de topo lista "Cinnamon, Cardamom, Orange Blossom, Bergamot", a coluna central apresenta "Bourbon Vanilla, elemi", e o fundo enumera "Praline, Musk, Ambroxan"5.  
A instrução de uso para este *dataset* específico envolve o carregamento do CSV e a aplicação de uma função de divisão (*split*) nas vírgulas de cada célula, transformando as *strings* em matrizes (arrays) de nós, que podem ser carregados diretamente no Neo4j. Adicionalmente, este *dataset* incorpora dicionários JSON com pesos percentuais para os acordes (ex: {"sweet": 10.0, "vanilla": 9.8, "warm spicy": 9.0})5. Estes valores numéricos devem ser injetados como propriedades nas arestas do grafo, permitindo que o sistema de recomendação da IA calcule distâncias de similaridade através de algoritmos baseados em cossenos.  
O repositório **Perfume Recommendation LLM** (https://huggingface.co/datasets/abhirajeshbhai/perfume\_recommendation\_llm/viewer) destina-se explicitamente ao afinamento (*fine-tuning*) de modelos conversacionais6. O formato estrutural imita interações humanas diretas, tais como solicitações por ingredientes específicos, retornando o nome exato da fragrância que os contém6. A integração deste conjunto na camada RAG garante que o LLM compreenda o jargão utilizado pelos consumidores ao solicitar perfumes baseados em matérias-primas específicas.

### **1.2. Repositórios Kaggle e Limitações Estruturais**

No domínio do Kaggle e do Google Dataset Search, os dados frequentemente requerem processamento adicional (*data wrangling*). O **Fragrantica.com Fragrance Dataset** (https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset) contém um volume expressivo de 70.103 registos de perfumes extraídos da referida plataforma7. Contudo, a análise do esquema de dados revela que as notas não se encontram separadas em colunas independentes; em vez disso, estão diluídas na coluna de Descrição (Description)9.  
Para contornar esta limitação arquitetural e alimentar o grafo com precisão, a instrução de uso exige a conceção de um fluxo de extração de informação (Information Extraction). O engenheiro de dados deve empregar Expressões Regulares (Regex), como r'(.\*?)by(\[A-Z\].\*?)is\\s' para extrair a marca do início do texto9, e, subsequentemente, utilizar um modelo de Reconhecimento de Entidades Nomeadas (NER), treinado especificamente com o vocabulário de ingredientes do FragDB, para identificar as ocorrências das notas de saída, corpo e fundo incrustadas no texto narrativo.  
O **Perfume E-Commerce Dataset 2024** (https://www.kaggle.com/datasets/kanchana1990/perfume-e-commerce-dataset-2024) oferece uma perspetiva distinta, baseada em 2.000 listagens de comércio eletrónico obtidas do eBay via API da Apify10. Embora seja rico em dados sobre preços e volumes de venda, este conjunto omite completamente a pirâmide olfativa, limitando a sua utilidade para o mapeamento da química da fragrância10. A sua inclusão no grafo de conhecimento deve restringir-se à camada comercial, permitindo que a IA forneça estimativas de preço de mercado juntamente com as recomendações olfativas.

| Fonte / Dataset | Link Direto | Formato | Aplicação no Grafo de Conhecimento |
| :---- | :---- | :---- | :---- |
| **FragDB (Amostras)** | github.com/FragDB/fragrance-database | CSV / Parquet | Criação do vocabulário base de notas (2.500+ nós) e injeção de avaliações em 23 idiomas. |
| **MrBob23 Metadata** | huggingface.co/datasets/MrBob23/... | CSV | Extração limpa de Topo/Corpo/Fundo; pesos de acordes em JSON para cálculo de similaridade. |
| **Fragrantica Kaggle** | kaggle.com/datasets/olgagmiufana1/... | CSV | Expansão de catálogo (70k+), requer modelos NLP/Regex para extrair notas da coluna de descrição. |
| **TidyTuesday Parfumo** | github.com/rfordatascience/tidytuesday | CSV | Extração organizada de 2024 sobre o Parfumo, contendo notas perfeitamente mapeadas. |

O repositório do **TidyTuesday**, focado no *Parfumo Fragrance Dataset* (https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-12-10/readme.md), apresenta dados extraídos por utilizadores que contêm colunas explícitas para Top\_Notes, Middle\_Notes e Base\_Notes, bem como a concentração e o criador (perfumista)11. Este ficheiro atua como um excelente acelerador para a inicialização do projeto de IA, visto que a limpeza dos dados já foi executada pela comunidade académica.  
Adicionalmente, para vertentes de Inteligência Artificial Multimodal, o **ODOR Dataset (Object Detection for Olfactory References)** (https://github.com/mathiaszinnen/odor-dataset) oferece 38.116 anotações visuais sobre obras de arte, mapeando 139 categorias de referências olfativas12. O seu uso permite que arquiteturas RAG expandam o contexto textual para a análise da semântica visual associada à perfumaria e à história dos aromas12.

## **2\. Repositórios Open Source de Web Scraping e Extração Dinâmica**

Dada a volatilidade do mercado de perfumaria, onde centenas de fragrâncias são lançadas anualmente, depender apenas de bases estáticas compromete a relevância do sistema de IA. A extração dinâmica de metadados a partir de catálogos como Fragrantica, Parfumo, Basenotes e The Good Scents Company (TGSC) torna-se obrigatória. O GitHub acolhe uma vasta gama de robôs de *web scraping* desenvolvidos em Python, Node.js e Rust, que efetuam o *parsing* do código HTML dessas plataformas.

### **2.1. Extração Estruturada do Fragrantica e Parfumo**

O repositório **PerfumAPI** (https://github.com/seccaz/PerfumAPI) destaca-se como o estado da arte para a ingestão contínua a partir do portal Fragrantica13. Desenvolvida em Python com a *framework* FastAPI, esta aplicação não se limita a extrair dados; ela aloja uma API REST local que comunica diretamente com uma base de dados PostgreSQL via Supabase, executando as migrações de esquemas automaticamente13.  
**Instruções de Uso para PerfumAPI:**

> 1. Execute a clonagem do repositório através do comando git clone https://github.com/seccaz/PerfumAPI.git e aceda ao diretório13.  
> 2. Configure o ambiente virtual Python e instale as dependências com pip install \-r requirements.txt13.  
> 3. Na plataforma Supabase, crie um projeto e copie os identificadores SUPABASE\_URL, SUPABASE\_KEY e a chave de serviço (SUPABASE\_SERVICE\_KEY), inserindo-os no ficheiro local .env13.  
> 4. Inicie o servidor local correndo o comando uvicorn api.main:app \--reload \--port 900013.  
> 5. Para extrair a pirâmide completa de uma marca inteira, efetue um pedido POST para o *endpoint* /scrape/brand enviando o *payload* JSON: {"brand\_name": "Jean Paul Gaultier", "limit": 10}13.

A arquitetura do PerfumAPI mapeia diretamente os campos notes\_top, notes\_middle e notes\_base em formato de matrizes (arrays) estruturadas de texto, além de extrair as taxas de longevidade e silagem percebidas pelos utilizadores13. O sistema incorpora atrasos programados de dois segundos entre pedidos, essencial para respeitar políticas de esgotamento de taxa (*rate limiting*) do servidor alvo, minimizando a possibilidade de rutura de conexão13.  
Para o portal Parfumo, o repositório **Parfumo Top Perfumes Scraper** (https://github.com/djigoio/perfume-scrapper) oferece uma abordagem baseada na linguagem Rust, conhecida pela sua alocação de memória determinística e elevado desempenho14. Utilizando as bibliotecas reqwest para comunicações HTTP e scraper para a seleção CSS, o código efetua o desdobramento da interface do Parfumo14.  
**Instruções de Uso para o Scraper Rust (Parfumo):**

> 1. Com o Rust instalado (via rustup), clone o repositório e aceda à pasta14.  
> 2. Execute o comando cargo run14. O robô irá autonomamente navegar pelos diretórios /Tops/Women, /Tops/Men e /Tops/Unisex14.  
> 3. O algoritmo escreverá três ficheiros CSV independentes (ex: perfumes\_Men.csv), catalogando o nome do perfume, marca, URL direta e a origem da imagem14. O uso desta ferramenta é ideal para alimentar a base de grafos com os índices de popularidade mais recentes.

### **2.2. Aprofundamento Químico e Plataformas Alternativas**

Para uma arquitetura RAG que pretenda aconselhar com precisão molecular e química, o repositório **The Good Scent Company Scraper** (https://github.com/NielBohr/tgsc-The-good-scent-company-scrapper) é uma descoberta inestimável15. A plataforma *The Good Scents Company (TGSC)* é a bíblia técnica dos perfumistas, albergando as "Fórmulas de Demonstração" de compostos químicos. O *scraper* desenvolvido em Python, assente na biblioteca requests, extrai e cruza as fórmulas dos acordes com as percentagens exatas de ingredientes moleculares15.  
**Instruções de Uso para o TGSC Scraper:** Após a extração do código, o utilizador deve instanciar o objeto principal invocando Scrapper(url, User\_Agent, titulo) e acionar o método scrape(). É imperativo copiar o cabeçalho User-Agent nativo através da inspeção de rede do navegador para evitar bloqueios triviais15. O programa irá gerar dois ficheiros CSV críticos: um contendo os metadados da fórmula, e outro detalhando cada ingrediente isolado com a sua respetiva percentagem estrita de uso e o limiar seguro (100 pct)15. Ao mapear estas percentagens no Grafo de Conhecimento, as arestas entre os nós "Fragrância" e "Composto Químico" passarão a possuir pesos reais baseados na formulação orgânica.  
No contexto de plataformas maduras como o Apify, existe também um **Fragrantica Scraper Actor** público (https://apify.com/lexis-solutions/fragrantica) baseado em Node.js17. Este ator, se fornecido com URLs de início (ex: {"url": "https://www.fragrantica.com/search/?query=Avon"}), lida nativamente com a paginação e exporta um documento JSON detalhado18. Os metadados processados revelam se a pirâmide é do tipo full (dividida em topNotes, middleNotes e baseNotes) ou single (misturada em allNotes), e extraem inclusivamente as cores hexadecimais de representação visual de cada acorde18. O uso destes atores elimina a necessidade de gestão de infraestrutura de *scraping*, mas pode envolver custos operacionais caso se ultrapasse a quota gratuita.

## **3\. Telemetria e Evasão de Sistemas Anti-Bot (Bypass de Cloudflare)**

O maior constrangimento na mineração de dados em portais da especialidade como Fragrantica, Parfumo, Basenotes e lojas como a Sephora é a implementação generalizada do **Cloudflare Bot Management**19. A arquitetura de proteção contemporânea combina a recolha de impressões digitais da camada de transporte criptográfico (TLS Fingerprinting), avaliações interativas via Cloudflare Turnstile, e inspeção de comportamento em ambiente JavaScript (DOM)19. Se o engenheiro de dados recorrer a bibliotecas de abstração HTTP convencionais, como o requests em Python ou o fetch não alterado no Node.js, os pedidos serão imediatamente bloqueados com o erro HTTP 403 Forbidden ou ficarão presos em ciclos infinitos de verificação "Verify you are human"20.

### **3.1. Evasão na Camada de Rede: Impressão Digital TLS e HTTP/2**

Sistemas de firewall de nova geração não se limitam a ler o cabeçalho User-Agent. Inspecionam os pacotes *ClientHello* da negociação TLS (identificados por hashes como JA3 e JA4). Se a assinatura criptográfica remeter a módulos OpenSSL genéricos, o Cloudflare saberá que não se trata de um navegador real, que nativamente utiliza bibliotecas como o BoringSSL (no caso do Google Chrome)21. Adicionalmente, a sequência de ordem dos pacotes *frames* do protocolo HTTP/2 expõe facilmente scripts amadores20.  
A ferramenta imperativa, e sem custos, no ecossistema Python em 2026 para superar esta barreira chama-se **curl\_cffi**19. Este pacote injeta as assinaturas exatas de impressão digital na camada criptográfica do cURL. A instrução de implementação dita a substituição completa das chamadas tradicionais:

> 1. Instalação via terminal: pip install curl-cffi20.  
> 2. Ao configurar o *script*, deve-se instruir o módulo a personificar uma versão recente do navegador. A definição do parâmetro impersonate="chrome124" obriga o tráfego a enviar os dados criptográficos exatos do Chrome, contornando a validação TLS do Cloudflare e assegurando que as frames HTTP/2 são ordenadas como as de um humano20.  
> 3. Quando combinado com o roteamento através de um *proxy* residencial, este vetor anula os filtros iniciais de reputação de IP (Bot Fight Mode)20.

### **3.2. Evasão em Camada de Aplicação: Inspeção DOM e JavaScript**

Para catálogos cujas páginas exigem a resolução ativa do desafio Cloudflare Turnstile, a execução de um emulador de navegador invisível (*headless*) é fundamental19. Bibliotecas legadas de automação, como o Selenium ou o Puppeteer nativo, injetam variáveis no motor JavaScript do navegador, particularmente a propriedade navigator.webdriver \= true19. O Cloudflare deteta esta variável e também inspeciona anomalias no motor gráfico WebGL, permissões de interface e simulações de API de áudio, resultando num bloqueio sumário23.  
As táticas avançadas para o bypass a este nível recomendam a integração de três ferramentas essenciais:

> 1. **Nodriver**: Atualmente a evolução recomendada face ao undetected-chromedriver. Este pacote concebido para Python opera patches profundos no binário do navegador e suprime de forma absoluta os vazamentos inerentes ao protocolo CDP (Chrome DevTools Protocol)19. O script lança a instância invisível com browser \= await uc.start(), navega para o alvo e permite a execução orgânica dos scripts de validação de segurança até o acesso à base de dados olfativa ser concedido19.  
> 2. **SeleniumBase (Modo UC)**: Utiliza a configuração expressa uc=True na sua invocação para reestruturar as assinaturas de automação, mimetizando de forma passiva um comportamento cívico perante a rede do Cloudflare19.  
> 3. **FlareSolverr (Abordagem de Interceção de Cookies)**: Uma solução centralizada operada frequentemente através de contentores Docker. O FlareSolverr funciona como um servidor proxy local24. As instruções determinam que o extrator Python não interaja diretamente com o Fragrantica. Em vez disso, o extrator envia um pedido POST para http://localhost:8191/v1 com a carga útil {"cmd": "request.get", "url": "https://target.com"}24. O FlareSolverr processa o desafio utilizando instâncias limpas do Chromium, resolve as verificações matemáticas do Cloudflare e devolve os cookies de sessão validados (cf\_clearance) e a resposta HTML pura21. O sistema de extração pode então reverter para o uso de bibliotecas de baixo custo de processamento passando a anexar estes cookies vitais.

## **4\. Exploração de Endpoints Ocultos e APIs de E-Commerce**

Enquanto o *web scraping* força a desconstrução de HTML, a arquitetura moderna de comércio eletrónico permite uma abordagem mais cirúrgica e com zero custos de licenciamento de APIs corporativas. A monitorização da aba de Rede (*Network tab*) no navegador, focada em requisições Fetch/XHR, revela os *payloads* em formato JSON que o servidor entrega ao *front-end* (APIs Ocultas).

### **4.1. O Paradigma da Arquitetura VTEX**

A VTEX é uma das plataformas de *e-commerce headless* mais prevalentes entre gigantes globais, redes de retalho na América Latina (ex: Época Cosméticos, Lojas Renner, Lojas Rede) e distribuidores atacadistas25. Todo o catálogo das lojas hospedadas na VTEX é gerido centralmente por um motor que possui uma API Pública de Catálogo (*Legacy Search API*) aberta para consultas externas sem autenticação obrigatória29.  
O vetor de extração centralizado na VTEX explora o *endpoint*: GET /api/catalog\_system/pub/products/search/30.  
Nesta infraestrutura, cada produto (como um perfume) contém grupos de dados denominados specificationGroups ou propriedades sob a estrutura de allSpecifications33. Os distribuidores e as marcas parametrizam exaustivamente estes campos no *back-office* da VTEX29. Ao efetuar uma pesquisa segmentada anexando o termo na URL genérica (ex: https://www.{dominio\_vtex}.com.br/api/catalog\_system/pub/products/search/perfume ou ?fq=C:{ID\_da\_Categoria}), o servidor responde com listas maciças de SKUs em JSON30.  
**Análise Estrutural do Payload (JSON):** Ao capturar a resposta para um produto real operado num domínio VTEX (ex: Gucci Flora ou Dolce & Gabbana Velvet Black Patchouli), a taxonomia revela os vetores ideais para a IA. O campo das especificações expõe arrays cristalinos25:

* "Familia Olfativa": \["Floral", "Gourmand"\]25.  
* "Notas de Topo": \["pera", "mandarina italiana"\]25.  
* "Notas de Coracao": \["gardenia", "jasmim", "frangipani"\]25.  
* "Notas de Fundo": \["açúcar mascavo", "patchouli"\]25.  
* Campos adicionais frequentemente encontrados englobam "Concentração": \["Eau de Parfum"\] e "Ocasião"25.

Esta estratégia de mineração de dados permite um desenvolvimento ágil e escalável sem interrupções operacionais. O *script* pode iterar sobre parâmetros de paginação padrão (ex: &\_from=0&\_to=49), varrendo e modelando milhares de pirâmides olfativas organizadas que já foram auditadas pela própria marca. Adicionalmente, chamadas ao *endpoint* de crossselling como api/catalog\_system/pub/products/crossselling/whosawalsosaw/ fornecem dados de comportamento e coocorrência (produtos frequentemente visualizados juntos), possibilitando a construção de arestas de recomendação autênticas (ex: ALSO\_VIEWED) no Grafo de Conhecimento31.

### **4.2. Beleza na Web e Plataformas Independentes**

Plataformas com ecossistemas REST independentes, como a Beleza na Web, gerem as listagens baseadas no seu próprio *framework*35. Embora a documentação oficial da plataforma e do seu portal de *sellers* indique arquiteturas rigorosas (como em https://api.marketplace.hml.belezanaweb.com.br/global/v1/marketplace)37, a inspeção orgânica dos pedidos de preenchimento da página frontal (na aba Network) possibilita a interceção do tráfego JSON sem estado (stateless) das páginas de produto35.  
A plataforma global **Wikiparfum**, gerida em estreita colaboração com a *Fragrances of the World* (a principal taxonomia da indústria), catalogou 32.219 perfumes e 1.563 ingredientes olfativos únicos38. Apesar dos *endpoints* formais para consumo programático exigirem a provisão de uma chave de autenticação rigorosa (API Key) perante a sua documentação técnica (https://docs.wikiparfum.com/)40, a monitorização de tráfego de interface, particularmente focada nas barras de autocompletar e de visualização gráfica da matriz do perfume, emite chamadas abertas à rede que devolvem a distribuição exata dos identificadores de ingredientes38. A ingestão tática destas respostas resolve a ambiguidade na grafia de ingredientes, mapeando termos informais de volta à sua categorização olfativa mestre.

## **5\. Web Semântica e a Ontologia Interconectada (Wikidata)**

Na transição de meros repositórios documentais para um RAG baseado num Grafo de Conhecimento, as ontologias estritamente ligadas (Linked Data) assumem o protagonismo. A Web Semântica do Wikidata fornece aos modelos a base estrutural que liga a definição abstrata de uma substância aos seus identificadores globais interconectados41.  
A entidade âncora da taxonomia universal olfativa é estruturada pelo identificador do item Wikidata **Q131746 (Perfume)**41. A classe hierárquica dita que esta entidade é uma subclasse primária de um composto de aroma e cosmético42. Em torno da entidade do Perfume, existem propriedades vitais e formalmente mapeadas que devem ditar os esquemas nodais da base de dados:

* **Propriedade P14076**: Fragrantica perfume ID. Estabelece a ligação indubitável e universal do item armazenado na Web Semântica com o seu URL formatado no portal Fragrantica43.  
* **Propriedade P14082**: Parfumo perfume brand ID. Mapeia a ligação semântica direta à casa criadora ou ao fabricante do perfume no ecossistema do Parfumo44.  
* **Propriedade P14080**: Fragrantica perfume notes ID. Representa a indexação de um determinado ingrediente químico ao seu vetor olfativo oficial no site correspondente44.  
* **Propriedades Químicas e de Ingredientes (P527, P186)**: Traduzem as dependências ontológicas (material do qual é composto, constituído por).

### **5.1. Construção Funcional da Query SPARQL**

O *Wikidata Query Service* (WDQS), acessível publicamente através de query.wikidata.org, aloja o motor para a consulta estruturada destas entidades. O código redigido em sintaxe SPARQL possibilita a agregação imediata destes campos sem a necessidade de processamento da linguagem natural ou infraestrutura de hospedagem complexa.  
O código funcional abaixo efetua a pesquisa do universo de instâncias derivadas do perfume e exporta o nome da fragrância, a marca matriz, os identificadores chave do Fragrantica e os componentes químicos listados. Os rótulos foram instruídos para, primeiramente, devolver resultados em português (pt), seguidos de inglês e francês:

Snippet de código  
SELECT DISTINCT ?perfume ?perfumeLabel ?brandLabel ?fragranticaID ?parfumoID ?chemicalLabel WHERE {  
  \# Limita o escopo aos itens que são instâncias (P31) ou subclasses (P279)   
  \# da entidade matriz 'Perfume' (Q131746) em qualquer profundidade hierárquica.  
  ?perfume wdt:P31/wdt:P279\* wd:Q131746 .  
    
  \# Captura de forma opcional o fabricante, marca ou criador (P176 ou P2079)  
  OPTIONAL {   
    ?perfume wdt:P176|wdt:P2079 ?brand .   
  }  
    
  \# Isola o identificador externo da base do Fragrantica (P14076)  
  OPTIONAL {   
    ?perfume wdt:P14076 ?fragranticaID .   
  }  
    
  \# Isola o identificador de marca na base do Parfumo (P14082)  
  OPTIONAL {   
    ?perfume wdt:P14082 ?parfumoID .   
  }  
    
  \# Busca elementos constituintes orgânicos, peças ativas químicas ou materiais (P527 ou P186)  
  OPTIONAL {  
    ?perfume wdt:P527|wdt:P186 ?chemical .  
  }  
    
  \# Serviço automático de resolução de rótulos da entidade (WikiBase) priorizando Português  
  SERVICE wikibase:label {   
    bd:serviceParam wikibase:language "pt,en,fr" .   
    ?perfume rdfs:label ?perfumeLabel .  
    ?brand rdfs:label ?brandLabel .  
    ?chemical rdfs:label ?chemicalLabel .  
  }  
}  
\# Previne tempos de limite de execução do servidor público limitando o volume do retorno  
LIMIT 5000

Este *script* funciona como a pedra basilar de integração. O ficheiro resultante pode ser importado para o sistema primário de bases de dados do projeto de IA. A extração simultânea do fragranticaID assegura que os robôs de extração (como o PerfumAPI) não tenham de efetuar buscas incertas com base nos nomes comerciais dos perfumes; em vez disso, o construtor do sistema invoca URLs definitivos a partir das listagens do Wikidata, garantindo uma congruência de 100% de precisão cruzada (Lookup Table)13.

## **6\. Síntese e Implementação Arquitetural para a IA**

A convergência destas frentes de extração viabiliza uma taxonomia imbatível e ágil para o desenho de um Grafo de Conhecimento especializado. A ingestão destas fontes deve seguir uma orquestração faseada, permitindo que as limitações estruturais de um vetor sejam compensadas pela clareza do subsequente.  
A arquitetura final do RAG adquire poder através do preenchimento estrutural do motor vetorial. O vocabulário das matérias-primas constrói-se com a riqueza do Wikidata e os ficheiros de suporte do FragDB1. As complexas percentagens das formulações moleculares fluem a partir do *scraping* agressivo efetuado ao *The Good Scents Company* (gerando pesos das arestas do grafo)15.  
No estrato de mercado dinâmico, as APIs do ecossistema VTEX garantem que novas fragrâncias injetadas no comércio eletrónico diariamente pela indústria cosmética (como listagens em lojas atacadistas) forneçam pirâmides olfativas pré-estruturadas (specificationGroups) a custo zero computacional para a equipa33. E, de forma crucial, perante desafios em recintos vigiados por ferramentas corporativas de cibersegurança como o Cloudflare, a personificação cirúrgica das conexões através de *curl\_cffi* mimetiza comportamentos humanos civis perfeitos20.  
Esta interligação de inteligência em rede aberta permite que o LLM responda com profundidade química autêntica e embasada, substituindo a incerteza da geração de texto não validada por um encadeamento seguro, escalável e perfeitamente ancorado às matrizes físicas da perfumaria contemporânea.

#### **Referências citadas**

> 1. FragDB — Fragrance Database (multilingual) \- GitHub, [https://github.com/FragDB/fragrance-database](https://github.com/FragDB/fragrance-database)  
> 2. FragDB, [https://fragdb.net/](https://fragdb.net/)  
> 3. FragDBnet/fragrance-database · Datasets at Hugging Face, [https://huggingface.co/datasets/FragDBnet/fragrance-database](https://huggingface.co/datasets/FragDBnet/fragrance-database)  
> 4. FragDB: Fragrance Database Data Exploration \- Kaggle, [https://www.kaggle.com/code/eriklindqvist/fragdb-fragrance-database-data-exploration](https://www.kaggle.com/code/eriklindqvist/fragdb-fragrance-database-data-exploration)  
> 5. perfume\_metadata.csv · MrBob23/perfume-description at main \- Hugging Face, [https://huggingface.co/datasets/MrBob23/perfume-description/blob/main/perfume\_metadata.csv](https://huggingface.co/datasets/MrBob23/perfume-description/blob/main/perfume_metadata.csv)  
> 6. abhirajeshbhai/perfume\_recommendation\_llm · Datasets at Hugging Face, [https://huggingface.co/datasets/abhirajeshbhai/perfume\_recommendation\_llm/viewer](https://huggingface.co/datasets/abhirajeshbhai/perfume_recommendation_llm/viewer)  
> 7. Fragrantica.com Fragrance Dataset | Kaggle, [https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset)  
> 8. Fragrantica.com Fragrance Dataset \- Kaggle, [https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset/code](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset/code)  
> 9. Fragrantica Analysis \- Kaggle, [https://www.kaggle.com/code/kmljts/fragrantica-analysis](https://www.kaggle.com/code/kmljts/fragrantica-analysis)  
> 10. Perfume E-Commerce Dataset 2024 \- Kaggle, [https://www.kaggle.com/datasets/kanchana1990/perfume-e-commerce-dataset-2024](https://www.kaggle.com/datasets/kanchana1990/perfume-e-commerce-dataset-2024)  
> 11. The Scent of Data \- Exploring the Parfumo Fragrance Dataset \- GitHub, [https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-12-10/readme.md](https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-12-10/readme.md)  
> 12. mathiaszinnen/odor-dataset \- GitHub, [https://github.com/mathiaszinnen/odor-dataset](https://github.com/mathiaszinnen/odor-dataset)  
> 13. PerfumAPI \- API for perfume enthusiasts. Feel free to use for testing and educational purposes only. \- GitHub, [https://github.com/seccaz/PerfumAPI](https://github.com/seccaz/PerfumAPI)  
> 14. GitHub \- djigoio/perfume-scrapper: This Rust project scrapes the top perfumes listed on Parfumo for different categories (Women, Men, Unisex) and saves the results into CSV files. Made for learning purposes, [https://github.com/djigoio/perfume-scrapper](https://github.com/djigoio/perfume-scrapper)  
> 15. NielBohr/tgsc-The-good-scent-company-scrapper \- GitHub, [https://github.com/NielBohr/tgsc-The-good-scent-company-scrapper](https://github.com/NielBohr/tgsc-The-good-scent-company-scrapper)  
> 16. perfume · GitHub Topics, [https://github.com/topics/perfume](https://github.com/topics/perfume)  
> 17. Discover Niche Perfume Brands and Unique Fragrance Pyramids \- Apify, [https://apify.com/crawlerbros/fragrantica-scraper/examples/fragrantica-scraper-niche-perfume-brand-discovery](https://apify.com/crawlerbros/fragrantica-scraper/examples/fragrantica-scraper-niche-perfume-brand-discovery)  
> 18. Fragrantica Scraper \- Perfume Data Extractor \- Apify, [https://apify.com/lexis-solutions/fragrantica](https://apify.com/lexis-solutions/fragrantica)  
> 19. How to Bypass Cloudflare When Web Scraping in 2026 \- Scrapfly, [https://scrapfly.io/blog/posts/how-to-bypass-cloudflare-anti-scraping](https://scrapfly.io/blog/posts/how-to-bypass-cloudflare-anti-scraping)  
> 20. How to Bypass Cloudflare When Web Scraping (2026): Every Method Ranked | Use Apify, [https://use-apify.com/blog/how-to-bypass-cloudflare-web-scraping](https://use-apify.com/blog/how-to-bypass-cloudflare-web-scraping)  
> 21. How to Bypass Cloudflare in Python \- ZenRows, [https://www.zenrows.com/blog/bypass-cloudflare-python](https://www.zenrows.com/blog/bypass-cloudflare-python)  
> 22. Is it possible to bypass Cloudflare Turnstile from a datacenter IP using Selenium or curl\_cffi in 2026? Local works, Docker/Hosted always fails \- Stack Overflow, [https://stackoverflow.com/questions/79877820/is-it-possible-to-bypass-cloudflare-turnstile-from-a-datacenter-ip-using-seleniu](https://stackoverflow.com/questions/79877820/is-it-possible-to-bypass-cloudflare-turnstile-from-a-datacenter-ip-using-seleniu)  
> 23. Bypassing Cloudflare and DDoS-Guard: A Complete Technical Reference for Web Scrapers (2026) | by Sudipto Chandra \- Medium, [https://medium.com/@dipu.sudipta/bypassing-cloudflare-and-ddos-guard-a-complete-technical-reference-for-web-scrapers-2026-6375c38af658](https://medium.com/@dipu.sudipta/bypassing-cloudflare-and-ddos-guard-a-complete-technical-reference-for-web-scrapers-2026-6375c38af658)  
> 24. FlareSolverr Guide \- Bypassing Cloudflare With Python (2026) \- ScrapeOps, [https://scrapeops.io/python-web-scraping-playbook/python-flaresolverr/](https://scrapeops.io/python-web-scraping-playbook/python-flaresolverr/)  
> 25. Gucci Flora Gorgeous Gardenia Intense Eau de Parfum \- Perfume Feminino 50ml, [https://www.lojasrede.com.br/gucci-flora-gorgeous-gardenia-intense-eau-de-parfum-perfume-feminino-50ml-z177023c4u561264/p](https://www.lojasrede.com.br/gucci-flora-gorgeous-gardenia-intense-eau-de-parfum-perfume-feminino-50ml-z177023c4u561264/p)  
> 26. Dolce & Gabbana Velvet Black Patchouli Eau de Parfum \- Perfume Unissex 100ml, [https://www.lojasrede.com.br/dolce-gabbana-velvet-black-patchouli-eau-de-parfum-perfume-unissex-100ml-177bo08c95521307/p](https://www.lojasrede.com.br/dolce-gabbana-velvet-black-patchouli-eau-de-parfum-perfume-unissex-100ml-177bo08c95521307/p)  
> 27. Controle de exibir brindes, não exibe nenhum. \- Português \- VTEX, [https://community.vtex.com/t/controle-de-exibir-brindes-nao-exibe-nenhum/16663](https://community.vtex.com/t/controle-de-exibir-brindes-nao-exibe-nenhum/16663)  
> 28. Nioxin System 4 Kit \- Shampoo \+ Condicionador \+ Tratamento \- kit ÚNICO \- Renner, [https://www.lojasrenner.com.br/p/nioxin-system-4-kit-shampoo-condicionador-tratamento-kit/-/A-7010702289487-br.lr](https://www.lojasrenner.com.br/p/nioxin-system-4-kit-shampoo-condicionador-tratamento-kit/-/A-7010702289487-br.lr)  
> 29. Catalog \- VTEX Developers, [https://developers.vtex.com/docs/guides/catalog-overview](https://developers.vtex.com/docs/guides/catalog-overview)  
> 30. felipe-ssilva/vtex-utils: ‍ · GitHub, [https://github.com/felipe-ssilva/vtex-utils](https://github.com/felipe-ssilva/vtex-utils)  
> 31. Legacy Search API \- VTEX Developers, [https://developers.vtex.com/docs/api-reference/search-api](https://developers.vtex.com/docs/api-reference/search-api)  
> 32. Catalog API \- VTEX Developers, [https://developers.vtex.com/docs/api-reference/catalog-api](https://developers.vtex.com/docs/api-reference/catalog-api)  
> 33. VTEX Product Specification Badges, [https://developers.vtex.com/docs/apps/vtex.product-specification-badges](https://developers.vtex.com/docs/apps/vtex.product-specification-badges)  
> 34. Product Specifications by vtex \- VTEX Developers, [https://developers.vtex.com/docs/apps/vtex.product-specifications](https://developers.vtex.com/docs/apps/vtex.product-specifications)  
> 35. Beleza na Web API, [https://developer.belezanaweb.com.br/$](https://developer.belezanaweb.com.br/$)  
> 36. Beleza na Web API, [https://developer.belezanaweb.com.br/](https://developer.belezanaweb.com.br/)  
> 37. Beleza na Web API, [https://developer.belezanaweb.com.br/products/criar-anuncios](https://developer.belezanaweb.com.br/products/criar-anuncios)  
> 38. Wikiparfum: Perfume wiki and fragrance recommendations, [https://www.wikiparfum.com/](https://www.wikiparfum.com/)  
> 39. How does it work? \- Wikiparfum, [https://www.wikiparfum.com/en/how-does-it-work/](https://www.wikiparfum.com/en/how-does-it-work/)  
> 40. WikiParfum API Docs, [https://docs.wikiparfum.com/](https://docs.wikiparfum.com/)  
> 41. Property talk:P452 \- Wikidata, [https://www.wikidata.org/wiki/Property\_talk:P452](https://www.wikidata.org/wiki/Property_talk:P452)  
> 42. perfume \- Wikidata, [https://www.wikidata.org/wiki/Q131746](https://www.wikidata.org/wiki/Q131746)  
> 43. Fragrantica perfume ID \- Wikidata, [https://www.wikidata.org/wiki/Property:P14076](https://www.wikidata.org/wiki/Property:P14076)  
> 44. MediaWiki:Wikibase-SortedProperties \- Wikidata, [https://www.wikidata.org/wiki/MediaWiki:Wikibase-SortedProperties](https://www.wikidata.org/wiki/MediaWiki:Wikibase-SortedProperties)  
> 45. Parfumo perfume brand ID \- Wikidata, [https://www.wikidata.org/wiki/Property:P14082](https://www.wikidata.org/wiki/Property:P14082)