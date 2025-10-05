/**
 * Metrics Collection and Performance Monitoring
 * Designed for massive scale monitoring of 200k+ agents
 */

import { EventEmitter } from 'events';
import { register, Counter, Histogram, Gauge, collectDefaultMetrics } from 'prom-client';

export interface SystemMetrics {
  totalAgents: number;
  activeAgents: number;
  totalEngines: number;
  activeEngines: number;
  tasksProcessed: number;
  errorsCount: number;
  averageResponseTime: number;
  memoryUsage: number;
  cpuUsage: number;
  networkConnections: number;
  web3Transactions: number;
}

export interface PerformanceAlert {
  level: 'INFO' | 'WARNING' | 'CRITICAL' | 'EMERGENCY';
  component: string;
  message: string;
  timestamp: Date;
  metrics: any;
}

export class MetricsCollector extends EventEmitter {
  private static instance: MetricsCollector;
  
  // Prometheus metrics
  private agentCounter!: Counter<string>;
  private engineCounter!: Counter<string>;
  private taskCounter!: Counter<string>;
  private errorCounter!: Counter<string>;
  private responseTimeHistogram!: Histogram<string>;
  private memoryGauge!: Gauge<string>;
  private cpuGauge!: Gauge<string>;
  private web3TransactionCounter!: Counter<string>;
  
  private performanceThresholds: any;
  private alertHistory: PerformanceAlert[] = [];
  private metricsBuffer: Map<string, number> = new Map();
  private collectionInterval: NodeJS.Timeout | null = null;

  private constructor() {
    super();
    this.initializeMetrics();
    this.setupPerformanceThresholds();
    this.startMetricsCollection();
  }

  public static getInstance(): MetricsCollector {
    if (!MetricsCollector.instance) {
      MetricsCollector.instance = new MetricsCollector();
    }
    return MetricsCollector.instance;
  }

  private initializeMetrics(): void {
    // Initialize Prometheus metrics for large-scale monitoring
    collectDefaultMetrics({ prefix: 'ai_time_machines_' });

    this.agentCounter = new Counter({
      name: 'ai_agents_total',
      help: 'Total number of AI agents',
      labelNames: ['type', 'status']
    });

    this.engineCounter = new Counter({
      name: 'ai_engines_total',
      help: 'Total number of AI engines',
      labelNames: ['agent_id', 'status']
    });

    this.taskCounter = new Counter({
      name: 'tasks_processed_total',
      help: 'Total number of tasks processed',
      labelNames: ['agent_type', 'task_type', 'status']
    });

    this.errorCounter = new Counter({
      name: 'errors_total',
      help: 'Total number of errors',
      labelNames: ['component', 'error_type']
    });

    this.responseTimeHistogram = new Histogram({
      name: 'response_time_seconds',
      help: 'Response time for operations',
      labelNames: ['operation', 'agent_type'],
      buckets: [0.1, 0.5, 1, 2, 5, 10, 30]
    });

    this.memoryGauge = new Gauge({
      name: 'memory_usage_bytes',
      help: 'Memory usage in bytes',
      labelNames: ['component']
    });

    this.cpuGauge = new Gauge({
      name: 'cpu_usage_percent',
      help: 'CPU usage percentage',
      labelNames: ['component']
    });

    this.web3TransactionCounter = new Counter({
      name: 'web3_transactions_total',
      help: 'Total Web3 transactions',
      labelNames: ['type', 'status']
    });
  }

