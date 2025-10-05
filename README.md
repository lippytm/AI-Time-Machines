# AI-Time-Machines

Adding AI Agents to everything with Time Machines - OpenAI ChatGPT Integration

## Overview

AI-Time-Machines is a powerful integration that brings OpenAI's ChatGPT capabilities to your applications. This repository provides a clean, easy-to-use wrapper for interacting with the OpenAI API, enabling advanced AI-powered conversations and automation.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 18.0.0 or higher)
- **npm** (comes with Node.js)
- **OpenAI API Key** (requires an OpenAI account)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Your OpenAI API Key

#### Obtain Your API Key

1. Create an account or log in at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to [API Keys](https://platform.openai.com/api-keys)
3. Click "Create new secret key"
4. Copy your API key (you won't be able to see it again!)

#### Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Open `.env` and replace `your_openai_api_key_here` with your actual API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

⚠️ **Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Running the Examples

Run the included examples to test your setup:

```bash
npm start
```

This will execute several example interactions with ChatGPT, demonstrating:
- Simple chat messages
- Conversations with context
- Custom parameters (temperature, max_tokens)

### Using in Your Code

```javascript
const { ChatGPT } = require('./src/index');

// Initialize ChatGPT
const chatgpt = new ChatGPT();

// Simple chat
async function example() {
  const response = await chatgpt.chat('Hello, ChatGPT!');
  console.log(response);
}

// Conversation with context
async function conversationExample() {
  const messages = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'What is AI?' }
  ];
  const response = await chatgpt.conversation(messages);
  console.log(response);
}
```

### Available Methods

#### `chat(message, options)`

Send a single message to ChatGPT.

- **message** (string): The message to send
- **options** (object, optional):
  - `model`: The model to use (default: 'gpt-4')
  - `temperature`: Controls randomness, 0-1 (default: 0.7)
  - `max_tokens`: Maximum response length (default: 1000)

#### `conversation(messages, options)`

Have a conversation with context.

- **messages** (array): Array of message objects with `role` and `content`
- **options** (object, optional): Same as `chat()` options

#### `setModel(model)`

Change the default model.

```javascript
chatgpt.setModel('gpt-3.5-turbo');
```

#### `getAvailableModels()`

Get a list of commonly available models.

## Development

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Project Structure

```
AI-Time-Machines/
├── src/
│   ├── chatgpt.js       # ChatGPT wrapper class
│   └── index.js         # Main entry point with examples
├── tests/
│   └── chatgpt.test.js  # Unit tests
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
├── package.json         # Project dependencies
└── README.md           # This file
```

## Security Best Practices

- ✅ Always use environment variables for API keys
- ✅ Never commit `.env` files to version control
- ✅ Use `.env.example` as a template without real credentials
- ✅ Keep your API key secure and don't share it publicly
- ✅ Rotate your API keys regularly
- ✅ Monitor your OpenAI usage dashboard for unexpected activity

## Advanced Features (OpenAI Pro Account)

With an OpenAI Pro account, you can access:

- **GPT-4**: More capable model with better reasoning
- **Higher rate limits**: More requests per minute
- **Priority access**: Faster response times
- **Extended context**: Longer conversation history

To use GPT-4 (requires appropriate API access):

```javascript
const chatgpt = new ChatGPT();
chatgpt.setModel('gpt-4');
```

## Troubleshooting

### "OpenAI API key is required" Error

Make sure your `.env` file exists and contains a valid API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### API Rate Limit Errors

If you encounter rate limit errors, you may need to:
- Wait a moment before retrying
- Upgrade your OpenAI plan
- Implement rate limiting in your application

### Module Not Found Errors

Ensure all dependencies are installed:

```bash
npm install
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Platform](https://platform.openai.com/)
- [Node.js OpenAI SDK](https://github.com/openai/openai-node)

## Support

For questions and support:
- Check [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
- Review the [OpenAI API Documentation](https://platform.openai.com/docs)
- Open an issue for bugs or feature requests 
