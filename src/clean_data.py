import pandas as pd
from src.utils import load_params


def clean_data(params: dict):
    """Clean the dataset by removing identifier columns."""
    src = params["data"]["raw_dataset_path"]
    dest = params["data"]["clean_dataset_path"]
    columns_to_drop = params["data"]["columns_to_drop"]

    df = pd.read_csv(src)
    df = df.drop(columns_to_drop, axis=1)
    df.to_csv(dest, index=False)


if __name__ == "__main__":
    params = load_params()
    clean_data(params)
