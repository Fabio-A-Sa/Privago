# Milestone 2 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## TODO

- Explorar "hotéis com boa acessibilidade e transportes públicos próximos". Tratar como necessidade de informação e não tanto como queries. Reformular essa parte do relatório;
- Corrigir os "problemas" do M1;
- use \parts (Latex) for each milestone;
- Retirar a secção "Conclusions and Future work";
- Colocar as seguintes secções;

## Information Retrieval

Introdução a [Information Retrieval]. Justificar choose the information retrieval tool [Solr]. Falar sobre o Solr. Colocá-lo nas referências.

## Document Characterization

- Caracterização do documento final;
- Analyze the documents and identify their indexable components;
- Construção de uma tabela com todos os atributos;

## Indexing Process

Dizer que o Solr apresenta indexes. Referência.
Selected [indexes do Solr] por atributo apresentado na tabela de cima. Justificar.

## Retrieval Process and Setup

use the selected tool to configure and execute the queries;

demonstrate the indexing and retrieval processes;
implement and evaluate two distinct retrieval setups;

o que não é schemaless vai ter pesos nos parâmetros. Justificar. Justificar o porquê de não usarmos pesos diferentes de atributos para diferentes queries. Vai enviesar os resultados. 

## Evaluation

### Formas de avaliação usadas

- Vamos usar P@20, Recall, AvP, MAP. Fazer RC Curves.
- Manualmente, para avaliar os 2 setups criados;

### Precondições

- Fixar ranking baseado nos primeiros 20. Justificar que num search engine normal, Google, só os primeiros importam.
- Fixar a amostragem/universo para o Recall. Tem de ser superior em pelo menos 3 vezes o target. Prós e contras.

### Resultados

#### Q1

#### Q2

#### Q3

- Recall. Por amostragem. Para cada query vai enviesar prós e contras. optar por um, justificando.
- default, schema, pesos

- manually evaluate the returned results;
- evaluate the results obtained for the defined information needs.

## Conclusions and Future work

Concluir acerca da consistência global do search engine / system.
Adaptar do M1 e explorar possibilidade do M2:
- Melhorar o parâmetro X e Y, e justificação teórica
- work on user interfaces by developing a frontend for the search system, including specific features such as snippet generation, results clustering

## Annexes

Todos os anteriores mais:

-
-
-

## References

Todos os anteriores mais:

- [Information Retrieval](link)
- [Solr](https://solr.apache.org/guide/6_6/introduction-to-solr-indexing.html), 18/10/2023
- [Solr Indexes]()
-
-