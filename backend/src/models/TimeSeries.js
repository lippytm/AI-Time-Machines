const { DataTypes } = require('sequelize');
const sequelize = require('../config/sequelize');

const TimeSeries = sequelize.define('TimeSeries', {
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
  data: {
    type: DataTypes.JSONB,
    allowNull: false,
    comment: 'Time series data in JSON format: [{timestamp, value}, ...]'
  },
  metadata: {
    type: DataTypes.JSONB,
    comment: 'Additional metadata (frequency, units, etc.)'
  },
  dataPoints: {
    type: DataTypes.INTEGER,
    comment: 'Number of data points in the series'
  },
  startDate: {
    type: DataTypes.DATE
  },
  endDate: {
    type: DataTypes.DATE
  }
}, {
  timestamps: true,
  indexes: [
    { fields: ['userId'] },
    { fields: ['name'] }
  ]
});

module.exports = TimeSeries;
