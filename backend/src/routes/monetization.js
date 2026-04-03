const express = require('express');
const router = express.Router();
const { auth } = require('../middleware/auth');
const { apiLimiter } = require('../middleware/rateLimiter');
const {
  getPlans,
  getOpportunities,
  getRevenueSummary
} = require('../controllers/monetizationController');

// All routes require authentication and rate limiting
router.use(auth);

// Get subscription plans
router.get('/plans', apiLimiter, getPlans);

// Get revenue opportunities per platform
router.get('/opportunities', apiLimiter, getOpportunities);

// Get revenue summary for the current user
router.get('/summary', apiLimiter, getRevenueSummary);

module.exports = router;
