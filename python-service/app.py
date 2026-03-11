import os
import time
import psutil
import hashlib
from collections import deque
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import model trainers and predictors (may not be available in test env)
try:
    from models.lstm_model import LSTMModel
    from models.time_series_predictor import TimeSeriesPredictor
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logger.warning("ML models not available. Running in limited mode.")

# Load environment variables
load_dotenv('../.env')

app = Flask(__name__)
CORS(app)

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
MODEL_STORAGE_PATH = os.getenv('MODEL_STORAGE_PATH', './saved_models')

# Ensure model storage directory exists
os.makedirs(MODEL_STORAGE_PATH, exist_ok=True)

# Health monitoring and metrics
class HealthMonitor:
    """ML-powered health monitoring with predictive analytics"""
    def __init__(self, max_history=100):
        self.request_times = deque(maxlen=max_history)
        self.error_count = 0
        self.total_requests = 0
        self.start_time = time.time()
        self.cpu_history = deque(maxlen=max_history)
        self.memory_history = deque(maxlen=max_history)
        
    def record_request(self, duration, is_error=False):
        """Record request metrics"""
        self.request_times.append(duration)
        self.total_requests += 1
        if is_error:
            self.error_count += 1
            
    def collect_system_metrics(self):
        """Collect system resource metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        self.cpu_history.append(cpu_percent)
        self.memory_history.append(memory.percent)
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_mb': memory.available / (1024 * 1024)
        }
    
    def predict_health_status(self):
        """Predict service health using simple ML heuristics"""
        # Calculate average response time
        avg_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        
        # Calculate error rate
        error_rate = (self.error_count / self.total_requests * 100) if self.total_requests > 0 else 0
        
        # Get current system metrics
        metrics = self.collect_system_metrics()
        
        # Predictive health scoring
        health_score = 100
        warnings = []
        
        # Response time threshold (>2s is concerning)
        if avg_response_time > 2.0:
            health_score -= 20
            warnings.append('High average response time detected')
        
        # Error rate threshold (>5% is concerning)
        if error_rate > 5:
            health_score -= 30
            warnings.append('High error rate detected')
        
        # CPU threshold (>80% is concerning)
        if metrics['cpu_percent'] > 80:
            health_score -= 25
            warnings.append('High CPU usage detected')
        
        # Memory threshold (>85% is concerning)
        if metrics['memory_percent'] > 85:
            health_score -= 25
            warnings.append('High memory usage detected')
        
        # Determine status
        if health_score >= 80:
            status = 'healthy'
        elif health_score >= 60:
            status = 'degraded'
        else:
            status = 'unhealthy'
        
        return {
            'status': status,
            'health_score': health_score,
            'warnings': warnings,
            'metrics': metrics,
            'avg_response_time': avg_response_time,
            'error_rate': error_rate
        }
    
    def get_uptime(self):
        """Get service uptime in seconds"""
        return time.time() - self.start_time

# Initialize health monitor
health_monitor = HealthMonitor()

@app.route('/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint with predictive analytics"""
    health_status = health_monitor.predict_health_status()
    
    return jsonify({
        'status': health_status['status'],
        'service': 'AI Time Machines Python Service',
        'version': '1.0.0',
        'uptime_seconds': health_monitor.get_uptime(),
        'health_score': health_status['health_score'],
        'predictions': {
            'warnings': health_status['warnings'],
            'avg_response_time_ms': health_status['avg_response_time'] * 1000,
            'error_rate_percent': health_status['error_rate']
        },
        'system_metrics': health_status['metrics'],
        'request_stats': {
            'total_requests': health_monitor.total_requests,
            'error_count': health_monitor.error_count
        }
    }), 200 if health_status['status'] in ['healthy', 'degraded'] else 503

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train a time series model with retry logic and fallback"""
    start_time = time.time()
    
    if not ML_AVAILABLE:
        health_monitor.record_request(time.time() - start_time, is_error=True)
        return jsonify({'error': 'ML models not available in this environment'}), 503
    
    try:
        data = request.json
        model_id = data.get('modelId')
        time_series_data = data.get('timeSeriesData')
        model_type = data.get('modelType', 'lstm')
        hyperparameters = data.get('hyperparameters', {})

        if not model_id or not time_series_data:
            health_monitor.record_request(time.time() - start_time, is_error=True)
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

        # Notify backend of completion with retry logic
        notify_backend_with_retry(
            endpoint=f'{BACKEND_URL}/api/models/{model_id}/status',
            payload={
                'status': 'completed',
                'metrics': metrics,
                'modelPath': model_path,
                'trainingDuration': metrics.get('training_time', 0)
            }
        )

        duration = time.time() - start_time
        health_monitor.record_request(duration, is_error=False)

        return jsonify({
            'message': 'Model trained successfully',
            'modelId': model_id,
            'metrics': metrics,
            'training_duration_seconds': duration
        }), 200

    except Exception as e:
        # Notify backend of failure with retry logic
        if 'model_id' in locals():
            notify_backend_with_retry(
                endpoint=f'{BACKEND_URL}/api/models/{model_id}/status',
                payload={'status': 'failed', 'error': str(e)}
            )

        duration = time.time() - start_time
        health_monitor.record_request(duration, is_error=True)
        return jsonify({'error': str(e)}), 500

# Prediction cache for improved performance
prediction_cache = {}
CACHE_TTL = 300  # 5 minutes

@app.route('/api/predict', methods=['POST'])
def generate_prediction():
    """Generate predictions with caching and performance optimization"""
    start_time = time.time()
    
    if not ML_AVAILABLE:
        # Use fallback mechanism when ML is not available
        try:
            data = request.json
            input_data = data.get('inputData', [])
            horizon = data.get('horizon', 10)
            
            fallback_predictions = generate_fallback_prediction(input_data, horizon)
            duration = time.time() - start_time
            health_monitor.record_request(duration, is_error=False)
            
            return jsonify({
                'predictions': fallback_predictions,
                'confidence': None,
                'horizon': horizon,
                'fallback': True,
                'fallback_reason': 'ML models not available',
                'inference_time_ms': duration * 1000
            }), 200
        except Exception as e:
            duration = time.time() - start_time
            health_monitor.record_request(duration, is_error=True)
            return jsonify({'error': str(e)}), 500
    
    try:
        data = request.json
        model_id = data.get('modelId')
        model_path = data.get('modelPath')
        model_type = data.get('modelType', 'lstm')
        input_data = data.get('inputData')
        horizon = data.get('horizon', 10)

        # Generate deterministic cache key using MD5
        cache_data = f"{model_id}_{str(input_data)}_{horizon}"
        cache_key = hashlib.md5(cache_data.encode()).hexdigest()
        
        # Check cache for improved response time
        if cache_key in prediction_cache:
            cache_entry = prediction_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < CACHE_TTL:
                duration = time.time() - start_time
                health_monitor.record_request(duration, is_error=False)
                
                response = cache_entry['data'].copy()
                response['cached'] = True
                response['cache_age_seconds'] = time.time() - cache_entry['timestamp']
                return jsonify(response), 200

        if not model_path or not os.path.exists(model_path):
            health_monitor.record_request(time.time() - start_time, is_error=True)
            return jsonify({'error': 'Model not found'}), 404

        # Initialize predictor and load model
        predictor = TimeSeriesPredictor(model_type=model_type)
        predictor.load(model_path)

        # Generate predictions
        predictions, confidence = predictor.predict(
            input_data=input_data,
            horizon=horizon
        )

        duration = time.time() - start_time
        health_monitor.record_request(duration, is_error=False)

        response_data = {
            'predictions': predictions,
            'confidence': confidence,
            'horizon': horizon,
            'inference_time_ms': duration * 1000,
            'cached': False
        }

        # Store in cache
        prediction_cache[cache_key] = {
            'data': response_data.copy(),
            'timestamp': time.time()
        }

        return jsonify(response_data), 200

    except Exception as e:
        duration = time.time() - start_time
        health_monitor.record_request(duration, is_error=True)
        
        # Fallback mechanism: return simple baseline prediction
        if 'input_data' in locals() and 'horizon' in locals():
            fallback_predictions = generate_fallback_prediction(input_data, horizon)
            return jsonify({
                'predictions': fallback_predictions,
                'confidence': None,
                'horizon': horizon,
                'fallback': True,
                'fallback_reason': str(e)
            }), 200
        
        return jsonify({'error': str(e)}), 500

def generate_fallback_prediction(input_data, horizon):
    """Generate simple baseline predictions as fallback"""
    try:
        # Simple moving average fallback
        if isinstance(input_data, list) and len(input_data) > 0:
            last_values = input_data[-min(5, len(input_data)):]
            avg = sum(last_values) / len(last_values)
            return [avg] * horizon
        return [0] * horizon
    except:
        return [0] * horizon

def notify_backend_with_retry(endpoint, payload, max_retries=3):
    """Notify backend with exponential backoff retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.put(
                endpoint,
                json=payload,
                timeout=5
            )
            if response.status_code < 500:
                return response
        except Exception as e:
            if attempt == max_retries - 1:
                print(f'Failed to notify backend after {max_retries} attempts: {str(e)}')
                raise
            # Exponential backoff: 1s, 2s, 4s
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    return None

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
