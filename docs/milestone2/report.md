# Milestone 2 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## TODO

- Explorar "hotéis com boa acessibilidade e transportes públicos próximos". Tratar como necessidade de informação e não tanto como queries. Reformular essa parte do relatório; Identificar quatro (4) possíveis queries, para bater certo com o que vai ser explorado neste M2;
- Corrigir os "problemas" apontados pelo professor do M1;
- use \parts (Latex) for each milestone;
- Retirar a secção "Conclusions and Future work";
- Preparar os slides anteriores para a versão M2;

- Colocar as seguintes secções:

## Information Retrieval

Introdução a [Information Retrieval]. Justificar choose the information retrieval tool [Solr]. Falar sobre o Solr. Colocá-lo nas referências.

## Document Characterization

- Caracterização do documento final;
- Analyze the documents and identify their indexable components;
- Construção de uma tabela com todos os atributos e se são indexáveis ou não. Tabela tem os headers attribute, context, index?;

## Indexing Process

Dizer que o Solr apresenta indexes. Referência.
Selected [indexes do Solr] por atributo apresentado na tabela de cima. Justificar.

## Retrieval Process and Setup

É aqui que se fala da indexação das queries? Verificar.

Há um schemaless. Justificar que o Solr já faz isso por default quando não é apresentado nada.

O que não é schemaless vai ter pesos nos parâmetros. Indicar quais os pesos (tabela?) e justificar. Question: dão-se pesos a atributos não indexados?

Justificar o porquê de não usarmos pesos diferentes de atributos para diferentes queries. Prós e contras. Fazer com pesos diferentes para as queries vai enviesar os resultados (em geral ficam melhores), mas não é realista. Todas as queries com o mesmo peso pode interferir no resultado esperado nas queries que precisem muito mais de determinados atributos do que outros. 

Justificar como vamos fazer as queries. Ver os parametros necessários no Solr.

## Evaluation

### Formas de avaliação usadas

- Vamos usar P@20, Recall, AvP, MAP. Fazer RC Curves.
- Manualmente, para avaliar os 2 setups criados;

No Solr vamos usar estes fields importantes:

- `query` (q) - a query que queremos
- `query field with optional boost` (qf) - para dar pesos a determinados fields na pesquisa;
- `phrase boosted field` (pf) - podemos escolher termos da query mais relevantes;
- `phrase boost slope` (ps) - definição do número máximo de tokens entre as palavras pesquisadas;

Vamos também usar o eDisMax [R]. Justificar que é porque permite queries mais complexas, com base em operações AND OR... e justificar com mais coisas. Ver referência.

### Precondições

- Fixar ranking baseado nos primeiros 20. Justificar que num search engine normal, Google, só os primeiros importam.
- Fixar a amostragem/universo para o Recall. Tem de ser superior em pelo menos 3 vezes o limite anterior. Prós e contras.

### Resultados

- TODO: que tabelas gerar? Se não couber tudo aqui vai para os anexos.

#### Q1

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

#### Q2

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

#### Q3

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

#### Q4

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

Global:
- evaluate the results obtained for the defined information needs.

## Conclusions and Future work

Concluir acerca da consistência global do search engine / system.
Adaptar do M1 e explorar possibilidade do M2:
- Melhorar o parâmetro X e Y, e justificação teórica
- work on user interfaces by developing a frontend for the search system, including specific features such as snippet generation, results clustering
- sentimental and context analysis, muito importante já que a nossa fonte de informação principal são reviews, logo são subjectivas;

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
- [eDismax](https://solr.apache.org/guide/7_7/the-extended-dismax-query-parser.html)
-