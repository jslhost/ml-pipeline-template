SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: model evaluations

model: model.pkl

data:
	mkdir data

data/raw_dataset.csv: | data
	PYTHONPATH=. python src/load_data.py

data/clean_dataset.csv: data/raw_dataset.csv
	PYTHONPATH=. python src/clean_data.py

data/preprocessed_features.npz: data/clean_dataset.csv
	PYTHONPATH=. python src/preprocess_data.py

model.pkl: data/preprocessed_features.npz
	PYTHONPATH=. python src/training.py

evaluations: model.pkl 
	mkdir -p reports
	PYTHONPATH=. python src/evaluate.py