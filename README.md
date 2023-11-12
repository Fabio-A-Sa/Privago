# PRI Project

### Run pipeline

```bash
cd pipeline/
make
```

### Run solr

```
cd solr
bash startup-(boosted|simple).sh
```

And open [`localhost:8983`](http://localhost:8983).

### Run queries

```
cd evaluation
make query [N]
```

### Run evaluation

```
cd evaluation
make evaluation [N]
```

## Data

### Data Domain Model

![UML](./imgs/UML.png)

### Word Cloud

![Reviews WordCloud](./imgs/reviews_wordcloud.png)

### Location distribution

![Locations Distribution](./imgs/location_distribution_v2.png)

### Average review rating distribution

![Average Review Rating Distribution](./imgs/rating_distributions.png)

### Reviews distribution by year

![Reviews distribution by year](./imgs/date_distributions.png)

### Reviews distribution by month - year 2016

![Reviews distribution by year](./imgs/date_distributions_2016.png)