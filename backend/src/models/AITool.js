const { DataTypes } = require('sequelize');
const sequelize = require('../config/sequelize');

const AITool = sequelize.define('AITool', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      len: [1, 255]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  category: {
    type: DataTypes.ENUM(
      'nlp',
      'computer-vision',
      'speech',
      'ml-framework',
      'data-processing',
      'deployment',
      'monitoring',
      'other'
    ),
    allowNull: false,
    defaultValue: 'other'
  },
  toolType: {
    type: DataTypes.ENUM('library', 'framework', 'platform', 'service', 'toolkit'),
    allowNull: false,
    defaultValue: 'library'
  },
  url: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isUrl: true
    }
  },
  version: {
    type: DataTypes.STRING,
    allowNull: true
  },
  documentation: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isUrl: true
    }
  },
  github: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isUrl: true
    }
  },
  programmingLanguages: {
    type: DataTypes.ARRAY(DataTypes.STRING),
    allowNull: true,
    defaultValue: []
  },
  tags: {
    type: DataTypes.ARRAY(DataTypes.STRING),
    allowNull: true,
    defaultValue: []
  },
  metadata: {
    type: DataTypes.JSONB,
    allowNull: true,
    defaultValue: {}
  },
  userId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'Users',
      key: 'id'
    },
    onDelete: 'CASCADE'
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  }
}, {
  timestamps: true,
  indexes: [
    {
      fields: ['userId']
    },
    {
      fields: ['category']
    },
    {
      fields: ['toolType']
    },
    {
      fields: ['isActive']
    }
  ]
});

module.exports = AITool;
