const express = require('express');
const { body } = require('express-validator');
const {
  getAllPredictions,
  getPrediction,
  createPrediction,
  deletePrediction,
  exportPredictionData
} = require('../controllers/predictionsController');
const { auth } = require('../middleware/auth');
const { apiLimiter, createLimiter } = require('../middleware/rateLimiter');

const router = express.Router();

// All routes require authentication
router.use(auth);

// Apply general API rate limiting
router.use(apiLimiter);

// Get all predictions
router.get('/', getAllPredictions);

// Get single prediction
router.get('/:id', getPrediction);

// Export prediction in various formats
router.get('/:id/export', exportPredictionData);

// Create prediction
router.post('/',
  createLimiter,
  [
    body('modelId').isUUID().withMessage('Valid model ID is required'),
    body('horizon').optional().isInt({ min: 1, max: 100 }).withMessage('Horizon must be between 1 and 100')
  ],
  createPrediction
);

// Delete prediction
router.delete('/:id', deletePrediction);

module.exports = router;
