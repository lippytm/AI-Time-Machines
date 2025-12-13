const TimeTravelAssistant = require('../agents/time-travel-assistant');

// Mock the ChatGPT module
jest.mock('../src/chatgpt');

describe('TimeTravelAssistant', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.OPENAI_API_KEY;
    process.env.OPENAI_API_KEY = 'test-key';
    jest.clearAllMocks();
  });

  afterEach(() => {
    process.env.OPENAI_API_KEY = originalEnv;
  });

  describe('Constructor', () => {
    test('should initialize with conversation history', () => {
      const assistant = new TimeTravelAssistant();
      expect(assistant).toBeDefined();
      expect(assistant.conversationHistory).toBeDefined();
      expect(assistant.systemPrompt).toBeDefined();
      expect(assistant.systemPrompt.role).toBe('system');
    });
  });

  describe('resetConversation', () => {
    test('should reset conversation history to system prompt only', () => {
      const assistant = new TimeTravelAssistant();
      assistant.conversationHistory.push({ role: 'user', content: 'test' });
      
      assistant.resetConversation();
      
      expect(assistant.conversationHistory.length).toBe(1);
      expect(assistant.conversationHistory[0].role).toBe('system');
    });
  });

  describe('chat', () => {
    test('should add user message and get response', async () => {
      const ChatGPT = require('../src/chatgpt');
      ChatGPT.mockImplementation(() => ({
        conversation: jest.fn().mockResolvedValue('Test response'),
      }));

      const assistant = new TimeTravelAssistant();
      const response = await assistant.chat('Hello');

      expect(response).toBe('Test response');
      expect(assistant.conversationHistory.length).toBeGreaterThanOrEqual(2);
      expect(assistant.conversationHistory[assistant.conversationHistory.length - 2].content).toBe('Hello');
      expect(assistant.conversationHistory[assistant.conversationHistory.length - 1].content).toBe('Test response');
    });
  });

  describe('recommendTimePeriod', () => {
    test('should recommend a time period based on interest', async () => {
      const ChatGPT = require('../src/chatgpt');
      ChatGPT.mockImplementation(() => ({
        conversation: jest.fn().mockResolvedValue('Visit the Renaissance'),
      }));

      const assistant = new TimeTravelAssistant();
      const response = await assistant.recommendTimePeriod('art');

      expect(response).toBe('Visit the Renaissance');
    });
  });

  describe('getSafetyBriefing', () => {
    test('should get safety briefing for a time period', async () => {
      const ChatGPT = require('../src/chatgpt');
      ChatGPT.mockImplementation(() => ({
        conversation: jest.fn().mockResolvedValue('Safety information'),
      }));

      const assistant = new TimeTravelAssistant();
      const response = await assistant.getSafetyBriefing('ancient Rome');

      expect(response).toBe('Safety information');
    });
  });

  describe('getHistoricalContext', () => {
    test('should get historical context for an event', async () => {
      const ChatGPT = require('../src/chatgpt');
      ChatGPT.mockImplementation(() => ({
        conversation: jest.fn().mockResolvedValue('Historical context'),
      }));

      const assistant = new TimeTravelAssistant();
      const response = await assistant.getHistoricalContext('Moon landing');

      expect(response).toBe('Historical context');
    });
  });

  describe('getHistory', () => {
    test('should return conversation history', async () => {
      const ChatGPT = require('../src/chatgpt');
      ChatGPT.mockImplementation(() => ({
        conversation: jest.fn().mockResolvedValue('Response'),
      }));

      const assistant = new TimeTravelAssistant();
      await assistant.chat('Test message');

      const history = assistant.getHistory();
      expect(history.length).toBeGreaterThanOrEqual(2);
    });
  });
});
