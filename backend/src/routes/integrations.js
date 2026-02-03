const express = require('express');
const router = express.Router();
const { body } = require('express-validator');
const { auth } = require('../middleware/auth');
const { apiLimiter, createLimiter } = require('../middleware/rateLimiter');
const {
  getAllIntegrations,
  getIntegration,
  createIntegration,
  updateIntegration,
  deleteIntegration,
  testIntegration,
  sendPrediction,
  receiveWebhook,
  getPlatforms
} = require('../controllers/integrationsController');

// Receive webhook (no auth for external webhooks - must be before auth middleware)
router.post('/webhooks/:platform', receiveWebhook);

// All other routes require authentication and rate limiting
router.use(auth);
router.use(apiLimiter);

// Get available platforms
router.get('/platforms', getPlatforms);

// Get all integrations
router.get('/', getAllIntegrations);

// Get single integration
router.get('/:id', getIntegration);

// Create integration
router.post(
  '/',
  createLimiter,
  [
    body('name').notEmpty().trim().isLength({ min: 1, max: 255 }),
    body('platform').notEmpty().isIn(['manychat', 'botbuilders', 'openclaw', 'moltbook', 'webhook', 'other']),
    body('description').optional().trim(),
    body('apiKey').optional().trim(),
    body('apiSecret').optional().trim(),
    body('webhookUrl').optional().isURL(),
    body('config').optional().isObject()
  ],
  createIntegration
);

// Update integration
router.put('/:id', updateIntegration);

// Delete integration
router.delete('/:id', deleteIntegration);

// Test integration
router.post('/:id/test', testIntegration);

// Send prediction to integration
router.post('/:id/send', sendPrediction);

module.exports = router;
