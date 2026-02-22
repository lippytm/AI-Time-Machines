const https = require('https');
const http = require('http');
require('dotenv').config();

/**
 * OpenClaw Client Class
 * Provides an interface to interact with the OpenClaw Analytics & Automation Platform
 */
class OpenClaw {
  constructor(apiKey = null) {
    // Use provided API key or fall back to environment variable
    const key = apiKey || process.env.OPENCLAW_API_KEY;

    if (!key) {
      throw new Error(
        'OpenClaw API key is required. Please set OPENCLAW_API_KEY in your .env file or pass it to the constructor.'
      );
    }

    this.apiKey = key;
    this.baseUrl = 'https://openclaw.io/api';
    this.version = '1.0';
    this.source = 'ai-time-machines';
  }

  /**
   * Send an event to OpenClaw
   * @param {string} eventName - The name of the event (e.g., 'prediction.created')
   * @param {Object} data - The event data payload
   * @returns {Promise<Object>} - The response from OpenClaw
   */
  async sendEvent(eventName, data) {
    const payload = {
      event: eventName,
      timestamp: new Date().toISOString(),
      data,
      metadata: {
        source: this.source,
        version: this.version,
      },
    };

    return this._request('POST', '/events', payload);
  }

  /**
   * Send a prediction to OpenClaw analytics pipeline
   * @param {Object} prediction - The prediction object with id, modelId, predictions, confidence, horizon
   * @returns {Promise<Object>} - The response from OpenClaw
   */
  async sendPrediction(prediction) {
    const data = {
      prediction_id: prediction.id,
      model_id: prediction.modelId,
      metrics: {
        horizon: prediction.horizon,
        prediction_count: prediction.predictions ? prediction.predictions.length : 0,
        has_confidence: !!prediction.confidence,
      },
      values: prediction.predictions,
      confidence_intervals: prediction.confidence,
    };

    return this.sendEvent('prediction.created', data);
  }

  /**
   * Trigger an automation workflow in OpenClaw
   * @param {string} workflowId - The ID of the workflow to trigger
   * @param {Object} params - Optional parameters to pass to the workflow
   * @returns {Promise<Object>} - The response from OpenClaw
   */
  async triggerWorkflow(workflowId, params = {}) {
    const payload = {
      workflow_id: workflowId,
      params,
      triggered_at: new Date().toISOString(),
      source: this.source,
    };

    return this._request('POST', '/workflows/trigger', payload);
  }

  /**
   * Export analytics data from OpenClaw
   * @param {Object} options - Export options (startDate, endDate, format, metrics)
   * @returns {Promise<Object>} - The exported analytics data
   */
  async exportAnalytics(options = {}) {
    const queryParams = new URLSearchParams();
    if (options.startDate) queryParams.append('start_date', options.startDate);
    if (options.endDate) queryParams.append('end_date', options.endDate);
    if (options.format) queryParams.append('format', options.format);
    if (options.metrics) queryParams.append('metrics', options.metrics.join(','));

    const path = `/analytics/export${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    return this._request('GET', path);
  }

  /**
   * Make an HTTP request to the OpenClaw API
   * @param {string} method - HTTP method (GET, POST, etc.)
   * @param {string} path - API path
   * @param {Object} body - Request body (for POST requests)
   * @returns {Promise<Object>} - Parsed response
   */
  _request(method, path, body = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + path);
      const isHttps = url.protocol === 'https:';
      const transport = isHttps ? https : http;

      const options = {
        hostname: url.hostname,
        port: url.port || (isHttps ? 443 : 80),
        path: url.pathname + url.search,
        method,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'X-Source': this.source,
          'X-Version': this.version,
        },
      };

      const bodyStr = body ? JSON.stringify(body) : null;
      if (bodyStr) {
        options.headers['Content-Length'] = Buffer.byteLength(bodyStr);
      }

      const req = transport.request(options, (res) => {
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
              reject(new Error(`OpenClaw API Error: ${res.statusCode} - ${parsed.message || data}`));
            }
          } catch {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ raw: data });
            } else {
              reject(new Error(`OpenClaw API Error: ${res.statusCode} - ${data}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`OpenClaw Request Error: ${error.message}`));
      });

      if (bodyStr) {
        req.write(bodyStr);
      }

      req.end();
    });
  }
}

module.exports = OpenClaw;