  private setupPerformanceThresholds(): void {
    this.performanceThresholds = {
      memory: {
        warning: 0.7,  // 70% memory usage
        critical: 0.85, // 85% memory usage
        emergency: 0.95 // 95% memory usage
      },
      cpu: {
        warning: 0.7,   // 70% CPU usage
        critical: 0.85, // 85% CPU usage
        emergency: 0.95 // 95% CPU usage
      },
      responseTime: {
        warning: 5000,   // 5 seconds
        critical: 10000, // 10 seconds
        emergency: 30000 // 30 seconds
      },
      errorRate: {
        warning: 0.05,  // 5% error rate
        critical: 0.1,  // 10% error rate
        emergency: 0.2  // 20% error rate
      },
      agentFailures: {
        warning: 10,    // 10 agent failures
        critical: 50,   // 50 agent failures
        emergency: 100  // 100 agent failures
      }
    };
  }

  private startMetricsCollection(): void {
    this.collectionInterval = setInterval(() => {
      this.collectSystemMetrics();
      this.checkPerformanceThresholds();
    }, 10000); // Collect every 10 seconds
  }

  public incrementCounter(metric: string, labels?: any): void {
    switch (metric) {
      case 'agents_created':
        this.agentCounter.inc({ ...labels, status: 'created' });
        break;
      case 'agents_active':
        this.agentCounter.inc({ ...labels, status: 'active' });
        break;
      case 'agents_error':
        this.agentCounter.inc({ ...labels, status: 'error' });
        break;
      case 'engines_added':
        this.engineCounter.inc({ ...labels, status: 'added' });
        break;
      case 'engines_removed':
        this.engineCounter.inc({ ...labels, status: 'removed' });
        break;
      case 'tasks_processed':
        this.taskCounter.inc({ ...labels, status: 'completed' });
        break;
      case 'task_errors':
        this.taskCounter.inc({ ...labels, status: 'error' });
        break;
      case 'operations_processed':
        this.taskCounter.inc({ ...labels, status: 'processed' });
        break;
      case 'operation_errors':
        this.errorCounter.inc({ component: 'engine', error_type: 'operation' });
        break;
      case 'agent_errors':
        this.errorCounter.inc({ component: 'agent', error_type: 'general' });
        break;
      case 'web3_transactions_confirmed':
        this.web3TransactionCounter.inc({ type: 'transaction', status: 'confirmed' });
        break;
      case 'web3_transactions_failed':
        this.web3TransactionCounter.inc({ type: 'transaction', status: 'failed' });
        break;
      case 'web3_agents_registered':
        this.web3TransactionCounter.inc({ type: 'registration', status: 'success' });
        break;
      case 'web3_registration_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'registration' });
        break;
      case 'web3_task_creation_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'task_creation' });
        break;
      case 'web3_result_submission_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'result_submission' });
        break;
      case 'web3_reward_claim_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'reward_claim' });
        break;
      case 'web3_governance_vote_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'governance_vote' });
        break;
      case 'ipfs_uploads':
        this.web3TransactionCounter.inc({ type: 'ipfs', status: 'upload' });
        break;
      case 'ipfs_upload_errors':
        this.errorCounter.inc({ component: 'ipfs', error_type: 'upload' });
        break;
      case 'ipfs_retrievals':
        this.web3TransactionCounter.inc({ type: 'ipfs', status: 'retrieval' });
        break;
      case 'ipfs_retrieval_errors':
        this.errorCounter.inc({ component: 'ipfs', error_type: 'retrieval' });
        break;
      case 'reputation_queries':
        this.web3TransactionCounter.inc({ type: 'reputation', status: 'query' });
        break;
      case 'reputation_query_errors':
        this.errorCounter.inc({ component: 'web3', error_type: 'reputation_query' });
        break;
      default:
        console.warn(`Unknown metric: ${metric}`);
    }
  }

  public recordHistogram(metric: string, value: number, labels?: any): void {
    switch (metric) {
      case 'operation_duration_ms':
        this.responseTimeHistogram.observe({ operation: 'engine_operation', ...labels }, value / 1000);
        break;
      case 'task_duration_ms':
        this.responseTimeHistogram.observe({ operation: 'task_processing', ...labels }, value / 1000);
        break;
      case 'agent_response_time_ms':
        this.responseTimeHistogram.observe({ operation: 'agent_response', ...labels }, value / 1000);
        break;
      default:
        console.warn(`Unknown histogram metric: ${metric}`);
    }
  }

