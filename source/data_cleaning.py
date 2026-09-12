"""Data loading, cleaning, and feature engineering for the coupon acceptance dataset.

Extracted from Coupon_Acceptance_Prediction.ipynb, cells 5-8 (cleaning) and
34-37 (feature engineering).
"""

import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo


def load_data() -> pd.DataFrame:
    """Pull the In-Vehicle Coupon Recommendation dataset from UCI (id=603)."""
    dataset = fetch_ucirepo(id=603)
    return pd.concat([dataset.data.features, dataset.data.targets], axis=1)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the mostly-null 'car' column, normalize text strings, and retain missing values
    so that downstream Scikit-Learn Pipeline imputers can handle them cleanly during training and API inference.
    """
    df = df.copy()

    # Drop mostly-null column
    if "car" in df.columns:
        df = df.drop("car", axis=1)

    # Clean object string columns (lowercasing and stripping whitespace)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().str.lower()
        # Replace string 'nan' produced by str conversion back to true NaNs
        df[col] = df[col].replace("nan", np.nan)

    # Explicitly cast columns used in OrdinalEncoder to string so numeric conversion doesn't break categorization
    string_categorical_cols = [
        "age",
        "education",
        "income",
        "Bar",
        "CoffeeHouse",
        "CarryAway",
        "RestaurantLessThan20",
        "Restaurant20To50",
    ]
    for col in string_categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    return df


# src/data_cleaning.py

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Drop redundant direction_same column and collapse the three toCoupon_GEQ*min binary
    columns into a single distToCoupon category.
    """
    df = df.copy()
    if "direction_same" in df.columns:
        df = df.drop(["direction_same"], axis=1)

    # Explicitly cast to int to ensure condition checks evaluate cleanly regardless of input source
    for col in ["toCoupon_GEQ5min", "toCoupon_GEQ15min", "toCoupon_GEQ25min"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    conditions = [
        (df["toCoupon_GEQ25min"] == 1),
        (df["toCoupon_GEQ15min"] == 1) & (df["toCoupon_GEQ25min"] == 0),
        (df["toCoupon_GEQ5min"] == 1) & (df["toCoupon_GEQ15min"] == 0),
    ]
    choices = ["25+ min", "15-25 min", "5-15 min"]
    df["distToCoupon"] = np.select(conditions, choices, default="< 5 min")

    df = df.drop(
        columns=["toCoupon_GEQ5min", "toCoupon_GEQ15min", "toCoupon_GEQ25min"],
        errors="ignore",
    )
    return df

def load_and_prepare() -> pd.DataFrame:
    """Convenience wrapper: load, clean, and engineer features in one call."""
    return engineer_features(clean_data(load_data()))