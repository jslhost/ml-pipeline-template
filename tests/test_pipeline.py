import pandas as pd
from scipy import sparse
import pytest
import os

from src.load_data import load_data
from src.clean_data import clean_data
from src.preprocess_data import preprocess_data
from src.training import training
from src.evaluate import evaluate
from src.utils import load_params

# Load parameters once for all tests
params = load_params()

@pytest.fixture
def setup_data_paths(tmp_path):
    """Fixture to set up temporary data paths based on params.yaml."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    # Override params with temporary paths for testing
    test_params = params.copy()
    test_params["data"]["raw_dataset_path"] = str(data_dir / os.path.basename(params["data"]["raw_dataset_path"]))
    test_params["data"]["clean_dataset_path"] = str(data_dir / os.path.basename(params["data"]["clean_dataset_path"]))
    test_params["data"]["preprocessed_features_path"] = str(data_dir / os.path.basename(params["data"]["preprocessed_features_path"]))
    test_params["model"]["path"] = str(tmp_path / os.path.basename(params["model"]["path"]))
    test_params["reports"]["dir"] = str(reports_dir)
    test_params["reports"]["classification_report_path"] = str(reports_dir / os.path.basename(params["reports"]["classification_report_path"]))
    test_params["reports"]["confusion_matrix_path"] = str(reports_dir / os.path.basename(params["reports"]["confusion_matrix_path"]))

    # For load_data, we need to point to the sample_data.csv for the source
    # This is a special case for testing, as load_data usually fetches from URL
    # We will simulate the raw data being loaded from sample_data.csv
    sample_data_path = "tests/sample_data.csv"
    pd.read_csv(sample_data_path).to_csv(test_params["data"]["raw_dataset_path"], index=False)

    return test_params

def test_pipeline_steps(setup_data_paths):
    """Test the entire pipeline using the temporary paths."""
    test_params = setup_data_paths

    # Clean data
    clean_data(test_params)
    clean_dataset_path = test_params["data"]["clean_dataset_path"]
    assert os.path.exists(clean_dataset_path), "Clean dataset should be created"
    df_clean = pd.read_csv(clean_dataset_path)
    assert not df_clean.empty, "Clean dataset should not be empty"
    for col in test_params["data"]["columns_to_drop"]:
        assert col not in df_clean.columns, f"{col} should be dropped"

    # Preprocess data
    preprocess_data(test_params)
    preprocessed_features_path = test_params["data"]["preprocessed_features_path"]
    assert os.path.exists(preprocessed_features_path), "Preprocessed features should be created"
    X = sparse.load_npz(preprocessed_features_path)
    assert X.shape[0] == len(df_clean), "Number of samples mismatch after preprocessing"

    # Training
    training(test_params)
    model_path = test_params["model"]["path"]
    assert os.path.exists(model_path), "Model should be trained and saved"

    # Evaluate
    evaluate(test_params)
    report_path = test_params["reports"]["classification_report_path"]
    matrix_path = test_params["reports"]["confusion_matrix_path"]
    assert os.path.exists(report_path), "Classification report should be generated"
    assert os.path.exists(matrix_path), "Confusion matrix should be generated"