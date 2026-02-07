/**
 * Integration Examples
 * 
 * This file demonstrates how to use the platform integrations with
 * ManyChat, BotBuilders, OpenClaw, and Moltbook.
 */

const axios = require('axios');

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000/api';
const API_TOKEN = process.env.API_TOKEN; // Set your JWT token

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json'
  }
});

/**
 * Example 1: Create a ManyChat Integration
 */
async function createManyChatIntegration() {
  console.log('\n=== Creating ManyChat Integration ===');
  
  try {
    const response = await api.post('/integrations', {
      name: 'My ManyChat Bot',
      platform: 'manychat',
      description: 'Send time-series predictions to ManyChat bot',
      apiKey: process.env.MANYCHAT_API_KEY,
      webhookUrl: 'https://api.manychat.com/webhook',
      config: {
        botId: 'your-bot-id',
        autoSend: true
      }
    });
    
    console.log('✅ Integration created:', response.data.integration.id);
    return response.data.integration;
  } catch (error) {
    console.error('❌ Failed to create integration:', error.response?.data || error.message);
  }
}

/**
 * Example 2: Create a BotBuilders Integration
 */
async function createBotBuildersIntegration() {
  console.log('\n=== Creating BotBuilders Integration ===');
  
  try {
    const response = await api.post('/integrations', {
      name: 'Multi-Platform Bot',
      platform: 'botbuilders',
      description: 'Send predictions to multiple messaging platforms',
      apiKey: process.env.BOTBUILDERS_API_KEY,
      apiSecret: process.env.BOTBUILDERS_API_SECRET,
      webhookUrl: 'https://api.botbuilders.com/webhook',
      config: {
        platforms: ['whatsapp', 'telegram', 'sms'],
        notificationTemplate: 'prediction_alert'
      }
    });
    
    console.log('✅ Integration created:', response.data.integration.id);
    return response.data.integration;
  } catch (error) {
    console.error('❌ Failed to create integration:', error.response?.data || error.message);
  }
}

/**
 * Example 3: Create an OpenClaw Integration
 */
async function createOpenClawIntegration() {
  console.log('\n=== Creating OpenClaw Integration ===');
  
  try {
    const response = await api.post('/integrations', {
      name: 'Analytics Pipeline',
      platform: 'openclaw',
      description: 'Feed predictions into analytics system',
      apiKey: process.env.OPENCLAW_API_KEY,
      webhookUrl: 'https://openclaw.io/api/events',
      config: {
        pipeline: 'time-series-analysis',
        triggerWorkflow: true
      }
    });
    
    console.log('✅ Integration created:', response.data.integration.id);
    return response.data.integration;
  } catch (error) {
    console.error('❌ Failed to create integration:', error.response?.data || error.message);
  }
}

/**
 * Example 4: Create a Moltbook Integration
 */
async function createMoltbookIntegration() {
  console.log('\n=== Creating Moltbook Integration ===');
  
  try {
    const response = await api.post('/integrations', {
      name: 'Analysis Notebook',
      platform: 'moltbook',
      description: 'Export predictions to interactive notebooks',
      apiKey: process.env.MOLTBOOK_API_KEY,
      config: {
        notebookId: 'predictions-analysis',
        autoVisualize: true,
        includeCode: true
      }
    });
    
    console.log('✅ Integration created:', response.data.integration.id);
    return response.data.integration;
  } catch (error) {
    console.error('❌ Failed to create integration:', error.response?.data || error.message);
  }
}

/**
 * Example 5: List All Integrations
 */
async function listIntegrations() {
  console.log('\n=== Listing All Integrations ===');
  
  try {
    const response = await api.get('/integrations');
    
    console.log(`Found ${response.data.count} integrations:`);
    response.data.integrations.forEach(integration => {
      console.log(`- ${integration.name} (${integration.platform}) - Status: ${integration.syncStatus}`);
    });
    
    return response.data.integrations;
  } catch (error) {
    console.error('❌ Failed to list integrations:', error.response?.data || error.message);
  }
}

/**
 * Example 6: Test an Integration
 */
async function testIntegration(integrationId) {
  console.log('\n=== Testing Integration ===');
  
  try {
    const response = await api.post(`/integrations/${integrationId}/test`);
    
    console.log('✅ Test result:', response.data.message);
    return response.data;
  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

/**
 * Example 7: Send Prediction to Integration
 */
async function sendPredictionToIntegration(integrationId, predictionId) {
  console.log('\n=== Sending Prediction to Integration ===');
  
  try {
    const response = await api.post(`/integrations/${integrationId}/send`, {
      predictionId
    });
    
    console.log('✅ Prediction sent:', response.data.message);
    return response.data;
  } catch (error) {
    console.error('❌ Failed to send prediction:', error.response?.data || error.message);
  }
}

/**
 * Example 8: Export Prediction in Different Formats
 */
async function exportPredictionExamples(predictionId) {
  console.log('\n=== Exporting Prediction in Multiple Formats ===');
  
  const formats = ['json', 'csv', 'xml', 'manychat', 'botbuilders', 'openclaw', 'moltbook'];
  
  for (const format of formats) {
    try {
      const response = await api.get(`/predictions/${predictionId}/export`, {
        params: { format }
      });
      
      console.log(`✅ Exported as ${format.toUpperCase()}`);
      
      // Show sample of data
      if (format === 'csv' || format === 'xml') {
        console.log(response.data.substring(0, 200) + '...\n');
      } else {
        console.log(JSON.stringify(response.data, null, 2).substring(0, 200) + '...\n');
      }
    } catch (error) {
      console.error(`❌ Failed to export as ${format}:`, error.response?.data || error.message);
    }
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('=================================================');
  console.log('   AI-Time-Machines Integration Examples');
  console.log('=================================================');
  
  if (!API_TOKEN) {
    console.error('❌ Error: API_TOKEN environment variable not set');
    console.log('Please set your JWT token: export API_TOKEN="your-token-here"');
    return;
  }
  
  // Create integrations
  const manychat = await createManyChatIntegration();
  const botbuilders = await createBotBuildersIntegration();
  const openclaw = await createOpenClawIntegration();
  const moltbook = await createMoltbookIntegration();
  
  // List all integrations
  await listIntegrations();
  
  // Test an integration (if created)
  if (manychat) {
    await testIntegration(manychat.id);
  }
  
  console.log('\n=================================================');
  console.log('   Examples completed!');
  console.log('=================================================');
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  createManyChatIntegration,
  createBotBuildersIntegration,
  createOpenClawIntegration,
  createMoltbookIntegration,
  listIntegrations,
  testIntegration,
  sendPredictionToIntegration,
  exportPredictionExamples
};
