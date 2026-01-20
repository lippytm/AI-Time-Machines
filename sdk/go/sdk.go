// Package aisdk provides AI/Web3 integration SDK for AI Time Machines
// Go equivalent to @lippytm/ai-sdk (Node) and lippytm-ai-sdk (Python)
package aisdk

import (
	"errors"
	"os"
)

// AIProviderConfig manages AI provider configuration
// Supports OpenAI, Hugging Face, and other AI providers
type AIProviderConfig struct {
	Provider string // "openai" | "huggingface" | "custom"
	APIKey   string
	Model    string
	// TODO: Load from secure secret manager
}

// NewAIProviderConfig creates a new AI provider configuration
func NewAIProviderConfig(provider, apiKey, model string) *AIProviderConfig {
	if provider == "" {
		provider = "openai"
	}
	if apiKey == "" {
		apiKey = os.Getenv("AI_API_KEY")
	}
	if model == "" {
		model = "gpt-4"
	}
	return &AIProviderConfig{
		Provider: provider,
		APIKey:   apiKey,
		Model:    model,
	}
}

// Validate checks if the configuration is valid
func (c *AIProviderConfig) Validate() error {
	if c.APIKey == "" {
		return errors.New("AI_API_KEY not configured. Set via environment or constructor")
	}
	return nil
}

// VectorStoreConfig manages vector store configuration
// Supports Pinecone, Weaviate, and Chroma
type VectorStoreConfig struct {
	Provider    string // "pinecone" | "weaviate" | "chroma"
	APIKey      string
	Environment string
	IndexName   string
	// TODO: Load from secure secret manager
}

// NewVectorStoreConfig creates a new vector store configuration
func NewVectorStoreConfig(provider, apiKey, environment, indexName string) *VectorStoreConfig {
	if provider == "" {
		provider = "pinecone"
	}
	if apiKey == "" {
		apiKey = os.Getenv("VECTOR_STORE_API_KEY")
	}
	if environment == "" {
		environment = os.Getenv("VECTOR_STORE_ENV")
	}
	if indexName == "" {
		indexName = "default-index"
	}
	return &VectorStoreConfig{
		Provider:    provider,
		APIKey:      apiKey,
		Environment: environment,
		IndexName:   indexName,
	}
}

// Validate checks if the configuration is valid
func (c *VectorStoreConfig) Validate() error {
	if c.APIKey == "" {
		return errors.New("VECTOR_STORE_API_KEY not configured")
	}
	return nil
}

// Web3Config manages Web3 provider configuration
// Supports Ethereum (EVM) and Solana chains
type Web3Config struct {
	Chain      string // "ethereum" | "solana" | "polygon" | etc
	RPCUrl     string
	PrivateKey string
	Network    string // "mainnet" | "testnet" | "devnet"
	// TODO: Load from secure secret manager
	// TODO: Add support for additional chains (see extension points in README)
}

// NewWeb3Config creates a new Web3 configuration
func NewWeb3Config(chain, rpcUrl, privateKey, network string) *Web3Config {
	if chain == "" {
		chain = "ethereum"
	}
	if rpcUrl == "" {
		rpcUrl = os.Getenv("WEB3_RPC_URL")
	}
	if privateKey == "" {
		privateKey = os.Getenv("WEB3_PRIVATE_KEY")
	}
	if network == "" {
		network = "mainnet"
	}
	return &Web3Config{
		Chain:      chain,
		RPCUrl:     rpcUrl,
		PrivateKey: privateKey,
		Network:    network,
	}
}

// Validate checks if the configuration is valid
func (c *Web3Config) Validate() error {
	if c.RPCUrl == "" {
		return errors.New("WEB3_RPC_URL not configured")
	}
	return nil
}

// MessagingConfig manages messaging provider configuration
// Supports Slack and Discord
type MessagingConfig struct {
	Provider string // "slack" | "discord"
	Token    string
	Channel  string
	// TODO: Load from secure secret manager
}

// NewMessagingConfig creates a new messaging configuration
func NewMessagingConfig(provider, token, channel string) *MessagingConfig {
	if provider == "" {
		provider = "slack"
	}
	if token == "" {
		token = os.Getenv("MESSAGING_TOKEN")
	}
	if channel == "" {
		channel = os.Getenv("MESSAGING_CHANNEL")
	}
	return &MessagingConfig{
		Provider: provider,
		Token:    token,
		Channel:  channel,
	}
}

// Validate checks if the configuration is valid
func (c *MessagingConfig) Validate() error {
	if c.Token == "" {
		return errors.New("MESSAGING_TOKEN not configured")
	}
	return nil
}

// DataStorageConfig manages data storage configuration
// Supports Postgres, Redis, S3, and IPFS
type DataStorageConfig struct {
	Type             string // "postgres" | "redis" | "s3" | "ipfs"
	ConnectionString string
	Bucket           string
	Region           string
	// TODO: Load from secure secret manager
}

// NewDataStorageConfig creates a new data storage configuration
func NewDataStorageConfig(storageType, connectionString, bucket, region string) *DataStorageConfig {
	if storageType == "" {
		storageType = "postgres"
	}
	if connectionString == "" {
		connectionString = os.Getenv("DATABASE_URL")
	}
	if bucket == "" {
		bucket = os.Getenv("S3_BUCKET")
	}
	if region == "" {
		region = os.Getenv("AWS_REGION")
	}
	return &DataStorageConfig{
		Type:             storageType,
		ConnectionString: connectionString,
		Bucket:           bucket,
		Region:           region,
	}
}

// Validate checks if the configuration is valid
func (c *DataStorageConfig) Validate() error {
	if c.Type == "postgres" && c.ConnectionString == "" {
		return errors.New("DATABASE_URL not configured for Postgres")
	}
	if c.Type == "s3" && c.Bucket == "" {
		return errors.New("S3_BUCKET not configured for S3 storage")
	}
	return nil
}

// SDK is the main SDK factory that creates and manages all provider configurations
type SDK struct {
	AI          *AIProviderConfig
	VectorStore *VectorStoreConfig
	Web3        *Web3Config
	Messaging   *MessagingConfig
	DataStorage *DataStorageConfig
}

// NewSDK creates a new SDK instance with default configurations
func NewSDK() *SDK {
	return &SDK{
		AI:          NewAIProviderConfig("", "", ""),
		VectorStore: NewVectorStoreConfig("", "", "", ""),
		Web3:        NewWeb3Config("", "", "", ""),
		Messaging:   NewMessagingConfig("", "", ""),
		DataStorage: NewDataStorageConfig("", "", "", ""),
	}
}

// ValidateAll validates all configurations
func (s *SDK) ValidateAll() bool {
	if err := s.AI.Validate(); err != nil {
		return false
	}
	if err := s.VectorStore.Validate(); err != nil {
		return false
	}
	if err := s.Web3.Validate(); err != nil {
		return false
	}
	if err := s.Messaging.Validate(); err != nil {
		return false
	}
	if err := s.DataStorage.Validate(); err != nil {
		return false
	}
	return true
}

// TODO: Add provider initialization methods
// TODO: Add connection pooling
// TODO: Add retry logic
// TODO: Add monitoring/logging hooks
