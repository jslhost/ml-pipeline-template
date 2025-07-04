import pandas as pd
from src.utils import load_params


def load_data(params: dict):
    """Load the dataset from ``src`` and save it to ``dest``.

    Parameters
    ----------
    params: dict
        Dictionary containing parameters for data loading.
    """
    data_link = params["data"]["raw_data_link"]
    dest = params["data"]["raw_dataset_path"]

    df = pd.read_csv(data_link)
    df.to_csv(dest, index=False)


if __name__ == "__main__":
    params = load_params()
    load_data(params)
