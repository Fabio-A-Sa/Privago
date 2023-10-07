# Milestone 1 - Report

### Title

### Name, surname, location, email de cada um

## Abstract

The exponential growth of data on the internet necessitates effective mechanisms to harness and connect this vast information resource. Our project addresses this need by focusing on the hotel industry, where reviews play a crucial role in shaping consumer choices. In this document, we present a comprehensive overview of our project, "__" Through this document, we aim to provide a clear and well-documented account of our work in the context of creating a powerful search engine for hotels and their reviews. To achieve this, we collect data from various datasets, perform data cleaning and preparation, and conduct in-depth data analysis.

#### CSS Concepts

- Information systems
- Information retrieval

#### Keywords

Hotels, Reviews, Information, Dataset, Data Retrieval, Data Preparation, Data Analysis, Data Processing, Data Refinement, Pipeline, Domain Conceptual Model.

## 1 - Introduction

This paper is developed as part of the course "Information Processing and Retrieval" (PRI) within the first year of the Master's in Informatics and Computing Engineering (MEIC) at the Faculty of Engineering of the University of Porto (FEUP).

The choice of the hotel reviews theme is motivated by its significant relevance and the rich diversity of attributes it encompasses. Hotel reviews, as a research focus, hold substantial importance in the modern information landscape. They not only provide valuable insights into the hospitality industry but also serve as a prime example of data diversity, combining numerical ratings, submission dates, and personal, subjective narratives. This diversity introduces intricacies in data structuring and presents challenges in contextual search, making it an ideal choice for aligning the search system with real-world scenarios. Thus, this theme strongly resonates with the course objectives, emphasizing practical applicability and the development of robust information retrieval solutions.

This document is structured into several major sections, each tailored to fulfill the objectives of Milestone 1. We commence with `Data Extraction and Enrichment`," where we introduce the data sources, briefly characterize the datasets, and assess data quality. Subsequently, `Data Preparation` outlines the selection criteria, processing methods, and data storage procedures for hotel-related information and associated reviews, following a clear and reproducible pipeline.

In `Data Characterization` we delve into the evaluation and visualization of the refined data. This involves examining various criteria and relationships, from the Domain Conceptual Model to Word Clouds. Finally, `Possible Search Tasks` and `Conclusions and Future Work` provide an overarching interpretation of the results, guiding the identification of suitable research objectives for the project's next phase.

## 2 - Data Extraction and Enrichment

After conducting research for relevant data in terms of variety and quantity, four datasets from different regions were selected through the Kaggle platform [1]. Table 1 provides a characterization of the acquired datasets:

Dataset | Features | Hotels | Reviews | Size (MBs)
Datafiniti's Hotel Reviews | 26 | 1400 | 10000 | 124.45
Hotel Review Insights | 7 | 570 | 7000 | 1.31
London Hotel Reviews | 6 | 20 | 27329 | 22.85
Europe Hotel Reviews | 17 | 1493 | 515000 | 238.15

Table 1: Initial datasets characterization 

O dataset Datafiniti's Hotel Reviews [2] foi retirado de Datafiniti's Business Database [3] através de sampling. Hotel Review Insights [4] é um compilado de algumas reviews de hotéis do mundo através de web-scrapping de reviews presentes em Booking.com [8]. London Hotel Reviews [5] é um sample retirado e parcialmente refinado de um dataset de DataStock [6]. Finalmente, Europe Hotel Reviews [7] também resulta de web scrapping de reviews de hoteis espalhados pela Europa publicados em Booking.com [8].

Todos os datasets têm "licença de utilização pública" (melhorar isto, procurar a definição correcta) e, segundo a plataforma Kaggle, um índice de usabilidade superior a 8.

The datasets contém features comuns, numerical data, such as rating, review date, and textual data, such a review text, hotel localisation and name. O último dataset contém dois parâmetros adicionais, positive review and negative review. As features enunciadas foram extraídas neste passo e refinadas em Data Preparation.

## 3 - Data Preparation

In this section, is presented the structured data preparation pipeline that was developed for the project. This pipeline encompasses various data cleaning and restructuring procedures aimed at achieving a clean, uniform, and ready-to-analyze dataset. The objective of this phase is to establish a solid foundation for meaningful analysis.

