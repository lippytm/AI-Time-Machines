const GitHub = require('../src/github');

// Mock the https module
jest.mock('https');

describe('GitHub', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.GITHUB_TOKEN;
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.GITHUB_TOKEN = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when token is not provided', () => {
      delete process.env.GITHUB_TOKEN;
      expect(() => new GitHub()).toThrow('GitHub token is required');
    });

    test('should initialize with token from environment', () => {
      process.env.GITHUB_TOKEN = 'test-token';
      const client = new GitHub();
      expect(client).toBeDefined();
      expect(client.baseUrl).toBe('https://api.github.com');
      expect(client.source).toBe('ai-time-machines');
    });

    test('should initialize with token from constructor parameter', () => {
      const client = new GitHub('custom-token');
      expect(client).toBeDefined();
      expect(client.token).toBe('custom-token');
    });
  });

  describe('getRepository', () => {
    test('should fetch repository information', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const repoData = { id: 1, full_name: 'owner/repo', name: 'repo' };
      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify(repoData));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const result = await client.getRepository('owner', 'repo');

      expect(https.request).toHaveBeenCalled();
      expect(result).toEqual(repoData);
    });

    test('should reject on API error response', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 404,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ message: 'Not Found' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      await expect(client.getRepository('owner', 'nonexistent')).rejects.toThrow('GitHub API Error');
    });
  });

  describe('syncPrediction', () => {
    test('should create a new prediction file when it does not exist', async () => {
      const https = require('https');

      let requestCount = 0;
      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      https.request = jest.fn((options, cb) => {
        requestCount++;
        // First request (GET to check existing) returns 404
        // Second request (PUT to create file) returns 201
        const statusCode = requestCount === 1 ? 404 : 201;
        const responseBody =
          requestCount === 1
            ? JSON.stringify({ message: 'Not Found' })
            : JSON.stringify({ commit: { sha: 'abc123' }, content: { path: 'predictions/pred-1.json' } });

        const mockRes = {
          statusCode,
          on: jest.fn((event, cbFn) => {
            if (event === 'data') cbFn(responseBody);
            if (event === 'end') cbFn();
          }),
        };
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const prediction = {
        id: 'pred-1',
        modelId: 'model-1',
        horizon: 5,
        predictions: [1, 2, 3, 4, 5],
        confidence: null,
      };

      const result = await client.syncPrediction('owner', 'repo', prediction);
      expect(result).toHaveProperty('commit');
      expect(https.request).toHaveBeenCalledTimes(2);
    });

    test('should update an existing prediction file with sha', async () => {
      const https = require('https');

      let requestCount = 0;
      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      let capturedBody = null;

      https.request = jest.fn((options, cb) => {
        requestCount++;
        let responseBody;
        let statusCode;

        if (requestCount === 1) {
          // GET to check existing — file exists
          statusCode = 200;
          responseBody = JSON.stringify({ sha: 'existing-sha', name: 'pred-2.json' });
        } else {
          // PUT to update file — capture body
          statusCode = 200;
          responseBody = JSON.stringify({ commit: { sha: 'new-sha' } });
        }

        const mockRes = {
          statusCode,
          on: jest.fn((event, cbFn) => {
            if (event === 'data') cbFn(responseBody);
            if (event === 'end') cbFn();
          }),
        };

        const req = {
          write: jest.fn((body) => { capturedBody = JSON.parse(body); }),
          end: jest.fn(),
          on: jest.fn(),
        };
        cb(mockRes);
        return req;
      });

      const client = new GitHub('test-token');
      const prediction = {
        id: 'pred-2',
        modelId: 'model-2',
        horizon: 3,
        predictions: [10, 11, 12],
        confidence: { lower: [9, 10, 11], upper: [11, 12, 13] },
      };

      await client.syncPrediction('owner', 'repo', prediction);
      expect(https.request).toHaveBeenCalledTimes(2);
    });

    test('should use custom path and commit message', async () => {
      const https = require('https');

      let capturedOptions = null;
      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      https.request = jest.fn((options, cb) => {
        capturedOptions = options;
        const statusCode = capturedOptions.method === 'GET' ? 404 : 201;
        const responseBody =
          capturedOptions.method === 'GET'
            ? JSON.stringify({ message: 'Not Found' })
            : JSON.stringify({ commit: { sha: 'abc' } });

        const mockRes = {
          statusCode,
          on: jest.fn((event, cbFn) => {
            if (event === 'data') cbFn(responseBody);
            if (event === 'end') cbFn();
          }),
        };
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const prediction = { id: 'pred-3', modelId: 'm', horizon: 1, predictions: [5] };

      await client.syncPrediction('owner', 'repo', prediction, 'custom/path.json', 'Custom commit');
      expect(capturedOptions.path).toContain('custom/path.json');
    });
  });

  describe('createPredictionIssue', () => {
    test('should create a GitHub issue with prediction data', async () => {
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
          if (event === 'data') cb(JSON.stringify({ id: 1, number: 42, title: 'Prediction Report' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const prediction = {
        id: 'pred-4',
        modelId: 'model-4',
        horizon: 10,
        predictions: [1, 2, 3],
        confidence: { lower: [0, 1, 2], upper: [2, 3, 4] },
        createdAt: '2026-01-01T00:00:00Z',
      };

      const result = await client.createPredictionIssue('owner', 'repo', prediction);

      expect(https.request).toHaveBeenCalled();
      expect(capturedBody).toHaveProperty('title');
      expect(capturedBody.title).toContain('pred-4');
      expect(capturedBody).toHaveProperty('body');
      expect(capturedBody.body).toContain('pred-4');
      expect(capturedBody).toHaveProperty('labels');
      expect(capturedBody.labels).toContain('ai-time-machines');
      expect(result).toHaveProperty('number', 42);
    });

    test('should use custom issue title when provided', async () => {
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
          if (event === 'data') cb(JSON.stringify({ id: 2, number: 43, title: 'My Custom Title' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const prediction = { id: 'pred-5', predictions: [1, 2], horizon: 2 };

      await client.createPredictionIssue('owner', 'repo', prediction, 'My Custom Title');

      expect(capturedBody.title).toBe('My Custom Title');
    });
  });

  describe('listSyncedPredictions', () => {
    test('should return list of synced prediction files', async () => {
      const https = require('https');

      const files = [
        { name: 'pred-1.json', path: 'predictions/pred-1.json' },
        { name: 'pred-2.json', path: 'predictions/pred-2.json' },
      ];

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 200,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify(files));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const result = await client.listSyncedPredictions('owner', 'repo');

      expect(result).toHaveLength(2);
      expect(result[0]).toHaveProperty('name', 'pred-1.json');
    });

    test('should return empty array when folder does not exist', async () => {
      const https = require('https');

      const mockReq = {
        write: jest.fn(),
        end: jest.fn(),
        on: jest.fn(),
      };

      const mockRes = {
        statusCode: 404,
        on: jest.fn((event, cb) => {
          if (event === 'data') cb(JSON.stringify({ message: 'Not Found' }));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('test-token');
      const result = await client.listSyncedPredictions('owner', 'repo');

      expect(result).toEqual([]);
    });
  });

  describe('_request', () => {
    test('should include correct GitHub API headers', async () => {
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
          if (event === 'data') cb(JSON.stringify({}));
          if (event === 'end') cb();
        }),
      };

      https.request = jest.fn((options, cb) => {
        capturedOptions = options;
        cb(mockRes);
        return mockReq;
      });

      const client = new GitHub('my-token');
      await client.getRepository('owner', 'repo');

      expect(capturedOptions.headers['Authorization']).toBe('Bearer my-token');
      expect(capturedOptions.headers['Accept']).toBe('application/vnd.github+json');
      expect(capturedOptions.headers['X-GitHub-Api-Version']).toBe('2022-11-28');
      expect(capturedOptions.headers['User-Agent']).toBe('ai-time-machines');
    });

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

      const client = new GitHub('test-token');
      await expect(client.getRepository('owner', 'repo')).rejects.toThrow('GitHub Request Error');
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

      const client = new GitHub('test-token');
      const result = await client.getRepository('owner', 'repo');
      expect(result).toHaveProperty('raw', 'OK');
    });
  });
});
