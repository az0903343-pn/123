"""
ML helpers for the vehicle project.

- train_model(df)      : trains a RandomForest price estimator on vehicles.csv
- ensure_model(df)     : loads model.joblib if present, otherwise trains & saves it
- predict_price(df,..) : estimates market price of a custom vehicle
- similar(df, name)    : K-nearest-neighbour similar vehicles
- money(n)             : 1234567 -> "12.35 Lakh" / "1.23 Crore"
- split_list(s)        : "a;b;c" -> ["a","b","c"]
"""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_FILE = os.path.join(os.path.dirname(__file__), "model.joblib")
CAT_COLS = ["category", "brand", "fuel_type"]
NUM_COLS = ["seats", "top_speed_kmh"]


def split_list(s):
    """CSV list fields use ';' as separator."""
    if not isinstance(s, str) or not s.strip():
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def money(n):
    n = float(n)
    if n >= 10_000_000:
        return f"{n / 10_000_000:.2f} Crore"
    if n >= 100_000:
        return f"{n / 100_000:.2f} Lakh"
    return f"{n:,.0f} PKR"


def train_model(df: pd.DataFrame):
    """Train a RandomForest that predicts price from category / brand / fuel / specs."""
    # 10,000+ rows par bhi app boot fast rahe - trees adaptively kam
    n_trees = 250 if len(df) < 3000 else 120
    pre = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
            ("num", StandardScaler(), NUM_COLS),
        ]
    )
    return Pipeline(
        [
            ("pre", pre),
            ("rf", RandomForestRegressor(n_estimators=n_trees, random_state=42)),
        ]
    )


def ensure_model(df: pd.DataFrame):
    """Load the saved Kaggle-trained model, or train one on the spot."""
    if os.path.exists(MODEL_FILE):
        try:
            model = joblib.load(MODEL_FILE)
            model.predict(df.head(1)[CAT_COLS + NUM_COLS])  # sanity check
            return model
        except Exception:
            pass
    return train_model(df)


def predict_price(model, category, brand, fuel_type, seats, top_speed_kmh):
    row = pd.DataFrame(
        [
            {
                "category": category,
                "brand": brand,
                "fuel_type": fuel_type,
                "seats": seats,
                "top_speed_kmh": top_speed_kmh,
            }
        ]
    )
    return float(max(model.predict(row)[0], 50_000))


def similar(df: pd.DataFrame, name: str, k: int = 5):
    """K-nearest vehicles by (seats, top_speed, price). Always returns brand too."""
    if name not in set(df["name"]):
        return pd.DataFrame()
    row = df[df["name"] == name].iloc[0]
    feats = df[["seats", "top_speed_kmh", "price_pkr"]].astype(float)
    scaler = StandardScaler().fit(feats)
    X = scaler.transform(feats)
    nn = NearestNeighbors(n_neighbors=min(k + 1, len(df))).fit(X)
    dist, idx = nn.kneighbors([X[df.index.get_loc(row.name)]])
    res = df.iloc[idx[0][1:]].copy()
    res["match_pct"] = (1 - dist[0][1:] / dist[0][1:].max() if dist[0][1:].max() else 1).round(3) * 100
    return res[["name", "brand", "category", "price_pkr"]].head(k)
