from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_score_input_validation():
    with TestClient(app) as client:
        response = client.post("/v1/score", json={
            "transaction_id": "tx-test",
            "amount": -5,
            "merchant_category": "electronics",
            "country": "IN",
            "account_age_days": 30,
            "transactions_last_hour": 2
        })
        assert response.status_code == 422

def test_score_happy_path():
    with TestClient(app) as client:
        response = client.post("/v1/score", json={
            "transaction_id": "tx-test-2",
            "amount": 125.5,
            "merchant_category": "electronics",
            "country": "IN",
            "account_age_days": 240,
            "transactions_last_hour": 2
        })
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["fraud_probability"] <= 1
        assert data["decision"] in {"approve", "review"}
