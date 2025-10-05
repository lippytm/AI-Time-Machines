# AI-Time-Machines

AI-powered GitHub automation system for processing pull requests and repository management with dynamic authorization and workflow capabilities.

## Features

- **Dynamic Authorization**: Secure GitHub API access with token-based authentication
- **Pull Request Automation**: Process PR numbers and repository names dynamically
- **Workflow Engine**: Automated processing without manual input
- **Multi-Repository Support**: Handle multiple repositories and PRs in batch
- **Flexible Input Formats**: Support URLs, numbers, auto-discovery, and JSON input
- **Extensible Hooks**: Pre/post-processing hooks for custom workflows

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment template and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your GitHub token and default repository settings:

```bash
# GitHub Authentication
GITHUB_TOKEN=your_github_token_here

# Default Repository Settings
DEFAULT_REPO_OWNER=your_username
DEFAULT_REPO_NAME=your_repository

# Automation Settings
AUTO_PROCESS_PRS=true
MAX_PR_BATCH_SIZE=10
```

### 3. Basic Usage

```bash
# Validate configuration
python main.py --validate

# Process specific PRs
python main.py --repo-owner myorg --repo-name myrepo --pr-numbers 123 124

# Process PR from URL
python main.py --pr-url https://github.com/myorg/myrepo/pull/123

# Auto-discover and process open PRs
python main.py --repo-owner myorg --repo-name myrepo --auto-discover

# Process with pattern filter
python main.py --repo-owner myorg --repo-name myrepo --auto-discover --pattern "bug fix"
```

## API Usage

### Python API

```python
from workflow import process_automation_request

# Define automation request
input_data = {
    "repository_owner": "myorg",
    "repository_name": "myrepo",
    "pull_request_numbers": [123, 124],
    "metadata": {"source": "api"}
}

# Process the request
result = process_automation_request(input_data)

print(f"Success: {result['success']}")
print(f"Processed PRs: {len(result['processed_prs'])}")
```

### JSON Input

```bash
# Process from JSON input
echo '{
  "repository_owner": "myorg",
  "repository_name": "myrepo", 
  "pull_request_numbers": [123, 124]
}' | python main.py --json
```

## Advanced Features

### Auto-Discovery

Automatically discover pull requests based on criteria:

```python
input_data = {
    "repository_owner": "myorg",
    "repository_name": "myrepo",
    "auto_discover": True,
    "discovery_pattern": "feature"  # Filter PRs with "feature" in title
}
```

### Workflow Hooks

Add custom processing logic:

```python
from workflow import workflow_engine

def my_pre_hook(context, **kwargs):
    print(f"Processing repo: {context.repository_owner}/{context.repository_name}")

def my_post_hook(context, processed_prs=None, **kwargs):
    print(f"Completed processing {len(processed_prs)} PRs")

# Register hooks
workflow_engine.add_hook('pre_process', my_pre_hook)
workflow_engine.add_hook('post_process', my_post_hook)
```

### Batch Processing

Process multiple PRs efficiently:

```python
from pr_handler import PRProcessor

processor = PRProcessor("myorg", "myrepo")
pr_numbers = [123, 124, 125]
results = processor.process_pr_batch(pr_numbers)

for pr_number, pr_info in results.items():
    if pr_info:
        print(f"PR #{pr_number}: {pr_info.title}")
    else:
        print(f"PR #{pr_number}: Failed to process")
```

## Architecture

### Core Components

- **`config.py`**: Configuration management with environment variable support
- **`auth.py`**: GitHub API authorization and authentication
- **`pr_handler.py`**: Pull request processing and data extraction
- **`workflow.py`**: Main automation workflow engine
- **`main.py`**: Command-line interface

### Data Flow

1. **Input Processing**: Parse URLs, numbers, or auto-discover PRs
2. **Authorization**: Validate GitHub token and repository access
3. **Context Creation**: Build workflow context with repository and PR information
4. **Batch Processing**: Process PRs efficiently with configurable batch sizes
5. **Hook Execution**: Run pre/post-processing hooks
6. **Result Generation**: Return structured results with success status and metadata

## Testing

Run the test suite:

```bash
python test_automation.py
```

The tests cover:
- Configuration management
- URL parsing and extraction
- PR information handling
- Workflow context creation
- Integration scenarios

## Error Handling

The system includes comprehensive error handling:

- **Authentication Errors**: Clear messages for token issues
- **Repository Access**: Validation of repository permissions
- **PR Processing**: Graceful handling of individual PR failures
- **Network Issues**: Retry logic and timeout handling

## Security

- **Token Management**: Secure storage in environment variables
- **Access Control**: Repository-level permission validation
- **Input Validation**: Sanitization of URLs and parameters
- **Error Logging**: Secure logging without exposing sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.
