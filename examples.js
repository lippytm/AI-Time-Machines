/**
 * AI-Time-Machines Example Usage
 * 
 * This file demonstrates how to use the ChatGPT integration
 * in your own projects.
 */

const { ChatGPT } = require('./src/index');

/**
 * Example 1: Basic Chat
 */
async function basicChatExample() {
  console.log('\n=== Example 1: Basic Chat ===\n');
  
  const chatgpt = new ChatGPT();
  
  const question = 'Explain quantum computing in simple terms.';
  console.log(`Question: ${question}`);
  
  const answer = await chatgpt.chat(question);
  console.log(`Answer: ${answer}`);
}

/**
 * Example 2: Conversation with System Context
 */
async function conversationWithContextExample() {
  console.log('\n=== Example 2: Conversation with System Context ===\n');
  
  const chatgpt = new ChatGPT();
  
  const messages = [
    { 
      role: 'system', 
      content: 'You are a motivational coach who helps people manage their time better.' 
    },
    { 
      role: 'user', 
      content: 'I struggle to stay productive. Can you give me 3 tips?' 
    }
  ];
  
  const response = await chatgpt.conversation(messages);
  console.log(`Coach Response:\n${response}`);
}

/**
 * Example 3: Using Different Models
 */
async function differentModelsExample() {
  console.log('\n=== Example 3: Using Different Models ===\n');
  
  const chatgpt = new ChatGPT();
  
  // Use GPT-3.5 Turbo for faster, cost-effective responses
  chatgpt.setModel('gpt-3.5-turbo');
  
  const question = 'What is the capital of France?';
  console.log(`Question: ${question}`);
  console.log(`Model: ${chatgpt.model}`);
  
  const answer = await chatgpt.chat(question);
  console.log(`Answer: ${answer}`);
}

/**
 * Example 4: Adjusting Temperature for Creativity
 */
async function temperatureExample() {
  console.log('\n=== Example 4: Adjusting Temperature ===\n');
  
  const chatgpt = new ChatGPT();
  
  const prompt = 'Write a creative slogan for a coffee shop.';
  
  // Low temperature (more focused and deterministic)
  console.log('Low Temperature (0.2):');
  const lowTemp = await chatgpt.chat(prompt, { temperature: 0.2 });
  console.log(lowTemp);
  
  console.log('\nHigh Temperature (0.9):');
  // High temperature (more creative and varied)
  const highTemp = await chatgpt.chat(prompt, { temperature: 0.9 });
  console.log(highTemp);
}

/**
 * Example 5: Multi-turn Conversation
 */
async function multiTurnConversationExample() {
  console.log('\n=== Example 5: Multi-turn Conversation ===\n');
  
  const chatgpt = new ChatGPT();
  
  const conversation = [
    { role: 'system', content: 'You are a helpful math tutor.' },
    { role: 'user', content: 'What is 15 * 23?' },
    { role: 'assistant', content: '15 * 23 = 345' },
    { role: 'user', content: 'Can you show me how you calculated that?' }
  ];
  
  const response = await chatgpt.conversation(conversation);
  console.log('Tutor Explanation:');
  console.log(response);
}

/**
 * Main function to run all examples
 */
async function runExamples() {
  try {
    console.log('AI-Time-Machines - ChatGPT Integration Examples');
    console.log('='.repeat(50));
    
    await basicChatExample();
    await conversationWithContextExample();
    await differentModelsExample();
    await temperatureExample();
    await multiTurnConversationExample();
    
    console.log('\n' + '='.repeat(50));
    console.log('All examples completed successfully!');
    
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
  runExamples();
}

module.exports = {
  basicChatExample,
  conversationWithContextExample,
  differentModelsExample,
  temperatureExample,
  multiTurnConversationExample,
};
