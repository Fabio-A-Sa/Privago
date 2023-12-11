# Milestone 3 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## 8. Information Retrieval Improvements

- pegar nesta fase nas fragilidades do sistema encontradas na fase de evaluation anterior
- implementar as propostas enunciadas

- x
- y

os improvements foram analisaods com:
- 
- uma terceira query que provocasse stress ao tópico que queremos explorar

além destas foi adicionado o more like this, por fazer sentido dentro do nosso contexto

- z 

- os resultados estão expressos nos anexos, tabela V

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
- [X4] - SUS https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html
- Form https://docs.google.com/forms/d/1SXVDPi1CKsRgmEZa9fsZQnka58HgxBNi1FSTMo1OaGw/edit
