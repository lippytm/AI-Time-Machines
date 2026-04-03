const https = require('https');
require('dotenv').config();

/**
 * Replit Client Class
 * Provides an interface to deploy and manage AI apps on Replit
 */
class Replit {
  constructor(apiToken = null) {
    const token = apiToken || process.env.REPLIT_API_TOKEN;

    if (!token) {
      throw new Error(
        'Replit API token is required. Please set REPLIT_API_TOKEN in your .env file or pass it to the constructor.'
      );
    }

    this.apiToken = token;
    this.baseUrl = 'https://replit.com/api/v0';
    this.source = 'ai-time-machines';
  }

  /**
   * Generate a deployable Replit package from a prediction
   * @param {Object} prediction - Prediction object with id, predictions, confidence, horizon, modelId
   * @returns {Object} - Replit-compatible package with files and configuration
   */
  generatePredictionPackage(prediction) {
    const scriptContent = [
      '# AI Time Machines - Prediction Package for Replit',
      '# Visualize and analyze your time-series forecast',
      '',
      'import json',
      '',
      `prediction_id = "${prediction.id || ''}"`,
      `model_id = "${prediction.modelId || ''}"`,
      `horizon = ${prediction.horizon || 0}`,
      `predictions = ${JSON.stringify(prediction.predictions || [])}`,
      `confidence = ${JSON.stringify(prediction.confidence || {})}`,
      '',
      'try:',
      '    import matplotlib.pyplot as plt',
      '    import numpy as np',
      '    steps = list(range(len(predictions)))',
      '    plt.figure(figsize=(12, 6))',
      "    plt.plot(steps, predictions, 'b-o', label='Predictions', linewidth=2)",
      "    if confidence.get('lower') and confidence.get('upper'):",
      "        plt.fill_between(steps, confidence['lower'], confidence['upper'],",
      "                         alpha=0.2, color='blue', label='Confidence Interval')",
      "    plt.title(f'Time Series Forecast (Horizon: {horizon} steps)')",
      "    plt.xlabel('Time Step')",
      "    plt.ylabel('Predicted Value')",
      '    plt.legend()',
      '    plt.grid(True)',
      '    plt.tight_layout()',
      "    plt.savefig('prediction_plot.png')",
      "    print('Plot saved to prediction_plot.png')",
      'except ImportError:',
      "    print('matplotlib not available. Install it with: pip install matplotlib numpy')",
      '',
      "print(f'Prediction {prediction_id}: {len(predictions)} values forecasted')",
      "print(f'Values: {predictions}')",
    ].join('\n');

    return {
      files: {
        'main.py': scriptContent,
        'prediction.json': JSON.stringify(
          {
            id: prediction.id,
            modelId: prediction.modelId,
            horizon: prediction.horizon,
            predictions: prediction.predictions,
            confidence: prediction.confidence,
            createdAt: prediction.createdAt,
          },
          null,
          2
        ),
        'requirements.txt': 'matplotlib\nnumpy\n',
        '.replit': 'run = "python main.py"\nlanguage = "python3"\n',
      },
      repl_config: {
        language: 'python3',
        entrypoint: 'main.py',
        title: `AI Prediction - ${prediction.id || 'export'}`,
      },
      metadata: {
        source: this.source,
        format: 'replit-v1',
        generatedAt: new Date().toISOString(),
      },
    };
  }

  /**
   * Create a new Repl via the Replit API
   * @param {string} title - Title of the Repl
   * @param {string} language - Programming language (e.g. 'python3')
   * @param {Object} files - Map of filename → content
   * @returns {Promise<Object>} - Created Repl details from the API
   */
  async createRepl(title, language, files = {}) {
    const payload = {
      title,
      language,
      files,
      source: this.source,
    };

    return this._request('POST', '/repls', payload);
  }

  /**
   * Deploy a prediction as a Repl
   * @param {Object} prediction - Prediction object
   * @returns {Promise<Object>} - Deploy result with Repl URL
   */
  async deployPrediction(prediction) {
    const pkg = this.generatePredictionPackage(prediction);
    return this.createRepl(pkg.repl_config.title, pkg.repl_config.language, pkg.files);
  }

  /**
   * Make an HTTPS request to the Replit API
   * @param {string} method - HTTP method
   * @param {string} path - API path
   * @param {Object} body - Request body
   * @returns {Promise<Object>} - Parsed response
   */
  _request(method, path, body = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + path);
      const bodyStr = body ? JSON.stringify(body) : null;

      const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname + url.search,
        method,
        headers: {
          Authorization: `Bearer ${this.apiToken}`,
          'Content-Type': 'application/json',
          'X-Source': this.source,
        },
      };

      if (bodyStr) {
        options.headers['Content-Length'] = Buffer.byteLength(bodyStr);
      }

      const req = https.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(parsed);
            } else {
              reject(new Error(`Replit API Error: ${res.statusCode} - ${parsed.message || data}`));
            }
          } catch {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ raw: data });
            } else {
              reject(new Error(`Replit API Error: ${res.statusCode} - ${data}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Replit Request Error: ${error.message}`));
      });

      if (bodyStr) {
        req.write(bodyStr);
      }

      req.end();
    });
  }
}

module.exports = Replit;
