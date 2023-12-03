# Milestone 3 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## TODO

> Colocar em anexo os resultados de cada query para servir de apoio à avaliação. O que colocar? Query, index, relevant/n-relevant, o nome do hotel, a review? <br>
> Colocar um ficheiro no código com isso? <br>

- Melhorar o report anterior de acordo com o feedback da Milestone 2;
- Atualizar o Abstract agora com informação de objectivos e resultados da Milestone 3;
- Eliminar a secção 8 e colocar as seguintes:

## 8. Information Retrieval Improvements

> A avaliação desta parte será individual, ou seja, avaliação a cada improvement. Na Milestone 2 tínhamos 4 queries, nesta fase podemos colocar só 3 queries? O espaço é limitado. <br>

> Avaliação por cada tópico, A, B, C ou avaliação no final? (separada claro) <br>

### A. Stop Words    

Stop Words, para que o search system faça skip de palavras comuns tanto em queries como em results.

### B. Contextual Analysis

> Para isto existe o Apache OpenNLP e o Tutorial do Sérgio <br>

Given that the main source of information for the system is reviews, which inherently carry subjective connotations.

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

- [X1] - [More Like This in Solr](https://solr.apache.org/guide/8_8/morelikethis.html)
- 