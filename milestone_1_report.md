# PRI Report Milestone 1 (Draft)

### Title

### Name, surname, location, email de cada um

## Abstract

Num século onde o turismo cresce exponencialmente, a qualidade dos hotéis disponíveis e a opinião dos anteriores hóspedes podem tornar-se fulcrais na escolha de um destino de férias. Há, portanto, necessidade de um sistema que seja capaz de agrupar várias reviews espalhados pelo mundo, filtrar os dados relevantes e pesquisar os melhores hotéis segundo determinadas exigências. O presente paper visa documentar todos os processos da criação de um information system que atende a essa necessidade, desde a data preparation, enrichement, analysis até ao retrieval.

#### CSS Concepts

- Information systems
- Information retrieval

#### Keywords

Hotels, reviews, information, retrieval, dataset, data, preparation, analysis, processing, refinement

## 1 - Introduction

Este paper é desenvolvido no âmbito da unidade curricular Processamento e Recuperação de Informação (PRI) do first year of the Master in Informatics and Computing Engineering (MEIC) da Faculdade de Engenharia da Universidade do Porto (FEUP).

A escolha do tema hotel reviews foi baseada em vários fatores. Por um lado, as reviews associadas a hotéis vêm geralmente acompanhadas de um rating numérico de range fixo, data de submissão e um texto de cariz pessoal e subjectivo. Estes atributos adicionam diversidade na estrutura dos dados manipulados e uma complexidade extra em pesquisas contextuais, tornando o search system mais próximo dos reais e mais relevante para o cumprimento dos objectivos da unidade curricular. Por outro lado, a indústria hoteleira possui elementos comuns e independentes da região ou país, como por exemplo a disposição de pequeno almoço, airport proximation, pet friendly e staff behaviour. Esta uniformidade, mesmo considerando a conotação subjectiva dos textos em análise, faz com que os hotéis sejam comparáveis.

O documento está organizado em X grandes secções que vão de encontro ao objectivo da Milestone 1. Numa fase inicial, em `Data Extraction and Enrichement` apresentam-se os datasources usados, há uma breve caracterização dos datasets e da qualidade dos mesmos. A seguinte secção, `Data Preparation`, detalha os critérios de seleção, processamento e storage das informações relevantes de hoteis e correspondentes reviews, seguindo uma pipeline bem definida e reproduzível. Em `Data Characterization` surge a avaliação e visualização dos dados já refinados através de vários critérios e relações, desde o Domain Conceptual Model a Word Cloud. Finalmente em `Possible search tasks` e `Conclusions and Future work` surge a interpretação global dos resultados, de modo a descobrir as necessidades de pesquisa adequadas à seguinte fase do projecto.

## 2 - Data Extraction and Enrichment

assess the authority of the data source and data quality;

The main dataset chosen contains the general information needed to
describe a book, gathered from Goodreads website. It was retrieved
from Goodreads 100k books, where the author retrieved the data
by scraping Goodreads website.
This dataset has both numerical data, such as the number of
pages, publish data, and textual data, such as the book description,
genres, etc

para enriquecer, fomos buscar a outros lados, ainda dentro do kaggle.

tabela com
location, n features, entradas, mbs, 

dizer que ficamos com as features comuns. dizer que no caso 4 os texts estão divididos. ficamos com os dois. futuramente vão ser juntados.

# 3 - Data Preparation

Apresentação da pipeline

Dividir em vários subtópicos

# 4 - Data Characterization

# 4.1 - Data Domain Conceptual Models

# 4.2 - Word Cloud

# 4.3 - Plot das locations

escolher os X mais frequentes e excluir os otros. fix no que está no github

# 4.4 - Frequência de reviews por "ano" ou "mes"

# 5 - Possible search tasks

# 6 - Conclusions and Future work

# References

kaggle1
kaggle2
kaggle3
kaggle4
talvez as bibliotecas em requirements.txt