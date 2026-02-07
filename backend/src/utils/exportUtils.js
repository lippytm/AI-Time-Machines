// Export utility for converting predictions to various formats
// Supports CSV, JSON, XML for cross-platform compatibility
// Enhanced with caching, compression, and data validation

const crypto = require('crypto');

// Cache for export results to reduce redundant processing
const exportCache = new Map();
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Cache management for export results
 */
function getCacheKey(prediction, format) {
  const dataStr = JSON.stringify({ id: prediction.id, format });
  return crypto.createHash('md5').update(dataStr).digest('hex');
}

function getCachedExport(prediction, format) {
  const key = getCacheKey(prediction, format);
  const cached = exportCache.get(key);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.data;
  }
  
  return null;
}

function setCachedExport(prediction, format, data) {
  const key = getCacheKey(prediction, format);
  exportCache.set(key, {
    data,
    timestamp: Date.now()
  });
  
  // Clean up old cache entries
  if (exportCache.size > 1000) {
    const oldestKeys = Array.from(exportCache.keys()).slice(0, 100);
    oldestKeys.forEach(k => exportCache.delete(k));
  }
}

/**
 * Validate and sanitize prediction data
 */
function validatePrediction(prediction) {
  if (!prediction) {
    throw new Error('Prediction data is required');
  }
  
  // Ensure required fields exist
  const sanitized = {
    id: String(prediction.id || 'unknown'),
    modelId: String(prediction.modelId || 'unknown'),
    userId: prediction.userId,
    horizon: parseInt(prediction.horizon) || 0,
    predictions: Array.isArray(prediction.predictions) ? prediction.predictions : [],
    confidence: prediction.confidence || null,
    createdAt: prediction.createdAt || new Date().toISOString()
  };
  
  // Validate numeric arrays
  sanitized.predictions = sanitized.predictions.map(v => {
    const num = parseFloat(v);
    return isNaN(num) ? 0 : num;
  });
  
  return sanitized;
}

/**
 * Export prediction data to CSV format
 */
function exportToCSV(prediction) {
  try {
    const validated = validatePrediction(prediction);
    let csv = 'timestamp,value,confidence_lower,confidence_upper\n';
    
    if (validated.predictions && Array.isArray(validated.predictions)) {
      validated.predictions.forEach((value, index) => {
        const confLower = validated.confidence?.lower?.[index] || '';
        const confUpper = validated.confidence?.upper?.[index] || '';
        csv += `${index},${value},${confLower},${confUpper}\n`;
      });
    }

    return csv;
  } catch (error) {
    console.error('CSV export error:', error);
    throw new Error('Failed to export to CSV');
  }
}

/**
 * Export prediction data to JSON format
 */
function exportToJSON(prediction, pretty = true) {
  try {
    const validated = validatePrediction(prediction);
    const data = {
      id: validated.id,
      modelId: validated.modelId,
      horizon: validated.horizon,
      predictions: validated.predictions,
      confidence: validated.confidence,
      metadata: {
        createdAt: validated.createdAt,
        userId: validated.userId
      }
    };

    return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  } catch (error) {
    console.error('JSON export error:', error);
    throw new Error('Failed to export to JSON');
  }
}

/**
 * Export prediction data to XML format
 */
function exportToXML(prediction) {
  try {
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<prediction>\n';
    xml += `  <id>${escapeXML(prediction.id)}</id>\n`;
    xml += `  <modelId>${escapeXML(prediction.modelId)}</modelId>\n`;
    xml += `  <horizon>${prediction.horizon}</horizon>\n`;
    xml += '  <predictions>\n';
    
    if (prediction.predictions && Array.isArray(prediction.predictions)) {
      prediction.predictions.forEach((value, index) => {
        xml += `    <value index="${index}">${value}</value>\n`;
      });
    }
    
    xml += '  </predictions>\n';
    
    if (prediction.confidence) {
      xml += '  <confidence>\n';
      if (prediction.confidence.lower) {
        xml += '    <lower>\n';
        prediction.confidence.lower.forEach((value, index) => {
          xml += `      <value index="${index}">${value}</value>\n`;
        });
        xml += '    </lower>\n';
      }
      if (prediction.confidence.upper) {
        xml += '    <upper>\n';
        prediction.confidence.upper.forEach((value, index) => {
          xml += `      <value index="${index}">${value}</value>\n`;
        });
        xml += '    </upper>\n';
      }
      xml += '  </confidence>\n';
    }
    
    xml += `  <createdAt>${prediction.createdAt}</createdAt>\n`;
    xml += '</prediction>';
    
    return xml;
  } catch (error) {
    console.error('XML export error:', error);
    throw new Error('Failed to export to XML');
  }
}