  public setGauge(metric: string, value: number, labels?: any): void {
    switch (metric) {
      case 'memory_usage':
        this.memoryGauge.set({ component: labels?.component || 'system' }, value);
        break;
      case 'cpu_usage':
        this.cpuGauge.set({ component: labels?.component || 'system' }, value);
        break;
      default:
        console.warn(`Unknown gauge metric: ${metric}`);
    }
  }

  private collectSystemMetrics(): void {
    // Collect system-level metrics
    const memoryUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();

    // Update memory metrics
    this.memoryGauge.set({ component: 'heap' }, memoryUsage.heapUsed);
    this.memoryGauge.set({ component: 'heap_total' }, memoryUsage.heapTotal);
    this.memoryGauge.set({ component: 'external' }, memoryUsage.external);
    this.memoryGauge.set({ component: 'rss' }, memoryUsage.rss);

    // Simulate CPU usage (in real implementation, this would be calculated)
    const cpuPercent = Math.random() * 0.3 + 0.1; // 10-40% usage simulation
    this.cpuGauge.set({ component: 'system' }, cpuPercent);

    // Store in buffer for threshold checking
    this.metricsBuffer.set('memory_usage_percent', memoryUsage.heapUsed / memoryUsage.heapTotal);
    this.metricsBuffer.set('cpu_usage_percent', cpuPercent);
  }

  private checkPerformanceThresholds(): void {
    // Check memory usage
    const memoryUsage = this.metricsBuffer.get('memory_usage_percent') || 0;
    this.checkThreshold('memory', memoryUsage, 'Memory usage');

    // Check CPU usage
    const cpuUsage = this.metricsBuffer.get('cpu_usage_percent') || 0;
    this.checkThreshold('cpu', cpuUsage, 'CPU usage');

    // Check error rate (simulated)
    const errorRate = Math.random() * 0.02; // Simulate 0-2% error rate
    this.checkThreshold('errorRate', errorRate, 'Error rate');

    // Emit performance summary
    this.emit('performance_update', this.getCurrentMetrics());
  }

  private checkThreshold(type: string, value: number, description: string): void {
    const thresholds = this.performanceThresholds[type];
    if (!thresholds) return;

    let level: 'INFO' | 'WARNING' | 'CRITICAL' | 'EMERGENCY' = 'INFO';
    
    if (value >= thresholds.emergency) {
      level = 'EMERGENCY';
    } else if (value >= thresholds.critical) {
      level = 'CRITICAL';
    } else if (value >= thresholds.warning) {
      level = 'WARNING';
    }

    if (level !== 'INFO') {
      const alert: PerformanceAlert = {
        level,
        component: type,
        message: `${description} is ${(value * 100).toFixed(2)}%`,
        timestamp: new Date(),
        metrics: { value, threshold: thresholds }
      };

      this.addAlert(alert);
      this.emit('performance_alert', alert);
    }
  }

  private addAlert(alert: PerformanceAlert): void {
    this.alertHistory.push(alert);
    
    // Keep only last 1000 alerts to prevent memory issues
    if (this.alertHistory.length > 1000) {
      this.alertHistory = this.alertHistory.slice(-500);
    }
  }

