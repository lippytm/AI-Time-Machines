# AI Agents

This directory contains specialized AI agents for time-machine-related functionalities. Each agent is designed to handle specific aspects of time travel planning, historical analysis, and temporal mechanics.

## Available Agents

### 1. Time Travel Assistant (`time-travel-assistant.js`)

A conversational agent that helps users plan safe and educational time travel journeys.

**Features**:
- Time period recommendations based on interests
- Safety briefings for specific time periods
- Historical context for events
- Maintains conversation history for contextual responses

**Example Usage**:

```javascript
const { TimeTravelAssistant } = require('./agents');

const assistant = new TimeTravelAssistant();

// Get recommendations
const rec = await assistant.recommendTimePeriod('ancient civilizations');

// Get safety briefing
const safety = await assistant.getSafetyBriefing('medieval Europe');

// Have a conversation
const response = await assistant.chat('What should I bring to ancient Rome?');
```

### 2. Historical Context Agent (`historical-context-agent.js`)

Provides detailed historical information and analysis for different time periods.

**Features**:
- Analyze specific historical periods
- Compare different time periods
- Get biographical information on historical figures
- Understand causes and consequences of events
- Daily life descriptions for any era

**Example Usage**:

```javascript
const { HistoricalContextAgent } = require('./agents');

const agent = new HistoricalContextAgent();

// Analyze a period
const analysis = await agent.analyzePeriod('the Renaissance', 'Italy');

// Compare periods
const comparison = await agent.comparePeriods('Ancient Egypt', 'Ancient Greece');

// Get daily life details
const dailyLife = await agent.getDailyLife('Victorian London', 'working class');
```

### 3. Temporal Paradox Resolver (`temporal-paradox-resolver.js`)

Analyzes time travel scenarios for potential paradoxes and provides solutions.

**Features**:
- Analyze scenarios for temporal paradoxes
- Explain different types of paradoxes
- Suggest solutions to avoid paradoxes
- Evaluate if specific actions would create paradoxes
- Compare time travel theories

**Example Usage**:

```javascript
const { TemporalParadoxResolver } = require('./agents');

const resolver = new TemporalParadoxResolver();

// Analyze a scenario
const analysis = await resolver.analyzeScenario(
  'A time traveler goes back and prevents the invention of the internet'
);

// Explain a paradox
const explanation = await resolver.explainParadox('bootstrap');

// Check if an action would cause a paradox
const evaluation = await resolver.evaluateAction(
  'save a historical figure from assassination',
  '1865'
);
```

## Agent Architecture

All agents follow a similar architecture:

```javascript
class Agent {
  constructor(apiKey = null) {
    this.chatgpt = new ChatGPT(apiKey);
    this.systemPrompt = { role: 'system', content: '...' };
  }

  async method(params) {
    const messages = [this.systemPrompt, { role: 'user', content: query }];
    return await this.chatgpt.conversation(messages);
  }
}
```

## Using Multiple Agents Together

Combine agents for comprehensive time travel planning:

```javascript
const { TimeTravelAssistant, HistoricalContextAgent, TemporalParadoxResolver } = require('./agents');

async function planTimeTravel(destination) {
  const assistant = new TimeTravelAssistant();
  const contextAgent = new HistoricalContextAgent();
  const paradoxResolver = new TemporalParadoxResolver();

  // Get historical context
  const context = await contextAgent.analyzePeriod(destination);
  
  // Check for safety
  const safety = await assistant.getSafetyBriefing(destination);
  
  // Verify no paradoxes
  const paradoxCheck = await paradoxResolver.evaluateAction(
    `visit ${destination}`,
    destination
  );

  return { context, safety, paradoxCheck };
}
```

## Customizing Agents

### Modify System Prompts

Each agent has a `systemPrompt` that defines its behavior. You can customize it:

