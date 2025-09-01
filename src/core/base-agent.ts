/**
 * Core AI Agent interface and base implementation
 * Designed to scale to 100,000+ instances
 */

import { EventEmitter } from 'events';
import { AIEngine } from '../engines/ai-engine';
import { MetricsCollector } from '../monitoring/metrics';

export interface AgentCapabilities {
  reasoning: boolean;
  learning: boolean;
  communication: boolean;
  decentralizedInteraction: boolean;
  web3Integration: boolean;
}

export interface AgentState {
  id: string;
  type: 'AI' | 'SYNTHETIC';
  status: 'ACTIVE' | 'IDLE' | 'PROCESSING' | 'ERROR' | 'OFFLINE';
  capabilities: AgentCapabilities;
  engines: Map<string, AIEngine>;
  createdAt: Date;
  lastActiveAt: Date;
  processedTasks: number;
  errorCount: number;
}

export abstract class BaseAgent extends EventEmitter {
  protected state: AgentState;
  protected metrics: MetricsCollector;
  protected maxEngines: number;

  constructor(id: string, type: 'AI' | 'SYNTHETIC', maxEngines: number = 100000) {
    super();
    this.maxEngines = maxEngines;
    this.metrics = MetricsCollector.getInstance();
    
    this.state = {
      id,
      type,
      status: 'IDLE',
      capabilities: {
        reasoning: true,
        learning: true,
        communication: true,
        decentralizedInteraction: true,
        web3Integration: true
      },
      engines: new Map(),
      createdAt: new Date(),
      lastActiveAt: new Date(),
      processedTasks: 0,
      errorCount: 0
    };

    this.setupEventHandlers();
  }

  public getId(): string {
    return this.state.id;
  }

  public getType(): 'AI' | 'SYNTHETIC' {
    return this.state.type;
  }

  public getStatus(): string {
    return this.state.status;
  }

  public getEngineCount(): number {
    return this.state.engines.size;
  }

  public async addEngine(engine: AIEngine): Promise<boolean> {
    if (this.state.engines.size >= this.maxEngines) {
      this.emit('error', new Error(`Maximum engines limit reached: ${this.maxEngines}`));
      return false;
    }

    this.state.engines.set(engine.getId(), engine);
    this.metrics.incrementCounter('engines_added');
    this.emit('engine_added', engine.getId());
    return true;
  }

  public async removeEngine(engineId: string): Promise<boolean> {
    const removed = this.state.engines.delete(engineId);
    if (removed) {
      this.metrics.incrementCounter('engines_removed');
      this.emit('engine_removed', engineId);
    }
    return removed;
  }

  public async processTask(task: any): Promise<any> {
    try {
      this.state.status = 'PROCESSING';
      this.state.lastActiveAt = new Date();
      
      const result = await this.executeTask(task);
      
      this.state.processedTasks++;
      this.state.status = 'ACTIVE';
      this.metrics.incrementCounter('tasks_processed');
      
      return result;
    } catch (error) {
      this.state.errorCount++;
      this.state.status = 'ERROR';
      this.metrics.incrementCounter('task_errors');
      this.emit('error', error);
      throw error;
    }
  }

  public getMetrics(): any {
    return {
      id: this.state.id,
      type: this.state.type,
      status: this.state.status,
      engineCount: this.state.engines.size,
      processedTasks: this.state.processedTasks,
      errorCount: this.state.errorCount,
      uptime: Date.now() - this.state.createdAt.getTime(),
      lastActive: this.state.lastActiveAt
    };
  }

  protected abstract executeTask(task: any): Promise<any>;

  protected setupEventHandlers(): void {
    this.on('error', (error) => {
      console.error(`Agent ${this.state.id} error:`, error);
      this.metrics.incrementCounter('agent_errors');
    });

    this.on('engine_added', (engineId) => {
      console.log(`Engine ${engineId} added to agent ${this.state.id}`);
    });

    this.on('engine_removed', (engineId) => {
      console.log(`Engine ${engineId} removed from agent ${this.state.id}`);
    });
  }

  public async shutdown(): Promise<void> {
    this.state.status = 'OFFLINE';
    // Cleanup engines
    for (const engine of this.state.engines.values()) {
      await engine.shutdown();
    }
    this.state.engines.clear();
    this.removeAllListeners();
  }
}