import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Import model trainers and predictors
from models.lstm_model import LSTMModel
from models.time_series_predictor import TimeSeriesPredictor

# Load environment variables
load_dotenv('../.env')

# Structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger('ai-time-machines')

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

        logger.info('Training model %s of type %s', model_id, model_type)

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

        logger.info('Model %s trained successfully. Metrics: %s', model_id, metrics)

        # Notify backend of completion
        try:
            requests.put(
                f'{BACKEND_URL}/api/models/{model_id}/status',
                json={
                    'status': 'completed',
                    'metrics': metrics,
                    'modelPath': model_path,
                    'trainingDuration': metrics.get('training_time', 0)
                },
                timeout=10
            )
        except Exception as e:
            logger.warning('Failed to notify backend for model %s: %s', model_id, str(e))

        return jsonify({
            'message': 'Model trained successfully',
            'modelId': model_id,
            'metrics': metrics
        }), 200

    except Exception as e:
        logger.error('Training failed for model %s: %s', locals().get('model_id', 'unknown'), str(e))
        # Notify backend of failure
        try:
            if 'model_id' in locals() and model_id:
                requests.put(
                    f'{BACKEND_URL}/api/models/{model_id}/status',
                    json={'status': 'failed'},
                    timeout=10
                )
        except Exception as notify_err:
            logger.warning('Failed to notify backend of training failure: %s', str(notify_err))

        return jsonify({'error': 'Training failed. Please check server logs.'}), 500

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

        logger.info('Generating prediction for model %s (horizon=%d)', model_id, horizon)

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
        logger.error('Prediction failed: %s', str(e))
        return jsonify({'error': 'Prediction failed. Please check server logs.'}), 500

@app.route('/api/monitor', methods=['POST'])
def monitor_model():
    """Detect performance drift and optionally trigger autonomous retraining.

    Expected JSON body:
      {
        "modelId":      "<uuid>",
        "modelPath":    "<path>",
        "modelType":    "lstm",
        "recentData":   [{timestamp, value}, ...],   // recent observations
        "baselineMetrics": {"test_loss": 0.01, ...}, // original training metrics
        "driftThreshold": 0.05,                      // optional, default 0.05
        "autoRetrain":  true                         // optional, triggers retraining
      }
    """
    try:
        data = request.json
        model_id = data.get('modelId')
        model_path = data.get('modelPath')
        model_type = data.get('modelType', 'lstm')
        recent_data = data.get('recentData', [])
        baseline_metrics = data.get('baselineMetrics', {})
        drift_threshold = float(data.get('driftThreshold', 0.05))
        auto_retrain = data.get('autoRetrain', False)

        if not model_id or not model_path:
            return jsonify({'error': 'modelId and modelPath are required'}), 400

        if len(recent_data) < 2:
            return jsonify({'error': 'At least 2 recent data points required for drift detection'}), 400

        # Validate model_path is within the allowed storage directory (prevent path traversal)
        allowed_dir = os.path.realpath(MODEL_STORAGE_PATH)
        resolved_path = os.path.realpath(model_path)
        if not resolved_path.startswith(allowed_dir + os.sep) and resolved_path != allowed_dir:
            return jsonify({'error': 'Invalid model path'}), 400

        if not os.path.exists(resolved_path):
            return jsonify({'error': 'Model file not found'}), 404

        logger.info('Running drift detection for model %s', model_id)

        # Load model and evaluate on recent data
        predictor = TimeSeriesPredictor(model_type=model_type)
        predictor.load(resolved_path)

        drift_result = predictor.detect_drift(
            recent_data=recent_data,
            baseline_metrics=baseline_metrics,
            drift_threshold=drift_threshold
        )

        response_payload = {
            'modelId': model_id,
            'driftDetected': drift_result['drift_detected'],
            'currentLoss': drift_result['current_loss'],
            'baselineLoss': drift_result.get('baseline_loss'),
            'driftScore': drift_result['drift_score'],
            'threshold': drift_threshold,
            'message': drift_result['message']
        }

        # Autonomous retraining if drift is detected and requested
        if drift_result['drift_detected'] and auto_retrain:
            logger.info('Drift detected for model %s – triggering autonomous retraining', model_id)
            try:
                retrain_resp = requests.post(
                    f'{BACKEND_URL}/api/models/{model_id}/retrain',
                    json={'reason': 'drift_detected', 'driftScore': drift_result['drift_score']},
                    timeout=10
                )
                response_payload['retrainTriggered'] = retrain_resp.status_code < 300
            except Exception as e:
                logger.warning('Could not trigger retraining for model %s: %s', model_id, str(e))
                response_payload['retrainTriggered'] = False
        else:
            response_payload['retrainTriggered'] = False

        return jsonify(response_payload), 200

    except Exception as e:
        logger.error('Monitor endpoint error: %s', str(e))
        return jsonify({'error': 'Monitor check failed. Please check server logs.'}), 500

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
