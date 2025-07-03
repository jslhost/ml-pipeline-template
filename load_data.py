import pandas as pd

data_link = "https://raw.githubusercontent.com/jslhost/dataset_repo/refs/heads/main/Churn_Modelling.csv"


def load_data(src: str = data_link, dest: str = "data/raw_dataset.csv"):
    """Load the dataset from ``src`` and save it to ``dest``.

    Parameters
    ----------
    src: str
        Path or URL to the CSV file to load.
    dest: str
        Path of the CSV file to write.
    """

    df = pd.read_csv(src)
    df.to_csv(dest, index=False)


if __name__ == "__main__":
    load_data()
