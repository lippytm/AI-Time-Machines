# AI Time Machines SDK

This directory contains adapter stubs for integrating AI and Web3 services across multiple languages.

## Available Adapters

### Node.js/TypeScript (`sdk/node`)
- Package: `@lippytm/ai-sdk`
- Import: `const { AITimesMachinesSDK } = require('@lippytm/ai-sdk');`

### Python (`sdk/python`)
- Package: `lippytm-ai-sdk`
- Import: `from lippytm_ai_sdk import AITimesMachinesSDK`

### Go (`sdk/go`)
- Package: `github.com/lippytm/ai-time-machines/sdk/go/aisdk`
- Import: `import "github.com/lippytm/ai-time-machines/sdk/go/aisdk"`

### Rust (`sdk/rust`)
- Crate: `ai-timemachines-sdk`
- Add to Cargo.toml: `ai-timemachines-sdk = { path = "../sdk/rust" }`

## Configuration Pattern

All adapters follow a consistent factory/config pattern:

```javascript
// Node.js example
const sdk = new AITimesMachinesSDK({
  ai: {
    provider: 'openai',
    apiKey: process.env.AI_API_KEY,
    model: 'gpt-4'
  },
  vectorStore: {
    provider: 'pinecone',
    apiKey: process.env.VECTOR_STORE_API_KEY
  },
  web3: {
    chain: 'ethereum',
    rpcUrl: process.env.WEB3_RPC_URL
  },
  messaging: {
    provider: 'slack',
    token: process.env.MESSAGING_TOKEN
  },
  dataStorage: {
    type: 'postgres',
    connectionString: process.env.DATABASE_URL
  }
});
```

## TODO Items

- [ ] Implement actual provider initialization methods
- [ ] Add connection pooling for database and Web3 connections
- [ ] Implement retry logic with exponential backoff
- [ ] Add monitoring and logging hooks
- [ ] Integrate with secure secret manager (e.g., AWS Secrets Manager, HashiCorp Vault)
- [ ] Add comprehensive error handling
- [ ] Add TypeScript type definitions for Node SDK
- [ ] Add unit tests for each language adapter
- [ ] Add integration tests with mock providers

## Security Notes

**IMPORTANT**: The current implementation loads secrets from environment variables. In production:
- Use a secure secret manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Never commit API keys or private keys to version control
- Rotate keys regularly
- Use different keys for dev/staging/production environments
