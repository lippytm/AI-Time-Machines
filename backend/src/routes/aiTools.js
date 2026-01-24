const express = require('express');
const { body } = require('express-validator');
const {
  getAllAITools,
  getAITool,
  createAITool,
  updateAITool,
  deleteAITool,
  getCategories,
  getToolTypes
} = require('../controllers/aiToolsController');
const { auth } = require('../middleware/auth');
const { apiLimiter, createLimiter } = require('../middleware/rateLimiter');

const router = express.Router();

// All routes require authentication
router.use(auth);

// Apply general API rate limiting
router.use(apiLimiter);

// Get categories
router.get('/categories', getCategories);

// Get tool types
router.get('/types', getToolTypes);

// Get all AI tools
router.get('/', getAllAITools);

// Get single AI tool
router.get('/:id', getAITool);

// Create AI tool
router.post('/',
  createLimiter,
  [
    body('name').trim().notEmpty().withMessage('Name is required'),
    body('category').isIn([
      'nlp',
      'computer-vision',
      'speech',
      'ml-framework',
      'data-processing',
      'deployment',
      'monitoring',
      'other'
    ]).withMessage('Invalid category'),
    body('toolType').isIn([
      'library',
      'framework',
      'platform',
      'service',
      'toolkit'
    ]).withMessage('Invalid tool type'),
    body('url').optional().isURL().withMessage('Invalid URL'),
    body('documentation').optional().isURL().withMessage('Invalid documentation URL'),
    body('github').optional().isURL().withMessage('Invalid GitHub URL')
  ],
  createAITool
);

// Update AI tool
router.put('/:id', updateAITool);

// Delete AI tool
router.delete('/:id', deleteAITool);

module.exports = router;
