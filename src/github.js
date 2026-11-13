const https = require('https');
require('dotenv').config();

/**
 * GitHub Client Class
 * Provides an interface to sync predictions and data with GitHub repositories
 * using the GitHub REST API and a Personal Access Token (PAT)
 */
class GitHub {
  constructor(token = null) {
    const accessToken = token || process.env.GITHUB_TOKEN;

    if (!accessToken) {
      throw new Error(
        'GitHub token is required. Please set GITHUB_TOKEN in your .env file or pass it to the constructor.'
      );
    }

    this.token = accessToken;
    this.baseUrl = 'https://api.github.com';
    this.source = 'ai-time-machines';
  }

  /**
   * Get repository information
   * @param {string} owner - Repository owner (username or organization)
   * @param {string} repo - Repository name
   * @returns {Promise<Object>} - Repository details from GitHub API
   */
  async getRepository(owner, repo) {
    return this._request('GET', `/repos/${owner}/${repo}`);
  }

  /**
   * Sync a prediction to a GitHub repository by creating or updating a file
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {Object} prediction - Prediction object with id, predictions, confidence, horizon, modelId
   * @param {string} path - File path in the repository (default: 'predictions/{id}.json')
   * @param {string} message - Commit message (default: 'Sync prediction from AI-Time-Machines')
   * @returns {Promise<Object>} - Commit details from GitHub API
   */
  async syncPrediction(owner, repo, prediction, path = null, message = null) {
    const filePath = path || `predictions/${prediction.id || 'prediction'}.json`;
    const commitMessage = message || `Sync prediction ${prediction.id || ''} from AI-Time-Machines`;

    const content = {
      id: prediction.id,
      modelId: prediction.modelId,
      horizon: prediction.horizon,
      predictions: prediction.predictions,
      confidence: prediction.confidence,
      createdAt: prediction.createdAt,
      syncedAt: new Date().toISOString(),
      source: this.source,
    };

    const encodedContent = Buffer.from(JSON.stringify(content, null, 2)).toString('base64');

    // Check if file already exists to get its SHA (required for updates)
    let sha = null;
    try {
      const existing = await this._request('GET', `/repos/${owner}/${repo}/contents/${filePath}`);
      sha = existing.sha;
    } catch {
      // File does not exist yet — will be created
    }

    const payload = {
      message: commitMessage,
      content: encodedContent,
      ...(sha && { sha }),
    };

    return this._request('PUT', `/repos/${owner}/${repo}/contents/${filePath}`, payload);
  }

  /**
   * Create a GitHub issue with prediction data
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {Object} prediction - Prediction object
   * @param {string} title - Issue title (default: auto-generated)
   * @returns {Promise<Object>} - Created issue details
   */
  async createPredictionIssue(owner, repo, prediction, title = null) {
    const issueTitle = title || `Prediction Report: ${prediction.id || new Date().toISOString()}`;
    const body = [
      '## AI Time Machines — Prediction Report',
      '',
      `**Prediction ID:** ${prediction.id || 'N/A'}`,
      `**Model ID:** ${prediction.modelId || 'N/A'}`,
      `**Horizon:** ${prediction.horizon || 0} steps`,
      `**Generated At:** ${prediction.createdAt || new Date().toISOString()}`,
      '',
      '### Predicted Values',
      '```json',
      JSON.stringify(prediction.predictions || [], null, 2),
      '```',
      prediction.confidence
        ? [
            '',
            '### Confidence Intervals',
            '```json',
            JSON.stringify(prediction.confidence, null, 2),
            '```',
          ].join('\n')
        : '',
      '',
      `*Synced from [AI-Time-Machines](https://github.com/lippytm/AI-Time-Machines)*`,
    ]
      .filter(line => line !== null)
      .join('\n');

    const payload = {
      title: issueTitle,
      body,
      labels: ['prediction', 'ai-time-machines'],
    };

    return this._request('POST', `/repos/${owner}/${repo}/issues`, payload);
  }

  /**
   * List prediction files synced to a GitHub repository
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {string} folder - Folder path to list (default: 'predictions')
   * @returns {Promise<Array>} - List of files in the folder
   */
  async listSyncedPredictions(owner, repo, folder = 'predictions') {
    try {
      const contents = await this._request('GET', `/repos/${owner}/${repo}/contents/${folder}`);
      return Array.isArray(contents) ? contents : [];
    } catch {
      return [];
    }
  }

  /**
   * Make an HTTPS request to the GitHub API
   * @param {string} method - HTTP method (GET, POST, PUT, etc.)
   * @param {string} path - API path
   * @param {Object} body - Request body (for POST/PUT requests)
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
          Authorization: `Bearer ${this.token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/vnd.github+json',
          'X-GitHub-Api-Version': '2022-11-28',
          'User-Agent': this.source,
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
