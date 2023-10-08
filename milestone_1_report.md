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

The data preparation process began with a comprehensive cleaning phase, where we focused on the removal of records containing ``empty or null values`` in any attribute. Simultaneously, we identified and eliminated incomplete or uninformative data, including strings with ``uninformative text``, such as "no comments available for this review.". This combined cleaning step ensured that the dataset was thoroughly cleansed.

With the data cleaned, we turned our attention to ``attribute normalization``. Given the presence of diverse datasets with varying formats, we embarked on a comprehensive normalization process. This included standardizing attributes such as ``"positive_reviews"`` and ``"negative_reviews"`` into a unified "review_text" attribute for the 4th dataset as is demonstrated in the Pipeline Diagram [ref]. Additionally, ``date formats`` were normalized to ensure uniformity and suitability for analysis. The date format was set as "month-year" due to the absence of day-specific review information in the second dataset. ``Rating scales`` were also normalized to a common range and converted to floating-point values, facilitating comparative analysis ([0.0, 5.0]).

In addiction, was established a ``standardized naming`` convention to address variations in ``hotel names``, such as "45 Park Lane - Dorchester Collection" and "45 Park Lane Dorchester Collection". This step was necessary to facilitate the addition of the feature "average_rate" to each hotel entity, referenced below. ``Location standardization`` involved reducing location names to their last two words, resulting in a format comprising capital and country names.

To gain insights into the textual content, we calculated the ``word count`` for each review across all datasets. This analysis was facilitated using the Pandas [ref] tool, allowing us to extract valuable information such as quartile ranges and make informed decisions during the review deletion phase. This process enabled us to identify and manage reviews with either an insufficient word count or an excessively high word count. We achieved this by removing reviews falling below the 25% threshold (first quartile) and those exceeding the 75% threshold (fourth quartile). This step was done separately for each dataset, due to the discrepation of each average word counting [ref].

At this state, we were finally able to merge all the datasets into a single, consolidated dataset, streamlining the remaining preparation tasks, beginning with the computation of the ``average rate`` for each unique hotel. This might be helpful for searching criterias for the futures milestones.

After completing the aforementioned steps, we proceeded to determine the minimum and maximum number of ``reviews per hotel`` that we aimed to retain. To accomplish this, we employed the same approach used for analyzing the number of words per review, utilizing the Pandas [ref] `.describe()` function. This statistical analysis provided crucial insights into the distribution of reviews across hotels.

We first addressed hotels with fewer reviews, removing those that fell below the established minimum threshold from our dataset. This step ensured that our dataset focused on hotels with a sufficient volume of reviews to provide meaningful insights.

Next, we turned our attention to hotels with an excessive number of reviews. To manage this situation, we implemented a strategy that allowed us to select and retain reviews while preserving the proportion of reviews per rating category for each specific hotel. This approach ensured that we maintained a balanced between the 'average_rate' and the rate of the selected reviews.

The final step in the data preparation phase involved organizing the data into the ``desired JSON file format``, which was designed based on our UML diagram[ref] and with a focus on the primary objective of our search tool. This format consisted of a collection of JSON objects, each representing a "Hotel" entity. Within each "Hotel" object, we included not only its associated attributes but also the related reviews, presented as JSON objects themselves.

Figure 1: Data preparation pipeline

## 4 - Data Characterization

### 4.1 - Data Domain Conceptual Model

### 4.2 - Reviews Word Cloud

### 4.3 - Hotel location distribution

escolher as 20 locations mais frequentes e excluir os outros. fix no que está no github. Se 20 for muito (o gráfico ficar muito partido), reduzir para 10.

### 4.4 - Average rating distribution

X = Ranges de 0 a 5, ints.
Y = # de hoteis com esse average_rating
verificar que tendencialmente os hotéis tem boas reviews && verificar que o pessoal é extremo (ou dá muito boa, ou dá muito má).

## 5 - Possible search tasks

In our data analysis journey, we uncovered valuable insights through the use of a word cloud diagram. This visual representation highlighted the most frequently occurring words in hotel reviews, shedding light on what matters most to travelers. Among these words, some stood out as pivotal in understanding the key factors that influence hotel choice and guest satisfaction.

``"Location"`` emerged as one of the top considerations in travelers' decision-making processes. Whether it's proximity to local attractions, accessibility to transportation hubs, or the overall neighborhood ambiance, the location of a hotel can greatly influence the overall travel experience. Queries like ``"best hotels in [City/Region/Country]"`` and "near the airport" can help travelers pinpoint accommodations that align with their preferred locations and provide convenient access to their destinations.

For many travelers, a good breakfast is an integral part of their stay. The word ``"breakfast"`` featured prominently in our word cloud, suggesting a keen interest in this aspect. Whether it's a hearty breakfast buffet or specialty morning treats, travelers seek accommodations that cater to their breakfast preferences. Queries like "Hotels with breakfast/good breakfast" can assist those who prioritize morning meals.

The words "staff" and "service" were significant contributors. This emphasizes the critical role that hotel staff play in the overall guest experience. From warm welcomes at the reception desk to prompt and efficient room service, exceptional staff service can elevate a stay. Queries about ``"staff service"`` and ``"room service"`` quality could be instrumental in identifying hotels that excel in providing exceptional service to their guests.

Another one of the foremost considerations in hotel selection is the quality of the room and its amenities. Words like "room," "bed," and "bathroom" featured prominently in our word cloud, underscoring the importance of these aspects to travelers. Queries related to "room"/"bed" quality or "bathroom" sanitation can guide travelers to accommodations that prioritize comfort and cleanliness.

## 6 - Conclusions and Future work

In concluding of this milestone, we're pleased to report that we've successfully completed all the planned tasks within the data preparation phase of our project. This achievement marks a significant milestone in our journey towards developing an effective hotel search engine, capable of providing travelers with valuable insights and assisting them in making informed decisions.

One of the most challenging aspects of our work was devising effective strategies to address the issue of an excessive number of reviews. The sheer volume of feedback available posed a unique challenge, and we invested significant effort in determining the best approach to manage and utilize this wealth of information. Through careful analysis and innovative methods, we were able to strike a balance between data volume and relevance, ensuring that our dataset remained rich with insights while maintaining a manageable size.

As we move forward, there are exciting opportunities for further enhancements and refinements in our project. 

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