import numpy as np
import pandas as pd
from source.data_cleaning import clean_data, engineer_features


def test_clean_data_drops_car_column():
    """Verify that clean_data drops the high-null 'car' column if present."""
    df = pd.DataFrame({"car": ["do not drive", None], "weather": ["Sunny", "Rainy"]})
    cleaned = clean_data(df)
    assert "car" not in cleaned.columns


def test_clean_data_normalizes_strings_and_preserves_nans():
    """Verify string lowercasing, stripping, and correct NaN preservation."""
    df = pd.DataFrame({
        "destination": ["  No Urgent Place  ", None],
        "Bar": [" Never ", "nan"],
    })
    cleaned = clean_data(df)

    # Asserts strings are stripped and lowercased
    assert cleaned["destination"].iloc[0] == "no urgent place"

    # Asserts missing values remain as true NaNs for downstream Pipeline imputers
    assert pd.isna(cleaned["destination"].iloc[1])
    assert pd.isna(cleaned["Bar"].iloc[1])


def test_engineer_features_creates_dist_to_coupon():
    """Verify that feature engineering correctly combines time flags into distToCoupon."""
    df = pd.DataFrame({
        "direction_same": [1],
        "toCoupon_GEQ5min": [1],
        "toCoupon_GEQ15min": [1],
        "toCoupon_GEQ25min": [0],
    })
    engineered = engineer_features(df)

    assert "direction_same" not in engineered.columns
    assert "distToCoupon" in engineered.columns
    assert engineered["distToCoupon"].iloc[0] == "15-25 min"