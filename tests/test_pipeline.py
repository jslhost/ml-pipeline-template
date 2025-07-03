import os
from pathlib import Path

import pandas as pd
from scipy import sparse

from load_data import load_data
from clean_data import clean_data
from preprocess_data import preprocess_data
from training import training
from evaluate import evaluate


def test_load_and_clean(tmp_path):
    # setup temporary data folder
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    raw_path = data_dir / "raw.csv"
    clean_path = data_dir / "clean.csv"

    load_data(src="tests/sample_data.csv", dest=raw_path)
    assert raw_path.exists(), "Raw dataset should be created"

    df_raw = pd.read_csv(raw_path)
    assert not df_raw.empty, "Raw dataset should not be empty"

    clean_data(src=raw_path, dest=clean_path)
    df_clean = pd.read_csv(clean_path)

    assert "RowNumber" not in df_clean.columns
    assert "CustomerId" not in df_clean.columns
    assert len(df_clean) == len(df_raw)


def test_preprocess(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    clean_path = data_dir / "clean.csv"
    features_path = data_dir / "feat.npz"

    # prepare clean data
    df = pd.read_csv("tests/sample_data.csv")
    df.drop(["RowNumber", "CustomerId"], axis=1).to_csv(clean_path, index=False)

    preprocess_data(src=clean_path, dest=features_path)
    assert features_path.exists()

    X = sparse.load_npz(features_path)
    assert X.shape[0] == len(df)


def test_training_and_evaluate(tmp_path):
    data_dir = tmp_path / "data"
    report_dir = tmp_path / "reports"
    data_dir.mkdir()
    report_dir.mkdir()
    clean_path = data_dir / "clean.csv"
    features_path = data_dir / "feat.npz"
    model_path = tmp_path / "model.pkl"
    report_path = report_dir / "report.txt"
    matrix_path = report_dir / "matrix.png"

    df = pd.read_csv("tests/sample_data.csv")
    df.drop(["RowNumber", "CustomerId"], axis=1).to_csv(clean_path, index=False)
    preprocess_data(src=clean_path, dest=features_path)

    training(data_csv=clean_path, features_file=features_path, model_path=model_path)
    assert model_path.exists()

    evaluate(
        data_csv=clean_path,
        features_file=features_path,
        model_path=model_path,
        report_path=report_path,
        matrix_path=matrix_path,
    )

    assert report_path.exists()
    assert matrix_path.exists()

