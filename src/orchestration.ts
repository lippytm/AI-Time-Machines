/**
 * AI Time Machines - Main Orchestration System
 * Scalable AI Agent platform supporting 100k+ AI Agents and Synthetic AI Agents
 */

import { EventEmitter } from 'events';
import cluster from 'cluster';
import os from 'os';
import express from 'express';
import { createServer } from 'http';
import WebSocket from 'ws';

import { AppConfig, defaultConfig } from './config/scale-config';
import { AIAgent } from './agents/ai-agent';
import { SyntheticAIAgent } from './agents/synthetic-ai-agent';
import { BaseAgent } from './core/base-agent';
import { Web3Integration } from './web3/integration';
import { MetricsCollector } from './monitoring/metrics';

export interface AgentPool {
  aiAgents: Map<string, AIAgent>;
  syntheticAgents: Map<string, SyntheticAIAgent>;
}

export interface SystemStatus {
  status: 'INITIALIZING' | 'RUNNING' | 'SCALING' | 'MAINTENANCE' | 'SHUTDOWN';
  totalAgents: number;
  activeAgents: number;
  totalEngines: number;
  web3Enabled: boolean;
  clusterId: number;
  uptime: number;
}

export class AITimeMachines extends EventEmitter {
  private config: AppConfig;
  private agentPool: AgentPool;
  private web3Integration: Web3Integration;
  private metrics: MetricsCollector;
  private expressApp!: express.Application;
  private httpServer: any;
  private wsServer!: WebSocket.Server;
  private systemStatus: SystemStatus;
  private agentIdCounter: number = 0;
  private isShuttingDown: boolean = false;

  constructor(config: AppConfig = defaultConfig) {
    super();
    this.config = config;
    this.agentPool = {
      aiAgents: new Map(),
      syntheticAgents: new Map()
    };
    
    this.systemStatus = {
      status: 'INITIALIZING',
      totalAgents: 0,
      activeAgents: 0,
      totalEngines: 0,
      web3Enabled: config.web3.enableWeb3,
      clusterId: cluster.worker?.id || 0,
      uptime: 0
    };

    this.metrics = MetricsCollector.getInstance();
    this.web3Integration = new Web3Integration(config.web3);
    this.initializeExpress();
    this.setupEventHandlers();
  }

  private initializeExpress(): void {
    this.expressApp = express();
    this.expressApp.use(express.json({ limit: '10mb' }));
    this.expressApp.use(express.urlencoded({ extended: true }));

    // Health check endpoint
    this.expressApp.get('/health', (req, res) => {
      res.json({
        status: this.systemStatus.status,
        ...this.getSystemMetrics(),
        timestamp: new Date().toISOString()
      });
    });

    // Metrics endpoint for Prometheus
    this.expressApp.get('/metrics', async (req, res) => {
      res.set('Content-Type', 'text/plain');
      const metrics = await this.metrics.getPrometheusMetrics();
      res.send(metrics);
    });

    // Agent management endpoints
    this.expressApp.post('/agents/create', async (req, res) => {
      try {
        const { type, count = 1 } = req.body;
        const agents = await this.createAgents(type, count);
        res.json({ success: true, agents: agents.map(a => a.getId()) });
      } catch (error) {
        res.status(500).json({ success: false, error: (error as Error).message });
      }
    });

    this.expressApp.get('/agents', (req, res) => {
      const agents = this.getAllAgents().map(agent => agent.getMetrics());
      res.json({ agents });
    });

    this.expressApp.post('/agents/:id/task', async (req, res) => {
      try {
        const agent = this.getAgent(req.params.id);
        if (!agent) {
          return res.status(404).json({ success: false, error: 'Agent not found' });
        }
        
        const result = await agent.processTask(req.body);
        res.json({ success: true, result });
      } catch (error) {
        res.status(500).json({ success: false, error: (error as Error).message });
      }
    });

    // Scaling endpoints
    this.expressApp.post('/scale/agents', async (req, res) => {
      try {
        const { targetAI, targetSynthetic } = req.body;
        const result = await this.scaleAgents(targetAI, targetSynthetic);
        res.json({ success: true, result });
      } catch (error) {
        res.status(500).json({ success: false, error: (error as Error).message });
      }
    });

    // Web3 endpoints
    this.expressApp.post('/web3/register-agent', async (req, res) => {
      try {
        const result = await this.web3Integration.registerAgent(req.body);
        res.json({ success: true, transactionId: result });
      } catch (error) {
        res.status(500).json({ success: false, error: (error as Error).message });
      }
    });

    this.expressApp.get('/web3/status', (req, res) => {
      res.json(this.web3Integration.getMetrics());
    });

    // Performance report endpoint
    this.expressApp.get('/reports/performance', async (req, res) => {
      try {
        const report = await this.metrics.generatePerformanceReport();
        res.json(report);
      } catch (error) {
        res.status(500).json({ success: false, error: (error as Error).message });
      }
    });
  }

