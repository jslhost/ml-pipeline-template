from fastapi.testclient import TestClient
import os

os.system("make evaluations")

from app.api import app  # ton script principal (nom à adapter)

client = TestClient(app)


def test_predict_valid():
    data = {
        "Surname": "michel",
        "CreditScore": 650,
        "Geography": "France",
        "Gender": "Male",
        "Age": 32,
        "Tenure": 2,
        "Balance": 22000.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000.0,
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert response.json() in ["Exited", "Not Exited"]


os.system("make clean")
