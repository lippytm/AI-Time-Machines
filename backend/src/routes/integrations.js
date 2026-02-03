const express = require('express');
const router = express.Router();
const { body } = require('express-validator');
const { auth } = require('../middleware/auth');
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

// Get available platforms
router.get('/platforms', auth, getPlatforms);

// Get all integrations
router.get('/', auth, getAllIntegrations);

// Get single integration
router.get('/:id', auth, getIntegration);

// Create integration
router.post(
  '/',
  auth,
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
router.put('/:id', auth, updateIntegration);

// Delete integration
router.delete('/:id', auth, deleteIntegration);

// Test integration
router.post('/:id/test', auth, testIntegration);

// Send prediction to integration
router.post('/:id/send', auth, sendPrediction);

// Receive webhook (no auth for external webhooks)
router.post('/webhooks/:platform', receiveWebhook);

module.exports = router;
