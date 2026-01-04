import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Import model trainers and predictors
from models.lstm_model import LSTMModel
from models.time_series_predictor import TimeSeriesPredictor

# Load environment variables
load_dotenv('../.env')

app = Flask(__name__)
CORS(app)

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
MODEL_STORAGE_PATH = os.getenv('MODEL_STORAGE_PATH', './saved_models')

# Ensure model storage directory exists
os.makedirs(MODEL_STORAGE_PATH, exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Time Machines Python Service',
        'version': '1.0.0'
    }), 200

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train a time series model"""
    try:
        data = request.json
        model_id = data.get('modelId')
        time_series_data = data.get('timeSeriesData')
        model_type = data.get('modelType', 'lstm')
        hyperparameters = data.get('hyperparameters', {})

        if not model_id or not time_series_data:
            return jsonify({'error': 'Missing required fields'}), 400

        # Initialize predictor
        predictor = TimeSeriesPredictor(model_type=model_type)

        # Train the model
        metrics = predictor.train(
            data=time_series_data,
            model_id=model_id,
            hyperparameters=hyperparameters
        )

        # Save model
        model_path = os.path.join(MODEL_STORAGE_PATH, f'{model_id}.pkl')
        predictor.save(model_path)

        # Notify backend of completion
        try:
            requests.put(
                f'{BACKEND_URL}/api/models/{model_id}/status',
                json={
                    'status': 'completed',
                    'metrics': metrics,
                    'modelPath': model_path,
                    'trainingDuration': metrics.get('training_time', 0)
                }
            )
        except Exception as e:
            print(f'Failed to notify backend: {str(e)}')

        return jsonify({
            'message': 'Model trained successfully',
            'modelId': model_id,
            'metrics': metrics
        }), 200

    except Exception as e:
        # Notify backend of failure
        try:
            if 'model_id' in locals():
                requests.put(
                    f'{BACKEND_URL}/api/models/{model_id}/status',
                    json={'status': 'failed'}
                )
        except:
            pass

        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def generate_prediction():
    """Generate predictions using a trained model"""
    try:
        data = request.json
        model_id = data.get('modelId')
        model_path = data.get('modelPath')
        model_type = data.get('modelType', 'lstm')
        input_data = data.get('inputData')
        horizon = data.get('horizon', 10)

        if not model_path or not os.path.exists(model_path):
            return jsonify({'error': 'Model not found'}), 404

        # Initialize predictor and load model
        predictor = TimeSeriesPredictor(model_type=model_type)
        predictor.load(model_path)

        # Generate predictions
        predictions, confidence = predictor.predict(
            input_data=input_data,
            horizon=horizon
        )

        return jsonify({
            'predictions': predictions,
            'confidence': confidence,
            'horizon': horizon
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/types', methods=['GET'])
def get_model_types():
    """Get available model types and their descriptions"""
    return jsonify({
        'models': [
            {
                'type': 'lstm',
                'name': 'LSTM',
                'description': 'Long Short-Term Memory neural network for time series forecasting'
            },
            {
                'type': 'gru',
                'name': 'GRU',
                'description': 'Gated Recurrent Unit for efficient time series prediction'
            },
            {
                'type': 'arima',
                'name': 'ARIMA',
                'description': 'AutoRegressive Integrated Moving Average for statistical forecasting'
            },
            {
                'type': 'prophet',
                'name': 'Prophet',
                'description': 'Facebook Prophet for time series with strong seasonal patterns'
            },
            {
                'type': 'transformer',
                'name': 'Transformer',
                'description': 'Transformer-based model for complex time series patterns'
            }
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_SERVICE_PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
