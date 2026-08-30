import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestPythonService(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'AI Time Machines Python Service')
    
    def test_model_types(self):
        """Test get model types endpoint"""
        response = self.app.get('/api/models/types')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('models', data)
        self.assertIsInstance(data['models'], list)
        self.assertGreater(len(data['models']), 0)
        
        types = [m['type'] for m in data['models']]
        self.assertIn('lstm', types)
        self.assertIn('gru', types)

    def test_monitor_missing_fields(self):
        """Monitor endpoint should return 400 when required fields are missing"""
        response = self.app.post('/api/monitor', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_monitor_insufficient_data(self):
        """Monitor endpoint should return 400 when fewer than 2 data points are provided"""
        response = self.app.post('/api/monitor', json={
            'modelId': 'test-id',
            'recentData': [{'timestamp': '2026-01-01', 'value': 1.0}],
            'baselineMetrics': {'test_loss': 0.01}
        })
        self.assertEqual(response.status_code, 400)

    def test_monitor_invalid_model_id(self):
        """Monitor endpoint should return 400 for model IDs with invalid characters"""
        response = self.app.post('/api/monitor', json={
            'modelId': '../etc/passwd',
            'recentData': [
                {'timestamp': '2026-01-01', 'value': 1.0},
                {'timestamp': '2026-01-02', 'value': 2.0}
            ],
            'baselineMetrics': {'test_loss': 0.01}
        })
        self.assertEqual(response.status_code, 400)

    def test_monitor_model_not_found(self):
        """Monitor endpoint should return 404 when model file does not exist"""
        response = self.app.post('/api/monitor', json={
            'modelId': 'nonexistent-model-12345',
            'recentData': [
                {'timestamp': '2026-01-01', 'value': 1.0},
                {'timestamp': '2026-01-02', 'value': 2.0}
            ],
            'baselineMetrics': {'test_loss': 0.01}
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
