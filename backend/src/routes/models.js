const express = require('express');
const { body } = require('express-validator');
const {
  getAllModels,
  getModel,
  createModel,
  updateModelStatus,
  deleteModel,
  streamModelStatus
} = require('../controllers/modelsController');
const { auth } = require('../middleware/auth');
const { apiLimiter, createLimiter } = require('../middleware/rateLimiter');

const router = express.Router();

// All routes require authentication
router.use(auth);

// Apply general API rate limiting
router.use(apiLimiter);

// Get all models
router.get('/', getAllModels);

// Stream real-time training status updates via Server-Sent Events
router.get('/:id/stream', streamModelStatus);

// Get single model
router.get('/:id', getModel);

// Create model
router.post('/',
  createLimiter,
  [
    body('name').trim().notEmpty().withMessage('Name is required'),
    body('timeSeriesId').isUUID().withMessage('Valid time series ID is required'),
    body('modelType').isIn(['lstm', 'gru', 'arima', 'prophet', 'transformer']).withMessage('Invalid model type')
  ],
  createModel
);

// Update model status (webhook from Python service)
router.put('/:id/status', updateModelStatus);

// Delete model
router.delete('/:id', deleteModel);

module.exports = router;
