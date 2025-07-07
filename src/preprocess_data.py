import pandas as pd
import numpy as np

from scipy import sparse
from pickle import dump

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector

from src.utils import load_params


def preprocess_data(params: dict):
    """Preprocess features and save them as a sparse matrix."""
    src = params["data"]["clean_dataset_path"]
    dest = params["data"]["preprocessed_features_path"]
    preprocessor_path = params["model"]["preprocessor_path"]
    target_column = params["base"]["target_column"]

    df = pd.read_csv(src)
    X = df.drop(target_column, axis=1)

    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, make_column_selector(dtype_include=np.number)),
            (
                "cat",
                categorical_transformer,
                make_column_selector(dtype_include=object),
            ),
        ]
    )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])

    X_preprocessed = pipeline.fit_transform(X)
    
    with open(preprocessor_path, "wb") as f:
        dump(pipeline, f)
        
    X_preprocessed_sparse = sparse.csr_matrix(X_preprocessed)
    sparse.save_npz(dest, X_preprocessed_sparse)


if __name__ == "__main__":
    params = load_params()
    preprocess_data(params)
