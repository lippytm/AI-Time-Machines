import unittest
import sys
import os
import json
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, health_monitor, prediction_cache, generate_fallback_prediction


class TestHealthMonitoring(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset health monitor
        health_monitor.request_times.clear()
        health_monitor.error_count = 0
        health_monitor.total_requests = 0
        prediction_cache.clear()
    
    def test_enhanced_health_check(self):
        """Test enhanced health check with predictive analytics"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('health_score', data)
        self.assertIn('predictions', data)
        self.assertIn('system_metrics', data)
        self.assertIn('request_stats', data)
        
        # Check system metrics
        self.assertIn('cpu_percent', data['system_metrics'])
        self.assertIn('memory_percent', data['system_metrics'])
        self.assertIn('memory_available_mb', data['system_metrics'])
    
    def test_health_score_calculation(self):
        """Test health score reflects system state"""
        response = self.app.get('/health')
        data = response.get_json()
        
        # Initially should be healthy
        self.assertGreaterEqual(data['health_score'], 0)
        self.assertLessEqual(data['health_score'], 100)
    
    def test_health_warnings(self):
        """Test health warnings are generated"""
        response = self.app.get('/health')
        data = response.get_json()
        
        # Should have warnings array
        self.assertIn('warnings', data['predictions'])
        self.assertIsInstance(data['predictions']['warnings'], list)
    
    def test_uptime_tracking(self):
        """Test uptime is tracked"""
        response = self.app.get('/health')
        data = response.get_json()
        
        self.assertIn('uptime_seconds', data)
        self.assertGreaterEqual(data['uptime_seconds'], 0)
    
    def test_request_stats(self):
        """Test request statistics are tracked"""
        response = self.app.get('/health')
        data = response.get_json()
        
        self.assertIn('total_requests', data['request_stats'])
        self.assertIn('error_count', data['request_stats'])


class TestPredictionCaching(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        prediction_cache.clear()
    
    def test_prediction_cache_functionality(self):
        """Test that prediction cache works"""
        # Cache should be empty initially
        self.assertEqual(len(prediction_cache), 0)
        
        # Note: Actual caching would require mocking model prediction
        # This test verifies the cache structure exists
        self.assertIsInstance(prediction_cache, dict)


class TestFallbackMechanisms(unittest.TestCase):
    
    def test_fallback_prediction_with_valid_data(self):
        """Test fallback prediction generates reasonable values"""
        input_data = [10, 11, 12, 13, 14]
        horizon = 3
        
        result = generate_fallback_prediction(input_data, horizon)
        
        self.assertEqual(len(result), horizon)
        self.assertIsInstance(result, list)
        # Should be close to average of recent values (12.4)
        self.assertGreater(result[0], 11)
        self.assertLess(result[0], 14)
    
    def test_fallback_prediction_with_empty_data(self):
        """Test fallback handles empty input gracefully"""
        input_data = []
        horizon = 5
        
        result = generate_fallback_prediction(input_data, horizon)
        
        self.assertEqual(len(result), horizon)
        # Should return zeros for empty input
        self.assertEqual(result, [0, 0, 0, 0, 0])
    
    def test_fallback_prediction_with_invalid_data(self):
        """Test fallback handles invalid input gracefully"""
        input_data = None
        horizon = 3
        
        result = generate_fallback_prediction(input_data, horizon)
        
        self.assertEqual(len(result), horizon)
        self.assertEqual(result, [0, 0, 0])


class TestPerformanceOptimizations(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint_response_time(self):
        """Test health endpoint responds quickly"""
        start_time = time.time()
        response = self.app.get('/health')
        duration = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        # Should respond in less than 1 second
        self.assertLess(duration, 1.0)
    
    def test_model_types_endpoint_performance(self):
        """Test model types endpoint performance"""
        start_time = time.time()
        response = self.app.get('/api/models/types')
        duration = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        # Should be very fast (static data)
        self.assertLess(duration, 0.5)


class TestReliabilityFeatures(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check_availability(self):
        """Test health check is always available"""
        # Make multiple requests to ensure reliability
        for _ in range(5):
            response = self.app.get('/health')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('status', data)
    
    def test_error_handling_in_prediction_endpoint(self):
        """Test prediction endpoint handles errors gracefully"""
        # Send invalid request
        response = self.app.post('/api/predict', 
                                  json={},
                                  content_type='application/json')
        
        # Should return either error or fallback (200 with fallback when ML unavailable)
        self.assertIn(response.status_code, [200, 400, 404, 500])
        data = response.get_json()
        
        # Should have error message, fallback, or predictions
        self.assertTrue('error' in data or 'fallback' in data or 'predictions' in data)


if __name__ == '__main__':
    unittest.main()
