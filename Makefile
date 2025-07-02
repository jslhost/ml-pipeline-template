SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: model evaluations

model: model.pkl

data:
	mkdir data

data/raw_dataset.csv: | data
	python load_data.py

data/clean_dataset.csv: data/raw_dataset.csv
	python clean_data.py

data/preprocessed_features.npz: data/clean_dataset.csv
	python preprocess_data.py

model.pkl: data/preprocessed_features.npz
	python training.py

evaluations: model.pkl 
	mkdir -p reports
	python evaluate.py