  private setupEventHandlers(): void {
    // System event handlers
    this.on('agent_created', (agentId, type) => {
      console.log(`Agent created: ${agentId} (${type})`);
      this.updateSystemStatus();
    });

    this.on('agent_error', (agentId, error) => {
      console.error(`Agent ${agentId} error:`, error);
      this.metrics.incrementCounter('agent_errors');
    });

    this.on('scaling_event', (event) => {
      console.log('Scaling event:', event);
      this.updateSystemStatus();
    });

    // Metrics events
    this.metrics.on('performance_alert', (alert) => {
      console.warn('Performance Alert:', alert);
      this.handlePerformanceAlert(alert);
    });

    // Web3 events
    this.web3Integration.on('agent_registered', (agentId) => {
      console.log(`Agent registered on blockchain: ${agentId}`);
    });

    // Graceful shutdown
    process.on('SIGTERM', () => this.gracefulShutdown());
    process.on('SIGINT', () => this.gracefulShutdown());
  }

  public async start(port: number = 3000): Promise<void> {
    try {
      console.log('Starting AI Time Machines...');
      
      // Start HTTP server
      this.httpServer = createServer(this.expressApp);
      this.httpServer.listen(port, () => {
        console.log(`AI Time Machines server listening on port ${port}`);
      });

      // Start WebSocket server
      this.wsServer = new WebSocket.Server({ server: this.httpServer });
      this.setupWebSocketHandlers();

      // Initialize agents
      await this.initializeDefaultAgents();

      // Update status
      this.systemStatus.status = 'RUNNING';
      this.systemStatus.uptime = Date.now();
      
      console.log('AI Time Machines started successfully');
      console.log(`Configuration: ${this.config.scale.maxAIAgents} AI Agents, ${this.config.scale.maxSyntheticAgents} Synthetic Agents`);
      console.log(`Web3 enabled: ${this.config.web3.enableWeb3}`);
      
      this.emit('system_started');
    } catch (error) {
      console.error('Failed to start AI Time Machines:', error);
      throw error;
    }
  }

  private setupWebSocketHandlers(): void {
    this.wsServer.on('connection', (ws) => {
      console.log('WebSocket client connected');
      
      // Send initial system status
      ws.send(JSON.stringify({
        type: 'system_status',
        data: this.getSystemMetrics()
      }));

      ws.on('message', async (message) => {
        try {
          const data = JSON.parse(message.toString());
          await this.handleWebSocketMessage(ws, data);
        } catch (error) {
          ws.send(JSON.stringify({
            type: 'error',
            error: (error as Error).message
          }));
        }
      });

      ws.on('close', () => {
        console.log('WebSocket client disconnected');
      });
    });

    // Broadcast system updates
    setInterval(() => {
      this.broadcastSystemUpdate();
    }, 5000);
  }

  private async handleWebSocketMessage(ws: WebSocket, data: any): Promise<void> {
    switch (data.type) {
      case 'create_agent':
        const agents = await this.createAgents(data.agentType, data.count || 1);
        ws.send(JSON.stringify({
          type: 'agents_created',
          data: agents.map(a => a.getId())
        }));
        break;

      case 'process_task':
        const agent = this.getAgent(data.agentId);
        if (agent) {
          const result = await agent.processTask(data.task);
          ws.send(JSON.stringify({
            type: 'task_result',
            data: { agentId: data.agentId, result }
          }));
        }
        break;

      case 'get_metrics':
        ws.send(JSON.stringify({
          type: 'metrics',
          data: this.getSystemMetrics()
        }));
        break;

      default:
        ws.send(JSON.stringify({
          type: 'error',
          error: `Unknown message type: ${data.type}`
        }));
    }
  }

