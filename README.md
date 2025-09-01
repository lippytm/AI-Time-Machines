# AI Time Machines

An intelligent ChatGPT-powered system that integrates with GitHub APIs to provide automated repository management, issue tracking, pull request assistance, and email notifications.

## Features

- **ChatGPT Integration**: Intelligent AI agent for repository interactions
- **GitHub API Integration**: Full repository management capabilities
- **Email Notifications**: Automated notifications for events and errors
- **Repository Health Analysis**: AI-powered repository health monitoring
- **Issue Management**: Automated issue creation and commenting
- **Pull Request Assistance**: AI-powered PR management
- **Monitoring**: Real-time repository activity monitoring

## Quick Start

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key
- Gmail account with App Password (for notifications)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

### Configuration

Edit the `.env` file with your credentials:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPOSITORY_OWNER=lippytm
GITHUB_REPOSITORY_NAME=AI-Time-Machines

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Email Configuration (for lippytimemachines@gmail.com)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
EMAIL_ADDRESS=lippytimemachines@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Usage

#### Command Line Interface

Test all integrations:
```bash
python -m src.ai_time_machines --test
```

Process a query with AI:
```bash
python -m src.ai_time_machines --query "What are the current open issues?"
```

Get repository health analysis:
```bash
python -m src.ai_time_machines --health
```

Get repository summary:
```bash
python -m src.ai_time_machines --summary
```

Start repository monitoring:
```bash
python -m src.ai_time_machines --monitor
```

#### Python API

```python
from src.ai_time_machines import AITimeMachines

# Initialize the application
app = AITimeMachines()

# Process a query
result = app.process_query("Create an issue for improving documentation")
print(result['response'])

# Get repository health
health = app.get_repository_health()
print(f"Health Score: {health['health_score']}/100")

# Test integrations
test_results = app.test_integrations()
```

## Architecture

### Components

1. **Configuration Management** (`src/ai_time_machines/config/`)
   - Environment variable management
   - Pydantic-based configuration validation
   - Secure credential handling

2. **GitHub Integration** (`src/ai_time_machines/github_integration/`)
   - Repository information retrieval
   - Issue creation and management
   - Pull request operations
   - File operations
   - Commit history access

3. **Email Service** (`src/ai_time_machines/email_service/`)
   - SMTP email notifications
   - Event-based notifications
   - Error alerting
   - HTML email templates

4. **AI Components** (`src/ai_time_machines/ai_components/`)
   - ChatGPT integration
   - Intelligent GitHub action parsing
   - Repository health analysis
   - Context-aware responses

5. **Main Application** (`src/ai_time_machines/`)
   - CLI interface
   - Integration orchestration
   - Monitoring capabilities
   - Error handling

### Email Notifications

The system sends notifications for:

- **GitHub Events**: New issues, pull requests, commits
- **AI Actions**: Issue creation, comments, responses
- **Errors**: System errors, API failures
- **Health Checks**: Repository health analysis results
- **Monitoring**: Real-time activity updates

All notifications are sent to `lippytimemachines@gmail.com` by default.

### AI Capabilities

The ChatGPT agent can:

- Answer questions about repository status
- Create issues based on natural language requests
- Comment on existing issues
- Analyze repository health and provide recommendations
- Suggest improvements and best practices
- Monitor repository activity

### GitHub API Features

- **Repository Management**: Get info, statistics, health metrics
- **Issue Tracking**: Create, update, comment, list issues
- **Pull Request Management**: Create, comment, review PRs
- **File Operations**: Read, create, update repository files
- **Commit History**: Access and analyze commit data
- **Branch Management**: Work with different branches

## Security

- All sensitive credentials are stored in environment variables
- GitHub token requires appropriate repository permissions
- Email passwords should use Gmail App Passwords
- Configuration validation prevents invalid setups

## Error Handling

The system includes comprehensive error handling:

- Automatic email notifications for system errors
- Graceful degradation when services are unavailable
- Detailed logging for debugging
- Connection retries for transient failures

## Monitoring

The built-in monitoring system:

- Checks for new repository activity
- Sends real-time notifications
- Configurable check intervals
- Automatic error recovery

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Features

1. Create new modules in appropriate directories
2. Update configuration if needed
3. Add error handling and logging
4. Update documentation

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **GitHub Token Issues**
   - Ensure token has `repo` scope
   - Check token expiration
   - Verify repository access

2. **Email Configuration**
   - Use Gmail App Passwords, not regular passwords
   - Enable 2FA on Gmail account
   - Check SMTP settings

3. **OpenAI API Issues**
   - Verify API key validity
   - Check usage limits
   - Ensure billing is set up

4. **Permission Errors**
   - Check file permissions
   - Ensure Python can write to log directories
   - Verify environment variable access

### Logs

Logs are output to stderr with configurable levels:
- DEBUG: Detailed debugging information
- INFO: General operational messages
- WARNING: Warning messages
- ERROR: Error messages

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For support and questions:
- Email: lippytimemachines@gmail.com
- GitHub Issues: [Create an issue](https://github.com/lippytm/AI-Time-Machines/issues)

---

**AI Time Machines** - Adding AI Agents to everything with Time Machines 
