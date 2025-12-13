const { ChatGPT } = require('../src/index');

/**
 * Temporal Paradox Resolver Agent
 * Specialized AI agent for analyzing and resolving temporal paradoxes and time travel logic
 */
class TemporalParadoxResolver {
  constructor(apiKey = null) {
    this.chatgpt = new ChatGPT(apiKey);
    
    this.systemPrompt = {
      role: 'system',
      content: `You are a Temporal Paradox Resolver AI with expertise in theoretical physics, logic, and time travel scenarios.
      Your role is to:
      1. Analyze potential temporal paradoxes in time travel scenarios
      2. Explain different theories of time travel (many-worlds, self-consistency, etc.)
      3. Suggest ways to avoid creating paradoxes
      4. Evaluate the logical consistency of time travel plans
      5. Explain complex concepts like causality, bootstrap paradoxes, and grandfather paradoxes
      
      Use clear explanations grounded in physics theories while remaining accessible.`
    };
  }

  /**
   * Analyze a scenario for potential paradoxes
   * @param {string} scenario - Description of the time travel scenario
   * @returns {Promise<string>} - Analysis of potential paradoxes
   */
  async analyzeScenario(scenario) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Analyze this time travel scenario for potential paradoxes: ${scenario}. Identify any logical inconsistencies and explain what could go wrong.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Explain a specific type of paradox
   * @param {string} paradoxType - Type of paradox (e.g., 'grandfather', 'bootstrap', 'predestination')
   * @returns {Promise<string>} - Detailed explanation
   */
  async explainParadox(paradoxType) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Explain the ${paradoxType} paradox in detail. Include examples, theoretical solutions, and implications for time travel.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Suggest solutions to avoid a paradox
   * @param {string} paradoxDescription - Description of the paradox
   * @returns {Promise<string>} - Suggested solutions
   */
  async suggestSolutions(paradoxDescription) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Given this paradox situation: ${paradoxDescription}. Suggest practical solutions and alternative approaches to avoid creating a temporal paradox.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Evaluate if an action in the past would create a paradox
   * @param {string} action - Proposed action
   * @param {string} timeperiod - When the action would occur
   * @returns {Promise<string>} - Evaluation result
   */
  async evaluateAction(action, timeperiod) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `If someone were to ${action} in ${timeperiod}, would this create a temporal paradox? Analyze the causal chain and potential timeline effects.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Compare different time travel theories
   * @param {Array<string>} theories - List of theories to compare
   * @returns {Promise<string>} - Comparison
   */
  async compareTheories(theories = ['many-worlds', 'self-consistency', 'dynamic timeline']) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Compare and contrast these time travel theories: ${theories.join(', ')}. Explain how each handles paradoxes and what implications each has for time travelers.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }

  /**
   * Check if a planned time travel is logically consistent
   * @param {string} plan - Detailed time travel plan
   * @returns {Promise<string>} - Consistency check result
   */
  async checkConsistency(plan) {
    const messages = [
      this.systemPrompt,
      {
        role: 'user',
        content: `Review this time travel plan for logical consistency: ${plan}. Point out any potential issues, paradoxes, or violations of causality. Rate the consistency on a scale of 1-10.`
      }
    ];

    return await this.chatgpt.conversation(messages);
  }
}

module.exports = TemporalParadoxResolver;
