const OpenAI = require('openai');
require('dotenv').config();

/**
 * ChatGPT Wrapper Class
 * Provides an interface to interact with OpenAI's ChatGPT API
 */
class ChatGPT {
  constructor(apiKey = null) {
    // Use provided API key or fall back to environment variable
    const key = apiKey || process.env.OPENAI_API_KEY;
    
    if (!key) {
      throw new Error(
        'OpenAI API key is required. Please set OPENAI_API_KEY in your .env file or pass it to the constructor.'
      );
    }

    this.client = new OpenAI({
      apiKey: key,
    });

    // Default model – GPT-4o provides the best balance of speed and capability
    this.model = 'gpt-4o';
  }

  /**
   * Send a message to ChatGPT and get a response
   * @param {string} message - The message to send
   * @param {Object} options - Additional options (temperature, max_tokens, etc.)
   * @returns {Promise<string>} - The response from ChatGPT
   */
  async chat(message, options = {}) {
    try {
      const response = await this.client.chat.completions.create({
        model: options.model || this.model,
        messages: [
          {
            role: 'user',
            content: message,
          },
        ],
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 1000,
        ...options,
      });

      return response.choices[0].message.content;
    } catch (error) {
      throw new Error(`ChatGPT API Error: ${error.message}`);
    }
  }

  /**
   * Have a conversation with context
   * @param {Array} messages - Array of message objects with role and content
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The response from ChatGPT
   */
  async conversation(messages, options = {}) {
    try {
      const response = await this.client.chat.completions.create({
        model: options.model || this.model,
        messages: messages,
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 1000,
        ...options,
      });

      return response.choices[0].message.content;
    } catch (error) {
      throw new Error(`ChatGPT API Error: ${error.message}`);
    }
  }

  /**
   * Stream a response chunk-by-chunk (useful for long autonomous responses)
   * @param {string} message - The message to send
   * @param {Function} onChunk - Callback invoked with each text chunk
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The full assembled response
   */
  async streamChat(message, onChunk, options = {}) {
    try {
      const stream = await this.client.chat.completions.create({
        model: options.model || this.model,
        messages: [{ role: 'user', content: message }],
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 2000,
        stream: true,
        ...options,
      });

      let fullResponse = '';
      for await (const chunk of stream) {
        const delta = chunk.choices[0]?.delta?.content || '';
        if (delta) {
          fullResponse += delta;
          if (typeof onChunk === 'function') onChunk(delta);
        }
      }
      return fullResponse;
    } catch (error) {
      throw new Error(`ChatGPT Stream Error: ${error.message}`);
    }
  }

  /**
   * Autonomously analyse a time series dataset and return structured insights
   * @param {Array<{timestamp: string, value: number}>} data - Time series data points
   * @param {Object} options - Additional options (model, maxTokens)
   * @returns {Promise<Object>} - Parsed JSON with trends, anomalies, and recommendations
   */
  async analyzeTimeSeries(data, options = {}) {
    const summary = {
      count: data.length,
      first: data[0],
      last: data[data.length - 1],
      sample: data.slice(0, 5),
    };

    const prompt = [
      'You are an autonomous time-series analysis agent.',
      'Analyse the following time series dataset and respond ONLY with a valid JSON object.',
      '',
      'Dataset summary:',
      JSON.stringify(summary, null, 2),
      '',
      'Return JSON with these keys:',
      '  trend        - "increasing", "decreasing", or "stable"',
      '  seasonality  - detected seasonality description or null',
      '  anomalies    - array of anomaly descriptions (empty if none)',
      '  insights     - array of key observations (up to 5)',
      '  recommendations - array of actionable suggestions (up to 3)',
    ].join('\n');

    try {
      const raw = await this.chat(prompt, {
        model: options.model || this.model,
        temperature: 0.2,
        max_tokens: options.maxTokens || 800,
      });

      // Strip markdown code fences if present
      const cleaned = raw.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '').trim();
      return JSON.parse(cleaned);
    } catch (error) {
      throw new Error(`Time series analysis failed: ${error.message}`);
    }
  }

  /**
   * Set the default model to use
   * @param {string} model - The model name (e.g., 'gpt-4o', 'gpt-4-turbo')
   */
  setModel(model) {
    this.model = model;
  }

  /**
   * Get available models (for reference)
   * @returns {Array<string>} - List of commonly available models
   */
  getAvailableModels() {
    return [
      'gpt-4o',
      'gpt-4o-mini',
      'gpt-4-turbo',
      'gpt-4',
      'gpt-3.5-turbo',
    ];
  }
}

module.exports = ChatGPT;
