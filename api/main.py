"""
FastAPI wrapper around the trained coupon acceptance pipeline.

Loads models/model.pkl (built by src/train.py) on startup and exposes
a /predict endpoint. Fields on CouponRequest are the raw, pre-feature-
engineering inputs (e.g. the three toCoupon_GEQ*min flags rather than
the derived distToCoupon), so the same engineer_features() used in
training also runs here, keeping training and serving consistent.

NOTE: field names/types below are based on the known schema of the
UCI In-Vehicle Coupon Recommendation dataset. Verify these against
your own df.columns output before trusting this fully, in case your
notebook renamed or dropped anything beyond what's in data_cleaning.py.
"""

from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

from source.data_cleaning import clean_data, engineer_features

MODEL_PATH = Path("models/model.pkl")
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"No model found at {MODEL_PATH}. Run `python -m source.train` first.")
    model = joblib.load(MODEL_PATH)
    yield
    model = None


app = FastAPI(title="Coupon Acceptance Predictor", lifespan=lifespan)


class CouponRequest(BaseModel):
    destination: str
    passenger: str
    weather: str
    temperature: float
    time: str
    coupon: str
    expiration: str
    gender: str
    age: str
    maritalStatus: str
    has_children: int
    education: str
    occupation: str
    income: str
    Bar: str
    CoffeeHouse: str
    CarryAway: str
    RestaurantLessThan20: str
    Restaurant20To50: str
    toCoupon_GEQ5min: int
    toCoupon_GEQ15min: int
    toCoupon_GEQ25min: int
    direction_same: int
    direction_opp: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "destination": "no urgent place",
                "passenger": "alone",
                "weather": "sunny",
                "temperature": 80,
                "time": "10am",
                "coupon": "coffee house",
                "expiration": "1d",
                "gender": "female",
                "age": "21",
                "maritalStatus": "single",
                "has_children": 0,
                "education": "some college - no degree",
                "occupation": "student",
                "income": "$25000 - $37499",
                "Bar": "never",
                "CoffeeHouse": "1~3",
                "CarryAway": "1~3",
                "RestaurantLessThan20": "4~8",
                "Restaurant20To50": "less1",
                "toCoupon_GEQ5min": 1,
                "toCoupon_GEQ15min": 0,
                "toCoupon_GEQ25min": 0,
                "direction_same": 0,
                "direction_opp": 1,
            }
        }
    )


def prepare_row(request: CouponRequest) -> pd.DataFrame:
    """Turn one request into a single-row dataframe and run the same
    normalize_strings() + engineer_features() steps used at training time,
    in the same order the notebook applies them. Deliberately skips
    clean_data()'s df.mode().fillna() step, since that fill value is a
    property of the training set, not something to recompute per request.
    Missing values on a live row are instead handled by the SimpleImputers
    already fit inside the saved pipeline.
    """
    row = pd.DataFrame([request.model_dump()])
    row = clean_data(row)
    row = engineer_features(row)
    return row


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(request: CouponRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    row = prepare_row(request)
    try:
        prediction = model.predict(row)[0]
        probability = model.predict_proba(row)[0][1]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"accept_prediction": int(prediction), "probability": round(float(probability), 4)}