```javascript
const assistant = new TimeTravelAssistant();
assistant.systemPrompt = {
  role: 'system',
  content: 'Your custom system prompt here...'
};
```

### Using Fine-Tuned Models

Agents can use fine-tuned models for better performance:

```javascript
const assistant = new TimeTravelAssistant();
assistant.chatgpt.setModel('ft:gpt-3.5-turbo:your-org:time-machine:abc123');
```

### Extending Agents

Create your own specialized agents:

```javascript
const { ChatGPT } = require('../src/index');

class CustomTimeAgent {
  constructor(apiKey = null) {
    this.chatgpt = new ChatGPT(apiKey);
    this.systemPrompt = {
      role: 'system',
      content: 'Your specialized system prompt'
    };
  }

  async customMethod(input) {
    const messages = [
      this.systemPrompt,
      { role: 'user', content: input }
    ];
    return await this.chatgpt.conversation(messages);
  }
}

module.exports = CustomTimeAgent;
```

## Backend Integration

These agents are designed for backend integration:

### Express.js Example

```javascript
const express = require('express');
const { TimeTravelAssistant } = require('./agents');

const app = express();
const assistant = new TimeTravelAssistant();

app.post('/api/time-travel/plan', async (req, res) => {
  const { destination } = req.body;
  
  const recommendation = await assistant.getSafetyBriefing(destination);
  
  res.json({ success: true, recommendation });
});
```

### API Gateway Pattern

```javascript
class TimeTravelAPI {
  constructor() {
    this.assistant = new TimeTravelAssistant();
    this.contextAgent = new HistoricalContextAgent();
    this.paradoxResolver = new TemporalParadoxResolver();
  }

  async handleRequest(type, params) {
    switch(type) {
      case 'recommend':
        return await this.assistant.recommendTimePeriod(params.interest);
      case 'analyze':
        return await this.contextAgent.analyzePeriod(params.period);
      case 'checkParadox':
        return await this.paradoxResolver.analyzeScenario(params.scenario);
      default:
        throw new Error('Unknown request type');
    }
  }
}
```

## Testing Agents

Run the agent examples:

```bash
node agent-examples.js
```

Run agent tests:

```bash
npm test tests/agents.test.js
```

## Performance Optimization

### Rate Limiting

```javascript
class RateLimitedAgent extends TimeTravelAssistant {
  constructor(apiKey, maxRequests = 10, timeWindow = 60000) {
    super(apiKey);
    this.requests = [];
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindow;
  }

  async chat(message) {
    await this.checkRateLimit();
    return await super.chat(message);
  }

  async checkRateLimit() {
    const now = Date.now();
    this.requests = this.requests.filter(t => now - t < this.timeWindow);
    
    if (this.requests.length >= this.maxRequests) {
      throw new Error('Rate limit exceeded');
    }
    
    this.requests.push(now);
  }
}
```

### Caching Responses

```javascript
class CachedAgent extends HistoricalContextAgent {
  constructor(apiKey) {
    super(apiKey);
    this.cache = new Map();
  }

  async analyzePeriod(period, region = 'global') {
    const key = `${period}-${region}`;
    
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const result = await super.analyzePeriod(period, region);
    this.cache.set(key, result);
    
    return result;
  }
}
```

## Contributing

To add a new agent:

1. Create a new file in the `agents/` directory
2. Follow the existing agent architecture
3. Add comprehensive JSDoc comments
4. Export the agent in `agents/index.js`
5. Add tests in `tests/agents.test.js`
6. Document in this README
7. Add usage examples in `agent-examples.js`

## Resources

- [Agent Examples](../agent-examples.js)
- [Main Documentation](../README.md)
- [API Configuration](../docs/API_CONFIG.md)
- [OpenAI API Docs](https://platform.openai.com/docs)

## Support

For questions about agents:
- Check [agent-examples.js](../agent-examples.js) for usage patterns
- Open an issue on GitHub
- Review existing tests in `tests/agents.test.js`
