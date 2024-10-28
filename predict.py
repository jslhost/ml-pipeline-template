import pandas as pd
from scipy import sparse
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def predict():
    df = pd.read_csv("data/clean_dataset.csv")
    y = df['Exited']
    X = sparse.load_npz("data/preprocessed_features.npz")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    with open("model.pkl", "rb") as f:
        svc = load(f)

    y_test_pred = svc.predict(X_test)
    print(classification_report(y_test, y_test_pred))

if __name__ == '__main__':
    predict()