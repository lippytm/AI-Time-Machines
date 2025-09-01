/**
 * AI Time Machines - Main Entry Point
 * High-performance, scalable AI Agent platform with Web3 integration
 */

import { AITimeMachines } from './orchestration';
import { defaultConfig } from './config/scale-config';

async function main(): Promise<void> {
  try {
    console.log('🚀 AI Time Machines - Starting...');
    console.log('📊 Configuration:');
    console.log(`   • Max AI Agents: ${defaultConfig.scale.maxAIAgents.toLocaleString()}`);
    console.log(`   • Max Synthetic AI Agents: ${defaultConfig.scale.maxSyntheticAgents.toLocaleString()}`);
    console.log(`   • Max Engines per Agent: ${defaultConfig.scale.maxEnginesPerAgent.toLocaleString()}`);
    console.log(`   • Web3 Integration: ${defaultConfig.web3.enableWeb3 ? '✅ Enabled' : '❌ Disabled'}`);
    console.log(`   • Cluster Nodes: ${defaultConfig.scale.clusterNodes}`);
    console.log('');

    // Check if clustering is requested
    const useCluster = process.env.CLUSTER === 'true' || process.argv.includes('--cluster');
    
    if (useCluster) {
      console.log('🔧 Starting in clustered mode...');
      await AITimeMachines.createClusteredDeployment(defaultConfig);
    } else {
      console.log('🔧 Starting in single-node mode...');
      const aiTimeMachines = new AITimeMachines(defaultConfig);
      
      // Setup additional event handlers for main process
      aiTimeMachines.on('system_started', () => {
        console.log('✅ AI Time Machines system started successfully');
        console.log('🌐 Access the system at: http://localhost:3000');
        console.log('📈 Metrics endpoint: http://localhost:3000/metrics');
        console.log('🏥 Health check: http://localhost:3000/health');
        console.log('📊 Performance report: http://localhost:3000/reports/performance');
      });

      aiTimeMachines.on('agent_created', (agentId, type) => {
        console.log(`🤖 New ${type} agent created: ${agentId}`);
      });

      aiTimeMachines.on('scaling_event', (event) => {
        console.log('📈 Scaling event:', {
          aiAgents: `${event.aiAgents.current} → ${event.aiAgents.current + event.aiAgents.change}`,
          syntheticAgents: `${event.syntheticAgents.current} → ${event.syntheticAgents.current + event.syntheticAgents.change}`
        });
      });

      await aiTimeMachines.start(3000);
    }

  } catch (error) {
    console.error('❌ Failed to start AI Time Machines:', error);
    process.exit(1);
  }
}

// Handle unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

// Start the application
if (require.main === module) {
  main();
}

export { AITimeMachines } from './orchestration';
export { AIAgent } from './agents/ai-agent';
export { SyntheticAIAgent } from './agents/synthetic-ai-agent';
export { AIEngine } from './engines/ai-engine';
export { Web3Integration } from './web3/integration';
export { MetricsCollector } from './monitoring/metrics';
export * from './config/scale-config';