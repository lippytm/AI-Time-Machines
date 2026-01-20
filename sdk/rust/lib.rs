// AI/Web3 Integration SDK for AI Time Machines
// Rust equivalent to @lippytm/ai-sdk (Node), lippytm-ai-sdk (Python), and aisdk (Go)

use std::env;

/// AI Provider Configuration
/// Supports OpenAI, Hugging Face, and other AI providers
#[derive(Debug, Clone)]
pub struct AIProviderConfig {
    pub provider: String, // "openai" | "huggingface" | "custom"
    pub api_key: String,
    pub model: String,
    // TODO: Load from secure secret manager
}

impl AIProviderConfig {
    pub fn new(provider: Option<String>, api_key: Option<String>, model: Option<String>) -> Self {
        Self {
            provider: provider.unwrap_or_else(|| "openai".to_string()),
            api_key: api_key.unwrap_or_else(|| env::var("AI_API_KEY").unwrap_or_default()),
            model: model.unwrap_or_else(|| "gpt-4".to_string()),
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.api_key.is_empty() {
            return Err("AI_API_KEY not configured. Set via environment or constructor.".to_string());
        }
        Ok(())
    }
}

/// Vector Store Configuration
/// Supports Pinecone, Weaviate, and Chroma
#[derive(Debug, Clone)]
pub struct VectorStoreConfig {
    pub provider: String, // "pinecone" | "weaviate" | "chroma"
    pub api_key: String,
    pub environment: String,
    pub index_name: String,
    // TODO: Load from secure secret manager
}

impl VectorStoreConfig {
    pub fn new(
        provider: Option<String>,
        api_key: Option<String>,
        environment: Option<String>,
        index_name: Option<String>,
    ) -> Self {
        Self {
            provider: provider.unwrap_or_else(|| "pinecone".to_string()),
            api_key: api_key.unwrap_or_else(|| env::var("VECTOR_STORE_API_KEY").unwrap_or_default()),
            environment: environment.unwrap_or_else(|| env::var("VECTOR_STORE_ENV").unwrap_or_default()),
            index_name: index_name.unwrap_or_else(|| "default-index".to_string()),
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.api_key.is_empty() {
            return Err("VECTOR_STORE_API_KEY not configured.".to_string());
        }
        Ok(())
    }
}

/// Web3 Provider Configuration
/// Supports Ethereum (EVM) and Solana chains
#[derive(Debug, Clone)]
pub struct Web3Config {
    pub chain: String, // "ethereum" | "solana" | "polygon" | etc
    pub rpc_url: String,
    pub private_key: String,
    pub network: String, // "mainnet" | "testnet" | "devnet"
    // TODO: Load from secure secret manager
    // TODO: Add support for additional chains (see extension points in README)
}

impl Web3Config {
    pub fn new(
        chain: Option<String>,
        rpc_url: Option<String>,
        private_key: Option<String>,
        network: Option<String>,
    ) -> Self {
        Self {
            chain: chain.unwrap_or_else(|| "ethereum".to_string()),
            rpc_url: rpc_url.unwrap_or_else(|| env::var("WEB3_RPC_URL").unwrap_or_default()),
            private_key: private_key.unwrap_or_else(|| env::var("WEB3_PRIVATE_KEY").unwrap_or_default()),
            network: network.unwrap_or_else(|| "mainnet".to_string()),
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.rpc_url.is_empty() {
            return Err("WEB3_RPC_URL not configured.".to_string());
        }
        Ok(())
    }
}

/// Messaging Provider Configuration
/// Supports Slack and Discord
#[derive(Debug, Clone)]
pub struct MessagingConfig {
    pub provider: String, // "slack" | "discord"
    pub token: String,
    pub channel: String,
    // TODO: Load from secure secret manager
}

impl MessagingConfig {
    pub fn new(provider: Option<String>, token: Option<String>, channel: Option<String>) -> Self {
        Self {
            provider: provider.unwrap_or_else(|| "slack".to_string()),
            token: token.unwrap_or_else(|| env::var("MESSAGING_TOKEN").unwrap_or_default()),
            channel: channel.unwrap_or_else(|| env::var("MESSAGING_CHANNEL").unwrap_or_default()),
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.token.is_empty() {
            return Err("MESSAGING_TOKEN not configured.".to_string());
        }
        Ok(())
    }
}

/// Data Storage Configuration
/// Supports Postgres, Redis, S3, and IPFS
#[derive(Debug, Clone)]
pub struct DataStorageConfig {
    pub storage_type: String, // "postgres" | "redis" | "s3" | "ipfs"
    pub connection_string: String,
    pub bucket: String,
    pub region: String,
    // TODO: Load from secure secret manager
}

impl DataStorageConfig {
    pub fn new(
        storage_type: Option<String>,
        connection_string: Option<String>,
        bucket: Option<String>,
        region: Option<String>,
    ) -> Self {
        Self {
            storage_type: storage_type.unwrap_or_else(|| "postgres".to_string()),
            connection_string: connection_string
                .unwrap_or_else(|| env::var("DATABASE_URL").unwrap_or_default()),
            bucket: bucket.unwrap_or_else(|| env::var("S3_BUCKET").unwrap_or_default()),
            region: region.unwrap_or_else(|| env::var("AWS_REGION").unwrap_or_default()),
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.storage_type == "postgres" && self.connection_string.is_empty() {
            return Err("DATABASE_URL not configured for Postgres.".to_string());
        }
        if self.storage_type == "s3" && self.bucket.is_empty() {
            return Err("S3_BUCKET not configured for S3 storage.".to_string());
        }
        Ok(())
    }
}

/// Main SDK Factory
/// Creates and manages all provider configurations
#[derive(Debug, Clone)]
pub struct AITimesMachinesSDK {
    pub ai: AIProviderConfig,
    pub vector_store: VectorStoreConfig,
    pub web3: Web3Config,
    pub messaging: MessagingConfig,
    pub data_storage: DataStorageConfig,
}

impl AITimesMachinesSDK {
    pub fn new() -> Self {
        Self {
            ai: AIProviderConfig::new(None, None, None),
            vector_store: VectorStoreConfig::new(None, None, None, None),
            web3: Web3Config::new(None, None, None, None),
            messaging: MessagingConfig::new(None, None, None),
            data_storage: DataStorageConfig::new(None, None, None, None),
        }
    }

    pub fn validate_all(&self) -> bool {
        self.ai.validate().is_ok()
            && self.vector_store.validate().is_ok()
            && self.web3.validate().is_ok()
            && self.messaging.validate().is_ok()
            && self.data_storage.validate().is_ok()
    }

    // TODO: Add provider initialization methods
    // TODO: Add connection pooling
    // TODO: Add retry logic
    // TODO: Add monitoring/logging hooks
}

impl Default for AITimesMachinesSDK {
    fn default() -> Self {
        Self::new()
    }
}
