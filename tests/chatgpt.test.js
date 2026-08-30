const ChatGPT = require('../src/chatgpt');

// Mock the OpenAI module
jest.mock('openai');

describe('ChatGPT', () => {
  let originalEnv;

  beforeEach(() => {
    // Save original environment
    originalEnv = process.env.OPENAI_API_KEY;
    // Clear the mock
    jest.clearAllMocks();
  });

  afterEach(() => {
    // Restore original environment
    process.env.OPENAI_API_KEY = originalEnv;
  });

  describe('Constructor', () => {
    test('should throw error when API key is not provided', () => {
      delete process.env.OPENAI_API_KEY;
      expect(() => new ChatGPT()).toThrow('OpenAI API key is required');
    });

    test('should initialize with API key from environment', () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const chatgpt = new ChatGPT();
      expect(chatgpt).toBeDefined();
      expect(chatgpt.model).toBe('gpt-4o');
    });

    test('should initialize with API key from constructor parameter', () => {
      const chatgpt = new ChatGPT('custom-key');
      expect(chatgpt).toBeDefined();
    });
  });

  describe('setModel', () => {
    test('should update the model', () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const chatgpt = new ChatGPT();
      chatgpt.setModel('gpt-3.5-turbo');
      expect(chatgpt.model).toBe('gpt-3.5-turbo');
    });
  });

  describe('getAvailableModels', () => {
    test('should return list of available models including gpt-4o', () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const chatgpt = new ChatGPT();
      const models = chatgpt.getAvailableModels();
      expect(Array.isArray(models)).toBe(true);
      expect(models).toContain('gpt-4o');
      expect(models).toContain('gpt-4-turbo');
      expect(models).toContain('gpt-3.5-turbo');
    });
  });

  describe('chat', () => {
    test('should handle basic chat message', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockCreate = jest.fn().mockResolvedValue({
        choices: [{ message: { content: 'Test response' } }],
      });

      OpenAI.mockImplementation(() => ({
        chat: {
          completions: {
            create: mockCreate,
          },
        },
      }));

      const chatgpt = new ChatGPT();
      const response = await chatgpt.chat('Hello');

      expect(mockCreate).toHaveBeenCalled();
      expect(response).toBe('Test response');
    });
  });

  describe('conversation', () => {
    test('should handle conversation with context', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');
      
      const mockCreate = jest.fn().mockResolvedValue({
        choices: [{ message: { content: 'Conversation response' } }],
      });

      OpenAI.mockImplementation(() => ({
        chat: {
          completions: {
            create: mockCreate,
          },
        },
      }));

      const chatgpt = new ChatGPT();
      const messages = [
        { role: 'user', content: 'Hello' },
        { role: 'assistant', content: 'Hi there!' },
        { role: 'user', content: 'How are you?' },
      ];
      
      const response = await chatgpt.conversation(messages);

      expect(mockCreate).toHaveBeenCalled();
      expect(response).toBe('Conversation response');
    });
  });

  describe('streamChat', () => {
    test('should stream response chunks and return full text', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');

      const chunks = [
        { choices: [{ delta: { content: 'Hello' } }] },
        { choices: [{ delta: { content: ' world' } }] },
        { choices: [{ delta: {} }] },
      ];

      async function* fakeStream() {
        for (const c of chunks) yield c;
      }

      const mockCreate = jest.fn().mockResolvedValue(fakeStream());

      OpenAI.mockImplementation(() => ({
        chat: { completions: { create: mockCreate } },
      }));

      const chatgpt = new ChatGPT();
      const received = [];
      const full = await chatgpt.streamChat('Hi', (chunk) => received.push(chunk));

      expect(full).toBe('Hello world');
      expect(received).toEqual(['Hello', ' world']);
    });
  });

  describe('analyzeTimeSeries', () => {
    test('should return parsed JSON analysis', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');

      const analysis = {
        trend: 'increasing',
        seasonality: null,
        anomalies: [],
        insights: ['Values are rising'],
        recommendations: ['Continue monitoring'],
      };

      const mockCreate = jest.fn().mockResolvedValue({
        choices: [{ message: { content: JSON.stringify(analysis) } }],
      });

      OpenAI.mockImplementation(() => ({
        chat: { completions: { create: mockCreate } },
      }));

      const chatgpt = new ChatGPT();
      const data = [
        { timestamp: '2026-01-01', value: 10 },
        { timestamp: '2026-01-02', value: 11 },
        { timestamp: '2026-01-03', value: 12 },
      ];
      const result = await chatgpt.analyzeTimeSeries(data);

      expect(result).toHaveProperty('trend', 'increasing');
      expect(result).toHaveProperty('anomalies');
      expect(result).toHaveProperty('insights');
      expect(result).toHaveProperty('recommendations');
    });

    test('should strip markdown code fences from response', async () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const OpenAI = require('openai');

      const analysis = { trend: 'stable', seasonality: null, anomalies: [], insights: [], recommendations: [] };
      const fencedResponse = '```json\n' + JSON.stringify(analysis) + '\n```';

      const mockCreate = jest.fn().mockResolvedValue({
        choices: [{ message: { content: fencedResponse } }],
      });

      OpenAI.mockImplementation(() => ({
        chat: { completions: { create: mockCreate } },
      }));

      const chatgpt = new ChatGPT();
      const result = await chatgpt.analyzeTimeSeries([{ timestamp: '2026-01-01', value: 5 }]);
      expect(result).toHaveProperty('trend', 'stable');
    });
  });
});
