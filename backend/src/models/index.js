const User = require('./User');
const TimeSeries = require('./TimeSeries');
const AIModel = require('./AIModel');
const Prediction = require('./Prediction');
const AITool = require('./AITool');

// Define associations
User.hasMany(TimeSeries, { foreignKey: 'userId', as: 'timeSeries' });
TimeSeries.belongsTo(User, { foreignKey: 'userId', as: 'user' });

User.hasMany(AIModel, { foreignKey: 'userId', as: 'models' });
AIModel.belongsTo(User, { foreignKey: 'userId', as: 'user' });

TimeSeries.hasMany(AIModel, { foreignKey: 'timeSeriesId', as: 'models' });
AIModel.belongsTo(TimeSeries, { foreignKey: 'timeSeriesId', as: 'timeSeries' });

User.hasMany(Prediction, { foreignKey: 'userId', as: 'predictions' });
Prediction.belongsTo(User, { foreignKey: 'userId', as: 'user' });

AIModel.hasMany(Prediction, { foreignKey: 'modelId', as: 'predictions' });
Prediction.belongsTo(AIModel, { foreignKey: 'modelId', as: 'model' });

User.hasMany(AITool, { foreignKey: 'userId', as: 'aiTools' });
AITool.belongsTo(User, { foreignKey: 'userId', as: 'user' });

module.exports = {
  User,
  TimeSeries,
  AIModel,
  Prediction,
  AITool
};
