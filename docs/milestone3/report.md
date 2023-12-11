# Milestone 3 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## 8. Information Retrieval Improvements

The previous stage introduced an initial version of the information retrieval system, evaluating it based on well-defined information needs and metrics grounded in precision and recall. Looking from another perspective, it also helped identify the weaknesses and limitations of the chosen approaches. Therefore, to enhance the search engine, this phase will involve the implementation and evaluation of features aimed at addressing the identified gaps:

- Stop Words;
- Semantic Analysis;

The evaluation of these features will follow the same style as the previous ones, using real information needs as a base and adjusting them to the context encountered. There will still be two systems under analysis, this time the boosted system and the boosted system with the application of the improvement under study. Evaluating each improvement separately allows for both an isolated analysis of its contribution to the system's success and a discussion on its permanence in the final search engine.

Three information needs will be used. The first two will be the same as in the previous stage, ensuring a valid comparison of the systems when exposed to the same environment and providing a visualization of the progressive development of the hypothesis. There will also be a comparison of the systems using a third information need, this time tailored to the improvement's objective, adding extra stress to the system on the topic we want to explore and checking the system's ability to handle the adversities of the natural language characteristic of these searches.

Table [T1] documents the relevance of the top 20 results for each evaluated query and for the two improvements under analysis.

In order to explore the project's theme more focusedly, *More Like This* [X0] has been added to the list of improvements, with consequent analysis. Balancing the benefits of each of the topics addressed brings us even closer to what a contemporary information retrieval system looks like today.

### A. Stop Words    

-> Justificar o porquê da decisão de colocar esta feature;
-> Indicar que o Solr tem suporte para este tipo de feature, adicionar referência a isso [X1];

-> QX1 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement (breve, será semelhante a uma anterior de M2)
-> Query (breve, será semelhante a uma anterior de M2)
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Stop Words
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> QX2 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement (breve, será semelhante a uma anterior de M2)
-> Query (breve, será semelhante a uma anterior de M2)
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Stop Words
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> QX3 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement
-> Query
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Stop Words
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> No final, avaliar os dois sistemas com base no MAP
-> Justificar se esta feature vai ou não para o sistema final

### B. Semantic Analysis

-> Justificar o porquê da decisão de colocar esta feature
-> Indicar se o Solr suporta, adicionar referências importantes [X2];

-> QX1 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement
-> Query
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Semantic Analysis
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> QX2 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement
-> Query
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Semantic Analysis
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> QX3 (seguir a estrutura de M2)

-> Information Need
-> Relevance Judgement
-> Query
-> Tabela com AvP e P@20 para System Boosted, System Boosted + Semantic Analysis
-> Result Analysis, não esquecer de justificar as precision-recall curves

-> No final, avaliar os dois sistemas com base no MAP
-> Justificar se esta feature vai ou não para o sistema final

### C. More Like This

Within Solr, the More Like This (MLT) functionality empowers users to discover documents akin to a specified document. Solr's More Like This is a Lucene [X3] built-in functionality that operates by scrutinizing the text within the provided document and subsequently identifying other documents in the index that exhibit textual and contextual similarities. The outcomes of this query comprise documents with the most elevated similarity scores.

Uma abordagem a esta feature é particularmente adequada e importante no contexto do projecto corrente. De facto, dado a particular importância da subjectividade inerente à escolha de hotéis por força do turismo, é expectável que os utilizadores queiram encontrar mais zonas ou hotéis alinhadas às suas preferências.

Assim, a partir de uma review de hotel, o sistema encontra outras 10 com conteúdo semelhante e correspondentes hotéis. Esses resultados são computados e ordenados pelo score interno do match do Solr. Os parâmetros usados nas queries foram os seguintes:

