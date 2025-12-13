# OpenAI API Configuration Guide

This guide provides comprehensive instructions for securely setting up and testing the OpenAI API with AI Time Machines.

## Table of Contents

- [Getting Your API Key](#getting-your-api-key)
- [Environment Setup](#environment-setup)
- [Security Best Practices](#security-best-practices)
- [Testing Your Configuration](#testing-your-configuration)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Getting Your API Key

### Step 1: Create an OpenAI Account

1. Visit [https://platform.openai.com/](https://platform.openai.com/)
2. Click "Sign up" or "Log in" if you already have an account
3. Complete the registration process
4. Verify your email address

### Step 2: Access the API Keys Section

1. Log in to [https://platform.openai.com/](https://platform.openai.com/)
2. Navigate to [API Keys](https://platform.openai.com/api-keys)
3. You'll see a list of your existing API keys (if any)

### Step 3: Generate a New API Key

1. Click the **"Create new secret key"** button
2. (Optional) Give your key a name for identification (e.g., "AI-Time-Machines-Dev")
3. Click **"Create secret key"**
4. **IMPORTANT**: Copy the key immediately - you won't be able to see it again!
5. Store the key securely (see [Security Best Practices](#security-best-practices))

### API Key Format

Your API key will look like this:
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Environment Setup

### Method 1: Using .env File (Recommended)

This is the most secure and convenient method for local development.

#### 1. Copy the Example File

```bash
cp .env.example .env
```

#### 2. Edit the .env File

Open `.env` in your text editor:

```bash
# On macOS/Linux
nano .env

# On Windows
notepad .env
```

#### 3. Add Your API Key

Replace `your_openai_api_key_here` with your actual API key:

```bash
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

#### 4. Save and Close

- In nano: Press `Ctrl+X`, then `Y`, then `Enter`
- In notepad: Click File → Save

#### 5. Verify .env is Ignored by Git

Check that `.env` is in `.gitignore`:

```bash
cat .gitignore | grep .env
```

You should see `.env` listed. This prevents accidental commits of your API key.

### Method 2: System Environment Variables

For production deployments or CI/CD pipelines.

#### On Linux/macOS

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):

```bash
export OPENAI_API_KEY="sk-proj-your-actual-api-key-here"
```

Then reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

#### On Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY = "sk-proj-your-actual-api-key-here"
```

For permanent configuration:

```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-proj-your-actual-api-key-here', 'User')
```

#### On Windows (Command Prompt)

```cmd
setx OPENAI_API_KEY "sk-proj-your-actual-api-key-here"
```

### Method 3: Direct Code Configuration (Not Recommended)

Only use for testing or when other methods aren't possible.

```javascript
const { ChatGPT } = require('./src/index');

// Pass API key directly (NOT RECOMMENDED for production)
const chatgpt = new ChatGPT('sk-proj-your-actual-api-key-here');
```

⚠️ **Warning**: Never hard-code API keys in files that will be committed to version control!

## Security Best Practices

### 1. Never Commit API Keys

**✅ DO:**
- Use `.env` files for local development
- Ensure `.env` is in `.gitignore`
- Use `.env.example` as a template without real keys

**❌ DON'T:**
- Hard-code API keys in source code
- Commit `.env` files to version control
- Share API keys in chat, email, or public forums
- Store keys in unencrypted files

### 2. Restrict API Key Permissions

When creating API keys, you can set permissions:

1. Go to [API Keys](https://platform.openai.com/api-keys)
2. Click on your key or create a new one
3. Set permissions:
   - **Read-only**: For monitoring/analytics only
   - **Restricted**: Limit to specific endpoints
   - **Full access**: Only when necessary

### 3. Use Different Keys for Different Environments

Create separate API keys for:
- **Development**: For local testing
- **Staging**: For pre-production testing
- **Production**: For live applications

This allows you to:
- Track usage per environment
- Revoke keys without affecting other environments
- Set different rate limits

### 4. Rotate Keys Regularly

Best practices for key rotation:
- Rotate keys every 90 days
- Immediately rotate if a key is exposed
- Keep old keys active briefly during transition
- Update all applications using the old key

### 5. Monitor Usage

Regularly check your [OpenAI Usage Dashboard](https://platform.openai.com/usage):
- Review API call patterns
- Check for unexpected usage spikes
- Monitor costs
- Set up usage alerts

### 6. Implement Rate Limiting

Protect against abuse and unexpected costs:

```javascript
// Example: Simple rate limiting
class RateLimiter {
  constructor(maxRequests, timeWindow) {
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindow;
    this.requests = [];
  }

  async checkLimit() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.timeWindow);
    
    if (this.requests.length >= this.maxRequests) {
      throw new Error('Rate limit exceeded');
    }
    
    this.requests.push(now);
  }
}

// Usage
const limiter = new RateLimiter(10, 60000); // 10 requests per minute
```

### 7. Secure Storage in Production

For production applications:

**Cloud Platforms:**
- **AWS**: Use AWS Secrets Manager or Parameter Store
- **Google Cloud**: Use Secret Manager
- **Azure**: Use Azure Key Vault
- **Heroku**: Use Config Vars
- **Vercel/Netlify**: Use Environment Variables

**Container/Kubernetes:**
- Use Kubernetes Secrets
- Mount secrets as environment variables
- Never include secrets in container images

## Testing Your Configuration

### Test 1: Basic Connection Test

Create a test file `test-config.js`:

```javascript
const { ChatGPT } = require('./src/index');

async function testConnection() {
  try {
    console.log('Testing OpenAI API connection...\n');
    
    const chatgpt = new ChatGPT();
    console.log('✓ ChatGPT initialized successfully');
    console.log(`✓ Using model: ${chatgpt.model}\n`);
    
    console.log('Sending test message...');
    const response = await chatgpt.chat('Say "Hello, Time Traveler!" if you can read this.');
    console.log(`✓ Response received: ${response}\n`);
    
    console.log('✅ Configuration is correct! API is working properly.');
    
  } catch (error) {
    console.error('❌ Configuration test failed!');
    console.error(`Error: ${error.message}\n`);
    
    if (error.message.includes('API key')) {
      console.error('Solution: Check that your .env file exists and contains a valid OPENAI_API_KEY');
    } else if (error.message.includes('401')) {
      console.error('Solution: Your API key is invalid. Generate a new one at https://platform.openai.com/api-keys');
    } else if (error.message.includes('429')) {
      console.error('Solution: Rate limit exceeded. Wait a moment and try again, or upgrade your plan.');
    }
    
    process.exit(1);
  }
}

testConnection();
```

Run the test:

```bash
node test-config.js
```

### Test 2: Environment Variable Check

```bash
# Linux/macOS
echo $OPENAI_API_KEY

# Windows PowerShell
echo $env:OPENAI_API_KEY

# Windows CMD
echo %OPENAI_API_KEY%
```

You should see your API key (or at least confirm it's set). If empty, your environment variable isn't configured.

### Test 3: File Existence Check

```bash
# Check if .env file exists
ls -la .env

# Check if .env contains the API key (without showing the key)
grep -q "OPENAI_API_KEY=sk-" .env && echo "API key found in .env" || echo "API key not found in .env"
```

### Test 4: Run Existing Examples

```bash
# Run the main examples
npm start

# Run the comprehensive examples
node examples.js

# Run the agent examples
node agent-examples.js
```

### Test 5: Run Tests

```bash
npm test
```

## Advanced Configuration

### Multiple API Keys

For applications using multiple OpenAI accounts:

```bash
# .env
OPENAI_API_KEY_PRIMARY=sk-proj-primary-key-here
OPENAI_API_KEY_SECONDARY=sk-proj-secondary-key-here
```

```javascript
const chatgpt1 = new ChatGPT(process.env.OPENAI_API_KEY_PRIMARY);
const chatgpt2 = new ChatGPT(process.env.OPENAI_API_KEY_SECONDARY);
```

### Custom API Configuration

```javascript
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: 'org-your-organization-id', // Optional
  baseURL: 'https://api.openai.com/v1',     // Custom endpoint (optional)
  timeout: 60000,                            // Request timeout in ms
  maxRetries: 3,                             // Number of retries
});
```

### Proxy Configuration

If you're behind a corporate proxy:

```javascript
const OpenAI = require('openai');
const { HttpsProxyAgent } = require('https-proxy-agent');

const agent = new HttpsProxyAgent('http://proxy.example.com:8080');

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  httpAgent: agent,
});
```

### Organization IDs

If you're part of multiple OpenAI organizations:

```bash
# .env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_ORG_ID=org-your-organization-id
```

```javascript
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: process.env.OPENAI_ORG_ID,
});
```

## Troubleshooting

### Error: "OpenAI API key is required"

**Cause**: The API key is not set or cannot be found.

**Solutions**:
1. Check if `.env` file exists in the project root
2. Verify the `.env` file contains `OPENAI_API_KEY=sk-...`
3. Ensure no extra spaces around the `=` sign
4. Try restarting your terminal/IDE
5. Check if `dotenv` is installed: `npm install dotenv`

### Error: "Incorrect API key provided"

**Cause**: The API key format is invalid or the key doesn't exist.

**Solutions**:
1. Verify you copied the entire key (usually starts with `sk-proj-`)
2. Check for extra spaces or line breaks in the key
3. Generate a new API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Make sure you're using a valid, non-revoked key

### Error: "You exceeded your current quota"

**Cause**: You've run out of API credits or reached your usage limit.

**Solutions**:
1. Check your usage at [https://platform.openai.com/usage](https://platform.openai.com/usage)
2. Add billing information at [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing)
3. Purchase additional credits if needed
4. Check if your free trial has expired

### Error: "Rate limit reached"

**Cause**: Too many requests in a short period.

**Solutions**:
1. Wait a few moments before retrying
2. Implement exponential backoff in your code
3. Reduce the frequency of requests
4. Upgrade to a higher tier plan for better rate limits

### Error: "Model not found"

**Cause**: You're trying to use a model you don't have access to.

**Solutions**:
1. Check available models with `chatgpt.getAvailableModels()`
2. Use 'gpt-3.5-turbo' instead of 'gpt-4' if you don't have GPT-4 access
3. Verify your account type supports the requested model

### .env File Not Loading

**Cause**: The `dotenv` package might not be properly configured.

**Solutions**:
1. Ensure `require('dotenv').config()` is at the top of your entry file
2. Check that `dotenv` is installed: `npm install dotenv`
3. Try specifying the path: `require('dotenv').config({ path: '.env' })`
4. Verify the `.env` file is in the project root, not in a subdirectory

### Environment Variables Not Persisting

**Cause**: Environment variables set in terminal are session-specific.

**Solutions**:
1. Add export statements to shell profile (`~/.bashrc`, `~/.zshrc`)
2. Use `.env` file instead for local development
3. For permanent system variables, use system settings (varies by OS)

## Additional Resources

- [OpenAI Platform](https://platform.openai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [API Keys Management](https://platform.openai.com/api-keys)
- [Usage Dashboard](https://platform.openai.com/usage)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Error Codes](https://platform.openai.com/docs/guides/error-codes)

## Getting Help

If you're still having issues:

1. Check [GitHub Issues](https://github.com/lippytm/AI-Time-Machines/issues)
2. Visit [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
3. Review [OpenAI Community Forum](https://community.openai.com/)
4. Contact [OpenAI Support](https://help.openai.com/)

---

🔒 Remember: Keep your API keys secure and never share them publicly!
