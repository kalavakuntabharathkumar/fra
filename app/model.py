from pathlib import Path
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["amount", "account_age_days", "transactions_last_hour", "electronics", "cross_border"]

def _demo_data(seed: int = 41, n: int = 5000):
    rng = np.random.default_rng(seed)
    amount = rng.lognormal(3.7, 1.0, n)
    age = rng.integers(0, 3000, n)
    velocity = rng.poisson(2, n)
    electronics = rng.integers(0, 2, n)
    cross_border = rng.integers(0, 2, n)
    logit = -4.0 + 0.0015 * amount - 0.001 * age + 0.35 * velocity + 0.65 * electronics + 0.9 * cross_border
    probability = 1 / (1 + np.exp(-logit))
    y = rng.binomial(1, probability)
    X = np.column_stack([amount, age, velocity, electronics, cross_border])
    return X, y

def train_and_save(path: str | None = None):
    path = Path(path or os.getenv("MODEL_PATH", "models/fraud_model.joblib"))
    path.parent.mkdir(parents=True, exist_ok=True)
    X, y = _demo_data()
    model = Pipeline([
        ("scale", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=120, max_depth=8, random_state=41, class_weight="balanced_subsample")),
    ])
    model.fit(X, y)
    joblib.dump(model, path)
    return model

def load_or_train(path: str | None = None):
    path = Path(path or os.getenv("MODEL_PATH", "models/fraud_model.joblib"))
    if path.exists():
        return joblib.load(path)
    return train_and_save(str(path))

def features(tx):
    category = tx.merchant_category.lower()
    return [[tx.amount, tx.account_age_days, tx.transactions_last_hour,
             int(category == "electronics"), int(tx.country.upper() != "IN")]]
