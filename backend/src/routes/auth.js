const express = require('express');
const { body } = require('express-validator');
const { register, login, getCurrentUser, updateProfile } = require('../controllers/authController');
const { auth } = require('../middleware/auth');
const { authLimiter } = require('../middleware/rateLimiter');

const router = express.Router();

// Register
router.post('/register',
  authLimiter,
  [
    body('username').trim().isLength({ min: 3, max: 50 }).withMessage('Username must be 3-50 characters'),
    body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters')
  ],
  register
);

// Login
router.post('/login',
  authLimiter,
  [
    body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
    body('password').notEmpty().withMessage('Password is required')
  ],
  login
);

// Get current user (protected)
router.get('/me', auth, getCurrentUser);

// Update profile (protected)
router.put('/profile', auth, updateProfile);

module.exports = router;
