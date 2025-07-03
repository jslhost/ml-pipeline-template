import pandas as pd
import numpy as np

from scipy import sparse

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector


def preprocess_data(src: str = "data/clean_dataset.csv", dest: str = "data/preprocessed_features.npz"):
    """Preprocess features and save them as a sparse matrix."""

    df = pd.read_csv(src)
    X = df.drop("Exited", axis=1)

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

    sparse.save_npz(dest, X_preprocessed)


if __name__ == "__main__":
    preprocess_data()
