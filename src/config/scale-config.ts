/**
 * Configuration for scaling AI Time Machines to massive scale
 * Supports 100,000 AI Agents + 100,000 Synthetic AI Agents
 * Each agent can have up to 100,000 AI Engines
 */

export interface ScaleConfig {
  maxAIAgents: number;
  maxSyntheticAgents: number;
  maxEnginesPerAgent: number;
  clusterNodes: number;
  redisShards: number;
}

export interface PerformanceConfig {
  maxConcurrentOperations: number;
  requestTimeoutMs: number;
  healthCheckIntervalMs: number;
  metricsCollectionIntervalMs: number;
  memoryThresholdPercent: number;
  cpuThresholdPercent: number;
}

export interface Web3Config {
  enableWeb3: boolean;
  networkChainId: number;
  contractAddresses: {
    agentRegistry: string;
    tokenContract: string;
    governance: string;
  };
  ipfsGateway: string;
  decentralizedStorage: boolean;
  web3RpcEndpoints: string[];
}

export const defaultConfig = {
  scale: {
    maxAIAgents: 100000,
    maxSyntheticAgents: 100000,
    maxEnginesPerAgent: 100000,
    clusterNodes: 10,
    redisShards: 8
  } as ScaleConfig,
  
  performance: {
    maxConcurrentOperations: 1000,
    requestTimeoutMs: 30000,
    healthCheckIntervalMs: 5000,
    metricsCollectionIntervalMs: 10000,
    memoryThresholdPercent: 85,
    cpuThresholdPercent: 80
  } as PerformanceConfig,
  
  web3: {
    enableWeb3: true,
    networkChainId: 1, // Ethereum mainnet
    contractAddresses: {
      agentRegistry: '0x0000000000000000000000000000000000000000',
      tokenContract: '0x0000000000000000000000000000000000000000',
      governance: '0x0000000000000000000000000000000000000000'
    },
    ipfsGateway: 'https://gateway.pinata.cloud/ipfs/',
    decentralizedStorage: true,
    web3RpcEndpoints: [
      'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
      'https://eth-mainnet.alchemyapi.io/v2/YOUR_API_KEY'
    ]
  } as Web3Config
};

export type AppConfig = {
  scale: ScaleConfig;
  performance: PerformanceConfig;
  web3: Web3Config;
};