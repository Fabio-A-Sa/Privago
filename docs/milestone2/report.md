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

This section presents the indexing and query methods used in this information retrieval system powered by previously constructed documents. 

The implementation of the search system is based on Apache Solr [X2], an open-source tool that offers various features relevant to the project's purpose, including distributed and fast indexing, scalability, and advanced search capabilities surpassing a full-text match.

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

Assigning diverse weights within the 'qf' parameter prioritizes the significance of the 'text' field, being our main field of search, followed by 'location' and 'name.' In the 'pf' parameter, exclusive attention is given to the 'text' field, serving as a dedicated phrase boost. This is complemented by the 'ps' parameter set to 3, a value determined through some analysis of the results of our queries.

Being consistent with this boosted approach to every query has enhanced the system's query handling, leading to improvements in search results, as elaborated in the subsequent section.

## 7. Evaluation

Evaluation is also a fundamental aspect of Information Retrieval, contingent on the target document collection and the type of information required. Understanding potential user scenarios is crucial for defining new designs and implementations based on received feedback. In this specific case, the evaluation was conducted from the perspective of effectiveness — the system's ability to find the right information — rather than efficiency, which pertains to the system's speed in retrieving information.

The use of individual and subjective metrics can introduce bias in evaluating the two previously instantiated systems. To address this, a set of distinct metrics based on `precision` and `recall`, such as `Average Precision (AvP)`, `Precision at K (P@K)`, `Precision-Recall curves`, and `Mean Average Precision (MAP)`, were employed. Precision focuses on the percentage of the number of truly relevant documents among those extracted, while recall makes this comparison based on all relevant documents within the system. Since there are more than 2000 unique documents in this case, precise calculation is impractical, leading to a manual approximation based on extracting and sampling the first twenty returned documents.

The `Average Precision (AvP)` is important because precision is what defines user satisfaction for the majority of users. In fact, users often do not require high recall since the percentage of relevant results given all important documents in the system is almost always unknown, unlike the relevance of the first returned documents. In `Precision at K (P@K)`, the choice was to evaluate the first twenty documents returned per query as it represents a balanced value aligning with typical usage patterns of a search engine.

The `Precision-Recall Curves` are constructed for each query and each system based on the subset of ranked documents returned. Ideally, a system is considered more stable the smoother its formed curve, and its performance is deemed better with a higher Precision-Recall Area Under the Curve [X6]. This metric encapsulates the overall effectiveness of the system in balancing precision and recall across thresholds.

The `Mean Average Precision (MAP)` is a common metric used in Information Retrieval and represents the average of Average Precision metric across various sets returned over the evaluation period. It helps determine if the system is consistent even when applied to different information needs.

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

Todos os anteriores mais:

- [X1] - [Information Retrieval](https://en.wikipedia.org/wiki/Information_retrieval), 2023/10/23
- [X2] - [Apache Solr](https://solr.apache.org/guide/6_6/introduction-to-solr-indexing.html), 2023/10/23
- [X3] - [Solr Tokenizers](https://solr.apache.org/guide/solr/latest/indexing-guide/tokenizers.html), 2023/11/02
- [X4] - [Sorl Filters](https://solr.apache.org/guide/solr/latest/indexing-guide/filters.html), 2023/11/02
- [X5] - [eDismax](https://solr.apache.org/guide/7_7/the-extended-dismax-query-parser.html), 2023/11/04
- [X6] - [Precision-Recall Area Under the Curve](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html), 2023/11/07