  public getCurrentMetrics(): SystemMetrics {
    // This would be calculated from actual system state in real implementation
    return {
      totalAgents: Math.floor(Math.random() * 200000) + 150000, // 150k-350k simulation
      activeAgents: Math.floor(Math.random() * 180000) + 120000, // Active agents
      totalEngines: Math.floor(Math.random() * 20000000) + 15000000, // 15M-35M engines
      activeEngines: Math.floor(Math.random() * 18000000) + 12000000, // Active engines
      tasksProcessed: Math.floor(Math.random() * 1000000) + 500000, // Tasks processed
      errorsCount: Math.floor(Math.random() * 5000) + 1000, // Error count
      averageResponseTime: Math.random() * 2000 + 500, // 500-2500ms
      memoryUsage: this.metricsBuffer.get('memory_usage_percent') || 0,
      cpuUsage: this.metricsBuffer.get('cpu_usage_percent') || 0,
      networkConnections: Math.floor(Math.random() * 10000) + 5000, // Network connections
      web3Transactions: Math.floor(Math.random() * 50000) + 25000 // Web3 transactions
    };
  }

  public getAlerts(level?: string): PerformanceAlert[] {
    if (level) {
      return this.alertHistory.filter(alert => alert.level === level);
    }
    return [...this.alertHistory];
  }

  public getPrometheusMetrics(): Promise<string> {
    return register.metrics();
  }

  public async generatePerformanceReport(): Promise<any> {
    const metrics = this.getCurrentMetrics();
    const recentAlerts = this.alertHistory.slice(-50); // Last 50 alerts
    
    return {
      timestamp: new Date().toISOString(),
      summary: {
        agentUtilization: (metrics.activeAgents / metrics.totalAgents * 100).toFixed(2) + '%',
        engineUtilization: (metrics.activeEngines / metrics.totalEngines * 100).toFixed(2) + '%',
        systemHealth: this.calculateSystemHealth(metrics),
        scalabilityStatus: this.assessScalability(metrics)
      },
      metrics,
      recentAlerts,
      recommendations: this.generateRecommendations(metrics, recentAlerts)
    };
  }

  private calculateSystemHealth(metrics: SystemMetrics): string {
    let score = 100;
    
    if (metrics.memoryUsage > 0.8) score -= 20;
    if (metrics.cpuUsage > 0.8) score -= 20;
    if (metrics.averageResponseTime > 5000) score -= 15;
    if (metrics.errorsCount / metrics.tasksProcessed > 0.05) score -= 25;
    
    if (score >= 90) return 'EXCELLENT';
    if (score >= 75) return 'GOOD';
    if (score >= 60) return 'FAIR';
    if (score >= 40) return 'POOR';
    return 'CRITICAL';
  }

  private assessScalability(metrics: SystemMetrics): string {
    const agentUtilization = metrics.activeAgents / metrics.totalAgents;
    const engineUtilization = metrics.activeEngines / metrics.totalEngines;
    
    if (agentUtilization > 0.9 || engineUtilization > 0.9) {
      return 'SCALING_NEEDED';
    } else if (agentUtilization > 0.7 || engineUtilization > 0.7) {
      return 'MONITOR_CLOSELY';
    } else {
      return 'CAPACITY_AVAILABLE';
    }
  }

  private generateRecommendations(metrics: SystemMetrics, alerts: PerformanceAlert[]): string[] {
    const recommendations = [];
    
    if (metrics.memoryUsage > 0.8) {
      recommendations.push('Consider increasing memory allocation or optimizing memory usage');
    }
    
    if (metrics.cpuUsage > 0.8) {
      recommendations.push('Consider scaling horizontally or optimizing CPU-intensive operations');
    }
    
    if (metrics.averageResponseTime > 5000) {
      recommendations.push('Optimize task processing algorithms or increase parallel processing');
    }
    
    const criticalAlerts = alerts.filter(a => a.level === 'CRITICAL' || a.level === 'EMERGENCY');
    if (criticalAlerts.length > 5) {
      recommendations.push('Address critical performance issues immediately');
    }
    
    if (metrics.activeAgents / metrics.totalAgents > 0.9) {
      recommendations.push('Scale agent capacity to handle increased load');
    }
    
    return recommendations;
  }

  public shutdown(): void {
    if (this.collectionInterval) {
      clearInterval(this.collectionInterval);
    }
    this.removeAllListeners();
    register.clear();
  }
}