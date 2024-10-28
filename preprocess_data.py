import pandas as pd
import numpy as np

from scipy import sparse

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector


def preprocess_data():
    df = pd.read_csv('data/clean_dataset.csv')
    X = df.drop('Exited', axis=1)

    numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, make_column_selector(dtype_include=np.number)),
        ('cat', categorical_transformer, make_column_selector(dtype_include=object))
        ])
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
        ])

    X_preprocessed = pipeline.fit_transform(X)

    sparse.save_npz("data/preprocessed_features.npz", X_preprocessed)


if __name__ == '__main__':
    preprocess_data()