  private broadcastSystemUpdate(): void {
    const update = {
      type: 'system_update',
      data: this.getSystemMetrics()
    };

    this.wsServer.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(update));
      }
    });
  }

  private async initializeDefaultAgents(): Promise<void> {
    console.log('Initializing default agents...');
    
    // Create initial AI agents (start small, scale as needed)
    const initialAIAgents = Math.min(100, this.config.scale.maxAIAgents);
    await this.createAgents('AI', initialAIAgents);

    // Create initial Synthetic AI agents
    const initialSyntheticAgents = Math.min(50, this.config.scale.maxSyntheticAgents);
    await this.createAgents('SYNTHETIC', initialSyntheticAgents);

    console.log(`Initialized ${initialAIAgents} AI agents and ${initialSyntheticAgents} Synthetic AI agents`);
  }

  public async createAgents(type: 'AI' | 'SYNTHETIC', count: number): Promise<BaseAgent[]> {
    const agents: BaseAgent[] = [];
    const maxCount = type === 'AI' ? this.config.scale.maxAIAgents : this.config.scale.maxSyntheticAgents;
    const currentCount = type === 'AI' ? this.agentPool.aiAgents.size : this.agentPool.syntheticAgents.size;
    
    const allowedCount = Math.min(count, maxCount - currentCount);
    
    for (let i = 0; i < allowedCount; i++) {
      const agentId = `${type.toLowerCase()}_agent_${this.agentIdCounter++}_${Date.now()}`;
      
      let agent: BaseAgent;
      if (type === 'AI') {
        agent = new AIAgent(agentId);
        this.agentPool.aiAgents.set(agentId, agent as AIAgent);
      } else {
        agent = new SyntheticAIAgent(agentId);
        this.agentPool.syntheticAgents.set(agentId, agent as SyntheticAIAgent);
      }

      // Register agent with Web3 if enabled
      if (this.config.web3.enableWeb3) {
        try {
          await this.web3Integration.registerAgent({
            agentId,
            agentType: type,
            capabilities: ['reasoning', 'learning', 'communication'],
            engineCount: agent.getEngineCount(),
            metadata: JSON.stringify({ createdAt: new Date().toISOString() })
          });
        } catch (error) {
          console.warn(`Failed to register agent ${agentId} on Web3:`, error);
        }
      }

      agents.push(agent);
      this.metrics.incrementCounter('agents_created', { type });
      this.emit('agent_created', agentId, type);
    }

    return agents;
  }

  public async scaleAgents(targetAI: number, targetSynthetic: number): Promise<any> {
    this.systemStatus.status = 'SCALING';
    
    const currentAI = this.agentPool.aiAgents.size;
    const currentSynthetic = this.agentPool.syntheticAgents.size;
    
    const result = {
      aiAgents: { current: currentAI, target: targetAI, change: 0 },
      syntheticAgents: { current: currentSynthetic, target: targetSynthetic, change: 0 }
    };

    // Scale AI Agents
    if (targetAI > currentAI) {
      const newAgents = await this.createAgents('AI', targetAI - currentAI);
      result.aiAgents.change = newAgents.length;
    } else if (targetAI < currentAI) {
      const toRemove = currentAI - targetAI;
      result.aiAgents.change = -await this.removeAgents('AI', toRemove);
    }

    // Scale Synthetic Agents
    if (targetSynthetic > currentSynthetic) {
      const newAgents = await this.createAgents('SYNTHETIC', targetSynthetic - currentSynthetic);
      result.syntheticAgents.change = newAgents.length;
    } else if (targetSynthetic < currentSynthetic) {
      const toRemove = currentSynthetic - targetSynthetic;
      result.syntheticAgents.change = -await this.removeAgents('SYNTHETIC', toRemove);
    }

    this.systemStatus.status = 'RUNNING';
    this.emit('scaling_event', result);
    
    return result;
  }

  private async removeAgents(type: 'AI' | 'SYNTHETIC', count: number): Promise<number> {
    const pool = type === 'AI' ? this.agentPool.aiAgents : this.agentPool.syntheticAgents;
    const agents = Array.from(pool.keys()).slice(0, count);
    
    for (const agentId of agents) {
      const agent = pool.get(agentId);
      if (agent) {
        await agent.shutdown();
        pool.delete(agentId);
      }
    }
    
    return agents.length;
  }

  public getAgent(agentId: string): BaseAgent | undefined {
    return this.agentPool.aiAgents.get(agentId) || this.agentPool.syntheticAgents.get(agentId);
  }

  public getAllAgents(): BaseAgent[] {
    return [
      ...Array.from(this.agentPool.aiAgents.values()),
      ...Array.from(this.agentPool.syntheticAgents.values())
    ];
  }

  private updateSystemStatus(): void {
    this.systemStatus.totalAgents = this.agentPool.aiAgents.size + this.agentPool.syntheticAgents.size;
    this.systemStatus.activeAgents = this.getAllAgents().filter(a => a.getStatus() === 'ACTIVE').length;
    this.systemStatus.totalEngines = this.getAllAgents().reduce((sum, agent) => sum + agent.getEngineCount(), 0);
  }

  private getSystemMetrics(): any {
    this.updateSystemStatus();
    
    return {
      ...this.systemStatus,
      agentPoolSizes: {
        ai: this.agentPool.aiAgents.size,
        synthetic: this.agentPool.syntheticAgents.size
      },
      limits: {
        maxAIAgents: this.config.scale.maxAIAgents,
        maxSyntheticAgents: this.config.scale.maxSyntheticAgents,
        maxEnginesPerAgent: this.config.scale.maxEnginesPerAgent
      },
      performance: this.metrics.getCurrentMetrics(),
      web3: this.web3Integration.getMetrics()
    };
  }

  private handlePerformanceAlert(alert: any): void {
    // Implement auto-scaling or other responses to performance alerts
    if (alert.level === 'CRITICAL' || alert.level === 'EMERGENCY') {
      console.warn(`Critical performance issue detected: ${alert.message}`);
      
      // Example: Auto-scale if agents are overloaded
      if (alert.component === 'cpu' && alert.metrics.value > 0.9) {
        this.autoScale();
      }
    }
  }

  private async autoScale(): Promise<void> {
    if (this.systemStatus.status === 'SCALING') return;
    
    console.log('Triggering auto-scale...');
    const currentTotal = this.systemStatus.totalAgents;
    const scaleUp = Math.min(Math.floor(currentTotal * 0.1), 1000); // Scale up by 10% or max 1000
    
    await this.createAgents('AI', Math.floor(scaleUp * 0.7));
    await this.createAgents('SYNTHETIC', Math.floor(scaleUp * 0.3));
  }

  public async gracefulShutdown(): Promise<void> {
    if (this.isShuttingDown) return;
    
    this.isShuttingDown = true;
    this.systemStatus.status = 'SHUTDOWN';
    
    console.log('Initiating graceful shutdown...');
    
    // Stop accepting new connections
    this.wsServer.close();
    this.httpServer.close();
    
    // Shutdown all agents
    const allAgents = this.getAllAgents();
    await Promise.all(allAgents.map(agent => agent.shutdown()));
    
    // Shutdown integrations
    await this.web3Integration.shutdown();
    this.metrics.shutdown();
    
    console.log('AI Time Machines shutdown complete');
    process.exit(0);
  }

  // Static method to create clustered deployment
  public static async createClusteredDeployment(config: AppConfig = defaultConfig): Promise<void> {
    const numCPUs = config.scale.clusterNodes || os.cpus().length;
    
    if (cluster.isMaster) {
      console.log(`Master ${process.pid} is running`);
      console.log(`Starting ${numCPUs} worker processes...`);
      
      // Fork workers
      for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
      }
      
      cluster.on('exit', (worker, code, signal) => {
        console.log(`Worker ${worker.process.pid} died with code ${code} and signal ${signal}`);
        console.log('Starting a new worker');
        cluster.fork();
      });
    } else {
      // Worker process
      const aiTimeMachines = new AITimeMachines(config);
      const port = 3000 + (cluster.worker?.id || 0);
      await aiTimeMachines.start(port);
      console.log(`Worker ${process.pid} started on port ${port}`);
    }
  }
}