- `mlt.fl = text`, a comparação de semelhança será sempre com base no texto entre reviews, pois é este texto que contém o contexto da avaliação do mesmo;
- `mlt.mintf = 2` (número default do Lucene), o mínimo de matches entre termos para o documento ser considerado válido;
- `mlt.mindf = 5` (número default do Lucene), o mínimo de documentos válidos para que a pesquisa seja considerada válida;

Apesar da feature More Like This permitir ainda boosts em determinados parâmetros, isso não foi utilizado. Não faria sentido criar um boost adicional aos fields do documento a processar, visto que só aplicamos as funcionalidades do MTL ao field text na review. A aplicação do boost a termos ou tokens concretos iria desvirtuar o conceito de um search system global capaz de analisar de forma equilibrada cada query ao beneficiar o surgimento de algumas palavras.

A avaliação deste improvement não segue a abordagem das necessidades de informação anteriores. A comparação de semântica e semelhança entre dois textos pode ser ainda mais complexa e subjectiva quando efetuada de forma manual. Como tal, optamos por avaliar a relevância destas queries recorrendo à objectividade da biblioteca Python SpaCy [X4]. SpaCy é especializada em processamento avançado de linguagem natural (NLP) e permite comparação e quantificação da similiaridade entre dois textos através do seu contexto.

Após recolha de uma amostra do sistema, onde se selecionou aleatoriamente 20 reviews e as correspondentes 10 reviews mais semelhantes segundo o output do Solr, computou-se externamente o grau de similiaridade dos seus textos. O resultado da semelhança média entre os dez primeiros resultados de cada query MLT encontra-se descrito na Figura [F1].

![Figura F1](../../evaluation/mlt/mean_similiarity.png) - Average similiarity percentage for each query

A média global da similiaridade entre as queries é bastante elevada, nunca sendo inferior a 60% nesta amostra. Por outro lado, tratando-se de um sistema de ranking de documentos, importa saber o nível de decaimento da similiaridade com o índex dos outputs. Espera-se, em modo teórico, que os documentos que se encontram no topo tenham um grau de similiaridade superior aos restantes. Para avaliar esse comportamento, computou-se para cada índex do output o seu correspondente grau de similiaridade. A mean similiarity evolution across indexes pode ser encontrado na figura [F2]: 

![Figura F2](../../evaluation/mlt/similiarity_average_evolution.png) -  Evolution of average similiarity across result indexes

Ao contrário do esperado, não houve na amostra selecionada uma relação inversa entre o grau de similiriaridade da query original e o index do documento. Este facto pode ser justificado em duas vertentes. Por um lado, uma vez que o número de reviews do dataset é muito superior ao output do sistema MLT, não houve espaçamento para se notar uma diferença notória na ordenação dos resultados. Por outro lado o score do SpaCy é diferente do score interno do Solr, ao qual não temos acesso, dando azo a algumas oscilações.

Com resultados bastante satisfatórios, esta feature estará presente no sistema final.

## 9. User Interface

> Como avaliar? Meter uma pessoa a fazer queries em solr e depois na web app? Contar cliques, fazer formulário, tempo, a pessoa dizer se os resultados são relevantes ou não. Valor de referência, estudos.

Ver exatamente as features que queremos para a web interface. definir ordenações, limites de busca na API, entre outros. Implementar paginação de results, para uma melhor performance.

- Filtros (a meter tanto na home como na search):
    - location (drop down)
    - rating (1+, 2+, 3+, +4, 5) -> bolinhas do ávila
    - average_rating (1+, 2+, 3+, +4, 5) -> bolinhas do ávila

Homepage:
    - rating average descendente
    - limit = 20 hotels melhores

Search page:
    - paginação (até 10 * 10)
    - limite de results = 10 por página
    - 1,2..limit (=10 na maioria dos casos)

Hotels page:
    - paginação (até 10 * 10)
    - limite de results = 10 por página
    - Igual à search page

More like this page:
    - Botão em todas reviews na search page (não tem na home, nem na hotels, nem nesta)
    - a mesma cena que a query normal, só que coisa
    - a avaliação com python (?)

De forma a podermos avaliar aspectos qualitativos da plataforma Privago, tanto a nível global como de cada feature, os utilizadores são convidados no final da sessão de experimentação a responder a um breve questionário de satisfação.

Este questionário é baseado na versão standard da System Usability Scale (SUS) e contempla questões que avaliam a percepção do utilizador acerca da usabilidade e pertinência geral da aplicação, bem como na clareza de cada funcionalidade implementada.

O formulário demora cerca de 2 minutos a responder e todas as informações obtidas serão anónimas e utilizadas para fins de avaliação da plataforma.

In order to assess qualitative aspects of the Privago platform, both globally and for each feature, users are invited to respond to a brief satisfaction questionnaire at the end of the experimentation session.

This questionnaire is based on the standard version of the System Usability Scale (SUS) and includes questions that evaluate the user's perception of the overall usability and relevance of the application, as well as the clarity of each implemented functionality.

The form takes approximately 2 minutes to complete, and all information obtained will be anonymous and used for platform evaluation purposes.

I think that I would like to use this system frequently.
I found the system unnecessarily complex.
I thought the system was easy to use.
I think that I would need the support of a technical person to be able to use this system.
I found the various functions in this system were well integrated.
I thought there was too much inconsistency in this system.
I would imagine that most people would learn to use this system very quickly.
I found the system very cumbersome to use.
I felt very confident using the system.
I needed to learn a lot of things before I could get going with this system.

## 10. Final System Characterization

Indicar aqui que funcionalidades são aplicadas, por tópicos

com MAP X, a estas features adiciona-se ainda o MLT com acuracy Y e uma user interface avaiada em W.

aO LONGO DE TRES ITERAÇÕES, LOGO TÁ FIZE PARA AVABAR EM GRANDEII

## 11. Conclusions and Future Work

(modificar, este é o de M2)

adicionar filtro de location no mlt para future work

In conclusion of this milestone, all the planned tasks within the Information Retrieval phase of the project have been successfully completed. This accomplishment marks a crucial turning point in the process of creating a useful hotel search engine that aids tourists in making informed choices.

One of the most challenging aspects of the work involved developing effective strategies for dealing with nested documents, as well as their indexing and retrieval. Solr lacks documentation and concrete examples supporting the addressed document format.

Through the evaluation of the search engine, the system's stability and capability to handle different information needs within the chosen context have been verified. As the project progresses, opportunities for further enhancements and refinements emerge. Analyzing the results obtained from the first prototype of the hotel's information retrieval system:

- The `Stop Words` [X7] filter can be applied to `boosted_text` to reduce sensitivity to common words;
- `Sentimental and contextual analysis` is relevant, given that the main source of information for the system is reviews, which inherently carry subjective connotations;

In the next phase, work will be done on user interfaces by developing a frontend for the search system, incorporating specific features like snippet generation and results clustering. This engine will enable travelers to explore and filter accommodations based on preferences, such as location, room quality, staff service, or other factors identified during the analysis phase.

## References

Todas as anteriores mais:

- [X0] - [More Like This in Solr](https://solr.apache.org/guide/8_8/morelikethis.html)
- [X1] - Referências de Stop Words
- [X2] - Referências de Semantic Analysis. Uma delas tem de ser obrigatoriamente o Tutorial do regente
- [X3] - [Lucene Solr](https://lucene.apache.org/core/9_9_0/index.html)
- [X4] - [Python SpaCy](https://spacy.io)
- [X4] - SUS https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html
- Form https://docs.google.com/forms/d/1SXVDPi1CKsRgmEZa9fsZQnka58HgxBNi1FSTMo1OaGw/edit

## Annexes

[T1] - Tabela com 0s e 1s, com 20 linhas e colunas suficientes para suportar os improvements e a comparação entre o boosted e a nova approach;