const { TimeSeries } = require('../models');
const { validationResult } = require('express-validator');

// Get all time series for user
const getAllTimeSeries = async (req, res) => {
  try {
    const timeSeries = await TimeSeries.findAll({
      where: { userId: req.userId },
      order: [['createdAt', 'DESC']]
    });

    res.json({ timeSeries, count: timeSeries.length });
  } catch (error) {
    console.error('Get time series error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch time series' } });
  }
};

// Get single time series
const getTimeSeries = async (req, res) => {
  try {
    const { id } = req.params;

    const timeSeries = await TimeSeries.findOne({
      where: { id, userId: req.userId }
    });

    if (!timeSeries) {
      return res.status(404).json({ error: { message: 'Time series not found' } });
    }

    res.json({ timeSeries });
  } catch (error) {
    console.error('Get time series error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch time series' } });
  }
};

// Create time series
const createTimeSeries = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { name, description, data, metadata } = req.body;

    // Calculate data points and date range
    const dataPoints = data.length;
    const timestamps = data.map(d => new Date(d.timestamp));
    const startDate = new Date(Math.min(...timestamps));
    const endDate = new Date(Math.max(...timestamps));

    const timeSeries = await TimeSeries.create({
      name,
      description,
      userId: req.userId,
      data,
      metadata,
      dataPoints,
      startDate,
      endDate
    });

    res.status(201).json({
      message: 'Time series created successfully',
      timeSeries
    });
  } catch (error) {
    console.error('Create time series error:', error);
    res.status(500).json({ error: { message: 'Failed to create time series' } });
  }
};

// Update time series
const updateTimeSeries = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, data, metadata } = req.body;

    const timeSeries = await TimeSeries.findOne({
      where: { id, userId: req.userId }
    });

    if (!timeSeries) {
      return res.status(404).json({ error: { message: 'Time series not found' } });
    }

    const updates = {};
    if (name) updates.name = name;
    if (description !== undefined) updates.description = description;
    if (metadata) updates.metadata = metadata;

    if (data) {
      updates.data = data;
      updates.dataPoints = data.length;
      const timestamps = data.map(d => new Date(d.timestamp));
      updates.startDate = new Date(Math.min(...timestamps));
      updates.endDate = new Date(Math.max(...timestamps));
    }

    await timeSeries.update(updates);

    res.json({
      message: 'Time series updated successfully',
      timeSeries
    });
  } catch (error) {
    console.error('Update time series error:', error);
    res.status(500).json({ error: { message: 'Failed to update time series' } });
  }
};

// Delete time series
const deleteTimeSeries = async (req, res) => {
  try {
    const { id } = req.params;

    const timeSeries = await TimeSeries.findOne({
      where: { id, userId: req.userId }
    });

    if (!timeSeries) {
      return res.status(404).json({ error: { message: 'Time series not found' } });
    }

    await timeSeries.destroy();

    res.json({ message: 'Time series deleted successfully' });
  } catch (error) {
    console.error('Delete time series error:', error);
    res.status(500).json({ error: { message: 'Failed to delete time series' } });
  }
};

module.exports = {
  getAllTimeSeries,
  getTimeSeries,
  createTimeSeries,
  updateTimeSeries,
  deleteTimeSeries
};
