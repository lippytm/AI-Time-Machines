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
        # Updated to match new enhanced health check format
        self.assertIn('status', data)
        self.assertEqual(data['service'], 'AI Time Machines Python Service')
        self.assertIn('health_score', data)
        self.assertIn('system_metrics', data)
    
    def test_model_types(self):
        """Test get model types endpoint"""
        response = self.app.get('/api/models/types')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('models', data)
        self.assertIsInstance(data['models'], list)
        self.assertGreater(len(data['models']), 0)


if __name__ == '__main__':
    unittest.main()
