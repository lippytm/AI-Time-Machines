/**
 * Standard AI Agent Implementation
 * Supports up to 100,000 AI Engines for massive parallel processing
 */

import { BaseAgent } from '../core/base-agent';
import { AIEngine } from '../engines/ai-engine';

export class AIAgent extends BaseAgent {
  private engineIdCounter: number = 0;

  constructor(id: string) {
    super(id, 'AI');
    this.initializeDefaultEngines();
  }

  protected async executeTask(task: any): Promise<any> {
    // Route task to appropriate engines based on task type
    const engines = this.selectEnginesForTask(task);
    
    if (engines.length === 0) {
      throw new Error(`No suitable engines found for task type: ${task.type}`);
    }

    // Process task using selected engines
    const results = await Promise.all(
      engines.map(engine => engine.processOperation(task))
    );

    // Aggregate results
    return this.aggregateResults(results, task);
  }

  private selectEnginesForTask(task: any): AIEngine[] {
    const allEngines = Array.from(this.state.engines.values());
    
    // Simple selection strategy - can be enhanced with more sophisticated routing
    switch (task.type) {
      case 'NLP':
        return allEngines.slice(0, Math.min(5, allEngines.length));
      case 'ML':
        return allEngines.slice(0, Math.min(10, allEngines.length));
      case 'ANALYSIS':
        return allEngines.slice(0, Math.min(3, allEngines.length));
      default:
        return allEngines.slice(0, Math.min(2, allEngines.length));
    }
  }

  private aggregateResults(results: any[], task: any): any {
    return {
      taskId: task.id || `task_${Date.now()}`,
      type: task.type,
      engineCount: results.length,
      results: results,
      aggregatedResult: this.synthesizeResults(results),
      completedAt: new Date().toISOString(),
      agentId: this.getId()
    };
  }

  private synthesizeResults(results: any[]): any {
    // Simple synthesis - can be enhanced with more sophisticated algorithms
    const confidenceSum = results.reduce((sum, result) => {
      return sum + (result.confidence || result.accuracy || 0.5);
    }, 0);
    
    return {
      averageConfidence: confidenceSum / results.length,
      consensusReached: results.length > 1 && confidenceSum / results.length > 0.7,
      primaryResult: results[0]?.result,
      alternativeResults: results.slice(1).map(r => r.result)
    };
  }

  public async createEngine(): Promise<string> {
    const engineId = `${this.getId()}_engine_${this.engineIdCounter++}`;
    const engine = new AIEngine(engineId, this.getId());
    
    const added = await this.addEngine(engine);
    if (!added) {
      throw new Error('Failed to add engine - maximum limit reached');
    }
    
    return engineId;
  }

  public async createMultipleEngines(count: number): Promise<string[]> {
    const engineIds: string[] = [];
    const maxAllowed = Math.min(count, this.maxEngines - this.getEngineCount());
    
    for (let i = 0; i < maxAllowed; i++) {
      try {
        const engineId = await this.createEngine();
        engineIds.push(engineId);
      } catch (error) {
        console.warn(`Failed to create engine ${i + 1}/${count}:`, error);
        break;
      }
    }
    
    return engineIds;
  }

  private async initializeDefaultEngines(): Promise<void> {
    // Create initial set of engines for basic operations
    const defaultEngineCount = Math.min(10, this.maxEngines);
    await this.createMultipleEngines(defaultEngineCount);
  }

  public async scaleEngines(targetCount: number): Promise<number> {
    const currentCount = this.getEngineCount();
    
    if (targetCount > currentCount) {
      // Scale up
      const toAdd = Math.min(targetCount - currentCount, this.maxEngines - currentCount);
      const added = await this.createMultipleEngines(toAdd);
      return added.length;
    } else if (targetCount < currentCount) {
      // Scale down
      const toRemove = currentCount - targetCount;
      const engines = Array.from(this.state.engines.keys());
      let removed = 0;
      
      for (let i = 0; i < toRemove && i < engines.length; i++) {
        const success = await this.removeEngine(engines[i]);
        if (success) removed++;
      }
      
      return -removed;
    }
    
    return 0; // No scaling needed
  }

  public async processComplexTask(task: any): Promise<any> {
    // Break down complex tasks into subtasks for parallel processing
    const subtasks = this.decomposeTask(task);
    const subtaskResults = [];

    for (const subtask of subtasks) {
      const result = await this.executeTask(subtask);
      subtaskResults.push(result);
    }

    return this.combineSubtaskResults(task, subtaskResults);
  }

  private decomposeTask(task: any): any[] {
    // Simple task decomposition - can be enhanced
    if (task.complexity === 'high' && task.data && Array.isArray(task.data)) {
      return task.data.map((item: any, index: number) => ({
        ...task,
        id: `${task.id || 'task'}_subtask_${index}`,
        data: item,
        complexity: 'low'
      }));
    }
    
    return [task];
  }

  private combineSubtaskResults(originalTask: any, subtaskResults: any[]): any {
    return {
      originalTask: originalTask.id || 'unknown',
      subtaskCount: subtaskResults.length,
      combinedResults: subtaskResults,
      overallSuccess: subtaskResults.every(r => r.aggregatedResult?.consensusReached !== false),
      completedAt: new Date().toISOString(),
      agentId: this.getId()
    };
  }
}