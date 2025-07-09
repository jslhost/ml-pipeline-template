"""A simple API to expose our trained model."""

from fastapi import FastAPI
from pydantic import BaseModel
from pickle import load
import pandas as pd
from src.utils import load_params
from fastapi.middleware.cors import CORSMiddleware


params = load_params()
model_path = params["model"]["path"]
preprocessor_path = params["model"]["preprocessor_path"]

with open(model_path, "rb") as f:
    model = load(f)

with open(preprocessor_path, "rb") as f:
    preprocessor = load(f)

app = FastAPI(
    title="Prédiction de Churn",
    description="Application de prédiction de Churn Churn 💸 <br>Une version par API pour faciliter la réutilisation du modèle 🚀",
)


class CustomerData(BaseModel):
    Surname: str
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Welcome"])
def show_welcome_page():
    """
    Show welcome page with model name and version.
    """

    return {
        "Message": "API de prédiction de Churn",
        "Model_name": "Churn SVC",
        "Model_version": "0.1",
    }


@app.post("/predict", tags=["Predict"])
async def predict(data: CustomerData) -> str:
    """ """
    df = pd.DataFrame([data.dict()])

    preprocessed_data = preprocessor.transform(df)

    prediction = (
        "Exited" if int(model.predict(preprocessed_data)) == 1 else "Not Exited"
    )

    return prediction
