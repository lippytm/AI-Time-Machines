// @lippytm/ai-sdk - AI/Web3 Integration SDK for Node.js
// This is a stub adapter package that references the shared package name

/**
 * AI Provider Configuration Factory
 * Supports OpenAI, Hugging Face, and other AI providers
 */
class AIProviderConfig {
  constructor(config = {}) {
    this.provider = config.provider || 'openai'; // 'openai' | 'huggingface' | 'custom'
    this.apiKey = config.apiKey || process.env.AI_API_KEY;
    this.model = config.model || 'gpt-4';
    // TODO: Load from secure secret manager
  }

  validate() {
    if (!this.apiKey) {
      throw new Error('AI_API_KEY not configured. Set via environment or constructor.');
    }
    return true;
  }
}

/**
 * Vector Store Configuration Factory
 * Supports Pinecone, Weaviate, and Chroma
 */
class VectorStoreConfig {
  constructor(config = {}) {
    this.provider = config.provider || 'pinecone'; // 'pinecone' | 'weaviate' | 'chroma'
    this.apiKey = config.apiKey || process.env.VECTOR_STORE_API_KEY;
    this.environment = config.environment || process.env.VECTOR_STORE_ENV;
    this.indexName = config.indexName || 'default-index';
    // TODO: Load from secure secret manager
  }

  validate() {
    if (!this.apiKey) {
      throw new Error('VECTOR_STORE_API_KEY not configured.');
    }
    return true;
  }
}

/**
 * Web3 Provider Configuration Factory
 * Supports Ethereum (EVM) and Solana chains
 */
class Web3Config {
  constructor(config = {}) {
    this.chain = config.chain || 'ethereum'; // 'ethereum' | 'solana' | 'polygon' | etc
    this.rpcUrl = config.rpcUrl || process.env.WEB3_RPC_URL;
    this.privateKey = config.privateKey || process.env.WEB3_PRIVATE_KEY;
    this.network = config.network || 'mainnet'; // 'mainnet' | 'testnet' | 'devnet'
    // TODO: Load from secure secret manager
    // TODO: Add support for additional chains (see extension points in README)
  }

  validate() {
    if (!this.rpcUrl) {
      throw new Error('WEB3_RPC_URL not configured.');
    }
    return true;
  }
}

/**
 * Messaging Provider Configuration Factory
 * Supports Slack and Discord
 */
class MessagingConfig {
  constructor(config = {}) {
    this.provider = config.provider || 'slack'; // 'slack' | 'discord'
    this.token = config.token || process.env.MESSAGING_TOKEN;
    this.channel = config.channel || process.env.MESSAGING_CHANNEL;
    // TODO: Load from secure secret manager
  }

  validate() {
    if (!this.token) {
      throw new Error('MESSAGING_TOKEN not configured.');
    }
    return true;
  }
}

/**
 * Data Storage Configuration Factory
 * Supports Postgres, Redis, S3, and IPFS
 */
class DataStorageConfig {
  constructor(config = {}) {
    this.type = config.type || 'postgres'; // 'postgres' | 'redis' | 's3' | 'ipfs'
    this.connectionString = config.connectionString || process.env.DATABASE_URL;
    this.bucket = config.bucket || process.env.S3_BUCKET;
    this.region = config.region || process.env.AWS_REGION;
    // TODO: Load from secure secret manager
  }

  validate() {
    if (this.type === 'postgres' && !this.connectionString) {
      throw new Error('DATABASE_URL not configured for Postgres.');
    }
    if (this.type === 's3' && !this.bucket) {
      throw new Error('S3_BUCKET not configured for S3 storage.');
    }
    return true;
  }
}

/**
 * Main SDK Factory
 * Creates and manages all provider configurations
 */
class AITimesMachinesSDK {
  constructor(config = {}) {
    this.ai = new AIProviderConfig(config.ai);
    this.vectorStore = new VectorStoreConfig(config.vectorStore);
    this.web3 = new Web3Config(config.web3);
    this.messaging = new MessagingConfig(config.messaging);
    this.dataStorage = new DataStorageConfig(config.dataStorage);
  }

  validateAll() {
    try {
      this.ai.validate();
      this.vectorStore.validate();
      this.web3.validate();
      this.messaging.validate();
      this.dataStorage.validate();
      return true;
    } catch (error) {
      console.warn('SDK validation warning:', error.message);
      return false;
    }
  }

  // TODO: Add provider initialization methods
  // TODO: Add connection pooling
  // TODO: Add retry logic
  // TODO: Add monitoring/logging hooks
}

module.exports = {
  AITimesMachinesSDK,
  AIProviderConfig,
  VectorStoreConfig,
  Web3Config,
  MessagingConfig,
  DataStorageConfig,
};
