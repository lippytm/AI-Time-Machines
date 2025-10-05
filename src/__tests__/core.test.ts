/**
 * Basic tests for AI Time Machines components
 */

import { AIAgent } from '../agents/ai-agent';
import { SyntheticAIAgent } from '../agents/synthetic-ai-agent';
import { AIEngine } from '../engines/ai-engine';
import { Web3Integration } from '../web3/integration';
import { MetricsCollector } from '../monitoring/metrics';
import { defaultConfig } from '../config/scale-config';

describe('AI Time Machines Core Components', () => {
  
  describe('AIAgent', () => {
    let agent: AIAgent;

    beforeEach(() => {
      agent = new AIAgent('test_ai_agent');
    });

    afterEach(async () => {
      await agent.shutdown();
    });

    test('should create AI agent with default engines', () => {
      expect(agent.getId()).toBe('test_ai_agent');
      expect(agent.getType()).toBe('AI');
      expect(agent.getEngineCount()).toBeGreaterThan(0);
    });

    test('should process simple task', async () => {
      const task = {
        type: 'NLP',
        data: 'test data'
      };

      const result = await agent.processTask(task);
      expect(result).toBeDefined();
      expect(result.type).toBe('NLP');
      expect(result.engineCount).toBeGreaterThan(0);
    });

    test('should create additional engines', async () => {
      const initialCount = agent.getEngineCount();
      const engineId = await agent.createEngine();
      
      expect(engineId).toBeDefined();
      expect(agent.getEngineCount()).toBeGreaterThan(initialCount);
    });

    test('should scale engines', async () => {
      const initialCount = agent.getEngineCount();
      const scaled = await agent.scaleEngines(initialCount + 5);
      
      expect(scaled).toBeGreaterThan(0);
      expect(agent.getEngineCount()).toBeGreaterThan(initialCount);
    });
  });

  describe('SyntheticAIAgent', () => {
    let agent: SyntheticAIAgent;

    beforeEach(() => {
      agent = new SyntheticAIAgent('test_synthetic_agent');
    });

    afterEach(async () => {
      await agent.shutdown();
    });

    test('should create synthetic agent with enhanced capabilities', () => {
      expect(agent.getId()).toBe('test_synthetic_agent');
      expect(agent.getType()).toBe('SYNTHETIC');
      expect(agent.getEngineCount()).toBeGreaterThan(0);
    });

    test('should process task with synthetic enhancements', async () => {
      const task = {
        type: 'ML',
        data: { features: [1, 2, 3] },
        complexity: 'high'
      };

      const result = await agent.processTask(task);
      expect(result).toBeDefined();
      expect(result.syntheticAnalysis).toBeDefined();
      expect(result.syntheticAnalysis.emergentBehaviors).toBeDefined();
    });
  });

  describe('AIEngine', () => {
    let engine: AIEngine;

    beforeEach(() => {
      engine = new AIEngine('test_engine', 'test_agent');
    });

    afterEach(async () => {
      await engine.shutdown();
    });

    test('should create engine with correct properties', () => {
      expect(engine.getId()).toBe('test_engine');
      expect(engine.getAgentId()).toBe('test_agent');
      expect(engine.getStatus()).toBe('IDLE');
    });

    test('should process NLP operation', async () => {
      const operation = {
        type: 'NLP',
        data: 'test text'
      };

      const result = await engine.processOperation(operation);
      expect(result).toBeDefined();
      expect(result.type).toBe('NLP');
      expect(result.processed).toBe(true);
    });

    test('should process multiple operations concurrently', async () => {
      const operations = [
        { type: 'NLP', data: 'text 1' },
        { type: 'ML', data: 'data 1' },
        { type: 'ANALYSIS', data: 'dataset 1' }
      ];

      const results = await Promise.all(
        operations.map(op => engine.processOperation(op))
      );

      expect(results).toHaveLength(3);
      results.forEach((result, index) => {
        expect(result.type).toBe(operations[index].type);
        expect(result.processed).toBe(true);
      });
    });
  });

  describe('Web3Integration', () => {
    let web3: Web3Integration;

    beforeEach(() => {
      web3 = new Web3Integration(defaultConfig.web3);
    });

    afterEach(async () => {
      await web3.shutdown();
    });

    test('should initialize with correct configuration', () => {
      expect(web3.isWeb3Enabled()).toBe(defaultConfig.web3.enableWeb3);
      const metrics = web3.getMetrics();
      expect(metrics.enabledWeb3).toBe(defaultConfig.web3.enableWeb3);
    });

    test('should register agent on blockchain', async () => {
      if (!web3.isWeb3Enabled()) {
        return; // Skip if Web3 is disabled
      }

      const agentData = {
        agentId: 'test_agent',
        agentType: 'AI' as const,
        capabilities: ['reasoning', 'learning'],
        engineCount: 10,
        metadata: 'test metadata'
      };

      const txId = await web3.registerAgent(agentData);
      expect(txId).toBeDefined();
      expect(typeof txId).toBe('string');
    });

    test('should store and retrieve data from IPFS', async () => {
      if (!defaultConfig.web3.decentralizedStorage) {
        return; // Skip if decentralized storage is disabled
      }

      const testData = { message: 'test data', timestamp: Date.now() };
      const hash = await web3.storeDataOnIPFS(testData);
      
      expect(hash).toBeDefined();
      expect(typeof hash).toBe('string');

      const retrievedData = await web3.retrieveDataFromIPFS(hash);
      expect(retrievedData).toBeDefined();
      expect(retrievedData.hash).toBe(hash);
    });
  });

  describe('MetricsCollector', () => {
    let metrics: MetricsCollector;

    beforeEach(() => {
      metrics = MetricsCollector.getInstance();
    });

    test('should be singleton instance', () => {
      const another = MetricsCollector.getInstance();
      expect(metrics).toBe(another);
    });

    test('should increment counters', () => {
      expect(() => {
        metrics.incrementCounter('agents_created', { type: 'AI' });
        metrics.incrementCounter('tasks_processed');
        metrics.incrementCounter('engines_added');
      }).not.toThrow();
    });

    test('should record histograms', () => {
      expect(() => {
        metrics.recordHistogram('operation_duration_ms', 150);
        metrics.recordHistogram('task_duration_ms', 1000);
      }).not.toThrow();
    });

    test('should generate performance report', async () => {
      const report = await metrics.generatePerformanceReport();
      
      expect(report).toBeDefined();
      expect(report.timestamp).toBeDefined();
      expect(report.summary).toBeDefined();
      expect(report.metrics).toBeDefined();
      expect(report.recommendations).toBeDefined();
      expect(Array.isArray(report.recommendations)).toBe(true);
    });

    test('should get current metrics', () => {
      const currentMetrics = metrics.getCurrentMetrics();
      
      expect(currentMetrics).toBeDefined();
      expect(typeof currentMetrics.totalAgents).toBe('number');
      expect(typeof currentMetrics.activeAgents).toBe('number');
      expect(typeof currentMetrics.totalEngines).toBe('number');
      expect(typeof currentMetrics.tasksProcessed).toBe('number');
    });
  });

  describe('Scale Configuration', () => {
    test('should have valid default configuration', () => {
      expect(defaultConfig.scale.maxAIAgents).toBe(100000);
      expect(defaultConfig.scale.maxSyntheticAgents).toBe(100000);
      expect(defaultConfig.scale.maxEnginesPerAgent).toBe(100000);
      expect(defaultConfig.scale.clusterNodes).toBeGreaterThan(0);
    });

    test('should have valid performance thresholds', () => {
      expect(defaultConfig.performance.maxConcurrentOperations).toBeGreaterThan(0);
      expect(defaultConfig.performance.requestTimeoutMs).toBeGreaterThan(0);
      expect(defaultConfig.performance.memoryThresholdPercent).toBeLessThanOrEqual(100);
      expect(defaultConfig.performance.cpuThresholdPercent).toBeLessThanOrEqual(100);
    });

    test('should have valid Web3 configuration', () => {
      expect(typeof defaultConfig.web3.enableWeb3).toBe('boolean');
      expect(defaultConfig.web3.networkChainId).toBeGreaterThan(0);
      expect(Array.isArray(defaultConfig.web3.web3RpcEndpoints)).toBe(true);
    });
  });
});