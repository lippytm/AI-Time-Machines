import joblib
import numpy as np
from models.lstm_model import LSTMModel


class TimeSeriesPredictor:
    """Unified interface for different time series models"""

    def __init__(self, model_type='lstm'):
        self.model_type = model_type
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the appropriate model based on type"""
        if self.model_type == 'lstm':
            self.model = LSTMModel()
        elif self.model_type == 'gru':
            # Similar to LSTM but using GRU layers
            self.model = LSTMModel()  # Placeholder - would use GRU variant
        elif self.model_type == 'arima':
            # Would use statsmodels ARIMA
            pass
        elif self.model_type == 'prophet':
            # Would use Facebook Prophet
            pass
        elif self.model_type == 'transformer':
            # Would use transformer-based model
            pass
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def train(self, data, model_id, hyperparameters=None):
        """Train the model on provided data"""
        if hyperparameters is None:
            hyperparameters = {}

        # Extract hyperparameters
        epochs = hyperparameters.get('epochs', 50)
        batch_size = hyperparameters.get('batch_size', 32)

        # Train based on model type
        if self.model_type in ['lstm', 'gru']:
            metrics = self.model.train(
                data=data,
                epochs=epochs,
                batch_size=batch_size
            )
        else:
            # Placeholder for other model types
            metrics = {
                'training_loss': 0.0,
                'test_loss': 0.0,
                'training_time': 0
            }

        return metrics

    def predict(self, input_data, horizon=10):
        """Generate predictions"""
        if self.model is None:
            raise ValueError("Model not initialized or loaded")

        if self.model_type in ['lstm', 'gru']:
            # Extract values from input data
            if isinstance(input_data, list):
                values = [point['value'] if isinstance(point, dict) else point for point in input_data]
            else:
                values = input_data

            predictions = self.model.predict(values, horizon=horizon)

            # Calculate simple confidence intervals (placeholder)
            confidence = {
                'lower': [p * 0.9 for p in predictions],
                'upper': [p * 1.1 for p in predictions]
            }

            return predictions, confidence
        else:
            # Placeholder for other model types
            return [], {}

    def save(self, path):
        """Save the trained model"""
        joblib.dump({
            'model_type': self.model_type,
            'model': self.model
        }, path)

    def load(self, path):
        """Load a trained model"""
        saved_data = joblib.load(path)
        self.model_type = saved_data['model_type']
        self.model = saved_data['model']
