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
      expect(chatgpt.model).toBe('gpt-4');
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
    test('should return list of available models', () => {
      process.env.OPENAI_API_KEY = 'test-key';
      const chatgpt = new ChatGPT();
      const models = chatgpt.getAvailableModels();
      expect(Array.isArray(models)).toBe(true);
      expect(models).toContain('gpt-4');
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
});
