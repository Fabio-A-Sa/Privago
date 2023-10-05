all: clean requirements collect normalize merge process analyze

clean:
	rm -rf ../data/processed
	rm -rf ../data/analysis
	rm -rf ../data/plots

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
	python3 data_process.py

analyze:
	mkdir -p ../data/analysis
	mkdir -p ../data/plots
	python3 data_analyze.py