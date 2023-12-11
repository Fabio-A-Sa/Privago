# Milestone 3 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## 8. Information Retrieval Improvements

Due to certain system fragilities and obstacles, several enhancements were introduced to address these issues and improve the overall search system, thereby enhancing the client experience.

In the subsequent sections, two specific improvements were implemented, and their impact was assessed using two queries from the previous approach. The evaluation focused on analyzing the improvements within the query parameters. In order to offer a thorough examination of the enhancements, an additional query was examined to explicate its relevance and provide specific information about its operation.

### A. Stop Words    

The decision to implement a stopwords filter aimed at enhancing the exploration of complex queries, allowing clients more flexibility to conduct searches with more complex queries. Solr initially provides a set of predefined stopwords, but a custom file was chosen, derived from a word cloud diagram. Similar to the process for Synonyms, this custom stopwords file was incorporated into the Solr configuration files.

Two queries from Milestone 2 were reviewed in the following queries, each with a single stopword. When compared to the previous strategy, the new approach added two query parameters: stopwords and ignorecase, both of which were set to true, indicating that stopwords would be investigated regardless of capitalization.

#### Breakfast or Room Service

__Information Need:__ Hotels with good breakfast or good room service in New Delhi.
__Relevance Judgement:__ In this information need its intended to search for hotels with a good breakfast or a good room service in New Delhi. Therefore, the words "good breakfast" or "good room service" should appear in the same query/text of review and the location should be a filter query of the parents documents.
__Query:__
- q: (good breakfast) OR (good room service)
- q.op: AND
- fq: {!child of=\"\*:\* -_nest\_path\_:*\"}location:"new delhi"
- fl: *,[child]
- sort: score desc
- stopwords: true
- ignoreCase: true

### Vegetarian/Vegan

__Information Need:__ Hotels with good vegetarian/vegan options
__Relevance Judgement:__ In this task, the objective is to find hotels with good vegetarian or vegan options. So, the words "good vegetarian" or "good vegan" should appear in the review's text. The location isn't specified.
__Query:__
- q: (good vegetarian) OR (good vegan)
- q.op: AND
- fq: {!child of=\"\*:* -_nest_path_:\*\"}location:*
- fl: *,[child]
- sort: score desc
- stopwords: true
- ignoreCase: true

### Beach Views

__Information Need:__ Best hotels with beach views.
__Relevance Judgement:__ In this task, the objective is to find the best hotels with beach views. Since we are using the StopWords Filter, only the words "best hotels beach views" will be search in each review text. 
__Query:__
- q: What are the best hotels with beach views
- q.op: AND
- fq: {!child of=\"\*:* -_nest_path_:\*\"}location:*
- fl: *,[child]
- sort: score desc
- stopwords: true
- ignoreCase: true

Upon analyzing the results in each table, it is clear that the results of the two previous queries differ, as expected. The use of the stopwords filter during indexing and querying causes a difference in results. Considering that the query only contains one stopword, the results show a noticeable similarity even though they are not identical.

In contrast, the third query, which has four stopwords, produced no results in the original schema without the stopwords filter. The modified schema, on the other hand, provided the expected 20 outcomes with a precision of 13 out of 20, as shown in the [table].

In conclusion, the integration of a stopwords filter provides the advantage of handling more complex queries, granting clients greater freedom in their search parameters. This enhancement contributes to the complexity and accuracy of the search results, ultimately improving the overall search system.

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

[X1]

A partir de uma review, encontra outras 10 com conteúdo semelhante.
Resultados ordenados pelo score interno do match Solr.

Parâmetros usados e breve justificação:

- mlt.fl = text, a comparação de semelhança será sempre com base no texto entre reviews
- mlt.mintf = 2 (o default), mínimo de matches entre termos para o documento ser considerado válido;
- mlt.mindf = 5 (o default), mínimo de documentos válidos para que a pesquisa seja considerada válida;

Não usamos boost, visto que:
- Como só colocamos à prova uma variável, então só poderíamos dar boost a essa
- Há hipótese de colocarmos boost a determinados tokens, mas esses não são fixos e podem variar entre query/match/review. Um sistema global é melhor.

A avaliação foi feita não com formas subjectivas (manualmente) mas sim objectivas, através da biblioteca `spacy` do python.

É importante referir que o score do spacy é diferente do score interno do solr, por isso podemos ver algumas variações nos 10 primeiros. Idealmente a similiriaridade diminuiria do primeiro resultado para o último, mas não é assim para todos os casos.

Após uma amostra aleatória, onde se selecionou 10 reviews e as correspondentes 10 reviews mais semelhantes segundo o Solr, apresentar aqui alguns resultados.

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

## 10. Conclusions and Future Work

(modificar, este é o de M2)

In conclusion of this milestone, all the planned tasks within the Information Retrieval phase of the project have been successfully completed. This accomplishment marks a crucial turning point in the process of creating a useful hotel search engine that aids tourists in making informed choices.

One of the most challenging aspects of the work involved developing effective strategies for dealing with nested documents, as well as their indexing and retrieval. Solr lacks documentation and concrete examples supporting the addressed document format.

Through the evaluation of the search engine, the system's stability and capability to handle different information needs within the chosen context have been verified. As the project progresses, opportunities for further enhancements and refinements emerge. Analyzing the results obtained from the first prototype of the hotel's information retrieval system:

- The `Stop Words` [X7] filter can be applied to `boosted_text` to reduce sensitivity to common words;
- `Sentimental and contextual analysis` is relevant, given that the main source of information for the system is reviews, which inherently carry subjective connotations;

In the next phase, work will be done on user interfaces by developing a frontend for the search system, incorporating specific features like snippet generation and results clustering. This engine will enable travelers to explore and filter accommodations based on preferences, such as location, room quality, staff service, or other factors identified during the analysis phase.

## References

Todas as anteriores mais:

- [X1] - Referências de Stop Words
- [X2] - Referências de Semantic Analysis, uma delas tem de ser obrigatoriamente o tutorial do regente
- [X3] - [More Like This in Solr](https://solr.apache.org/guide/8_8/morelikethis.html)