const MyClaw = require('../src/myclaw');

// Mock the https and http modules
jest.mock('https');
jest.mock('http');

describe('MyClaw', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.MYCLAW_API_KEY;
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.MYCLAW_API_KEY = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when API key is not provided', () => {
      delete process.env.MYCLAW_API_KEY;
      expect(() => new MyClaw()).toThrow('MyClaw API key is required');
    });

    test('should initialize with API key from environment', () => {
      process.env.MYCLAW_API_KEY = 'test-key';
      const client = new MyClaw();
      expect(client).toBeDefined();
      expect(client.baseUrl).toBe('https://myclaw.io/api');
      expect(client.version).toBe('1.0');
      expect(client.source).toBe('ai-time-machines');
    });

    test('should initialize with API key from constructor parameter', () => {
      const client = new MyClaw('custom-key');
      expect(client).toBeDefined();
      expect(client.apiKey).toBe('custom-key');
    });
  });

  describe('sendEvent', () => {
    test('should send an event to MyClaw', async () => {
      process.env.MYCLAW_API_KEY = 'test-key';
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ success: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.sendEvent('test.event', { key: 'value' });

      expect(https.request).toHaveBeenCalled();
      expect(result).toEqual({ success: true });
    });

    test('should include correct event structure', async () => {
      process.env.MYCLAW_API_KEY = 'test-key';
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ success: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      await client.sendEvent('prediction.created', { id: 'abc123' });

      expect(capturedBody).toHaveProperty('event', 'prediction.created');
      expect(capturedBody).toHaveProperty('timestamp');
      expect(capturedBody).toHaveProperty('data', { id: 'abc123' });
      expect(capturedBody.metadata).toHaveProperty('source', 'ai-time-machines');
      expect(capturedBody.metadata).toHaveProperty('version', '1.0');
    });

    test('should reject on API error response', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 401,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ message: 'Unauthorized' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('invalid-key');
      await expect(client.sendEvent('test.event', {})).rejects.toThrow('MyClaw API Error');
    });
  });

  describe('sendPrediction', () => {
    test('should send a prediction event to MyClaw', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ success: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const mockPrediction = {
        id: 'pred-123',
        modelId: 'model-456',
        horizon: 5,
        predictions: [42.5, 43.1, 43.7, 44.2, 44.8],
        confidence: {
          lower: [40.2, 40.9, 41.5, 42.0, 42.5],
          upper: [44.8, 45.3, 45.9, 46.4, 47.1],
        },
      };

      const client = new MyClaw('test-key');
      await client.sendPrediction(mockPrediction);

      expect(capturedBody).toHaveProperty('event', 'prediction.created');
      expect(capturedBody.data).toHaveProperty('prediction_id', 'pred-123');
      expect(capturedBody.data).toHaveProperty('model_id', 'model-456');
      expect(capturedBody.data.metrics).toHaveProperty('horizon', 5);
      expect(capturedBody.data.metrics).toHaveProperty('prediction_count', 5);
      expect(capturedBody.data.metrics).toHaveProperty('has_confidence', true);
    });

    test('should handle prediction without confidence intervals', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ success: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const mockPrediction = {
        id: 'pred-789',
        modelId: 'model-101',
        horizon: 3,
        predictions: [10.0, 11.0, 12.0],
        confidence: null,
      };

      const client = new MyClaw('test-key');
      await client.sendPrediction(mockPrediction);

      expect(capturedBody.data.metrics).toHaveProperty('has_confidence', false);
    });
  });

  describe('updateDashboard', () => {
    test('should update a dashboard widget in MyClaw', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ widget_id: 'widget-123', status: 'updated' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.updateDashboard('widget-123', { title: 'Predictions Chart' });

      expect(capturedBody).toHaveProperty('widget_id', 'widget-123');
      expect(capturedBody).toHaveProperty('data', { title: 'Predictions Chart' });
      expect(capturedBody).toHaveProperty('source', 'ai-time-machines');
      expect(result).toHaveProperty('status', 'updated');
    });

    test('should update dashboard widget with no data', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ status: 'updated' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      await client.updateDashboard('widget-456');

      expect(capturedBody).toHaveProperty('data', {});
    });
  });

  describe('getAnalytics', () => {
    test('should retrieve analytics from MyClaw', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ analytics: [] }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.getAnalytics({ groupBy: 'day' });

      expect(https.request).toHaveBeenCalled();
      expect(result).toHaveProperty('analytics');
    });

    test('should build correct query params for analytics', async () => {
      const https = require('https');

      let capturedOptions = null;
      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ analytics: [] }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        capturedOptions = options;
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      await client.getAnalytics({
        startDate: '2026-01-01',
        endDate: '2026-02-01',
        metrics: ['predictions', 'accuracy'],
        groupBy: 'week',
      });

      expect(capturedOptions.path).toContain('start_date=2026-01-01');
      expect(capturedOptions.path).toContain('end_date=2026-02-01');
      expect(capturedOptions.path).toContain('metrics=predictions%2Caccuracy');
      expect(capturedOptions.path).toContain('group_by=week');
    });
  });

  describe('_request', () => {
    test('should handle network errors', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn((event, cb) => {
          if (event === 'error') cb(new Error('Network error'));
        }),
      };

      https.request = jest.fn((options, cb) => mockReq);

      const client = new MyClaw('test-key');
      await expect(client.sendEvent('test.event', {})).rejects.toThrow('MyClaw Request Error');
    });

    test('should handle non-JSON response', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb('OK');
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.sendEvent('test.event', {});
      expect(result).toHaveProperty('raw', 'OK');
    });
  });
});
