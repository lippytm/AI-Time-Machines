/**
 * AI-Time-Machines Backend Agent Examples
 * 
 * This file demonstrates how to use the specialized AI agents
 * for various time-machine-related functionalities.
 */

const TimeTravelAssistant = require('./agents/time-travel-assistant');
const HistoricalContextAgent = require('./agents/historical-context-agent');
const TemporalParadoxResolver = require('./agents/temporal-paradox-resolver');

/**
 * Example 1: Using the Time Travel Assistant
 */
async function timeTravelAssistantExample() {
  console.log('\n=== Example 1: Time Travel Assistant ===\n');
  
  const assistant = new TimeTravelAssistant();
  
  // Get a time period recommendation
  console.log('Getting recommendation for someone interested in art...');
  const recommendation = await assistant.recommendTimePeriod('Renaissance art and culture');
  console.log(recommendation);
  
  console.log('\n---\n');
  
  // Get safety briefing
  console.log('Getting safety briefing for ancient Egypt...');
  const safetyBriefing = await assistant.getSafetyBriefing('ancient Egypt around 2500 BCE');
  console.log(safetyBriefing);
  
  console.log('\n---\n');
  
  // Have a conversation
  assistant.resetConversation();
  console.log('User: I want to visit the first moon landing');
  const response1 = await assistant.chat('I want to visit the first moon landing. What should I know?');
  console.log(`Assistant: ${response1}`);
  
  console.log('\nUser: What if I accidentally interfere with the mission?');
  const response2 = await assistant.chat('What if I accidentally interfere with the mission?');
  console.log(`Assistant: ${response2}`);
}

/**
 * Example 2: Using the Historical Context Agent
 */
async function historicalContextExample() {
  console.log('\n=== Example 2: Historical Context Agent ===\n');
  
  const agent = new HistoricalContextAgent();
  
  // Analyze a period
  console.log('Analyzing the Industrial Revolution...');
  const analysis = await agent.analyzePeriod('the Industrial Revolution', 'Britain');
  console.log(analysis);
  
  console.log('\n---\n');
  
  // Compare periods
  console.log('Comparing Medieval Europe with Ancient Rome...');
  const comparison = await agent.comparePeriods('Medieval Europe', 'Ancient Rome');
  console.log(comparison);
  
  console.log('\n---\n');
  
  // Get daily life description
  console.log('Daily life in Victorian England...');
  const dailyLife = await agent.getDailyLife('Victorian England (1850s)', 'working class');
  console.log(dailyLife);
}

/**
 * Example 3: Using the Temporal Paradox Resolver
 */
async function temporalParadoxExample() {
  console.log('\n=== Example 3: Temporal Paradox Resolver ===\n');
  
  const resolver = new TemporalParadoxResolver();
  
  // Explain a paradox
  console.log('Explaining the grandfather paradox...');
  const explanation = await resolver.explainParadox('grandfather');
  console.log(explanation);
  
  console.log('\n---\n');
  
  // Analyze a scenario
  console.log('Analyzing a time travel scenario...');
  const scenario = 'A time traveler goes back to 1920 and invents the smartphone before the transistor was invented';
  const scenarioAnalysis = await resolver.analyzeScenario(scenario);
  console.log(scenarioAnalysis);
  
  console.log('\n---\n');
  
  // Evaluate an action
  console.log('Evaluating a proposed action...');
  const actionEval = await resolver.evaluateAction(
    'prevent the assassination of Archduke Franz Ferdinand',
    '1914'
  );
  console.log(actionEval);
}

/**
 * Example 4: Combining Multiple Agents
 */
async function combinedAgentsExample() {
  console.log('\n=== Example 4: Combined Agents Workflow ===\n');
  
  const assistant = new TimeTravelAssistant();
  const contextAgent = new HistoricalContextAgent();
  const paradoxResolver = new TemporalParadoxResolver();
  
  // Step 1: User wants to visit a period
  console.log('Step 1: Planning a trip to witness the signing of the Declaration of Independence');
  const context = await contextAgent.analyzeEventCausality('the signing of the Declaration of Independence in 1776');
  console.log(`Historical Context:\n${context}\n`);
  
  // Step 2: Get safety briefing
  console.log('Step 2: Getting safety briefing');
  const safety = await assistant.getSafetyBriefing('Philadelphia in 1776');
  console.log(`Safety Briefing:\n${safety}\n`);
  
  // Step 3: Check for paradox risks
  console.log('Step 3: Checking for paradox risks');
  const paradoxCheck = await paradoxResolver.evaluateAction(
    'observe the signing of the Declaration of Independence',
    '1776'
  );
  console.log(`Paradox Analysis:\n${paradoxCheck}\n`);
  
  console.log('Trip approved! Safe travels through time! 🚀');
}

/**
 * Example 5: Backend API Integration Pattern
 */
async function backendAPIExample() {
  console.log('\n=== Example 5: Backend API Integration Pattern ===\n');
  
  // Simulate a REST API endpoint handler
  const handleTimeTravelRequest = async (requestData) => {
    const { destination, userInterests, concerns } = requestData;
    
    console.log(`Processing request for: ${destination}`);
    
    const assistant = new TimeTravelAssistant();
    const contextAgent = new HistoricalContextAgent();
    
    // Gather information
    const historicalInfo = await contextAgent.analyzePeriod(destination);
    const safetyInfo = await assistant.getSafetyBriefing(destination);
    const personalizedAdvice = await assistant.chat(
      `I'm interested in ${userInterests} and concerned about ${concerns}. What should I know about visiting ${destination}?`
    );
    
    return {
      destination,
      historicalContext: historicalInfo,
      safetyBriefing: safetyInfo,
      personalizedAdvice: personalizedAdvice,
      status: 'approved'
    };
  };
  
  // Example request
  const request = {
    destination: 'ancient Greece, 400 BCE',
    userInterests: 'philosophy and architecture',
    concerns: 'language barriers and cultural customs'
  };
  
  const response = await handleTimeTravelRequest(request);
  console.log('API Response:');
  console.log(JSON.stringify(response, null, 2));
}

/**
 * Main function to run all examples
 */
async function runAllExamples() {
  try {
    console.log('AI-Time-Machines - Backend Agent Examples');
    console.log('='.repeat(60));
    
    // Note: Uncomment the examples you want to run
    // Running all examples requires API calls and may take time
    
    // await timeTravelAssistantExample();
    // await historicalContextExample();
    // await temporalParadoxExample();
    // await combinedAgentsExample();
    await backendAPIExample();
    
    console.log('\n' + '='.repeat(60));
    console.log('Examples completed successfully!');
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error('\nMake sure you have:');
    console.error('1. Created a .env file with your OPENAI_API_KEY');
    console.error('2. Installed dependencies with: npm install');
    process.exit(1);
  }
}

// Run examples if this file is executed directly
if (require.main === module) {
  runAllExamples();
}

module.exports = {
  timeTravelAssistantExample,
  historicalContextExample,
  temporalParadoxExample,
  combinedAgentsExample,
  backendAPIExample,
};
