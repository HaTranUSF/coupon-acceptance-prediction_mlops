"""Trains and compares two candidate models on the coupon acceptance dataset,
logs each run to MLflow, and saves the best pipeline to models/model.pkl.
"""

import os
import joblib
import mlflow
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder

from source.data_cleaning import load_and_prepare

# --- Column groups ---
NOMINAL_COLS = [
    "distToCoupon",
    "destination",
    "passenger",
    "weather",
    "time",
    "coupon",
    "expiration",
    "maritalStatus",
    "occupation",
    "gender",
]
ORDINAL_COLS = ["education", "income", "age"]
FREQUENCY_COLS = [
    "Bar",
    "CoffeeHouse",
    "CarryAway",
    "RestaurantLessThan20",
    "Restaurant20To50",
]
NUMERIC_COLS = ["temperature"]

# Combined ordinal list strictly matching ALL_ORDINAL_CATEGORIES order
ALL_ORDINAL_COLS = ORDINAL_COLS + FREQUENCY_COLS

# --- Ordinal category orders ---
EDUCATION_ORDER = [
    "some high school",
    "high school graduate",
    "some college - no degree",
    "associates degree",
    "bachelors degree",
    "graduate degree (masters or doctorate)",
]
INCOME_ORDER = [
    "less than $12500",
    "$12500 - $24999",
    "$25000 - $37499",
    "$37500 - $49999",
    "$50000 - $62499",
    "$62500 - $74999",
    "$75000 - $87499",
    "$87500 - $99999",
    "$100000 or more",
]
AGE_ORDER = ["below21", "21", "26", "31", "36", "41", "46", "50plus"]
FREQUENCY_ORDER = ["never", "less1", "1~3", "4~8", "gt8"]

ALL_ORDINAL_CATEGORIES = [
    EDUCATION_ORDER,
    INCOME_ORDER,
    AGE_ORDER,
    FREQUENCY_ORDER,
    FREQUENCY_ORDER,
    FREQUENCY_ORDER,
    FREQUENCY_ORDER,
    FREQUENCY_ORDER,
]


def build_preprocessor() -> ColumnTransformer:
    """Rebuilds the ColumnTransformer pipeline with explicit imputation and encoding."""
    nominal_pipeline = Pipeline(
        [
            (
                "imputer",
                SimpleImputer(strategy="constant", fill_value="missing"),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore", sparse_output=False, drop="first"
                ),
            ),
        ]
    )

    ordinal_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "ordinal",
                OrdinalEncoder(
                    categories=ALL_ORDINAL_CATEGORIES,
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    numerical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("nominal_enc", nominal_pipeline, NOMINAL_COLS),
            ("ordinal_enc", ordinal_pipeline, ALL_ORDINAL_COLS),
            ("numeric_pass", numerical_pipeline, NUMERIC_COLS),
        ],
        remainder="drop",
    )


def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]
    return {
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, probs),
    }


def get_candidate_models() -> dict:
    """Logistic regression baseline and the tuned Random Forest model."""
    return {
        "logistic_regression": LogisticRegression(
            penalty="l1", solver="liblinear", C=0.1, random_state=42
        ),
        "random_forest_optimized": RandomForestClassifier(
            class_weight="balanced",
            max_depth=15,
            max_features=0.9,
            max_samples=0.6,
            min_samples_leaf=5,
            min_samples_split=20,
            n_estimators=300,
            random_state=42,
        ),
    }


def main():
    df = load_and_prepare()
    X, y = df.drop(["Y"], axis=1), df["Y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    mlflow.set_experiment("coupon-acceptance")
    best_pipeline, best_f1, best_name = None, -1.0, None

    for name, model in get_candidate_models().items():
        with mlflow.start_run(run_name=name):
            pipeline = Pipeline(
                [
                    ("preprocessor", build_preprocessor()),
                    ("model", model),
                ]
            )
            pipeline.fit(X_train, y_train)
            metrics = evaluate(pipeline, X_test, y_test)

            mlflow.log_param("model_type", name)
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)
            mlflow.sklearn.log_model(sk_model=pipeline, artifact_path="model", skops_trusted_types=["numpy.dtype"])

            print(f"{name}: {metrics}")

            if metrics["f1"] > best_f1:
                best_pipeline, best_f1, best_name = pipeline, metrics["f1"], name

    print(f"\nBest model: {best_name}, F1 {best_f1:.3f}")

    # Ensure target output folder exists prior to serialization
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_pipeline, "models/model.pkl")
    print("Saved best pipeline to models/model.pkl")


if __name__ == "__main__":
    main()