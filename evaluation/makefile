all: clean requirements query evaluation

clean:
	for i in {1..4}; do \
		for file_type in "schemaless" "boosted"; do \
			rm "./q$$i/result-$${file_type}.json"; \
		done; \
	done

requirements:
	pip3 install -r requirements.txt

query:
	python3 query.py

evaluation:
	python3 evaluation.py