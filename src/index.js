const ChatGPT = require('./chatgpt');
const FineTuningManager = require('./fine-tuning');

/**
 * Main entry point for AI-Time-Machines ChatGPT Integration
 */

// Export the ChatGPT class and FineTuningManager for use in other modules
module.exports = {
  ChatGPT,
  FineTuningManager,
};

/**
 * Main function with example usage
 */
async function main() {
  try {
    console.log('AI-Time-Machines - ChatGPT Integration\n');

    // Initialize ChatGPT
    const chatgpt = new ChatGPT();
    console.log('✓ ChatGPT initialized successfully');
    console.log(`✓ Using model: ${chatgpt.model}\n`);

    // Example 1: Simple chat
    console.log('Example 1: Simple chat');
    console.log('Question: What is AI?');
    const response1 = await chatgpt.chat('What is AI? Give a brief answer.');
    console.log(`Response: ${response1}\n`);

    // Example 2: Conversation with context
    console.log('Example 2: Conversation with context');
    const conversationMessages = [
      { role: 'system', content: 'You are a helpful assistant specializing in time management and AI.' },
      { role: 'user', content: 'How can AI help with time management?' },
    ];
    const response2 = await chatgpt.conversation(conversationMessages);
    console.log(`Response: ${response2}\n`);

    // Example 3: Using different parameters
    console.log('Example 3: Creative response with higher temperature');
    const response3 = await chatgpt.chat(
      'Write a creative tagline for AI-Time-Machines',
      { temperature: 0.9, max_tokens: 50 }
    );
    console.log(`Response: ${response3}\n`);

    console.log('✓ All examples completed successfully!');
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Example usage when run directly
if (require.main === module) {
  main();
}
