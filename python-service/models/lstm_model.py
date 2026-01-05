import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import time


class LSTMModel:
    """LSTM-based time series forecasting model"""

    def __init__(self, sequence_length=30, units=50, dropout=0.2):
        self.sequence_length = sequence_length
        self.units = units
        self.dropout = dropout
        self.model = None
        self.scaler = MinMaxScaler()

    def prepare_data(self, data, test_size=0.2):
        """Prepare time series data for LSTM training"""
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # Extract values and scale
        values = df['value'].values.reshape(-1, 1)
        scaled_values = self.scaler.fit_transform(values)

        # Create sequences
        X, y = [], []
        for i in range(len(scaled_values) - self.sequence_length):
            X.append(scaled_values[i:i + self.sequence_length])
            y.append(scaled_values[i + self.sequence_length])

        X = np.array(X)
        y = np.array(y)

        # Split train/test
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        return X_train, X_test, y_train, y_test

    def build_model(self):
        """Build LSTM model architecture"""
        model = keras.Sequential([
            layers.LSTM(self.units, return_sequences=True, input_shape=(self.sequence_length, 1)),
            layers.Dropout(self.dropout),
            layers.LSTM(self.units, return_sequences=False),
            layers.Dropout(self.dropout),
            layers.Dense(25),
            layers.Dense(1)
        ])

        model.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['mae']
        )

        self.model = model
        return model

    def train(self, data, epochs=50, batch_size=32, validation_split=0.1):
        """Train the LSTM model"""
        start_time = time.time()

        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_data(data)

        # Build model if not already built
        if self.model is None:
            self.build_model()

        # Train model
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=0
        )

        # Evaluate on test set
        test_loss, test_mae = self.model.evaluate(X_test, y_test, verbose=0)

        training_time = time.time() - start_time

        return {
            'training_loss': float(history.history['loss'][-1]),
            'validation_loss': float(history.history['val_loss'][-1]),
            'test_loss': float(test_loss),
            'test_mae': float(test_mae),
            'training_time': int(training_time),
            'epochs': epochs
        }

    def predict(self, input_sequence, horizon=10):
        """Generate predictions for future time steps"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")

        # Ensure input is properly shaped
        current_sequence = np.array(input_sequence[-self.sequence_length:]).reshape(-1, 1)
        current_sequence = self.scaler.transform(current_sequence)

        predictions = []
        for _ in range(horizon):
            # Predict next value
            pred = self.model.predict(current_sequence.reshape(1, self.sequence_length, 1), verbose=0)
            predictions.append(pred[0, 0])

            # Update sequence with prediction
            current_sequence = np.append(current_sequence[1:], pred).reshape(-1, 1)

        # Inverse transform predictions
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

        return predictions.flatten().tolist()
