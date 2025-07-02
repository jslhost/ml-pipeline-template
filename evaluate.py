import pandas as pd
from scipy import sparse
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def evaluate():
    df = pd.read_csv("data/clean_dataset.csv")
    y = df["Exited"]
    X = sparse.load_npz("data/preprocessed_features.npz")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    with open("model.pkl", "rb") as f:
        svc = load(f)

    y_test_pred = svc.predict(X_test)

    clf_report = classification_report(y_test, y_test_pred)

    cm = confusion_matrix(y_test, y_test_pred, labels=svc.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=svc.classes_)

    # Afficher et sauvegarder
    with open("reports/classification-report.txt", "w") as f:
        f.write(clf_report)

    disp.plot()
    plt.savefig("reports/confusion-matrix.png")
    plt.close()

    print("Rapport sauvegardé dans reports/classification-report.txt")
    print("Matrice de confusion sauvegardée dans reports/confusion-matrix.jpg")


if __name__ == "__main__":
    evaluate()
