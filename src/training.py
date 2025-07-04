import pandas as pd
from scipy import sparse
from pickle import dump

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from src.utils import load_params


def training(params: dict):
    """Train a SVC model and save it to ``model_path``."""
    data_csv = params["data"]["clean_dataset_path"]
    features_file = params["data"]["preprocessed_features_path"]
    model_path = params["model"]["path"]
    target_column = params["base"]["target_column"]
    test_size = params["base"]["test_size"]
    random_state = params["base"]["random_state"]

    df = pd.read_csv(data_csv)
    y = df[target_column]
    X = sparse.load_npz(features_file)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    svc = SVC()

    svc.fit(X_train, y_train)

    with open(model_path, "wb") as f:
        dump(svc, f, protocol=5)


if __name__ == "__main__":
    params = load_params()
    training(params)
