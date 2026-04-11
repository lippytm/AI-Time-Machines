const https = require('https');
require('dotenv').config();

/**
 * GitHub Client Class
 * Provides an interface to interact with the GitHub API
 */
class GitHub {
  constructor(token = null) {
    // Use provided token or fall back to environment variable
    const key = token || process.env.GITHUB_TOKEN;

    if (!key) {
      throw new Error(
        'GitHub token is required. Please set GITHUB_TOKEN in your .env file or pass it to the constructor.'
      );
    }

    this.token = key;
    this.baseUrl = 'https://api.github.com';
    this.createRepoUrl = 'https://github.com/new';
    this.source = 'ai-time-machines';
  }

  /**
   * Get the URL to create a new GitHub repository
   * @returns {string} - The URL to create a new repository on GitHub
   */
  getCreateRepositoryUrl() {
    return this.createRepoUrl;
  }

  /**
   * Get information about a GitHub repository
   * @param {string} owner - The repository owner (username or org)
   * @param {string} repo - The repository name
   * @returns {Promise<Object>} - Repository information
   */
  async getRepository(owner, repo) {
    return this._request('GET', `/repos/${owner}/${repo}`);
  }

  /**
   * Create a GitHub issue for a prediction
   * @param {string} owner - The repository owner
   * @param {string} repo - The repository name
   * @param {Object} prediction - The prediction object
   * @returns {Promise<Object>} - The created issue
   */
  async createPredictionIssue(owner, repo, prediction) {
    const body = [
      `**Prediction ID:** ${prediction.id}`,
      `**Model ID:** ${prediction.modelId || 'N/A'}`,
      `**Horizon:** ${prediction.horizon || 'N/A'}`,
      `**Created At:** ${prediction.createdAt || new Date().toISOString()}`,
      '',
      '## Prediction Results',
      prediction.predictions
        ? `\`\`\`json\n${JSON.stringify(prediction.predictions, null, 2)}\n\`\`\``
        : '_No prediction values available_',
    ].join('\n');

    const payload = {
      title: `Prediction: ${prediction.id}`,
      body,
      labels: ['prediction', 'ai-time-machines'],
    };

    return this._request('POST', `/repos/${owner}/${repo}/issues`, payload);
  }

  /**
   * Sync a prediction to GitHub by creating an issue
   * @param {string} owner - The repository owner
   * @param {string} repo - The repository name
   * @param {Object} prediction - The prediction object
   * @returns {Promise<Object>} - The synced issue
   */
  async syncPrediction(owner, repo, prediction) {
    return this.createPredictionIssue(owner, repo, prediction);
  }

  /**
   * List issues synced from predictions
   * @param {string} owner - The repository owner
   * @param {string} repo - The repository name
   * @returns {Promise<Array>} - List of prediction issues
   */
  async listSyncedPredictions(owner, repo) {
    return this._request('GET', `/repos/${owner}/${repo}/issues?labels=prediction,ai-time-machines`);
  }

  /**
   * Make an HTTPS request to the GitHub API
   * @param {string} method - HTTP method (GET, POST, etc.)
   * @param {string} path - API path
   * @param {Object} body - Request body (for POST requests)
   * @returns {Promise<Object>} - Parsed response
   */
  _request(method, path, body = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + path);

      const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname + url.search,
        method,
        headers: {
          'Authorization': `token ${this.token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/vnd.github+json',
          'User-Agent': this.source,
          'X-GitHub-Api-Version': '2022-11-28',
        },
      };

      const bodyStr = body ? JSON.stringify(body) : null;
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
              reject(new Error(`GitHub API Error: ${res.statusCode} - ${parsed.message || data}`));
            }
          } catch {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ raw: data });
            } else {
              reject(new Error(`GitHub API Error: ${res.statusCode} - ${data}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`GitHub Request Error: ${error.message}`));
      });

      if (bodyStr) {
        req.write(bodyStr);
      }

      req.end();
    });
  }
}

module.exports = GitHub;
