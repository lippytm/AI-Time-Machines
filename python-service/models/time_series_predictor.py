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
            self.model = LSTMModel(use_gru=False)
        elif self.model_type == 'gru':
            self.model = LSTMModel(use_gru=True)
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

    def detect_drift(self, recent_data, baseline_metrics, drift_threshold=0.05):
        """Detect performance drift by comparing current loss against baseline.

        Args:
            recent_data: list of {timestamp, value} dicts – the new observations.
            baseline_metrics: dict containing at least 'test_loss'.
            drift_threshold: fractional increase in loss that triggers a drift alert.

        Returns:
            dict with drift_detected, current_loss, drift_score, and message.
        """
        if self.model is None:
            raise ValueError("Model not initialized or loaded")

        baseline_loss = float(baseline_metrics.get('test_loss', 0))

        if self.model_type in ['lstm', 'gru']:
            values = [
                point['value'] if isinstance(point, dict) else point
                for point in recent_data
            ]

            if len(values) <= self.model.sequence_length:
                return {
                    'drift_detected': False,
                    'current_loss': None,
                    'baseline_loss': baseline_loss,
                    'drift_score': 0.0,
                    'message': 'Not enough data points to evaluate drift'
                }

            # Evaluate model on recent data using mean absolute error
            import numpy as np  # noqa: PLC0415
            scaler = self.model.scaler
            seq_len = self.model.sequence_length

            scaled = scaler.transform(np.array(values).reshape(-1, 1))
            X, y_true = [], []
            for i in range(len(scaled) - seq_len):
                X.append(scaled[i:i + seq_len])
                y_true.append(scaled[i + seq_len, 0])

            X = np.array(X)
            y_true = np.array(y_true)
            y_pred = self.model.model.predict(X, verbose=0).flatten()

            current_loss = float(np.mean(np.abs(y_pred - y_true)))
        else:
            # Non-neural models: use a simple variance-based proxy
            vals = [p['value'] if isinstance(p, dict) else p for p in recent_data]
            current_loss = float(np.std(vals)) if len(vals) > 1 else 0.0

        drift_score = (
            (current_loss - baseline_loss) / baseline_loss
            if baseline_loss > 0 else 0.0
        )
        drift_detected = drift_score > drift_threshold

        return {
            'drift_detected': drift_detected,
            'current_loss': round(current_loss, 6),
            'baseline_loss': round(baseline_loss, 6),
            'drift_score': round(drift_score, 6),
            'message': (
                f'Drift detected: loss increased by {drift_score:.1%} '
                f'(threshold {drift_threshold:.1%})'
                if drift_detected
                else 'No significant drift detected'
            )
        }

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
