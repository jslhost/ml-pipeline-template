import pandas as pd
from scipy import sparse
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os

from src.utils import load_params


def get_next_version_path(path: str) -> str:
    """
    Finds the next available versioned path for a file.
    Example: 'reports/file.txt' -> 'reports/file-1.txt' if 'file.txt' exists.
    """
    if not os.path.exists(path):
        return path

    base, ext = os.path.splitext(path)
    version = 1
    while True:
        new_path = f"{base}-{version}{ext}"
        if not os.path.exists(new_path):
            return new_path
        version += 1


def evaluate(params: dict):
    """Evaluate the trained model and save evaluation artefacts."""
    data_csv = params["data"]["clean_dataset_path"]
    features_file = params["data"]["preprocessed_features_path"]
    model_path = params["model"]["path"]
    report_path = params["reports"]["classification_report_path"]
    matrix_path = params["reports"]["confusion_matrix_path"]
    target_column = params["base"]["target_column"]
    test_size = params["base"]["test_size"]
    random_state = params["base"]["random_state"]
    reports_dir = params["reports"]["dir"]

    df = pd.read_csv(data_csv)
    y = df[target_column]
    X = sparse.load_npz(features_file)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    with open(model_path, "rb") as f:
        svc = load(f)

    y_test_pred = svc.predict(X_test)

    clf_report = classification_report(y_test, y_test_pred)

    cm = confusion_matrix(y_test, y_test_pred, labels=svc.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=svc.classes_)

    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Get versioned paths for report and matrix
    versioned_report_path = get_next_version_path(report_path)
    versioned_matrix_path = get_next_version_path(matrix_path)

    # Save artifacts
    with open(versioned_report_path, "w") as f:
        f.write(clf_report)

    disp.plot()
    plt.savefig(versioned_matrix_path)
    plt.close()

    print(f"Rapport sauvegardé dans {versioned_report_path}")
    print(f"Matrice de confusion sauvegardée dans {versioned_matrix_path}")


if __name__ == "__main__":
    params = load_params()
    evaluate(params)
