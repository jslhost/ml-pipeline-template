import os
import pandas as pd
import numpy as np
from scipy import sparse
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics

import pickle
import wandb
from wandb.sklearn import plot_learning_curve, plot_confusion_matrix, plot_roc

from src.utils import load_params


def experiment(params: dict):
    """Experiment with wandb"""
    data_csv = params["data"]["clean_dataset_path"]
    features_file = params["data"]["preprocessed_features_path"]
    target_column = params["base"]["target_column"]
    test_size = params["base"]["test_size"]
    random_state = params["base"]["random_state"]

    df = pd.read_csv(data_csv)
    y = df[target_column]
    X = sparse.load_npz(features_file)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    run = wandb.init(project="ml-pipeline-experiment")
    cfg = dict(wandb.config)

    svc = SVC(**cfg)

    svc.fit(X_train, y_train)

    y_test_pred = svc.predict(X_test)
    y_test_probas = svc.predict_proba(X_test)
    acc = metrics.accuracy_score(y_test, y_test_pred)

    wandb.log({
        "accuracy/test": acc,
    })

    wandb.config.update({"test_size": test_size,
                         "train_len": X_train.shape[0],
                         "test_len": X_test.shape[0]})
    
    labels = np.array([1, 0])
    plot_learning_curve(svc, X_train, y_train)
    plot_confusion_matrix(y_test, y_test_pred, labels=labels)
    plot_roc(y_test, y_test_probas, labels)

    os.makedirs("artifacts", exist_ok=True)
    model_path = os.path.join("artifacts", "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(svc, f)
    model_path = os.path.join("artifacts", "model.pkl")


    art = wandb.Artifact(
        name=f"svc-{wandb.run.id}",
        type="model",
        metadata={
            "params": cfg,
            "metric": "accuracy/test",
            "score": acc
        }
    )

    art.add_file(model_path)
    wandb.log_artifact(art)

    run.finish()


if __name__ == "__main__":
    params = load_params()
    experiment(params)