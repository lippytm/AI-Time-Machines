/**
 * Smoke tests for AI/Web3 SDK configuration loaders
 */

const {
  AITimesMachinesSDK,
  AIProviderConfig,
  VectorStoreConfig,
  Web3Config,
  MessagingConfig,
  DataStorageConfig,
} = require('../sdk/node/index');

describe('AI/Web3 SDK Configuration', () => {
  beforeEach(() => {
    // Clear environment variables
    delete process.env.AI_API_KEY;
    delete process.env.VECTOR_STORE_API_KEY;
    delete process.env.WEB3_RPC_URL;
    delete process.env.MESSAGING_TOKEN;
    delete process.env.DATABASE_URL;
  });

  describe('AIProviderConfig', () => {
    test('should create with default values', () => {
      const config = new AIProviderConfig();
      expect(config.provider).toBe('openai');
      expect(config.model).toBe('gpt-4');
    });

    test('should create with custom values', () => {
      const config = new AIProviderConfig({
        provider: 'huggingface',
        apiKey: 'test-key',
        model: 'gpt-3.5',
      });
      expect(config.provider).toBe('huggingface');
      expect(config.apiKey).toBe('test-key');
      expect(config.model).toBe('gpt-3.5');
    });

    test('should validate with API key', () => {
      const config = new AIProviderConfig({ apiKey: 'test-key' });
      expect(() => config.validate()).not.toThrow();
    });

    test('should throw error when validating without API key', () => {
      const config = new AIProviderConfig();
      expect(() => config.validate()).toThrow('AI_API_KEY not configured');
    });
  });

  describe('VectorStoreConfig', () => {
    test('should create with default values', () => {
      const config = new VectorStoreConfig();
      expect(config.provider).toBe('pinecone');
      expect(config.indexName).toBe('default-index');
    });

    test('should validate with API key', () => {
      const config = new VectorStoreConfig({ apiKey: 'test-key' });
      expect(() => config.validate()).not.toThrow();
    });
  });

  describe('Web3Config', () => {
    test('should create with default values', () => {
      const config = new Web3Config();
      expect(config.chain).toBe('ethereum');
      expect(config.network).toBe('mainnet');
    });

    test('should validate with RPC URL', () => {
      const config = new Web3Config({ rpcUrl: 'https://eth-mainnet.example.com' });
      expect(() => config.validate()).not.toThrow();
    });
  });

  describe('MessagingConfig', () => {
    test('should create with default values', () => {
      const config = new MessagingConfig();
      expect(config.provider).toBe('slack');
    });

    test('should validate with token', () => {
      const config = new MessagingConfig({ token: 'test-token' });
      expect(() => config.validate()).not.toThrow();
    });
  });

  describe('DataStorageConfig', () => {
    test('should create with default values', () => {
      const config = new DataStorageConfig();
      expect(config.type).toBe('postgres');
    });

    test('should validate postgres with connection string', () => {
      const config = new DataStorageConfig({
        type: 'postgres',
        connectionString: 'postgresql://localhost/test',
      });
      expect(() => config.validate()).not.toThrow();
    });

    test('should validate S3 with bucket', () => {
      const config = new DataStorageConfig({
        type: 's3',
        bucket: 'test-bucket',
      });
      expect(() => config.validate()).not.toThrow();
    });
  });

  describe('AITimesMachinesSDK', () => {
    test('should create SDK with default configs', () => {
      const sdk = new AITimesMachinesSDK();
      expect(sdk.ai).toBeInstanceOf(AIProviderConfig);
      expect(sdk.vectorStore).toBeInstanceOf(VectorStoreConfig);
      expect(sdk.web3).toBeInstanceOf(Web3Config);
      expect(sdk.messaging).toBeInstanceOf(MessagingConfig);
      expect(sdk.dataStorage).toBeInstanceOf(DataStorageConfig);
    });

    test('should create SDK with custom configs', () => {
      const sdk = new AITimesMachinesSDK({
        ai: { provider: 'huggingface', apiKey: 'ai-key' },
        vectorStore: { provider: 'weaviate', apiKey: 'vector-key' },
        web3: { chain: 'solana', rpcUrl: 'https://solana.example.com' },
        messaging: { provider: 'discord', token: 'discord-token' },
        dataStorage: { type: 'redis', connectionString: 'redis://localhost' },
      });
      expect(sdk.ai.provider).toBe('huggingface');
      expect(sdk.vectorStore.provider).toBe('weaviate');
      expect(sdk.web3.chain).toBe('solana');
      expect(sdk.messaging.provider).toBe('discord');
      expect(sdk.dataStorage.type).toBe('redis');
    });

    test('validateAll should return false when configs are invalid', () => {
      const sdk = new AITimesMachinesSDK();
      expect(sdk.validateAll()).toBe(false);
    });

    test('validateAll should return true when configs are valid', () => {
      const sdk = new AITimesMachinesSDK({
        ai: { apiKey: 'ai-key' },
        vectorStore: { apiKey: 'vector-key' },
        web3: { rpcUrl: 'https://example.com' },
        messaging: { token: 'msg-token' },
        dataStorage: { connectionString: 'postgresql://localhost' },
      });
      expect(sdk.validateAll()).toBe(true);
    });
  });
});
