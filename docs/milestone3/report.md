# Milestone 3 - Report

## Privago

#### André Ávila, Porto, up202006767@up.pt
#### André Costa, Porto, up201905916@up.pt
#### Fábio Morais, Porto, up202008052@up.pt
#### Fábio Sá, Porto, up202007658@up.pt

## TODO

- Colocar em anexos uma tabela com Q,I,Hotel,Bool para o professor conseguir investigar a veracidade da relevância de cada query feita neste M3;
- Melhorar o report anterior segundo a Milestone 2 feedback;
- Eliminar a secção 8 e colocar as seguintes:

## 8. Information Retrieval Improvements

Introdução. Falar que os sinónimos e tokens simples da etapa anterior não resolvem alguns problemas.

### A. Stop Words

- The `Stop Words` [X7] filter can be applied to `boosted_text` to reduce sensitivity to common words;

### B. 

- `Sentimental and contextual analysis` is relevant, given that the main source of information for the system is reviews, which inherently carry subjective connotations;

### C. Learning To Rank

Pensar neste improvement.

### D. More Like This

Pensar neste improvement.

## 9. User Interface

Introdução. Motivo, não só pelo Solr ser horrível. Talvez imagens só nos anexos.

## 10. Conclusions and Future Work

(modificar, este é o de M2)

In conclusion of this milestone, all the planned tasks within the Information Retrieval phase of the project have been successfully completed. This accomplishment marks a crucial turning point in the process of creating a useful hotel search engine that aids tourists in making informed choices.

One of the most challenging aspects of the work involved developing effective strategies for dealing with nested documents, as well as their indexing and retrieval. Solr lacks documentation and concrete examples supporting the addressed document format.

Through the evaluation of the search engine, the system's stability and capability to handle different information needs within the chosen context have been verified. As the project progresses, opportunities for further enhancements and refinements emerge. Analyzing the results obtained from the first prototype of the hotel's information retrieval system:

- The `Stop Words` [X7] filter can be applied to `boosted_text` to reduce sensitivity to common words;
- `Sentimental and contextual analysis` is relevant, given that the main source of information for the system is reviews, which inherently carry subjective connotations;

In the next phase, work will be done on user interfaces by developing a frontend for the search system, incorporating specific features like snippet generation and results clustering. This engine will enable travelers to explore and filter accommodations based on preferences, such as location, room quality, staff service, or other factors identified during the analysis phase.

## References

Todos os anteriores mais:

- 