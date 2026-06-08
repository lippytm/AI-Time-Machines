const { AIModel, TimeSeries } = require('../models');
const { validationResult } = require('express-validator');
const axios = require('axios');

const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';

// Get all models for user
const getAllModels = async (req, res) => {
  try {
    const models = await AIModel.findAll({
      where: { userId: req.userId },
      include: [{ model: TimeSeries, as: 'timeSeries', attributes: ['id', 'name'] }],
      order: [['createdAt', 'DESC']]
    });

    res.json({ models, count: models.length });
  } catch (error) {
    console.error('Get models error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch models' } });
  }
};

// Get single model
const getModel = async (req, res) => {
  try {
    const { id } = req.params;

    const model = await AIModel.findOne({
      where: { id, userId: req.userId },
      include: [{ model: TimeSeries, as: 'timeSeries' }]
    });

    if (!model) {
      return res.status(404).json({ error: { message: 'Model not found' } });
    }

    res.json({ model });
  } catch (error) {
    console.error('Get model error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch model' } });
  }
};

// Create and train model
const createModel = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { name, description, timeSeriesId, modelType, hyperparameters } = req.body;

    // Verify time series exists and belongs to user
    const timeSeries = await TimeSeries.findOne({
      where: { id: timeSeriesId, userId: req.userId }
    });

    if (!timeSeries) {
      return res.status(404).json({ error: { message: 'Time series not found' } });
    }

    // Create model record
    const model = await AIModel.create({
      name,
      description,
      userId: req.userId,
      timeSeriesId,
      modelType,
      hyperparameters: hyperparameters || {},
      status: 'pending'
    });

    // Trigger training in Python service (async)
    try {
      // Don't await - let training happen in background
      axios.post(`${PYTHON_SERVICE_URL}/api/train`, {
        modelId: model.id,
        timeSeriesData: timeSeries.data,
        modelType,
        hyperparameters: hyperparameters || {}
      }).catch(err => {
        console.error('Training request failed:', err.message);
        // Update model status to failed
        model.update({ status: 'failed' });
      });

      // Update status to training
      await model.update({ status: 'training' });
    } catch (error) {
      console.error('Failed to start training:', error);
    }

    res.status(201).json({
      message: 'Model created and training initiated',
      model
    });
  } catch (error) {
    console.error('Create model error:', error);
    res.status(500).json({ error: { message: 'Failed to create model' } });
  }
};

// Update model status (called by Python service)
const updateModelStatus = async (req, res) => {
  try {
    const { id } = req.params;
    const { status, metrics, modelPath, trainingDuration } = req.body;

    const model = await AIModel.findByPk(id);

    if (!model) {
      return res.status(404).json({ error: { message: 'Model not found' } });
    }

    const updates = { status };
    if (metrics) updates.metrics = metrics;
    if (modelPath) updates.modelPath = modelPath;
    if (trainingDuration) updates.trainingDuration = trainingDuration;

    await model.update(updates);

    res.json({
      message: 'Model status updated successfully',
      model
    });
  } catch (error) {
    console.error('Update model status error:', error);
    res.status(500).json({ error: { message: 'Failed to update model status' } });
  }
};

// Delete model
const deleteModel = async (req, res) => {
  try {
    const { id } = req.params;

    const model = await AIModel.findOne({
      where: { id, userId: req.userId }
    });

    if (!model) {
      return res.status(404).json({ error: { message: 'Model not found' } });
    }

    await model.destroy();

    res.json({ message: 'Model deleted successfully' });
  } catch (error) {
    console.error('Delete model error:', error);
    res.status(500).json({ error: { message: 'Failed to delete model' } });
  }
};

// Stream real-time model training status via Server-Sent Events
const streamModelStatus = async (req, res) => {
  const { id } = req.params;

  const model = await AIModel.findOne({ where: { id, userId: req.userId } });
  if (!model) {
    return res.status(404).json({ error: { message: 'Model not found' } });
  }

  // Set SSE headers
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no'
  });
  res.flushHeaders();

  const sendEvent = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  // Send initial state
  sendEvent({ status: model.status, modelId: model.id, timestamp: new Date().toISOString() });

  // Poll for status changes every 5 seconds
  const interval = setInterval(async () => {
    try {
      const updated = await AIModel.findByPk(id);
      if (!updated) {
        clearInterval(interval);
        res.end();
        return;
      }
      sendEvent({ status: updated.status, modelId: updated.id, metrics: updated.metrics, timestamp: new Date().toISOString() });

      // Stop streaming once training completes or fails
      if (updated.status === 'completed' || updated.status === 'failed') {
        clearInterval(interval);
        res.end();
      }
    } catch (err) {
      console.error('SSE polling error:', err.message);
      clearInterval(interval);
      res.end();
    }
  }, 5000);

  // Clean up on client disconnect
  req.on('close', () => {
    clearInterval(interval);
  });
};

module.exports = {
  getAllModels,
  getModel,
  createModel,
  updateModelStatus,
  deleteModel,
  streamModelStatus
};
