# PRI Report Milestone 1 (Draft)

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

<TODO: table>
- Index 1..4
- Name [ref]
- Number of features / columns
- Number of distinct hotels 
- Number of reviews / lines
- Size (MBs)

Table 1: <TODO: label>

O dataset Datafiniti's Hotel Reviews [2] é um sample retirado de Datafiniti's Business Database [3]. Hotel Review Insights [4] é um 

Todos os datasets têm "licença de utilização pública" (melhorar isto, procurar a definição correcta) e, segundo a plataforma Kaggle, um índice de usabilidade superior a 8.

The datasets has both numerical data, such as rating, review date, and textual data, such a review text, hotel localisation and name. O último dataset contém um. As features comuns enunciadas foram extraídas neste passo e refinadas em Data Preparation.

## 3 - Data Preparation

Apresentação da pipeline

Dividir em vários subtópicos

Adicionar figura da pipeline

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
- [4] - [](https://www.kaggle.com/datasets/juhibhojani/hotel-reviews)
- [5] - []()
- [6] - []()
- talvez as bibliotecas em requirements.txt, ver se nos 4 exemplos tem isso