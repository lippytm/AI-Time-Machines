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

  describe('sendNotification', () => {
    test('should send a notification to MyClaw', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ success: true, notificationId: 'notif-123' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.sendNotification('email', { title: 'Test', body: 'Hello' });

      expect(https.request).toHaveBeenCalled();
      expect(result).toEqual({ success: true, notificationId: 'notif-123' });
    });

    test('should include correct notification structure', async () => {
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
      await client.sendNotification('sms', { title: 'Alert', body: 'Prediction ready' });

      expect(capturedBody).toHaveProperty('channel', 'sms');
      expect(capturedBody).toHaveProperty('message', { title: 'Alert', body: 'Prediction ready' });
      expect(capturedBody).toHaveProperty('timestamp');
      expect(capturedBody).toHaveProperty('source', 'ai-time-machines');
      expect(capturedBody).toHaveProperty('version', '1.0');
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
      await expect(client.sendNotification('email', {})).rejects.toThrow('MyClaw API Error');
    });
  });

  describe('sendPredictionAlert', () => {
    test('should send a prediction alert via MyClaw', async () => {
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
      await client.sendPredictionAlert(mockPrediction, 'email');

      expect(capturedBody).toHaveProperty('channel', 'email');
      expect(capturedBody.message).toHaveProperty('title');
      expect(capturedBody.message).toHaveProperty('body');
      expect(capturedBody.message.data).toHaveProperty('prediction_id', 'pred-123');
      expect(capturedBody.message.data).toHaveProperty('model_id', 'model-456');
      expect(capturedBody.message.data).toHaveProperty('horizon', 5);
      expect(capturedBody.message.data).toHaveProperty('prediction_count', 5);
      expect(capturedBody.message.data).toHaveProperty('has_confidence', true);
    });

    test('should default to email channel', async () => {
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
      await client.sendPredictionAlert(mockPrediction);

      expect(capturedBody).toHaveProperty('channel', 'email');
      expect(capturedBody.message.data).toHaveProperty('has_confidence', false);
    });
  });

  describe('upsertWidget', () => {
    test('should create a new widget when no widgetId provided', async () => {
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
          if (event === 'data') cb(JSON.stringify({ widget_id: 'new-widget-123' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        capturedOptions = options;
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.upsertWidget(null, { title: 'Forecast Chart', type: 'line' });

      expect(capturedOptions.method).toBe('POST');
      expect(capturedOptions.path).toBe('/api/widgets');
      expect(result).toHaveProperty('widget_id', 'new-widget-123');
    });

    test('should update an existing widget when widgetId is provided', async () => {
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
          if (event === 'data') cb(JSON.stringify({ widget_id: 'widget-123', updated: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        capturedOptions = options;
        cb(mockRes);
        return mockReq;
      });

      const client = new MyClaw('test-key');
      const result = await client.upsertWidget('widget-123', { title: 'Updated Chart' });

      expect(capturedOptions.method).toBe('PUT');
      expect(capturedOptions.path).toBe('/api/widgets/widget-123');
      expect(result).toHaveProperty('updated', true);
    });
  });

  describe('syncPredictionToDashboard', () => {
    test('should sync prediction data to a MyClaw dashboard', async () => {
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
          if (event === 'data') cb(JSON.stringify({ synced: true }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const mockPrediction = {
        id: 'pred-sync-123',
        modelId: 'model-sync-456',
        horizon: 7,
        predictions: [1, 2, 3, 4, 5, 6, 7],
        confidence: { lower: [0, 1, 2, 3, 4, 5, 6], upper: [2, 3, 4, 5, 6, 7, 8] },
      };

      const client = new MyClaw('test-key');
      const result = await client.syncPredictionToDashboard(mockPrediction, 'dash-abc');

      expect(capturedBody).toHaveProperty('dashboard_id', 'dash-abc');
      expect(capturedBody).toHaveProperty('prediction_id', 'pred-sync-123');
      expect(capturedBody).toHaveProperty('model_id', 'model-sync-456');
      expect(capturedBody.metrics).toHaveProperty('horizon', 7);
      expect(capturedBody.metrics).toHaveProperty('prediction_count', 7);
      expect(capturedBody.metrics).toHaveProperty('has_confidence', true);
      expect(capturedBody).toHaveProperty('source', 'ai-time-machines');
      expect(result).toHaveProperty('synced', true);
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
      await expect(client.sendNotification('email', {})).rejects.toThrow('MyClaw Request Error');
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
      const result = await client.sendNotification('push', {});
      expect(result).toHaveProperty('raw', 'OK');
    });
  });
});
