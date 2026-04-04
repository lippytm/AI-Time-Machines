const https = require('https');
require('dotenv').config();

/**
 * Grok (xAI) Client Class
 * Provides an interface to interact with xAI's Grok API
 */
class Grok {
  constructor(apiKey = null) {
    const key = apiKey || process.env.GROK_API_KEY;

    if (!key) {
      throw new Error(
        'Grok API key is required. Please set GROK_API_KEY in your .env file or pass it to the constructor.'
      );
    }

    this.apiKey = key;
    this.baseUrl = 'https://api.x.ai/v1';
    this.model = 'grok-beta';
  }

  /**
   * Send a message to Grok and get a response
   * @param {string} message - The message to send
   * @param {Object} options - Additional options (temperature, max_tokens, stream, etc.)
   * @returns {Promise<string>} - The response from Grok
   */
  async chat(message, options = {}) {
    const payload = {
      model: options.model || this.model,
      messages: [
        {
          role: 'user',
          content: message,
        },
      ],
      temperature: options.temperature !== undefined ? options.temperature : 0.7,
      max_tokens: options.max_tokens || 1000,
      stream: false,
    };

    const response = await this._request('POST', '/chat/completions', payload);
    return response.choices[0].message.content;
  }

  /**
   * Have a conversation with context
   * @param {Array} messages - Array of message objects with role and content
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The response from Grok
   */
  async conversation(messages, options = {}) {
    const payload = {
      model: options.model || this.model,
      messages,
      temperature: options.temperature !== undefined ? options.temperature : 0.7,
      max_tokens: options.max_tokens || 1000,
      stream: false,
    };

    const response = await this._request('POST', '/chat/completions', payload);
    return response.choices[0].message.content;
  }

  /**
   * Analyze time-series prediction data using Grok
   * @param {Object} prediction - Prediction object with id, predictions, horizon, confidence
   * @param {string} context - Optional additional context for the analysis
   * @returns {Promise<string>} - Grok's analysis of the prediction
   */
  async analyzePrediction(prediction, context = '') {
    const message = [
      'Analyze the following time-series prediction data and provide insights:',
      `- Prediction ID: ${prediction.id || 'N/A'}`,
      `- Forecast horizon: ${prediction.horizon} steps`,
      `- Predicted values: ${JSON.stringify(prediction.predictions)}`,
      prediction.confidence
        ? `- Confidence intervals: lower=${JSON.stringify(prediction.confidence.lower)}, upper=${JSON.stringify(prediction.confidence.upper)}`
        : '- No confidence intervals provided',
      context ? `\nAdditional context: ${context}` : '',
    ]
      .filter(Boolean)
      .join('\n');

    return this.chat(message);
  }

  /**
   * Set the default model to use
   * @param {string} model - The Grok model name
   */
  setModel(model) {
    this.model = model;
  }

  /**
   * Get available Grok models (for reference)
   * @returns {Array<string>} - List of available models
   */
  getAvailableModels() {
    return ['grok-beta', 'grok-vision-beta'];
  }

  /**
   * Make an HTTPS request to the xAI API
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
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
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
              reject(new Error(`Grok API Error: ${res.statusCode} - ${parsed.error?.message || data}`));
            }
          } catch {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ raw: data });
            } else {
              reject(new Error(`Grok API Error: ${res.statusCode} - ${data}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Grok Request Error: ${error.message}`));
      });

      if (bodyStr) {
        req.write(bodyStr);
      }

      req.end();
    });
  }
}

module.exports = Grok;
