import pandas as pd

def clean_data():
    df = pd.read_csv('data/raw_dataset.csv')
    df = df.drop(["RowNumber", "CustomerId"], axis=1)
    df.to_csv('data/clean_dataset.csv', index=False)

if __name__ == "__main__":
    clean_data()