const request = require('supertest');

describe('Health Monitoring and Predictive Analytics', () => {
  describe('Export Cache Performance', () => {
    const { exportPrediction, clearExportCache, getCacheStats } = require('../src/utils/exportUtils');
    
    const mockPrediction = {
      id: 'test-cache-id',
      modelId: 'model-id',
      userId: 'user-id',
      horizon: 3,
      predictions: [42.5, 43.1, 43.7],
      confidence: {
        lower: [40.2, 40.9, 41.5],
        upper: [44.8, 45.3, 45.9]
      },
      createdAt: new Date('2026-02-03T21:00:00Z')
    };

    beforeEach(() => {
      clearExportCache();
    });

    test('should cache export results for improved performance', () => {
      // First call should generate result
      const result1 = exportPrediction(mockPrediction, 'json');
      
      // Second call should return cached result
      const result2 = exportPrediction(mockPrediction, 'json');
      
      expect(result1).toBe(result2); // Same reference means cached
    });

    test('should track cache statistics', () => {
      exportPrediction(mockPrediction, 'json');
      exportPrediction(mockPrediction, 'csv');
      
      const stats = getCacheStats();
      expect(stats.size).toBeGreaterThan(0);
      expect(stats.ttl_ms).toBeDefined();
    });

    test('should cache different formats separately', () => {
      const jsonResult = exportPrediction(mockPrediction, 'json');
      const csvResult = exportPrediction(mockPrediction, 'csv');
      
      expect(typeof jsonResult).toBe('string');
      expect(typeof csvResult).toBe('string');
      expect(jsonResult).not.toBe(csvResult);
    });

    test('should clear cache when requested', () => {
      exportPrediction(mockPrediction, 'json');
      let stats = getCacheStats();
      expect(stats.size).toBeGreaterThan(0);
      
      clearExportCache();
      stats = getCacheStats();
      expect(stats.size).toBe(0);
    });
  });

  describe('Data Validation and Sanitization', () => {
    const { validatePrediction, exportToJSON } = require('../src/utils/exportUtils');

    test('should validate and sanitize prediction data', () => {
      const invalidPrediction = {
        id: 123, // Should be string
        modelId: null, // Should be string
        horizon: '5', // Should be number
        predictions: [1, 2, 'invalid', 4], // Should filter invalid values
        createdAt: null
      };

      const validated = validatePrediction(invalidPrediction);
      
      expect(typeof validated.id).toBe('string');
      expect(typeof validated.modelId).toBe('string');
      expect(typeof validated.horizon).toBe('number');
      expect(validated.horizon).toBe(5);
      expect(Array.isArray(validated.predictions)).toBe(true);
      expect(validated.createdAt).toBeDefined();
    });

    test('should handle missing prediction data gracefully', () => {
      expect(() => validatePrediction(null)).toThrow('Prediction data is required');
    });

    test('should sanitize numeric values in predictions array', () => {
      const prediction = {
        id: 'test',
        predictions: ['42.5', 'not-a-number', null, undefined, 43.7]
      };

      const validated = validatePrediction(prediction);
      
      expect(validated.predictions).toHaveLength(5);
      expect(validated.predictions[0]).toBe(42.5);
      expect(validated.predictions[1]).toBe(0); // Invalid becomes 0
      expect(validated.predictions[2]).toBe(0);
      expect(validated.predictions[3]).toBe(0);
      expect(validated.predictions[4]).toBe(43.7);
    });

    test('should export validated data', () => {
      const invalidPrediction = {
        id: 123,
        predictions: ['1', '2', 'bad']
      };

      const result = exportToJSON(invalidPrediction);
      const parsed = JSON.parse(result);
      
      expect(typeof parsed.id).toBe('string');
      expect(parsed.predictions[2]).toBe(0); // Sanitized
    });
  });

  describe('Fallback and Fail-Safe Mechanisms', () => {
    test('should provide fallback for invalid exports', () => {
      const { exportPrediction } = require('../src/utils/exportUtils');
      
      // Should not throw, should return JSON as fallback
      const result = exportPrediction({ id: 'test' }, 'unknown-format');
      expect(() => JSON.parse(result)).not.toThrow();
    });
  });

  describe('Cross-Platform Integration Reliability', () => {
    const { exportForManyChat, exportForBotBuilders, exportForOpenClaw, exportForMoltbook } = require('../src/utils/exportUtils');
    
    const mockPrediction = {
      id: 'platform-test',
      modelId: 'model-1',
      horizon: 5,
      predictions: [1, 2, 3, 4, 5],
      confidence: { lower: [0.8, 0.9, 1.0, 1.1, 1.2], upper: [1.2, 2.1, 3.0, 4.1, 5.2] },
      createdAt: new Date().toISOString()
    };

    test('should export for ManyChat with validated data', () => {
      const result = exportForManyChat(mockPrediction);
      expect(result.messaging_type).toBe('UPDATE');
      expect(result.custom_user_field.prediction_id).toBe('platform-test');
      expect(Array.isArray(result.custom_user_field.predictions)).toBe(true);
    });

    test('should export for BotBuilders with validated data', () => {
      const result = exportForBotBuilders(mockPrediction);
      expect(result.type).toBe('prediction_update');
      expect(result.data.predictionId).toBe('platform-test');
      expect(result.actions).toHaveLength(2);
    });

    test('should export for OpenClaw with validated data', () => {
      const result = exportForOpenClaw(mockPrediction);
      expect(result.event).toBe('prediction.created');
      expect(result.data.prediction_id).toBe('platform-test');
      expect(result.metadata.source).toBe('ai-time-machines');
    });

    test('should export for Moltbook with validated data', () => {
      const result = exportForMoltbook(mockPrediction);
      expect(Array.isArray(result.cells)).toBe(true);
      expect(result.cells.length).toBeGreaterThan(0);
      expect(result.metadata.prediction_id).toBe('platform-test');
    });

    test('should handle edge cases in platform exports', () => {
      const edgeCasePrediction = {
        id: null,
        predictions: []
      };

      expect(() => exportForManyChat(edgeCasePrediction)).not.toThrow();
      expect(() => exportForBotBuilders(edgeCasePrediction)).not.toThrow();
      expect(() => exportForOpenClaw(edgeCasePrediction)).not.toThrow();
      expect(() => exportForMoltbook(edgeCasePrediction)).not.toThrow();
    });
  });
});