The data preparation process commenced with ``dataset cleaning``, primarily focusing on the removal of records containing empty or null values in any attribute. However, before proceeding further, a crucial task intervened in this phase. It involved establishing a ``standardized naming`` convention to address variations in hotel names, such as "45 Park Lane - Dorchester Collection" and "45 Park Lane Dorchester Collection". This step was necessary to facilitate the addition of the feature "mean_hotel_rate" to each hotel entity.

Once the hotel name standardization was in place, we resumed the cleansing process by eliminating incomplete or ``uninformative data``, including strings with uninformative text. This comprehensive approach ensured that the dataset was thoroughly cleansed, setting a solid foundation for subsequent processing and analysis. 

(o parágrafo é demasiado genérico. que strings são influenciadas por este step? apenas a review_text, que é abordada só no terceiro parágrafo)

With the data cleaned, we turned our attention to ``attribute normalization``. Given the presence of diverse datasets with varying formats, we embarked on a comprehensive normalization process. This included standardizing attributes such as "positive_reviews" and "negative_reviews" into a unified "review_text" attribute for the 4th dataset as is demonstrated in the Pipeline Diagram [ref]. Additionally, date formats were normalized to ensure uniformity and suitability for analysis. Rating scales were also normalized to a common range and converted to floating-point values, facilitating comparative analysis.

(split data, first cleaning then normalization)
(comprehensive normalization, comprehensive approach, comprehensive -> repetições)
(date formats were normalized -> em que formato? os dias não foram considerados porque não são relevantes. essencialmente é a época que conta, não o dia específico)

To gain insights into the textual content, we calculated the ``word count`` for each review across all datasets. This analysis was facilitated using the Pandas [ref] tool, allowing us to extract valuable information such as quartile ranges and make informed decisions during the review deletion phase. It helped us identify and handle reviews with either very few words or an excessively high word count. With this step completed, we were finally able to merge all the datasets into a single, consolidated dataset, streamlining the remaining preparation tasks.

(utilização de quartis. mas como? 25 até 75)
(porque é que não fizemos os quartis com all.json? porque cada dataset tem a sua própria média. se fossem juntos teríamos muitos dados do 4, p.e, e poucos dos outros)

After completing the aforementioned steps, we proceeded to determine the minimum and maximum number of ``reviews per hotel`` that we aimed to retain. To accomplish this, we employed the same approach used for analyzing the number of words per review, utilizing the Pandas [ref] `.describe()` function. This statistical analysis provided crucial insights into the distribution of reviews across hotels.

(antes deste passo é importante dizer do merge. só depois o reviews_per_hotel. porquê do merge antes deste passo? a ideia é que nenhum hotel sobressaia mais do que os outros apenas por ter muito mais. enviesava os resultados.)

We first addressed hotels with fewer reviews, removing those that fell below the established minimum threshold from our dataset. This step ensured that our dataset focused on hotels with a sufficient volume of reviews to provide meaningful insights.

Next, we turned our attention to hotels with an excessive number of reviews. To manage this situation, we implemented a strategy that allowed us to select and retain reviews while preserving the proportion of reviews per rating category for each specific hotel. This approach ensured that we maintained a balanced between the 'mean_hotel_rate' and the rate of the selected reviews.

(next: final dataset with normalized documents. justify document structure - avoiding redundancy...)

Figure 1: Data preparation pipeline

## 4 - Data Characterization

brief explanation

### 4.1 - Data Domain Conceptual Model

### 4.2 - Word Cloud

### 4.3 - Plot das locations

escolher os X mais frequentes e excluir os otros. fix no que está no github

### 4.4 - Frequência de reviews por "ano" ou "mes"

## 5 - Possible search tasks

dizer que foi baseado na word cloud e nas coisas normais de um hotel. ver introdução.

## 6 - Conclusions and Future work

## References

- [1] - [Kaggle](https://www.kaggle.com)
- [2] - [Datafiniti's Hotel Reviews](https://www.kaggle.com/datasets/datafiniti/hotel-reviews)
- [3] - [Datafiniti's Business Database](https://www.datafiniti.co)
- [4] - [Hotel Review Insights](https://www.kaggle.com/datasets/juhibhojani/hotel-reviews)
- [5] - [London Hotel Reviews](https://www.kaggle.com/datasets/PromptCloudHQ/reviews-of-londonbased-hotels)
- [6] - [DataStock](https://datastock.shop)
- [7] - [Europe Hotel Reviews](https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe)
- [8] - [Booking](https://www.booking.com)

- talvez as bibliotecas em requirements.txt, ver se nos 4 exemplos tem isso