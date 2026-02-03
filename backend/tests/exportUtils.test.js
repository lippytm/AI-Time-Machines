const { exportPrediction, exportToCSV, exportToJSON, exportToXML } = require('../src/utils/exportUtils');

describe('Export Utils', () => {
  const mockPrediction = {
    id: 'test-id',
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

  describe('exportToJSON', () => {
    test('should export prediction to JSON format', () => {
      const result = exportToJSON(mockPrediction);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
      const parsed = JSON.parse(result);
      expect(parsed.id).toBe('test-id');
      expect(parsed.horizon).toBe(3);
      expect(parsed.predictions).toHaveLength(3);
    });

    test('should include metadata in JSON export', () => {
      const result = exportToJSON(mockPrediction);
      const parsed = JSON.parse(result);
      expect(parsed.metadata).toBeDefined();
      expect(parsed.metadata.userId).toBe('user-id');
    });
  });

  describe('exportToCSV', () => {
    test('should export prediction to CSV format', () => {
      const result = exportToCSV(mockPrediction);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
      expect(result).toContain('timestamp,value,confidence_lower,confidence_upper');
      expect(result).toContain('0,42.5,40.2,44.8');
    });

    test('should handle predictions without confidence intervals', () => {
      const predictionNoConfidence = {
        ...mockPrediction,
        confidence: null
      };
      const result = exportToCSV(predictionNoConfidence);
      expect(result).toBeTruthy();
      expect(result).toContain('timestamp,value,confidence_lower,confidence_upper');
    });
  });

  describe('exportToXML', () => {
    test('should export prediction to XML format', () => {
      const result = exportToXML(mockPrediction);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
      expect(result).toContain('<?xml version="1.0" encoding="UTF-8"?>');
      expect(result).toContain('<prediction>');
      expect(result).toContain('</prediction>');
      expect(result).toContain('<id>test-id</id>');
    });

    test('should include confidence intervals in XML', () => {
      const result = exportToXML(mockPrediction);
      expect(result).toContain('<confidence>');
      expect(result).toContain('<lower>');
      expect(result).toContain('<upper>');
    });

    test('should escape XML special characters', () => {
      const predictionWithSpecialChars = {
        ...mockPrediction,
        id: 'test&special<chars>'
      };
      const result = exportToXML(predictionWithSpecialChars);
      expect(result).toContain('&amp;');
      expect(result).toContain('&lt;');
      expect(result).toContain('&gt;');
    });
  });

  describe('exportPrediction', () => {
    test('should route to correct format handler', () => {
      const csvResult = exportPrediction(mockPrediction, 'csv');
      expect(csvResult).toContain('timestamp,value');

      const jsonResult = exportPrediction(mockPrediction, 'json');
      expect(jsonResult).toContain('"id"');

      const xmlResult = exportPrediction(mockPrediction, 'xml');
      expect(xmlResult).toContain('<?xml');
    });

    test('should default to JSON for unknown format', () => {
      const result = exportPrediction(mockPrediction, 'unknown');
      expect(typeof result).toBe('string');
      expect(() => JSON.parse(result)).not.toThrow();
    });
  });

  describe('Platform-specific exports', () => {
    test('should export for ManyChat format', () => {
      const result = exportPrediction(mockPrediction, 'manychat');
      expect(result).toHaveProperty('messaging_type', 'UPDATE');
      expect(result).toHaveProperty('message');
      expect(result.custom_user_field).toHaveProperty('prediction_id', 'test-id');
    });

    test('should export for BotBuilders format', () => {
      const result = exportPrediction(mockPrediction, 'botbuilders');
      expect(result).toHaveProperty('type', 'prediction_update');
      expect(result).toHaveProperty('data');
      expect(result.data).toHaveProperty('predictionId', 'test-id');
      expect(result).toHaveProperty('actions');
      expect(Array.isArray(result.actions)).toBe(true);
    });

    test('should export for OpenClaw format', () => {
      const result = exportPrediction(mockPrediction, 'openclaw');
      expect(result).toHaveProperty('event', 'prediction.created');
      expect(result).toHaveProperty('data');
      expect(result.data).toHaveProperty('prediction_id', 'test-id');
      expect(result).toHaveProperty('metadata');
      expect(result.metadata).toHaveProperty('source', 'ai-time-machines');
    });

    test('should export for Moltbook format', () => {
      const result = exportPrediction(mockPrediction, 'moltbook');
      expect(result).toHaveProperty('cells');
      expect(Array.isArray(result.cells)).toBe(true);
      expect(result.cells.length).toBeGreaterThan(0);
      expect(result.cells[0]).toHaveProperty('type', 'markdown');
      expect(result).toHaveProperty('metadata');
      expect(result.metadata).toHaveProperty('prediction_id', 'test-id');
    });
  });
});
