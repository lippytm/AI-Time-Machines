const express = require('express');
const { body } = require('express-validator');
const {
  getAllTimeSeries,
  getTimeSeries,
  createTimeSeries,
  updateTimeSeries,
  deleteTimeSeries
} = require('../controllers/timeSeriesController');
const { auth } = require('../middleware/auth');

const router = express.Router();

// All routes require authentication
router.use(auth);

// Get all time series
router.get('/', getAllTimeSeries);

// Get single time series
router.get('/:id', getTimeSeries);

// Create time series
router.post('/',
  [
    body('name').trim().notEmpty().withMessage('Name is required'),
    body('data').isArray({ min: 1 }).withMessage('Data must be a non-empty array'),
    body('data.*.timestamp').notEmpty().withMessage('Each data point must have a timestamp'),
    body('data.*.value').isNumeric().withMessage('Each data point must have a numeric value')
  ],
  createTimeSeries
);

// Update time series
router.put('/:id', updateTimeSeries);

// Delete time series
router.delete('/:id', deleteTimeSeries);

module.exports = router;
