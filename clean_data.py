import pandas as pd


def clean_data(src: str = "data/raw_dataset.csv", dest: str = "data/clean_dataset.csv"):
    """Clean the dataset by removing identifier columns."""

    df = pd.read_csv(src)
    df = df.drop(["RowNumber", "CustomerId"], axis=1)
    df.to_csv(dest, index=False)


if __name__ == "__main__":
    clean_data()
