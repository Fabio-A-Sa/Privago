# Milestone 2 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## TODO

- Melhorar a secção "Abastract", adicionar uma frase sobre M2.
- Melhorar a secção "1 - Introduction", porque ela só fala das partes do M1. Diminuir e incluir as partes de M2;
- Melhorar a secção "5. Possible Search Tasks" com aquilo que definirmos na avaliação dos sistemas;
- use \parts (Latex) for each milestone;
- Retirar a secção "6. Conclusions and Future work";
- Preparar os slides anteriores para a versão M2;
- retirar referências a "we", "our", "us" que possam surgir;
- Colocar as próximas secções:

## 6. Information Retrieval

Information Retrieval [X1] is the process of finding and extracting relevant information from large collections of naturally unstructured data, such as texts. This extraction is based on documents, which are the result of restructuring the initial data, and the output is sorted by relevance, becoming the main challenge.

In this section presents the indexing and query methods used in this information retrieval system powered by previously constructed documents.

The implementation of the search system is based on Apache Solr [X2]. It is an open-source tool that offers various features relevant to the project's purpose, including distributed and fast indexing, scalability, and advanced search capabilities surpassing a full-text match.

## 6.1 Document Characterization

The documents to be indexed and searched in the system are those resulting from the processes of data extraction, enrichment, and aggregation in the pipeline described above. 

Therefore, a hotel is a document consisting of a name, average rating, location, and has a set of associated reviews. These reviews have their corresponding date, the assigned rating, and the user's comment about the hotel.

## 6.2 Indexing Process

Indexing serves as a fundamental step in Information Retrieval, optimizing search efficiency by organizing the data. It involves creating a structured index that significantly enhances both search speed and scalability. Without proper indexing, search systems would face challenges, resulting in slower response times and increased computational overhead.

In Solr, various types of indexing exist for document fields and associated queries, based on a Tokenizer [X3] and Filters [X4]. While Tokenizers create a token stream from the original string following a predefined rule, Filters transform these tokens for consistency in subsequent searches and matches.

In this specific case, the focus was primarily on indexing textual fields, as they provide the most context and information for searches. Conversely, given the project's context, it is not expected to search for specific dates or review ratings. Therefore, these latter two document fields were not indexed.

Textual fields were indexed by instantiating a new data type. The `boosted_text` index analyzer includes:

- `StandardTokenizerFactory` tokenizer: splits texts based on punctuation and spaces;
- `ASCIIFoldingFilterFactory` filter: handles special characters and accents, converting them to their equivalent ASCII form;
- `LowerCaseFilterFactory` filter, converts all characters to their lowercase counterparts;
- `SynonymGraphFilterFactory` filter, expands each token to include variations based on its synonyms;
- `EnglishMinimalStemFilterFactory` filter, reduces each token to its root form, facilitating the search for variations of specific terms;

Fields with native values were defined using Solr's default types. The English language was chosen for both stem assignment and synonym generation, aligning with the language of the manipulated data.

The `SynonymGraphFilterFactory` is crucial in this context. Since the search is conducted based on reviews, which are inherently subjective, derived from natural language and rich in adjectives, it is important not to rely on specific terms but rather to match synonyms of terms.

The same structure was used for the query analyzer. Thus, the indexing of the final document can be characterized by the following schema:

| **Field**    | **Type**     | **Indexed?** |
|--------------|--------------|--------------|
| name         | boosted_text | yes          |
| location     | boosted_text | yes          |
| average_rate | pint         | yes          |
| date         | string       | no           |
| rate         | pint         | no           |
| text         | boosted_text | yes          |

[Table T1]: Schema Field Types

## 6.3 Retrieval Process and Setup

The approach implemented involves two schemas: schema_simple utilizes default field types for each field, while schema_boosted incorporates instantiated field types for enhanced search capabilities. For query parameters the simple schema uses the default defType, while the boosted schema employs defType=edismax with specific parameters for optimizing search engine results:

- __Query Field with Optional Boost (``qf``)__: This assigns weights to specific fields in the search
- __Phrase-Boosted Field (``pf``)__: Focuses on selecting more relevant terms from the query
- __Phrase Boost Slope (``ps``)__: Defines the maximum number of tokens between searched words

| **Parameter** | **value** |
|--------------|--------------|
| qf | text^7 name location^2 |
| pf | text^10 |
| ps | 3 |

Assigning diverse weights within the 'qf' parameter prioritizes the significance of the 'text' field, followed by 'location' and 'name.' In the 'pf' parameter, exclusive attention is given to the 'text' field, serving as a dedicated phrase boost. This is complemented by the 'ps' parameter set to 3, a value determined through meticulous testing.

## 7. Evaluation

A avaliação é também uma das partes fundamentais da Information Retrieval e depende do target de coleção de documentos do tipo de informação necessária. É importante para entender os possíveis usos dos sistemas por parte dos utilizadores e definir novos designs e implementações com base no feedback recebido.

Neste caso em concreto, a avaliação foi efetuada sob o ponto de vista da eficácia, a habilidade do sistema em encontrar a informação certa, em vez da eficiência, a habilidade do sistema encontrar informação rapidamente. 

