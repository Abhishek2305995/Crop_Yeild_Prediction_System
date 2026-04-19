"""
preprocess.py - Data cleaning and feature engineering for Crop Yield Prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

CATEGORICAL_COLS = ['Crop_Type', 'Region', 'Soil_Type', 'Season']
NUMERIC_COLS = ['Year', 'Rainfall_mm', 'Temperature_C', 'Humidity_pct',
                'Fertilizer_kg_ha', 'Pesticide_kg_ha', 'Area_ha']
TARGET_COL = 'Yield_tons_ha'


def load_data(path):
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} rows, {df.shape[1]} columns")
    return df


def clean_data(df):
    initial = len(df)
    df = df.dropna()
    df = df[df['Yield_tons_ha'] > 0]
    df = df[df['Rainfall_mm'] >= 0]
    df = df[df['Temperature_C'].between(5, 50)]
    df = df.drop_duplicates()
    print(f"[INFO] Cleaned: {initial} → {len(df)} rows")
    return df.reset_index(drop=True)


def feature_engineering(df):
    df = df.copy()
    df['Temp_Rainfall_Index'] = df['Temperature_C'] * df['Rainfall_mm'] / 1000
    df['Fert_per_Area'] = df['Fertilizer_kg_ha'] / (df['Area_ha'] + 0.01)
    df['Humidity_Rain'] = df['Humidity_pct'] * df['Rainfall_mm'] / 1000
    return df


def encode_and_scale(df, encoders=None, scaler=None, fit=True):
    df = df.copy()
    if fit:
        encoders = {}
        for col in CATEGORICAL_COLS:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        scaler = StandardScaler()
        all_numeric = NUMERIC_COLS + ['Temp_Rainfall_Index', 'Fert_per_Area', 'Humidity_Rain']
        df[all_numeric] = scaler.fit_transform(df[all_numeric])
    else:
        for col in CATEGORICAL_COLS:
            df[col] = encoders[col].transform(df[col].astype(str))
        all_numeric = NUMERIC_COLS + ['Temp_Rainfall_Index', 'Fert_per_Area', 'Humidity_Rain']
        df[all_numeric] = scaler.transform(df[all_numeric])
    return df, encoders, scaler


def get_features_target(df):
    feature_cols = CATEGORICAL_COLS + NUMERIC_COLS + [
        'Temp_Rainfall_Index', 'Fert_per_Area', 'Humidity_Rain'
    ]
    X = df[feature_cols]
    y = df[TARGET_COL]
    return X, y


def run_pipeline(data_path, save_dir='../model'):
    os.makedirs(save_dir, exist_ok=True)
    df = load_data(data_path)
    df = clean_data(df)
    df = feature_engineering(df)
    df_encoded, encoders, scaler = encode_and_scale(df)
    X, y = get_features_target(df_encoded)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    joblib.dump(encoders, os.path.join(save_dir, 'encoders.joblib'))
    joblib.dump(scaler, os.path.join(save_dir, 'scaler.joblib'))
    print(f"[INFO] Train: {len(X_train)}, Test: {len(X_test)}")
    print(f"[INFO] Features: {list(X.columns)}")
    return X_train, X_test, y_train, y_test, encoders, scaler, df


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, encoders, scaler, df = run_pipeline(
        '../data/crop_yield.csv', save_dir='../model'
    )
    print("Preprocessing complete.")
