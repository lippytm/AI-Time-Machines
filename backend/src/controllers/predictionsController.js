const { Prediction, AIModel } = require('../models');
const { validationResult } = require('express-validator');
const axios = require('axios');

const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';

// Get all predictions for user
const getAllPredictions = async (req, res) => {
  try {
    const predictions = await Prediction.findAll({
      where: { userId: req.userId },
      include: [{ model: AIModel, as: 'model', attributes: ['id', 'name', 'modelType'] }],
      order: [['createdAt', 'DESC']]
    });

    res.json({ predictions, count: predictions.length });
  } catch (error) {
    console.error('Get predictions error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch predictions' } });
  }
};

// Get single prediction
const getPrediction = async (req, res) => {
  try {
    const { id } = req.params;

    const prediction = await Prediction.findOne({
      where: { id, userId: req.userId },
      include: [{ model: AIModel, as: 'model' }]
    });

    if (!prediction) {
      return res.status(404).json({ error: { message: 'Prediction not found' } });
    }

    res.json({ prediction });
  } catch (error) {
    console.error('Get prediction error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch prediction' } });
  }
};

// Create prediction
const createPrediction = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { modelId, inputData, horizon } = req.body;

    // Verify model exists and belongs to user
    const model = await AIModel.findOne({
      where: { id: modelId, userId: req.userId }
    });

    if (!model) {
      return res.status(404).json({ error: { message: 'Model not found' } });
    }

    if (model.status !== 'completed') {
      return res.status(400).json({
        error: { message: 'Model is not ready for predictions. Current status: ' + model.status }
      });
    }

    // Call Python service to generate prediction
    try {
      const response = await axios.post(`${PYTHON_SERVICE_URL}/api/predict`, {
        modelId: model.id,
        modelPath: model.modelPath,
        modelType: model.modelType,
        inputData,
        horizon: horizon || 10
      });

      // Create prediction record
      const prediction = await Prediction.create({
        userId: req.userId,
        modelId,
        inputData,
        predictions: response.data.predictions,
        confidence: response.data.confidence,
        horizon: horizon || 10
      });

      res.status(201).json({
        message: 'Prediction generated successfully',
        prediction
      });
    } catch (error) {
      console.error('Python service error:', error.message);
      res.status(500).json({
        error: { message: 'Failed to generate prediction from model' }
      });
    }
  } catch (error) {
    console.error('Create prediction error:', error);
    res.status(500).json({ error: { message: 'Failed to create prediction' } });
  }
};

// Delete prediction
const deletePrediction = async (req, res) => {
  try {
    const { id } = req.params;

    const prediction = await Prediction.findOne({
      where: { id, userId: req.userId }
    });

    if (!prediction) {
      return res.status(404).json({ error: { message: 'Prediction not found' } });
    }

    await prediction.destroy();

    res.json({ message: 'Prediction deleted successfully' });
  } catch (error) {
    console.error('Delete prediction error:', error);
    res.status(500).json({ error: { message: 'Failed to delete prediction' } });
  }
};

module.exports = {
  getAllPredictions,
  getPrediction,
  createPrediction,
  deletePrediction
};
