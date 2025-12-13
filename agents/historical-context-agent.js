const { ChatGPT } = require('../src/index');

/**
 * Historical Context Agent
 * Specialized AI agent for providing detailed historical information
 */
class HistoricalContextAgent {
  constructor(apiKey = null) {
    this.chatgpt = new ChatGPT(apiKey);
    
    this.systemPrompt = {
      role: 'system',
      content: `You are a Historical Context AI expert with deep knowledge of world history across all time periods.
      Your role is to:
      1. Provide accurate historical information about events, people, and periods
      2. Explain the social, political, and cultural context of historical moments
      3. Connect historical events to their causes and consequences
      4. Offer multiple perspectives on historical events
      5. Cite historical sources and acknowledge uncertainties
      
      Always maintain historical accuracy and provide nuanced, balanced perspectives.`
    };
  }

  /**
   * Analyze a specific historical period
   * @param {string} period - Time period to analyze
   * @param {string} region - Geographic region (optional)
   * @returns {Promise<string>} - Detailed analysis
   */
  async analyzePeriod(period, region = 'global') {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Provide a comprehensive analysis of ${period}${region !== 'global' ? ` in ${region}` : ''}. Include political, social, economic, and cultural aspects.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Compare two different time periods
   * @param {string} period1 - First time period
   * @param {string} period2 - Second time period
   * @returns {Promise<string>} - Comparison
   */
  async comparePeriods(period1, period2) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Compare and contrast ${period1} with ${period2}. Highlight key differences and similarities in technology, society, politics, and culture.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Get information about a historical figure
   * @param {string} person - Name of the historical figure
   * @returns {Promise<string>} - Biographical information
   */
  async getPersonInfo(person) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Provide detailed information about ${person}, including their life, achievements, historical context, and lasting impact.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Explain the causes and consequences of an event
   * @param {string} event - Historical event
   * @returns {Promise<string>} - Causal analysis
   */
  async analyzeEventCausality(event) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Analyze ${event} by explaining: 1) The causes that led to it, 2) How it unfolded, 3) Its immediate and long-term consequences.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Get daily life description for a time period
   * @param {string} period - Time period
   * @param {string} socialClass - Social class (optional)
   * @returns {Promise<string>} - Daily life description
   */
  async getDailyLife(period, socialClass = 'common people') {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Describe daily life for ${socialClass} during ${period}. Include details about housing, food, work, leisure, family life, and social customs.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Timeline of events for a specific topic
   * @param {string} topic - Historical topic or theme
   * @param {string} timeframe - Time range (optional)
   * @returns {Promise<string>} - Timeline
   */
  async getTimeline(topic, timeframe = null) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Create a chronological timeline of key events related to ${topic}${timeframe ? ` during ${timeframe}` : ''}. Include dates and brief descriptions.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }
}

module.exports = HistoricalContextAgent;
