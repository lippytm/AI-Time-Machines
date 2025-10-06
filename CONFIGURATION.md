# AI Time Machines Configuration Guide

This guide provides step-by-step instructions for setting up AI Time Machines with GitHub API and email integration.

## Prerequisites

1. **GitHub Account**: Access to the repository you want to manage
2. **OpenAI Account**: API access for ChatGPT integration
3. **Gmail Account**: For email notifications (lippytimemachines@gmail.com)
4. **Python 3.8+**: Required for running the application

## Setup Instructions

### 1. GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Set expiration and select scopes:
   - `repo` (Full control of private repositories)
   - `read:user` (Read user profile data)
   - `user:email` (Access user email addresses)
4. Copy the generated token

### 2. OpenAI API Key

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy the generated API key
4. Ensure you have billing set up for API usage

### 3. Gmail App Password

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Select "Mail" and "Other (custom name)" 
5. Enter "AI Time Machines" as the app name
6. Copy the generated 16-character app password

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```env
   # GitHub Configuration
   GITHUB_TOKEN=ghp_your_actual_github_token_here
   GITHUB_REPOSITORY_OWNER=lippytm
   GITHUB_REPOSITORY_NAME=AI-Time-Machines

   # OpenAI Configuration  
   OPENAI_API_KEY=sk-your_actual_openai_key_here

   # Email Configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USE_TLS=true
   EMAIL_ADDRESS=lippytimemachines@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password

   # Application Configuration
   LOG_LEVEL=INFO
   ENVIRONMENT=production
   ```

### 5. Installation and Testing

1. Run the setup script:
   ```bash
   python setup.py
   ```

2. Test all integrations:
   ```bash
   python -m src.ai_time_machines --test
   ```

3. If all tests pass, you're ready to use AI Time Machines!

## Verification Steps

### Test GitHub Integration
```bash
python -m src.ai_time_machines --summary
```
This should display repository information, issues, and PRs.

### Test AI Query Processing
```bash
python -m src.ai_time_machines --query "What is the current status of this repository?"
```
This should return an AI-generated response about the repository.

### Test Email Notifications
The setup script automatically sends a test email. Check the configured email address for the test message.

### Test Repository Health Analysis
```bash
python -m src.ai_time_machines --health
```
This should provide a health score and recommendations for the repository.

## Usage Examples

### Basic Queries
```bash
# Ask about open issues
python -m src.ai_time_machines --query "How many open issues do we have and what are they about?"

# Request issue creation
python -m src.ai_time_machines --query "Create an issue for improving the documentation"

# Get repository insights
python -m src.ai_time_machines --query "Analyze recent activity and suggest improvements"
```

### Monitoring
```bash
# Start continuous monitoring (checks every 5 minutes)
python -m src.ai_time_machines --monitor --monitor-interval 300
```

### Python API Usage
```python
from src.ai_time_machines import AITimeMachines

app = AITimeMachines()

# Process queries
result = app.process_query("Create an issue for adding unit tests")
print(result['response'])

# Get health analysis
health = app.get_repository_health()
print(f"Health Score: {health['health_score']}/100")
```

## Email Notification Types

The system sends notifications for:

1. **AI Actions**: When the AI creates issues or comments
2. **Repository Events**: New issues, PRs, significant changes
3. **Health Alerts**: When repository health score changes significantly
4. **Errors**: System errors, API failures, configuration issues
5. **Monitoring**: Regular activity summaries

## Troubleshooting

### GitHub Token Issues
- Ensure token has `repo` scope for the target repository
- Check if token has expired
- Verify repository name and owner are correct

### OpenAI API Issues
- Verify API key is valid and not expired
- Check OpenAI billing status and usage limits
- Ensure you have access to GPT-3.5-turbo model

### Email Issues
- Use Gmail App Password, not regular password
- Ensure 2FA is enabled on Gmail account
- Check SMTP settings (server: smtp.gmail.com, port: 587, TLS: enabled)

### Permission Issues
- Check file permissions in the project directory
- Ensure Python can create log files
- Verify environment variables are loaded correctly

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use app passwords** instead of regular Gmail passwords
3. **Rotate tokens regularly** - Set expiration dates on GitHub tokens
4. **Monitor API usage** - Check OpenAI usage to avoid unexpected charges
5. **Limit token scopes** - Only grant necessary permissions

## Advanced Configuration

### Custom Email Recipients
Modify the email service to send to additional recipients:

```python
# In your custom code
app.email_service.send_github_event_notification(
    event_type="Custom Event",
    event_data={"message": "Custom notification"},
    recipients=["additional@email.com"]
)
```

### Custom Repository
To work with a different repository, update the environment variables:

```env
GITHUB_REPOSITORY_OWNER=your_username
GITHUB_REPOSITORY_NAME=your_repository
```

### Custom AI Prompts
The AI system prompt can be customized in `src/ai_time_machines/ai_components/__init__.py` in the `_build_system_prompt` method.

## Support

For issues or questions:
- Check the main README.md for documentation
- Review logs for error details
- Email: lippytimemachines@gmail.com
- GitHub Issues: Create an issue in the repository

## Next Steps

Once configured, consider:

1. Setting up monitoring with `--monitor` flag
2. Creating custom queries for your workflow
3. Integrating with CI/CD pipelines
4. Adding custom notification rules
5. Extending AI capabilities for your specific needs