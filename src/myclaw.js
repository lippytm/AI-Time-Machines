const https = require('https');
const http = require('http');
require('dotenv').config();

/**
 * MyClaw Client Class
 * Provides an interface to interact with the MyClaw Personal Automation & Notification Platform
 */
class MyClaw {
  constructor(apiKey = null) {
    // Use provided API key or fall back to environment variable
    const key = apiKey || process.env.MYCLAW_API_KEY;

    if (!key) {
      throw new Error(
        'MyClaw API key is required. Please set MYCLAW_API_KEY in your .env file or pass it to the constructor.'
      );
    }

    this.apiKey = key;
    this.baseUrl = 'https://myclaw.io/api';
    this.version = '1.0';
    this.source = 'ai-time-machines';
  }

  /**
   * Send a notification via MyClaw
   * @param {string} channel - The notification channel (e.g., 'email', 'sms', 'push')
   * @param {Object} message - The message payload with title and body
   * @returns {Promise<Object>} - The response from MyClaw
   */
  async sendNotification(channel, message) {
    const payload = {
      channel,
      message,
      timestamp: new Date().toISOString(),
      source: this.source,
      version: this.version,
    };

    return this._request('POST', '/notifications', payload);
  }

  /**
   * Send a prediction alert via MyClaw
   * @param {Object} prediction - The prediction object with id, modelId, predictions, confidence, horizon
   * @param {string} channel - The notification channel to use (default: 'email')
   * @returns {Promise<Object>} - The response from MyClaw
   */
  async sendPredictionAlert(prediction, channel = 'email') {
    const message = {
      title: `New Prediction Available: ${prediction.id || 'N/A'}`,
      body: `Model ${prediction.modelId || 'N/A'} has generated ${prediction.predictions ? prediction.predictions.length : 0} forecast values over a ${prediction.horizon}-step horizon.`,
      data: {
        prediction_id: prediction.id,
        model_id: prediction.modelId,
        horizon: prediction.horizon,
        prediction_count: prediction.predictions ? prediction.predictions.length : 0,
        has_confidence: !!prediction.confidence,
        values: prediction.predictions,
      },
    };

    return this.sendNotification(channel, message);
  }

  /**
   * Create or update a dashboard widget in MyClaw
   * @param {string} widgetId - The ID of the widget to update (or null to create new)
   * @param {Object} data - The widget data (title, type, metrics)
   * @returns {Promise<Object>} - The response from MyClaw with widget details
   */
  async upsertWidget(widgetId, data) {
    const payload = {
      widget_id: widgetId,
      ...data,
      updated_at: new Date().toISOString(),
      source: this.source,
    };

    const method = widgetId ? 'PUT' : 'POST';
    const path = widgetId ? `/widgets/${widgetId}` : '/widgets';
    return this._request(method, path, payload);
  }

  /**
   * Sync prediction data to a MyClaw dashboard
   * @param {Object} prediction - The prediction object
   * @param {string} dashboardId - The MyClaw dashboard ID to sync to
   * @returns {Promise<Object>} - The response from MyClaw
   */
  async syncPredictionToDashboard(prediction, dashboardId) {
    const payload = {
      dashboard_id: dashboardId,
      prediction_id: prediction.id,
      model_id: prediction.modelId,
      metrics: {
        horizon: prediction.horizon,
        prediction_count: prediction.predictions ? prediction.predictions.length : 0,
        has_confidence: !!prediction.confidence,
      },
      values: prediction.predictions,
      confidence_intervals: prediction.confidence,
      synced_at: new Date().toISOString(),
      source: this.source,
    };

    return this._request('POST', '/dashboards/sync', payload);
  }

  /**
   * Make an HTTP request to the MyClaw API
   * @param {string} method - HTTP method (GET, POST, PUT, etc.)
   * @param {string} path - API path
   * @param {Object} body - Request body (for POST/PUT requests)
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
              reject(new Error(`MyClaw API Error: ${res.statusCode} - ${parsed.message || data}`));
            }
          } catch {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ raw: data });
            } else {
              reject(new Error(`MyClaw API Error: ${res.statusCode} - ${data}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`MyClaw Request Error: ${error.message}`));
      });

      if (bodyStr) {
        req.write(bodyStr);
      }

      req.end();
    });
  }
}

module.exports = MyClaw;
