from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Charger le modèle sauvegardé
model_path = 'avocado-model.pkl'
with open(model_path, 'rb') as file:
    pipeline = pickle.load(file)

# Définir les fonctionnalités attendues
NUMERIC_FEATURES = [
    'Quality1', 'Quality2', 'Quality3',
    'Small Bags', 'Large Bags', 'XLarge Bags',
    'year'
]

CATEGORICAL_FEATURES = ['type', 'region']

def validate_input(data):
    missing_features = []
    for feature in NUMERIC_FEATURES + CATEGORICAL_FEATURES:
        if feature not in data:
            missing_features.append(feature)
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features)}"
    return True, None

def preprocess_input(data):
    input_df = pd.DataFrame([data])
    for feature in NUMERIC_FEATURES:
        input_df[feature] = input_df[feature].astype(float)
    return input_df

@app.route('/predict_price', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({'error': 'Invalid input', 'message': error_message}), 400
        input_df = preprocess_input(data)
        prediction = pipeline.predict(input_df)
        predicted_price = float(round(prediction[0], 2))
        return jsonify({'predicted_price': predicted_price})
    except Exception as e:
        return jsonify({
            'error': 'Prediction error',
            'message': str(e)
        }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': 'Invalid JSON format in request body'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)