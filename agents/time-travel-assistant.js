const { ChatGPT } = require('../src/index');

/**
 * Time Travel Assistant Agent
 * Specialized AI agent for guiding users through time travel experiences
 */
class TimeTravelAssistant {
  constructor(apiKey = null) {
    this.chatgpt = new ChatGPT(apiKey);
    this.conversationHistory = [];
    
    // System prompt that defines the agent's personality and expertise
    this.systemPrompt = {
      role: 'system',
      content: `You are a Time Travel Assistant AI with expertise in history, physics, and temporal mechanics. 
      Your role is to:
      1. Help users plan safe and educational time travel journeys
      2. Provide historical context for different time periods
      3. Explain theoretical aspects of time travel
      4. Warn about potential dangers and paradoxes
      5. Suggest interesting historical events to witness
      
      Always be helpful, informative, and emphasize safety and historical accuracy.`
    };
  }

  /**
   * Start a new conversation
   */
  resetConversation() {
    this.conversationHistory = [this.systemPrompt];
  }

  /**
   * Send a message and maintain conversation context
   * @param {string} userMessage - The user's message
   * @returns {Promise<string>} - The assistant's response
   */
  async chat(userMessage) {
    // Add user message to history
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    });

    // Get response from ChatGPT
    const response = await this.chatgpt.conversation(this.conversationHistory);

    // Add assistant's response to history
    this.conversationHistory.push({
      role: 'assistant',
      content: response
    });

    return response;
  }

  /**
   * Get recommended time period based on user interests
   * @param {string} interest - User's area of interest
   * @returns {Promise<string>} - Recommendation
   */
  async recommendTimePeriod(interest) {
    const query = `Based on an interest in ${interest}, recommend an ideal time period to visit and explain why it would be fascinating.`;
    return await this.chat(query);
  }

  /**
   * Get safety briefing for a specific time period
   * @param {string} timePeriod - The time period to visit
   * @returns {Promise<string>} - Safety information
   */
  async getSafetyBriefing(timePeriod) {
    const query = `Provide a comprehensive safety briefing for visiting ${timePeriod}. Include health concerns, cultural considerations, and potential risks.`;
    return await this.chat(query);
  }

  /**
   * Get historical context for an event
   * @param {string} event - Historical event name
   * @returns {Promise<string>} - Historical context
   */
  async getHistoricalContext(event) {
    const query = `Provide detailed historical context for ${event}, including when it occurred, who was involved, and why it was significant.`;
    return await this.chat(query);
  }

  /**
   * Get the full conversation history
   * @returns {Array} - Array of message objects
   */
  getHistory() {
    return this.conversationHistory;
  }
}

module.exports = TimeTravelAssistant;
