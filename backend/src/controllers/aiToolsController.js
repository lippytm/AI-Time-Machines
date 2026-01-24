const { AITool } = require('../models');
const { validationResult } = require('express-validator');

// Get all AI tools for user
const getAllAITools = async (req, res) => {
  try {
    const { category, toolType, isActive } = req.query;
    
    const where = { userId: req.userId };
    
    if (category) where.category = category;
    if (toolType) where.toolType = toolType;
    if (isActive !== undefined) where.isActive = isActive === 'true';

    const aiTools = await AITool.findAll({
      where,
      order: [['createdAt', 'DESC']]
    });

    res.json({ aiTools, count: aiTools.length });
  } catch (error) {
    console.error('Get AI tools error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch AI tools' } });
  }
};

// Get single AI tool
const getAITool = async (req, res) => {
  try {
    const { id } = req.params;

    const aiTool = await AITool.findOne({
      where: { id, userId: req.userId }
    });

    if (!aiTool) {
      return res.status(404).json({ error: { message: 'AI tool not found' } });
    }

    res.json({ aiTool });
  } catch (error) {
    console.error('Get AI tool error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch AI tool' } });
  }
};

// Create AI tool
const createAITool = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const {
      name,
      description,
      category,
      toolType,
      url,
      version,
      documentation,
      github,
      programmingLanguages,
      tags,
      metadata
    } = req.body;

    const aiTool = await AITool.create({
      name,
      description,
      category,
      toolType,
      url,
      version,
      documentation,
      github,
      programmingLanguages,
      tags,
      metadata,
      userId: req.userId
    });

    res.status(201).json({
      message: 'AI tool created successfully',
      aiTool
    });
  } catch (error) {
    console.error('Create AI tool error:', error);
    res.status(500).json({ error: { message: 'Failed to create AI tool' } });
  }
};

// Update AI tool
const updateAITool = async (req, res) => {
  try {
    const { id } = req.params;
    const {
      name,
      description,
      category,
      toolType,
      url,
      version,
      documentation,
      github,
      programmingLanguages,
      tags,
      metadata,
      isActive
    } = req.body;

    const aiTool = await AITool.findOne({
      where: { id, userId: req.userId }
    });

    if (!aiTool) {
      return res.status(404).json({ error: { message: 'AI tool not found' } });
    }

    const updates = {};
    if (name) updates.name = name;
    if (description !== undefined) updates.description = description;
    if (category) updates.category = category;
    if (toolType) updates.toolType = toolType;
    if (url !== undefined) updates.url = url;
    if (version !== undefined) updates.version = version;
    if (documentation !== undefined) updates.documentation = documentation;
    if (github !== undefined) updates.github = github;
    if (programmingLanguages !== undefined) updates.programmingLanguages = programmingLanguages;
    if (tags !== undefined) updates.tags = tags;
    if (metadata !== undefined) updates.metadata = metadata;
    if (isActive !== undefined) updates.isActive = isActive;

    await aiTool.update(updates);

    res.json({
      message: 'AI tool updated successfully',
      aiTool
    });
  } catch (error) {
    console.error('Update AI tool error:', error);
    res.status(500).json({ error: { message: 'Failed to update AI tool' } });
  }
};

// Delete AI tool
const deleteAITool = async (req, res) => {
  try {
    const { id } = req.params;

    const aiTool = await AITool.findOne({
      where: { id, userId: req.userId }
    });

    if (!aiTool) {
      return res.status(404).json({ error: { message: 'AI tool not found' } });
    }

    await aiTool.destroy();

    res.json({ message: 'AI tool deleted successfully' });
  } catch (error) {
    console.error('Delete AI tool error:', error);
    res.status(500).json({ error: { message: 'Failed to delete AI tool' } });
  }
};

// Get categories
const getCategories = async (req, res) => {
  try {
    const categories = [
      { value: 'nlp', label: 'Natural Language Processing' },
      { value: 'computer-vision', label: 'Computer Vision' },
      { value: 'speech', label: 'Speech Recognition/Synthesis' },
      { value: 'ml-framework', label: 'ML Framework' },
      { value: 'data-processing', label: 'Data Processing' },
      { value: 'deployment', label: 'Model Deployment' },
      { value: 'monitoring', label: 'Model Monitoring' },
      { value: 'other', label: 'Other' }
    ];

    res.json({ categories });
  } catch (error) {
    console.error('Get categories error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch categories' } });
  }
};

// Get tool types
const getToolTypes = async (req, res) => {
  try {
    const toolTypes = [
      { value: 'library', label: 'Library' },
      { value: 'framework', label: 'Framework' },
      { value: 'platform', label: 'Platform' },
      { value: 'service', label: 'Service' },
      { value: 'toolkit', label: 'Toolkit' }
    ];

    res.json({ toolTypes });
  } catch (error) {
    console.error('Get tool types error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch tool types' } });
  }
};

module.exports = {
  getAllAITools,
  getAITool,
  createAITool,
  updateAITool,
  deleteAITool,
  getCategories,
  getToolTypes
};
