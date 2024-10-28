SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: model predictions

model: model.pkl

data:
	mkdir data

data/raw_dataset.csv: data
	python3 load_data.py

data/clean_dataset.csv: data/raw_dataset.csv
	python3 clean_data.py

data/preprocessed_features.npz: data/clean_dataset.csv
	python3 preprocess_data.py

model.pkl: data/preprocessed_features.npz
	python3 training.py

predictions: model.pkl
	python3 predict.py