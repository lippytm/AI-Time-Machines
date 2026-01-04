const { DataTypes } = require('sequelize');
const sequelize = require('../config/sequelize');

const AIModel = sequelize.define('AIModel', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  description: {
    type: DataTypes.TEXT
  },
  userId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'Users',
      key: 'id'
    }
  },
  timeSeriesId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'TimeSeries',
      key: 'id'
    }
  },
  modelType: {
    type: DataTypes.ENUM('lstm', 'gru', 'arima', 'prophet', 'transformer'),
    allowNull: false,
    defaultValue: 'lstm'
  },
  status: {
    type: DataTypes.ENUM('pending', 'training', 'completed', 'failed'),
    defaultValue: 'pending'
  },
  hyperparameters: {
    type: DataTypes.JSONB,
    comment: 'Model hyperparameters and configuration'
  },
  metrics: {
    type: DataTypes.JSONB,
    comment: 'Training metrics (loss, accuracy, etc.)'
  },
  modelPath: {
    type: DataTypes.STRING,
    comment: 'Path to saved model file'
  },
  trainingDuration: {
    type: DataTypes.INTEGER,
    comment: 'Training duration in seconds'
  }
}, {
  timestamps: true,
  indexes: [
    { fields: ['userId'] },
    { fields: ['timeSeriesId'] },
    { fields: ['status'] }
  ]
});

module.exports = AIModel;
