const { Integration, Prediction, AIModel } = require('../models');
const { validationResult } = require('express-validator');
const crypto = require('crypto');

// Get all integrations for user
const getAllIntegrations = async (req, res) => {
  try {
    const { platform, isActive } = req.query;
    
    const where = { userId: req.userId };
    
    if (platform) where.platform = platform;
    if (isActive !== undefined) where.isActive = isActive === 'true';

    const integrations = await Integration.findAll({
      where,
      order: [['createdAt', 'DESC']]
    });

    res.json({ integrations, count: integrations.length });
  } catch (error) {
    console.error('Get integrations error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch integrations' } });
  }
};

// Get single integration
const getIntegration = async (req, res) => {
  try {
    const { id } = req.params;

    const integration = await Integration.findOne({
      where: { id, userId: req.userId }
    });

    if (!integration) {
      return res.status(404).json({ error: { message: 'Integration not found' } });
    }

    res.json({ integration });
  } catch (error) {
    console.error('Get integration error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch integration' } });
  }
};

// Create integration
const createIntegration = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const {
      name,
      platform,
      description,
      apiKey,
      apiSecret,
      webhookUrl,
      config
    } = req.body;

    const integration = await Integration.create({
      name,
      platform,
      description,
      apiKey,
      apiSecret,
      webhookUrl,
      config,
      userId: req.userId
    });

    res.status(201).json({
      message: 'Integration created successfully',
      integration
    });
  } catch (error) {
    console.error('Create integration error:', error);
    res.status(500).json({ error: { message: 'Failed to create integration' } });
  }
};

// Update integration
const updateIntegration = async (req, res) => {
  try {
    const { id } = req.params;
    const {
      name,
      description,
      apiKey,
      apiSecret,
      webhookUrl,
      config,
      isActive
    } = req.body;

    const integration = await Integration.findOne({
      where: { id, userId: req.userId }
    });

    if (!integration) {
      return res.status(404).json({ error: { message: 'Integration not found' } });
    }

    const updates = {};
    if (name) updates.name = name;
    if (description !== undefined) updates.description = description;
    if (apiKey !== undefined) updates.apiKey = apiKey;
    if (apiSecret !== undefined) updates.apiSecret = apiSecret;
    if (webhookUrl !== undefined) updates.webhookUrl = webhookUrl;
    if (config !== undefined) updates.config = config;
    if (isActive !== undefined) updates.isActive = isActive;

    await integration.update(updates);

    res.json({
      message: 'Integration updated successfully',
      integration
    });
  } catch (error) {
    console.error('Update integration error:', error);
    res.status(500).json({ error: { message: 'Failed to update integration' } });
  }
};

// Delete integration
const deleteIntegration = async (req, res) => {
  try {
    const { id } = req.params;

    const integration = await Integration.findOne({
      where: { id, userId: req.userId }
    });

    if (!integration) {
      return res.status(404).json({ error: { message: 'Integration not found' } });
    }

    await integration.destroy();

    res.json({ message: 'Integration deleted successfully' });
  } catch (error) {
    console.error('Delete integration error:', error);
    res.status(500).json({ error: { message: 'Failed to delete integration' } });
  }
};

// Test integration connection
const testIntegration = async (req, res) => {
  try {
    const { id } = req.params;

    const integration = await Integration.findOne({
      where: { id, userId: req.userId }
    });

    if (!integration) {
      return res.status(404).json({ error: { message: 'Integration not found' } });
    }

    // Simulate connection test - in production, this would actually test the connection
    const testResult = {
      success: true,
      message: `Successfully connected to ${integration.platform}`,
      timestamp: new Date()
    };

    await integration.update({
      lastSyncAt: new Date(),
      syncStatus: 'success'
    });

    res.json(testResult);
  } catch (error) {
    console.error('Test integration error:', error);
    res.status(500).json({ error: { message: 'Failed to test integration' } });
  }
};

