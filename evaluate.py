import pandas as pd
from scipy import sparse
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def evaluate(
    data_csv: str = "data/clean_dataset.csv",
    features_file: str = "data/preprocessed_features.npz",
    model_path: str = "model.pkl",
    report_path: str = "reports/classification-report.txt",
    matrix_path: str = "reports/confusion-matrix.png",
):
    """Evaluate the trained model and save evaluation artefacts."""

    df = pd.read_csv(data_csv)
    y = df["Exited"]
    X = sparse.load_npz(features_file)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    with open(model_path, "rb") as f:
        svc = load(f)

    y_test_pred = svc.predict(X_test)

    clf_report = classification_report(y_test, y_test_pred)

    cm = confusion_matrix(y_test, y_test_pred, labels=svc.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=svc.classes_)

    # Afficher et sauvegarder
    with open(report_path, "w") as f:
        f.write(clf_report)

    disp.plot()
    plt.savefig(matrix_path)
    plt.close()

    print("Rapport sauvegardé dans reports/classification-report.txt")
    print("Matrice de confusion sauvegardée dans reports/confusion-matrix.png")


if __name__ == "__main__":
    evaluate()
