import pandas as pd

data_link = "https://raw.githubusercontent.com/jslhost/dataset_repo/refs/heads/main/Churn_Modelling.csv"

def load_data():
    df = pd.read_csv(data_link)
    df.to_csv('data/raw_dataset.csv', index=False)

if __name__ == "__main__":
    load_data()