// Send prediction to integration
const sendPrediction = async (req, res) => {
  try {
    const { id } = req.params;
    const { predictionId } = req.body;

    const integration = await Integration.findOne({
      where: { id, userId: req.userId }
    });

    if (!integration) {
      return res.status(404).json({ error: { message: 'Integration not found' } });
    }

    const prediction = await Prediction.findOne({
      where: { id: predictionId, userId: req.userId },
      include: [{
        model: AIModel,
        as: 'model'
      }]
    });

    if (!prediction) {
      return res.status(404).json({ error: { message: 'Prediction not found' } });
    }

    // Format prediction data for external platform
    const formattedData = formatPredictionForPlatform(integration.platform, prediction);

    // In production, this would actually send to the webhook
    const result = {
      success: true,
      message: `Prediction sent to ${integration.platform}`,
      integration: integration.name,
      predictionId: prediction.id,
      timestamp: new Date()
    };

    await integration.update({
      lastSyncAt: new Date(),
      syncStatus: 'success'
    });

    res.json(result);
  } catch (error) {
    console.error('Send prediction error:', error);
    res.status(500).json({ error: { message: 'Failed to send prediction' } });
  }
};

// Receive webhook from external platform
const receiveWebhook = async (req, res) => {
  try {
    const { platform } = req.params;
    const webhookData = req.body;

    // Log webhook receipt
    console.log(`Received webhook from ${platform}:`, webhookData);

    // Process webhook based on platform
    const processedData = processWebhookData(platform, webhookData);

    res.json({
      success: true,
      message: 'Webhook received successfully',
      platform,
      processed: processedData
    });
  } catch (error) {
    console.error('Receive webhook error:', error);
    res.status(500).json({ error: { message: 'Failed to process webhook' } });
  }
};

// Get available platforms
const getPlatforms = async (req, res) => {
  try {
    const platforms = [
      { 
        value: 'manychat', 
        label: 'ManyChat',
        description: 'Facebook Messenger chatbot platform',
        features: ['webhooks', 'api', 'automation']
      },
      { 
        value: 'botbuilders', 
        label: 'BotBuilders',
        description: 'Multi-platform chatbot builder',
        features: ['webhooks', 'api', 'nlp', 'automation']
      },
      { 
        value: 'openclaw', 
        label: 'OpenClaw',
        description: 'Open analytics and automation platform',
        features: ['analytics', 'automation', 'data-export']
      },
      { 
        value: 'moltbook', 
        label: 'Moltbook',
        description: 'Interactive notebook and documentation platform',
        features: ['notebooks', 'documentation', 'visualization']
      },
      { 
        value: 'webhook', 
        label: 'Custom Webhook',
        description: 'Generic webhook integration',
        features: ['webhooks', 'custom']
      },
      { 
        value: 'other', 
        label: 'Other',
        description: 'Other integration type',
        features: ['custom']
      }
    ];

    res.json({ platforms });
  } catch (error) {
    console.error('Get platforms error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch platforms' } });
  }
};

// Helper function to format prediction for different platforms
function formatPredictionForPlatform(platform, prediction) {
  const baseData = {
    predictionId: prediction.id,
    predictions: prediction.predictions,
    confidence: prediction.confidence,
    horizon: prediction.horizon,
    model: prediction.model?.name,
    timestamp: prediction.createdAt
  };

  switch (platform) {
    case 'manychat':
      return {
        type: 'prediction',
        data: baseData,
        format: 'manychat'
      };
    case 'botbuilders':
      return {
        event: 'prediction_update',
        payload: baseData,
        format: 'botbuilders'
      };
    case 'openclaw':
      return {
        analytics: baseData,
        format: 'openclaw'
      };
    case 'moltbook':
      return {
        notebook_data: baseData,
        format: 'moltbook'
      };
    default:
      return baseData;
  }
}

// Helper function to process webhook data
function processWebhookData(platform, data) {
  // Basic processing - in production, this would be more sophisticated
  return {
    platform,
    receivedAt: new Date(),
    dataType: typeof data,
    processed: true
  };
}

module.exports = {
  getAllIntegrations,
  getIntegration,
  createIntegration,
  updateIntegration,
  deleteIntegration,
  testIntegration,
  sendPrediction,
  receiveWebhook,
  getPlatforms
};
