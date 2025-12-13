const FineTuningManager = require('../src/fine-tuning');

// Mock the OpenAI module
jest.mock('openai');

describe('FineTuningManager', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.OPENAI_API_KEY;
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.OPENAI_API_KEY = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when API key is not provided', () => {
      delete process.env.OPENAI_API_KEY;
      expect(() => new FineTuningManager()).toThrow('OpenAI API key is required');
    });

    test('should initialize with API key from environment', () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const manager = new FineTuningManager();
      expect(manager).toBeDefined();
      expect(manager.client).toBeDefined();
    });

    test('should initialize with API key from constructor parameter', () => {
      const manager = new FineTuningManager('custom-key');
      expect(manager).toBeDefined();
    });
  });

  describe('uploadTrainingFile', () => {
    test('should upload a training file', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockCreate = jest.fn().mockResolvedValue({
        id: 'file-123',
        purpose: 'fine-tune',
      });

      OpenAI.mockImplementation(() => ({
        files: {
          create: mockCreate,
        },
      }));

      const manager = new FineTuningManager();
      
      // Mock fs.createReadStream
      const fs = require('fs');
      jest.spyOn(fs, 'createReadStream').mockReturnValue({});

      const result = await manager.uploadTrainingFile('test.jsonl');

      expect(result.id).toBe('file-123');
      expect(mockCreate).toHaveBeenCalled();
    });
  });

  describe('createFineTuningJob', () => {
    test('should create a fine-tuning job', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockCreate = jest.fn().mockResolvedValue({
        id: 'ftjob-123',
        model: 'gpt-3.5-turbo',
        status: 'queued',
      });

      OpenAI.mockImplementation(() => ({
        fineTuning: {
          jobs: {
            create: mockCreate,
          },
        },
      }));

      const manager = new FineTuningManager();
      const result = await manager.createFineTuningJob('file-123');

      expect(result.id).toBe('ftjob-123');
      expect(mockCreate).toHaveBeenCalledWith({
        training_file: 'file-123',
        model: 'gpt-3.5-turbo',
        hyperparameters: {
          n_epochs: 3,
        },
        suffix: 'time-machine',
      });
    });
  });

  describe('getJobStatus', () => {
    test('should retrieve job status', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockRetrieve = jest.fn().mockResolvedValue({
        id: 'ftjob-123',
        status: 'running',
      });

      OpenAI.mockImplementation(() => ({
        fineTuning: {
          jobs: {
            retrieve: mockRetrieve,
          },
        },
      }));

      const manager = new FineTuningManager();
      const result = await manager.getJobStatus('ftjob-123');

      expect(result.status).toBe('running');
      expect(mockRetrieve).toHaveBeenCalledWith('ftjob-123');
    });
  });

  describe('listJobs', () => {
    test('should list fine-tuning jobs', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockList = jest.fn().mockResolvedValue({
        data: [
          { id: 'ftjob-1', status: 'succeeded' },
          { id: 'ftjob-2', status: 'running' },
        ],
      });

      OpenAI.mockImplementation(() => ({
        fineTuning: {
          jobs: {
            list: mockList,
          },
        },
      }));

      const manager = new FineTuningManager();
      const result = await manager.listJobs(10);

      expect(result.length).toBe(2);
      expect(mockList).toHaveBeenCalledWith({ limit: 10 });
    });
  });

  describe('cancelJob', () => {
    test('should cancel a fine-tuning job', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockCancel = jest.fn().mockResolvedValue({
        id: 'ftjob-123',
        status: 'cancelled',
      });

      OpenAI.mockImplementation(() => ({
        fineTuning: {
          jobs: {
            cancel: mockCancel,
          },
        },
      }));

      const manager = new FineTuningManager();
      const result = await manager.cancelJob('ftjob-123');

      expect(result.status).toBe('cancelled');
      expect(mockCancel).toHaveBeenCalledWith('ftjob-123');
    });
  });
});
