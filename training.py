import pandas as pd
from scipy import sparse
from pickle import dump

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def training(
    data_csv: str = "data/clean_dataset.csv",
    features_file: str = "data/preprocessed_features.npz",
    model_path: str = "model.pkl",
):
    """Train a SVC model and save it to ``model_path``."""

    df = pd.read_csv(data_csv)
    y = df["Exited"]
    X = sparse.load_npz(features_file)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    svc = SVC()

    svc.fit(X_train, y_train)

    with open(model_path, "wb") as f:
        dump(svc, f, protocol=5)


if __name__ == "__main__":
    training()
