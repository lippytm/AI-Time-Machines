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

    // Default model for ChatGPT (using GPT-4 for Pro account features)
    this.model = 'gpt-4';
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
   * Set the default model to use
   * @param {string} model - The model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
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
      'gpt-4',
      'gpt-4-turbo-preview',
      'gpt-3.5-turbo',
      'gpt-3.5-turbo-16k',
    ];
  }
}

module.exports = ChatGPT;
