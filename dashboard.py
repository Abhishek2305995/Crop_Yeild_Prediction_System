"""
app.py - Flask REST API for Crop Yield Prediction
"""

from flask import Flask, request, jsonify
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from predict import predict, get_prediction_history

app = Flask(__name__)

VALID_CROPS = ['Rice', 'Wheat', 'Maize', 'Soybean', 'Cotton', 'Sugarcane', 'Potato', 'Tomato']
VALID_REGIONS = ['North', 'South', 'East', 'West', 'Central']
VALID_SOILS = ['Loamy', 'Sandy', 'Clay', 'Silt', 'Peaty']
VALID_SEASONS = ['Kharif', 'Rabi', 'Zaid']


def validate_inputs(data):
    errors = []
    required = ['Crop_Type', 'Region', 'Soil_Type', 'Season', 'Year',
                 'Rainfall_mm', 'Temperature_C', 'Humidity_pct',
                 'Fertilizer_kg_ha', 'Pesticide_kg_ha', 'Area_ha']
    for field in required:
        if field not in data:
            errors.append(f"Missing field: {field}")

    if errors:
        return errors

    if data['Crop_Type'] not in VALID_CROPS:
        errors.append(f"Invalid Crop_Type. Must be one of: {VALID_CROPS}")
    if data['Region'] not in VALID_REGIONS:
        errors.append(f"Invalid Region. Must be one of: {VALID_REGIONS}")
    if data['Soil_Type'] not in VALID_SOILS:
        errors.append(f"Invalid Soil_Type. Must be one of: {VALID_SOILS}")
    if data['Season'] not in VALID_SEASONS:
        errors.append(f"Invalid Season. Must be one of: {VALID_SEASONS}")
    if not (2000 <= int(data['Year']) <= 2030):
        errors.append("Year must be between 2000 and 2030")
    return errors


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'Crop Yield Prediction API',
        'version': '1.0',
        'endpoints': {
            'POST /predict': 'Get yield prediction',
            'GET /history': 'View prediction history',
            'GET /options': 'Get valid input options',
            'GET /health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'})


@app.route('/options', methods=['GET'])
def options():
    return jsonify({
        'Crop_Type': VALID_CROPS,
        'Region': VALID_REGIONS,
        'Soil_Type': VALID_SOILS,
        'Season': VALID_SEASONS,
        'Year': {'min': 2000, 'max': 2030},
        'Rainfall_mm': {'min': 100, 'max': 2500, 'unit': 'mm'},
        'Temperature_C': {'min': 5, 'max': 50, 'unit': 'Celsius'},
        'Humidity_pct': {'min': 20, 'max': 100, 'unit': '%'},
        'Fertilizer_kg_ha': {'min': 0, 'max': 500, 'unit': 'kg/ha'},
        'Pesticide_kg_ha': {'min': 0, 'max': 20, 'unit': 'kg/ha'},
        'Area_ha': {'min': 0.1, 'max': 50, 'unit': 'hectares'}
    })


@app.route('/predict', methods=['POST'])
def predict_yield():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON body provided'}), 400

        errors = validate_inputs(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 422

        inputs = {
            'Crop_Type': data['Crop_Type'],
            'Region': data['Region'],
            'Soil_Type': data['Soil_Type'],
            'Season': data['Season'],
            'Year': int(data['Year']),
            'Rainfall_mm': float(data['Rainfall_mm']),
            'Temperature_C': float(data['Temperature_C']),
            'Humidity_pct': float(data['Humidity_pct']),
            'Fertilizer_kg_ha': float(data['Fertilizer_kg_ha']),
            'Pesticide_kg_ha': float(data['Pesticide_kg_ha']),
            'Area_ha': float(data['Area_ha']),
        }
        result = predict(inputs)
        result['inputs'] = inputs
        result['status'] = 'success'
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500


@app.route('/history', methods=['GET'])
def history():
    try:
        limit = int(request.args.get('limit', 20))
        df = get_prediction_history(limit)
        return jsonify({
            'count': len(df),
            'predictions': df.to_dict(orient='records')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Crop Yield Prediction API on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
