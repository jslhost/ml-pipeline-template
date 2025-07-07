SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean model evaluations tests help

all: evaluations

# ======================================================================================================================
# Aide
# ======================================================================================================================

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all                  Run the entire pipeline and generate evaluations."
	@echo "  data/raw_dataset.csv Generate the raw dataset."
	@echo "  data/clean_dataset.csv Clean the raw dataset."
	@echo "  data/preprocessed_features.npz Preprocess the cleaned data."
	@echo "  model                Train the machine learning model."
	@echo "  evaluations          Evaluate the model and generate reports."
	@echo "  tests                Run tests."
	@echo "  clean                Remove generated files."
	@echo ""

# ======================================================================================================================
# Données
# ======================================================================================================================

model: model.pkl

data:
	mkdir data

data/raw_dataset.csv: | data
	PYTHONPATH=. python src/load_data.py

data/clean_dataset.csv: data/raw_dataset.csv
	PYTHONPATH=. python src/clean_data.py

data/preprocessed_features.npz: data/clean_dataset.csv
	PYTHONPATH=. python src/preprocess_data.py

# ======================================================================================================================
# Modèle
# ======================================================================================================================

model.pkl: data/preprocessed_features.npz
	PYTHONPATH=. python src/training.py

# ======================================================================================================================
# Évaluation
# ======================================================================================================================

evaluations: model.pkl
	mkdir -p reports
	PYTHONPATH=. python src/evaluate.py

# ======================================================================================================================
# Tests et Nettoyage
# ======================================================================================================================

tests:
	PYTHONPATH=. pytest

clean:
	rm -rf data model.pkl  preprocessor.pkl reports
