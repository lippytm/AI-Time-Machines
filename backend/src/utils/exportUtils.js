// Export utility for converting predictions to various formats
// Supports CSV, JSON, XML for cross-platform compatibility

/**
 * Export prediction data to CSV format
 */
function exportToCSV(prediction) {
  try {
    let csv = 'timestamp,value,confidence_lower,confidence_upper\n';
    
    if (prediction.predictions && Array.isArray(prediction.predictions)) {
      prediction.predictions.forEach((value, index) => {
        const confLower = prediction.confidence?.lower?.[index] || '';
        const confUpper = prediction.confidence?.upper?.[index] || '';
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
    const data = {
      id: prediction.id,
      modelId: prediction.modelId,
      horizon: prediction.horizon,
      predictions: prediction.predictions,
      confidence: prediction.confidence,
      metadata: {
        createdAt: prediction.createdAt,
        userId: prediction.userId
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
  return {
    messaging_type: 'UPDATE',
    notification_type: 'REGULAR',
    message: {
      text: 'New prediction available',
      quick_replies: [
        {
          content_type: 'text',
          title: 'View Details',
          payload: `PREDICTION_${prediction.id}`
        }
      ]
    },
    custom_user_field: {
      prediction_id: prediction.id,
      predictions: prediction.predictions,
      horizon: prediction.horizon
    }
  };
}

/**
 * Export for BotBuilders format
 */
function exportForBotBuilders(prediction) {
  return {
    type: 'prediction_update',
    data: {
      predictionId: prediction.id,
      values: prediction.predictions,
      confidence: prediction.confidence,
      horizon: prediction.horizon,
      timestamp: prediction.createdAt
    },
    actions: [
      {
        type: 'send_message',
        message: `New prediction generated with ${prediction.horizon} steps ahead`
      },
      {
        type: 'set_variable',
        key: 'last_prediction_id',
        value: prediction.id
      }
    ]
  };
}

/**
 * Export for OpenClaw format (analytics platform)
 */
function exportForOpenClaw(prediction) {
  return {
    event: 'prediction.created',
    timestamp: new Date().toISOString(),
    data: {
      prediction_id: prediction.id,
      model_id: prediction.modelId,
      metrics: {
        horizon: prediction.horizon,
        prediction_count: prediction.predictions?.length || 0,
        has_confidence: !!prediction.confidence
      },
      values: prediction.predictions,
      confidence_intervals: prediction.confidence
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
  const pythonVisualizationCode = [
    'import matplotlib.pyplot as plt',
    'import numpy as np',
    '',
    `predictions = np.array(${JSON.stringify(prediction.predictions)})`,
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
        content: `# Prediction ${prediction.id}\n\nGenerated on ${new Date(prediction.createdAt).toLocaleString()}`
      },
      {
        type: 'code',
        language: 'python',
        content: `# Prediction data\nprediction_id = "${prediction.id}"\nhorizon = ${prediction.horizon}\npredictions = ${JSON.stringify(prediction.predictions, null, 2)}`
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
      prediction_id: prediction.id,
      created_at: prediction.createdAt,
      format: 'moltbook-v1'
    }
  };
}

/**
 * Export for ChatGPT (OpenAI) format
 */
function exportForChatGPT(prediction) {
  return {
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: 'You are an AI time-series analysis assistant. Provide insights on the following prediction data.'
      },
      {
        role: 'user',
        content: `Analyze this time-series prediction:\n- Prediction ID: ${prediction.id}\n- Horizon: ${prediction.horizon} steps\n- Predicted values: ${JSON.stringify(prediction.predictions)}\n- Confidence intervals: ${JSON.stringify(prediction.confidence)}`
      }
    ],
    prediction_data: {
      id: prediction.id,
      modelId: prediction.modelId,
      horizon: prediction.horizon,
      predictions: prediction.predictions,
      confidence: prediction.confidence,
      createdAt: prediction.createdAt
    },
    metadata: {
      source: 'ai-time-machines',
      format: 'chatgpt-v1'
    }
  };
}

/**
 * Export for Grok (xAI) format
 */
function exportForGrok(prediction) {
  return {
    query: `Provide a detailed analysis of the following time-series forecast with ${prediction.horizon} steps ahead.`,
    context: {
      prediction_id: prediction.id,
      model_id: prediction.modelId,
      horizon: prediction.horizon,
      predicted_values: prediction.predictions,
      confidence_intervals: prediction.confidence,
      generated_at: prediction.createdAt
    },
    stream: false,
    metadata: {
      source: 'ai-time-machines',
      format: 'grok-v1'
    }
  };
}

/**
 * Export for Replit format (deployable Python script)
 */
function exportForReplit(prediction) {
  const scriptContent = [
    '# AI Time Machines - Prediction Export for Replit',
    '# Run this script to visualize and analyze your prediction',
    '',
    'import json',
    'import os',
    '',
    '# Prediction data',
    `prediction_id = "${prediction.id}"`,
    `model_id = "${prediction.modelId}"`,
    `horizon = ${prediction.horizon}`,
    `predictions = ${JSON.stringify(prediction.predictions)}`,
    `confidence = ${JSON.stringify(prediction.confidence || {})}`,
    '',
    'try:',
    '    import matplotlib.pyplot as plt',
    '    import numpy as np',
    '    steps = list(range(len(predictions)))',
    "    plt.figure(figsize=(12, 6))",
    "    plt.plot(steps, predictions, 'b-o', label='Predictions', linewidth=2)",
    "    if confidence.get('lower') and confidence.get('upper'):",
    "        plt.fill_between(steps, confidence['lower'], confidence['upper'],",
    "                         alpha=0.2, color='blue', label='Confidence Interval')",
    "    plt.title(f'Time Series Forecast (Horizon: {horizon} steps)')",
    "    plt.xlabel('Time Step')",
    "    plt.ylabel('Predicted Value')",
    "    plt.legend()",
    "    plt.grid(True)",
    "    plt.tight_layout()",
    "    plt.savefig('prediction_plot.png')",
    "    print('Plot saved to prediction_plot.png')",
    "except ImportError:",
    "    print('matplotlib not available. Install it with: pip install matplotlib numpy')",
    '',
    "print(f'Prediction {prediction_id}: {len(predictions)} values forecasted')",
    "print(f'Values: {predictions}')"
  ].join('\n');

  return {
    files: {
      'main.py': scriptContent,
      'prediction.json': JSON.stringify({
        id: prediction.id,
        modelId: prediction.modelId,
        horizon: prediction.horizon,
        predictions: prediction.predictions,
        confidence: prediction.confidence,
        createdAt: prediction.createdAt
      }, null, 2),
      'requirements.txt': 'matplotlib\nnumpy\n'
    },
    repl_config: {
      language: 'python3',
      entrypoint: 'main.py'
    },
    metadata: {
      source: 'ai-time-machines',
      format: 'replit-v1'
    }
  };
}


/**
 * Escape XML special characters to prevent XML injection
 * @param {*} str - The value to escape (non-strings are returned as-is)
 * @returns {string|*} - Escaped string safe for inclusion in XML
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
 * Main export function that routes to appropriate format
 */
function exportPrediction(prediction, format) {
  switch (format.toLowerCase()) {
    case 'csv':
      return exportToCSV(prediction);
    case 'json':
      return exportToJSON(prediction);
    case 'xml':
      return exportToXML(prediction);
    case 'manychat':
      return exportForManyChat(prediction);
    case 'botbuilders':
      return exportForBotBuilders(prediction);
    case 'openclaw':
      return exportForOpenClaw(prediction);
    case 'moltbook':
      return exportForMoltbook(prediction);
    case 'chatgpt':
      return exportForChatGPT(prediction);
    case 'grok':
      return exportForGrok(prediction);
    case 'replit':
      return exportForReplit(prediction);
    default:
      return exportToJSON(prediction);
  }
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
  exportForChatGPT,
  exportForGrok,
  exportForReplit
};
