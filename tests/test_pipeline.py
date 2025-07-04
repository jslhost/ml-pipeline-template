import pandas as pd
from scipy import sparse
import pytest

from src.load_data import load_data
from src.clean_data import clean_data
from src.preprocess_data import preprocess_data
from src.training import training
from src.evaluate import evaluate


@pytest.fixture
def clean_csv(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    raw_path = data_dir / "raw.csv"
    clean_path = data_dir / "clean.csv"
    # Génère le raw.csv
    load_data(src="tests/sample_data.csv", dest=raw_path)
    # Nettoie le raw.csv
    clean_data(src=raw_path, dest=clean_path)
    return clean_path


def test_load_and_clean(clean_csv):
    df_clean = pd.read_csv(clean_csv)
    assert clean_csv.exists(), "Clean dataset should be created"

    assert not df_clean.empty, "Clean dataset should not be empty"

    assert "RowNumber" not in df_clean.columns
    assert "CustomerId" not in df_clean.columns


def test_preprocess(clean_csv, tmp_path):
    data_dir = tmp_path / "data"
    features_path = data_dir / "feat.npz"

    preprocess_data(src=clean_csv, dest=features_path)
    assert features_path.exists()

    X = sparse.load_npz(features_path)
    df = pd.read_csv(clean_csv)
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
