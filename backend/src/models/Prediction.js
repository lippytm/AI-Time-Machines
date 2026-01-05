const { DataTypes } = require('sequelize');
const sequelize = require('../config/sequelize');

const Prediction = sequelize.define('Prediction', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  userId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'Users',
      key: 'id'
    }
  },
  modelId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'AIModels',
      key: 'id'
    }
  },
  inputData: {
    type: DataTypes.JSONB,
    comment: 'Input data used for prediction'
  },
  predictions: {
    type: DataTypes.JSONB,
    allowNull: false,
    comment: 'Predicted values with timestamps'
  },
  confidence: {
    type: DataTypes.JSONB,
    comment: 'Confidence intervals or uncertainty measures'
  },
  horizon: {
    type: DataTypes.INTEGER,
    comment: 'Prediction horizon (number of steps ahead)'
  }
}, {
  timestamps: true,
  indexes: [
    { fields: ['userId'] },
    { fields: ['modelId'] }
  ]
});

module.exports = Prediction;
