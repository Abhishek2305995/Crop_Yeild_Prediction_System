"""
predict.py - Prediction pipeline for Crop Yield System
"""

import numpy as np
import pandas as pd
import joblib
import os
import sqlite3
from datetime import datetime

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'predictions.db')

CATEGORICAL_COLS = ['Crop_Type', 'Region', 'Soil_Type', 'Season']
NUMERIC_COLS = ['Year', 'Rainfall_mm', 'Temperature_C', 'Humidity_pct',
                'Fertilizer_kg_ha', 'Pesticide_kg_ha', 'Area_ha']


def load_artifacts():
    model = joblib.load(os.path.join(MODEL_DIR, 'best_model.joblib'))
    encoders = joblib.load(os.path.join(MODEL_DIR, 'encoders.joblib'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.joblib'))
    return model, encoders, scaler


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        crop_type TEXT,
        region TEXT,
        soil_type TEXT,
        season TEXT,
        year INTEGER,
        rainfall REAL,
        temperature REAL,
        humidity REAL,
        fertilizer REAL,
        pesticide REAL,
        area REAL,
        predicted_yield REAL
    )''')
    conn.commit()
    conn.close()


def log_prediction(inputs, predicted_yield):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO predictions
        (timestamp, crop_type, region, soil_type, season, year, rainfall,
         temperature, humidity, fertilizer, pesticide, area, predicted_yield)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
        datetime.now().isoformat(),
        inputs.get('Crop_Type'), inputs.get('Region'),
        inputs.get('Soil_Type'), inputs.get('Season'),
        inputs.get('Year'), inputs.get('Rainfall_mm'),
        inputs.get('Temperature_C'), inputs.get('Humidity_pct'),
        inputs.get('Fertilizer_kg_ha'), inputs.get('Pesticide_kg_ha'),
        inputs.get('Area_ha'), predicted_yield
    ))
    conn.commit()
    conn.close()


def get_prediction_history(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f'SELECT * FROM predictions ORDER BY id DESC LIMIT {limit}', conn
    )
    conn.close()
    return df


def predict(inputs: dict) -> dict:
    """
    inputs: dict with keys matching column names
    Returns: dict with predicted_yield and confidence info
    """
    model, encoders, scaler = load_artifacts()

    df = pd.DataFrame([inputs])
    df['Temp_Rainfall_Index'] = df['Temperature_C'] * df['Rainfall_mm'] / 1000
    df['Fert_per_Area'] = df['Fertilizer_kg_ha'] / (df['Area_ha'] + 0.01)
    df['Humidity_Rain'] = df['Humidity_pct'] * df['Rainfall_mm'] / 1000

    for col in CATEGORICAL_COLS:
        df[col] = encoders[col].transform(df[col].astype(str))

    all_numeric = NUMERIC_COLS + ['Temp_Rainfall_Index', 'Fert_per_Area', 'Humidity_Rain']
    df[all_numeric] = scaler.transform(df[all_numeric])

    feature_cols = CATEGORICAL_COLS + NUMERIC_COLS + [
        'Temp_Rainfall_Index', 'Fert_per_Area', 'Humidity_Rain'
    ]
    X = df[feature_cols]
    predicted = float(model.predict(X)[0])
    predicted = max(0.1, round(predicted, 2))

    # Confidence via tree variance for GBR/RF
    confidence = None
    if hasattr(model, 'estimators_'):
        try:
            tree_preds = np.array([tree.predict(X)[0] for tree in model.estimators_])
            std = tree_preds.std()
            confidence = round(float(std), 3)
        except Exception:
            pass

    log_prediction(inputs, predicted)

    return {
        'predicted_yield_tons_ha': predicted,
        'std_dev': confidence,
        'unit': 'tons per hectare',
        'model': 'Gradient Boosting'
    }


if __name__ == '__main__':
    sample = {
        'Crop_Type': 'Rice', 'Region': 'South', 'Soil_Type': 'Loamy',
        'Season': 'Kharif', 'Year': 2023,
        'Rainfall_mm': 1200.0, 'Temperature_C': 28.0, 'Humidity_pct': 70.0,
        'Fertilizer_kg_ha': 180.0, 'Pesticide_kg_ha': 2.0, 'Area_ha': 3.0
    }
    result = predict(sample)
    print("Prediction:", result)
    history = get_prediction_history(5)
    print("\nHistory:\n", history)