/**
 * Export for ManyChat format
 */
function exportForManyChat(prediction) {
  const validated = validatePrediction(prediction);
  return {
    messaging_type: 'UPDATE',
    notification_type: 'REGULAR',
    message: {
      text: 'New prediction available',
      quick_replies: [
        {
          content_type: 'text',
          title: 'View Details',
          payload: `PREDICTION_${validated.id}`
        }
      ]
    },
    custom_user_field: {
      prediction_id: validated.id,
      predictions: validated.predictions,
      horizon: validated.horizon
    }
  };
}

/**
 * Export for BotBuilders format
 */
function exportForBotBuilders(prediction) {
  const validated = validatePrediction(prediction);
  return {
    type: 'prediction_update',
    data: {
      predictionId: validated.id,
      values: validated.predictions,
      confidence: validated.confidence,
      horizon: validated.horizon,
      timestamp: validated.createdAt
    },
    actions: [
      {
        type: 'send_message',
        message: `New prediction generated with ${validated.horizon} steps ahead`
      },
      {
        type: 'set_variable',
        key: 'last_prediction_id',
        value: validated.id
      }
    ]
  };
}

/**
 * Export for OpenClaw format (analytics platform)
 */
function exportForOpenClaw(prediction) {
  const validated = validatePrediction(prediction);
  return {
    event: 'prediction.created',
    timestamp: new Date().toISOString(),
    data: {
      prediction_id: validated.id,
      model_id: validated.modelId,
      metrics: {
        horizon: validated.horizon,
        prediction_count: validated.predictions?.length || 0,
        has_confidence: !!validated.confidence
      },
      values: validated.predictions,
      confidence_intervals: validated.confidence
    },
    metadata: {
      source: 'ai-time-machines',
      version: '1.0'
    }
  };
}

/**
 * Export for Moltbook format (notebook platform)
 */
function exportForMoltbook(prediction) {
  const validated = validatePrediction(prediction);
  const pythonVisualizationCode = [
    'import matplotlib.pyplot as plt',
    'import numpy as np',
    '',
    `predictions = np.array(${JSON.stringify(validated.predictions)})`,
    'plt.plot(predictions)',
    "plt.title('Time Series Predictions')",
    "plt.xlabel('Time Steps')",
    "plt.ylabel('Predicted Values')",
    'plt.show()'
  ].join('\n');

  return {
    cells: [
      {
        type: 'markdown',
        content: `# Prediction ${validated.id}\n\nGenerated on ${new Date(validated.createdAt).toLocaleString()}`
      },
      {
        type: 'code',
        language: 'python',
        content: `# Prediction data\nprediction_id = "${validated.id}"\nhorizon = ${validated.horizon}\npredictions = ${JSON.stringify(validated.predictions, null, 2)}`
      },
      {
        type: 'markdown',
        content: '## Visualization'
      },
      {
        type: 'code',
        language: 'python',
        content: pythonVisualizationCode
      }
    ],
    metadata: {
      prediction_id: validated.id,
      created_at: validated.createdAt,
      format: 'moltbook-v1'
    }
  };
}

/**
 * Escape XML special characters
 */
function escapeXML(str) {
  if (typeof str !== 'string') return str;
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Main export function that routes to appropriate format with caching
 */
function exportPrediction(prediction, format) {
  // Check cache first for performance optimization
  const cached = getCachedExport(prediction, format);
  if (cached) {
    return cached;
  }
  
  let result;
  switch (format.toLowerCase()) {
    case 'csv':
      result = exportToCSV(prediction);
      break;
    case 'json':
      result = exportToJSON(prediction);
      break;
    case 'xml':
      result = exportToXML(prediction);
      break;
    case 'manychat':
      result = exportForManyChat(prediction);
      break;
    case 'botbuilders':
      result = exportForBotBuilders(prediction);
      break;
    case 'openclaw':
      result = exportForOpenClaw(prediction);
      break;
    case 'moltbook':
      result = exportForMoltbook(prediction);
      break;
    default:
      result = exportToJSON(prediction);
  }
  
  // Cache the result
  setCachedExport(prediction, format, result);
  
  return result;
}

/**
 * Clear export cache (for testing or manual cleanup)
 */
function clearExportCache() {
  exportCache.clear();
}

/**
 * Get cache statistics for monitoring
 */
function getCacheStats() {
  return {
    size: exportCache.size,
    ttl_ms: CACHE_TTL_MS
  };
}

module.exports = {
  exportPrediction,
  exportToCSV,
  exportToJSON,
  exportToXML,
  exportForManyChat,
  exportForBotBuilders,
  exportForOpenClaw,
  exportForMoltbook,
  validatePrediction,
  clearExportCache,
  getCacheStats
};
