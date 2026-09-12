# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "model_loaded": True}


def test_predict():
    payload = {
        "destination": "No Urgent Place",
        "passenger": "Alone",
        "weather": "Sunny",
        "temperature": 80.0,
        "time": "2PM",
        "coupon": "Coffee House",
        "expiration": "1d",
        "gender": "Female",
        "age": "21",
        "maritalStatus": "Single",
        "has_children": 0,
        "education": "Some college - no degree",
        "occupation": "Unemployed",
        "income": "$37500 - $49999",
        "Bar": "never",
        "CoffeeHouse": "never",
        "CarryAway": "1~3",
        "RestaurantLessThan20": "4~8",
        "Restaurant20To50": "less1",
        "toCoupon_GEQ5min": 1,
        "toCoupon_GEQ15min": 0,
        "toCoupon_GEQ25min": 0,
        "direction_same": 0,
        "direction_opp": 1,
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        assert "accept_prediction" in response.json()
        assert "probability" in response.json()