all: requirements query evaluation

requirements:
	pip3 install -r requirements.txt

query:	
	python3 ../solr/synonyms.py
	python3 ../solr/stopwords.py
	python3 query.py

evaluation:
	python3 evaluation.py > stats.json