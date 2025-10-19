# Quick Start Guide

This guide will help you get up and running with the AI-Time-Machines ChatGPT integration in just a few minutes.

## Step 1: Prerequisites

Ensure you have:
- Node.js 18.0.0 or higher installed
- npm (comes with Node.js)
- An OpenAI account

## Step 2: Installation

Clone and set up the repository:

```bash
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines
npm install
```

## Step 3: Get Your OpenAI API Key

1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (you won't see it again!)

## Step 4: Configure Your Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 5: Test Your Setup

Run the examples to verify everything works:

```bash
npm start
```

You should see output from three different ChatGPT interactions!

## Step 6: Start Building

### Basic Usage

```javascript
const { ChatGPT } = require('./src/index');

const chatgpt = new ChatGPT();
const response = await chatgpt.chat('Hello, ChatGPT!');
console.log(response);
```

### Run More Examples

```bash
node examples.js
```

This runs 5 different examples showing various features.

## Common Issues

### Error: "OpenAI API key is required"

- Make sure your `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is set correctly in `.env`
- Ensure there are no extra spaces or quotes around the key

### Error: "Module not found"

Run `npm install` to install all dependencies.

### Rate Limit Errors

- Free tier has rate limits
- Consider upgrading your OpenAI plan
- Add delays between requests if needed

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review [examples.js](examples.js) for usage patterns
- Check out the [OpenAI API docs](https://platform.openai.com/docs) for advanced features

## Security Reminders

⚠️ **Never commit your `.env` file to version control!**

- `.env` is already in `.gitignore`
- Use `.env.example` as a template
- Keep your API key secure
- Rotate keys if they're exposed

## Getting Help

- [GitHub Issues](https://github.com/lippytm/AI-Time-Machines/issues)
- [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
- [OpenAI Community Forum](https://community.openai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

Happy coding! 🚀
