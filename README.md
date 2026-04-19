# 🌾 Crop Yield Prediction System

A complete end-to-end Machine Learning system that predicts agricultural crop yield based on environmental and farming inputs.

## 👤 Project Details
- Name:Abhishek Mishra
- Roll Number:2305995
- Batch/Program:Data Engineering
- Project: Crop Yield Prediction System

## 📌 Problem Statement
Traditional farming decisions rely on experience and intuition, often resulting in suboptimal yields. This system leverages Machine Learning to predict crop yield (tons per hectare) using climate, soil, and agricultural input data, enabling data-driven precision agriculture.

## 🎯 Features
- Predict yield for 8 major crops across 5 regions
- 3 ML models trained and compared (Gradient Boosting, Random Forest, Linear Regression)
- Best model achieves **R² = 0.9848**
- Exploratory Data Analysis with visualizations
- REST API (Flask) for external integration
- Interactive web dashboard (Streamlit)
- Prediction history logging via SQLite

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| API | Flask |
| Dashboard | Streamlit |
| Storage | SQLite, Joblib |

## 📂 Project Structure
```
crop-yield-prediction/
├── data/
│   ├── generate_data.py       # Dataset generation script
│   ├── crop_yield.csv         # Dataset (2000 rows)
│   └── predictions.db         # SQLite prediction log
├── src/
│   ├── preprocess.py          # ETL & feature engineering
│   ├── train.py               # Model training & evaluation
│   └── predict.py             # Prediction pipeline
├── model/
│   ├── best_model.joblib      # Trained Gradient Boosting model
│   ├── encoders.joblib        # Label encoders
│   └── scaler.joblib          # Feature scaler
├── app/
│   ├── app.py                 # Flask REST API
│   └── dashboard.py           # Streamlit dashboard
├── outputs/
│   ├── eda_plots.png
│   ├── feature_importance.png
│   ├── actual_vs_predicted.png
│   └── model_comparison.png
├── requirements.txt
└── README.md
```

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate dataset & train models
```bash
cd data && python generate_data.py
cd ../src && python train.py
```

### 3. Launch Streamlit Dashboard
```bash
cd app && streamlit run dashboard.py
```

### 4. Launch Flask API (optional)
```bash
cd app && python app.py
```

## 🔌 API Usage

**POST /predict**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Crop_Type": "Rice",
    "Region": "South",
    "Soil_Type": "Loamy",
    "Season": "Kharif",
    "Year": 2024,
    "Rainfall_mm": 1200,
    "Temperature_C": 28,
    "Humidity_pct": 70,
    "Fertilizer_kg_ha": 180,
    "Pesticide_kg_ha": 2.0,
    "Area_ha": 3.0
  }'
```

**Response:**
```json
{
  "predicted_yield_tons_ha": 5.75,
  "unit": "tons per hectare",
  "model": "Gradient Boosting",
  "status": "success"
}
```

## 📊 Model Results
| Model | RMSE | MAE | R² |
|---|---|---|---|
| **Gradient Boosting** ✅ | 2.78 | 1.45 | **0.9848** |
| Random Forest | 3.38 | 1.77 | 0.9775 |
| Linear Regression | 21.59 | 15.59 | 0.0827 |

## 🔑 Key Features
- **14 engineered features** including composite indices (Temp×Rainfall, Fert/Area)
- **Label encoding** for categorical variables (crop, region, soil, season)
- **StandardScaler** normalization for numeric features
- **80/20 train-test split** with fixed random seed for reproducibility

## 🚀 Future Improvements
- Integrate real-time weather API (OpenWeather)
- Add satellite NDVI imagery features
- Deploy on cloud (AWS / GCP)
- Mobile app interface
- Multi-year forecasting with time-series models
