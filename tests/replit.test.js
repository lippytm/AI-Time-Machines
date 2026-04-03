const Replit = require('../src/replit');

jest.mock('https');

describe('Replit', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.REPLIT_API_TOKEN;
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.REPLIT_API_TOKEN = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when API token is not provided', () => {
      delete process.env.REPLIT_API_TOKEN;
      expect(() => new Replit()).toThrow('Replit API token is required');
    });

    test('should initialize with API token from environment', () => {
      process.env.REPLIT_API_TOKEN = 'test-token';
      const replit = new Replit();
      expect(replit).toBeDefined();
      expect(replit.baseUrl).toBe('https://replit.com/api/v0');
      expect(replit.source).toBe('ai-time-machines');
    });

    test('should initialize with API token from constructor parameter', () => {
      const replit = new Replit('custom-token');
      expect(replit).toBeDefined();
      expect(replit.apiToken).toBe('custom-token');
    });
  });

  describe('generatePredictionPackage', () => {
    test('should generate a valid Replit package for a prediction', () => {
      const replit = new Replit('test-token');
      const prediction = {
        id: 'pred-123',
        modelId: 'model-456',
        horizon: 5,
        predictions: [10, 11, 12, 13, 14],
        confidence: { lower: [9, 10, 11, 12, 13], upper: [11, 12, 13, 14, 15] },
        createdAt: '2026-01-01T00:00:00Z',
      };

      const pkg = replit.generatePredictionPackage(prediction);

      expect(pkg).toHaveProperty('files');
      expect(pkg.files['main.py']).toBeDefined();
      expect(pkg.files['prediction.json']).toBeDefined();
      expect(pkg.files['requirements.txt']).toBeDefined();
      expect(pkg.files['.replit']).toBeDefined();
      expect(pkg).toHaveProperty('repl_config');
      expect(pkg.repl_config.language).toBe('python3');
      expect(pkg.repl_config.entrypoint).toBe('main.py');
    });

    test('should embed prediction data in the generated script', () => {
      const replit = new Replit('test-token');
      const prediction = {
        id: 'pred-abc',
        modelId: 'model-xyz',
        horizon: 3,
        predictions: [1.5, 2.5, 3.5],
        confidence: null,
        createdAt: '2026-04-01T00:00:00Z',
      };

      const pkg = replit.generatePredictionPackage(prediction);
      const script = pkg.files['main.py'];

      expect(script).toContain('pred-abc');
      expect(script).toContain('model-xyz');
      expect(script).toContain('horizon = 3');
      expect(script).toContain('[1.5,2.5,3.5]');
    });

    test('should include correct requirements.txt', () => {
      const replit = new Replit('test-token');
      const prediction = { id: 'p1', modelId: 'm1', horizon: 1, predictions: [5], confidence: null };
      const pkg = replit.generatePredictionPackage(prediction);

      expect(pkg.files['requirements.txt']).toContain('matplotlib');
      expect(pkg.files['requirements.txt']).toContain('numpy');
    });

    test('should include source in metadata', () => {
      const replit = new Replit('test-token');
      const prediction = { id: 'p2', modelId: 'm2', horizon: 2, predictions: [1, 2], confidence: null };
      const pkg = replit.generatePredictionPackage(prediction);

      expect(pkg.metadata.source).toBe('ai-time-machines');
      expect(pkg.metadata.format).toBe('replit-v1');
    });
  });

  describe('createRepl', () => {
    test('should create a Repl via the API', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 201,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ id: 'repl-001', url: 'https://replit.com/@user/repl-001' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const replit = new Replit('test-token');
      const result = await replit.createRepl('My Prediction App', 'python3', { 'main.py': 'print("hi")' });

      expect(https.request).toHaveBeenCalled();
      expect(capturedBody).toHaveProperty('title', 'My Prediction App');
      expect(capturedBody).toHaveProperty('language', 'python3');
      expect(capturedBody.files['main.py']).toBeDefined();
      expect(result).toHaveProperty('url');
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
          if (event === 'data') cb(JSON.stringify({ message: 'Unauthorized' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const replit = new Replit('invalid-token');
      await expect(replit.createRepl('Test', 'python3', {})).rejects.toThrow('Replit API Error');
    });
  });

  describe('deployPrediction', () => {
    test('should deploy a prediction as a Repl', async () => {
      const https = require('https');

      let capturedBody = null;
      const mockReq = {
        write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 201,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ id: 'repl-deploy', url: 'https://replit.com/@user/repl-deploy' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const replit = new Replit('test-token');
      const prediction = {
        id: 'pred-deploy',
        modelId: 'model-deploy',
        horizon: 4,
        predictions: [5, 6, 7, 8],
        confidence: null,
        createdAt: '2026-04-01T00:00:00Z',
      };

      const result = await replit.deployPrediction(prediction);

      expect(capturedBody.language).toBe('python3');
      expect(capturedBody.files['main.py']).toBeDefined();
      expect(capturedBody.files['prediction.json']).toBeDefined();
      expect(result).toHaveProperty('url');
    });
  });

  describe('_request', () => {
    test('should handle network errors', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn((event, cb) => {
          if (event === 'error') cb(new Error('Connection refused'));
        }),
      };

      https.request = jest.fn(() => mockReq);

      const replit = new Replit('test-token');
      await expect(replit._request('POST', '/repls', {})).rejects.toThrow('Replit Request Error');
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

      const replit = new Replit('test-token');
      const result = await replit._request('GET', '/status');
      expect(result).toHaveProperty('raw', 'OK');
    });
  });
});