Como individual e subjective metrics podem provocar um bias na avaliação dos dois sistemas anteriormente instanciados, recorremos a um conjunto de métricas distintas baseadas em `precision` and `recall`, como a `Precision at K (P@K)`, `Precision Recall curves` e `Mean Average Precision (MAP)`. Enquanto a precisão incide na percentagem do número de documentos realmente relevantes entre os extraídos, o recall faz essa comparação com base em todos os documentos relevantes dentro do sistema. Dado que neste caso existem mais de 2000 documentos únicos, o cálculo exato é inviável, pelo que se usou uma aproximação manual com base na extração e amostra dos primeiras dezenas de documentos retornados.

A `Precision at K (P@K)` é importante porque a precisão é o que define a satisfação da maioria dos utilizadores. De facto os utilizadores não requerem elevada recall, já que a percentagem de resultados relevantes dado todos os documentos importantes é quase sempre desconhecida, ao contrário da relevância dos primeiros documentos retornados. Assim, a precisão toma uma importante função. Optou-se por por ser um valor equilibrado e que vai ao encontro com a utilização normal de uma search engine:

- Fixar ranking baseado nos primeiros 20. Justificar que num search engine normal, Google, só os primeiros importam.
- Precision & Recal ignoram o ranking em si;

- `Precision Recall Curves`: Para cada subconjunto de documentos rankeados retornados, e para cada sequência de documentos nesse subconjunto, calcular valores de (recall, precision) para desenhar a curva.
- `Mean Average Precision (MAP)`: É uma das mais comuns medidas usadas em IR. Trata-se da média de Average Precision dos vários conjuntos retornados, calculados para K documentos rankeados e úteis.

### Q1

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

Query: Best hotels near center of london
Justificação: In this we intend to search for the hotels near the center of London with the best ratings. As our dataset doesnt have many entries with London location we set location to United Kingdom and search for the keywords center London in the review text. The results are sorted by descending rate.
Words: London Center
Location: United Kingdom
Ops: London AND London Eye

### Q2

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

Query: Hotels with good breakfast or great room service in new delhy<br>

Q3
Justificação: <br>
Words: good breakfast great room service <br>
Ops: good breakfast OR great room service <br>

### Q3

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

Query: Good accessibility for handicapped people that are also well-served in public transportation options
Justification:
Words: good accessibility handicapped public transportation
Ops: good accessibility handicapped AND public transportation

### Q4

Necessidade de informação:
Relevance Judgement:
Q:

Tabela com rank (AvP, P@20), e valores para cada System.
Gráfico R-C para cada System.
Interpretações, justificações.

Query: Vegetarian or vegan options in restaurant hotel around London
Justification:
Words: Vegetarian ORvegan options restaurant hotel london

Global:
- evaluate the results obtained for the defined information needs.

## 8. Conclusions and Future work

Tirar ideias do M1:

In conclusion of this milestone, all the planned tasks within the data preparation phase of the project have been successfully completed. This accomplishment marks a crucial turning point in the process of creating a useful hotel search engine that will give tourists useful information and help them make informed choices.

One of the most challenging aspects of the work was developing effective strategies to address the issue of an excessive number of reviews. Substantial effort was invested in determining the best approach to manage and utilize this abundance of information. Through meticulous analysis and innovative methods, a balance was struck between data volume and relevance, ensuring that the dataset remained rich with insights while maintaining a manageable size.

As the project progresses, there are always opportunities for further enhancements and refinements. With the cleansed and consolidated dataset, the next phase of the project will focus on the development of a robust hotel search engine. This engine will allow travelers to explore and filter accommodations according to their preferences, whether related to location, room quality, staff service, or other factors identified during the analysis phase.

Notas:

Concluir acerca da consistência global do search engine / system.
Adaptar do M1 e explorar possibilidade do M2:
- Melhorar o parâmetro X e Y, e justificação teórica
- work on user interfaces by developing a frontend for the search system, including specific features such as snippet generation, results clustering
- sentimental and context analysis, muito importante já que a nossa fonte de informação principal são reviews, logo são subjectivas;
- parsing segundo stopwords das queries do utilizador;

- __Stop Filter__, this filter discards, or stops analysis of, tokens that are on the given stop words list. A standard stop words list is included in the Solr conf directory, named stopwords.txt, which is appropriate for typical English language text.
    - We dont have stopwords.txt generated.

## References

Todos os anteriores mais (TODO: colocar data de acesso):

- [X1] - [Information Retrieval](https://en.wikipedia.org/wiki/Information_retrieval)
- [X2] - [Apache Solr](https://solr.apache.org/guide/6_6/introduction-to-solr-indexing.html)
- [X3] - [Solr Tokenizers](https://solr.apache.org/guide/solr/latest/indexing-guide/tokenizers.html)
- [X4] - [Sorl Filters](https://solr.apache.org/guide/solr/latest/indexing-guide/filters.html)
- [X5] - [eDismax](https://solr.apache.org/guide/7_7/the-extended-dismax-query-parser.html)