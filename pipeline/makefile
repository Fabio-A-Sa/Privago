all: clean requirements collect normalize merge process analyze

clean:
	rm -rf ../data/processed ../data/statistics

requirements:
	pip3 install -r requirements.txt

collect:
	mkdir -p ../data/processed
	python3 data_collect.py

normalize:
	python3 data_normalize.py

merge:
	python3 data_merge.py

process:
	

analyze:
