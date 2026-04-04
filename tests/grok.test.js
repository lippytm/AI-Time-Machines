const Grok = require('../src/grok');

jest.mock('https');

describe('Grok', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.GROK_API_KEY;
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.GROK_API_KEY = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when API key is not provided', () => {
      delete process.env.GROK_API_KEY;
      expect(() => new Grok()).toThrow('Grok API key is required');
    });

    test('should initialize with API key from environment', () => {
      process.env.GROK_API_KEY = 'test-key';
      const grok = new Grok();
      expect(grok).toBeDefined();
      expect(grok.model).toBe('grok-beta');
      expect(grok.baseUrl).toBe('https://api.x.ai/v1');
    });

    test('should initialize with API key from constructor parameter', () => {
      const grok = new Grok('custom-key');
      expect(grok).toBeDefined();
      expect(grok.apiKey).toBe('custom-key');
    });
  });

  describe('setModel', () => {
    test('should update the model', () => {
      process.env.GROK_API_KEY = 'test-key';
      const grok = new Grok();
      grok.setModel('grok-vision-beta');
      expect(grok.model).toBe('grok-vision-beta');
    });
  });

  describe('getAvailableModels', () => {
    test('should return list of available models', () => {
      process.env.GROK_API_KEY = 'test-key';
      const grok = new Grok();
      const models = grok.getAvailableModels();
      expect(Array.isArray(models)).toBe(true);
      expect(models).toContain('grok-beta');
      expect(models).toContain('grok-vision-beta');
    });
  });

  describe('chat', () => {
    test('should send a chat message and return response', async () => {
      process.env.GROK_API_KEY = 'test-key';
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({
            choices: [{ message: { content: 'Grok response' } }]
          }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const grok = new Grok('test-key');
      const response = await grok.chat('Hello Grok');

      expect(https.request).toHaveBeenCalled();
      expect(response).toBe('Grok response');
    });

    test('should reject on API error', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 401,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ error: { message: 'Unauthorized' } }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const grok = new Grok('invalid-key');
      await expect(grok.chat('Hello')).rejects.toThrow('Grok API Error');
    });
  });

  describe('conversation', () => {
    test('should handle conversation with context', async () => {
      process.env.GROK_API_KEY = 'test-key';
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({
            choices: [{ message: { content: 'Conversation response' } }]
          }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const grok = new Grok('test-key');
      const messages = [
        { role: 'user', content: 'Analyze my predictions' },
        { role: 'assistant', content: 'Sure, share the data.' },
        { role: 'user', content: 'Here it is: [1, 2, 3]' },
      ];

      const response = await grok.conversation(messages);
      expect(response).toBe('Conversation response');
    });
  });

  describe('analyzePrediction', () => {
    test('should analyze a prediction and return insights', async () => {
      process.env.GROK_API_KEY = 'test-key';
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
          if (event === 'data') cb(JSON.stringify({
            choices: [{ message: { content: 'Trend is upward.' } }]
          }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const grok = new Grok('test-key');
      const prediction = {
        id: 'pred-123',
        horizon: 5,
        predictions: [10, 12, 14, 16, 18],
        confidence: { lower: [9, 11, 13, 15, 17], upper: [11, 13, 15, 17, 19] },
      };

      const result = await grok.analyzePrediction(prediction, 'Stock market data');
      expect(result).toBe('Trend is upward.');
      expect(capturedBody.messages[0].content).toContain('pred-123');
      expect(capturedBody.messages[0].content).toContain('Stock market data');
    });

    test('should handle prediction without confidence intervals', async () => {
      process.env.GROK_API_KEY = 'test-key';
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
          if (event === 'data') cb(JSON.stringify({
            choices: [{ message: { content: 'Analysis complete.' } }]
          }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const grok = new Grok('test-key');
      const prediction = { id: 'pred-456', horizon: 3, predictions: [1, 2, 3], confidence: null };
      const result = await grok.analyzePrediction(prediction);

      expect(result).toBe('Analysis complete.');
      expect(capturedBody.messages[0].content).toContain('No confidence intervals provided');
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

      https.request = jest.fn(() => mockReq);

      const grok = new Grok('test-key');
      await expect(grok.chat('Hello')).rejects.toThrow('Grok Request Error');
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

      const grok = new Grok('test-key');
      const result = await grok._request('GET', '/test');
      expect(result).toHaveProperty('raw', 'OK');
    });
  });
});
