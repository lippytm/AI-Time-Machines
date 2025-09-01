# AI-Time-Machines

Adding AI Agents to everything with Time Machines - A framework for integrating AI capabilities across repositories and Web3 applications.

## Overview

AI-Time-Machines provides a unified framework for deploying and managing AI agents that can seamlessly integrate with various systems, particularly Web3AI and repository management platforms. The system enables AI capabilities to be shared across different repositories and blockchain applications through a Time Machine architecture.

## Key Features

- **Universal AI Agent Framework**: Deploy AI agents with configurable capabilities
- **Web3AI Integration**: Direct integration with Web3AI systems for blockchain and smart contract interactions
- **Repository Integration**: Connect with GitHub, GitLab, and other repository platforms
- **Time Machine Architecture**: Central coordination of multiple AI agents
- **Seamless Interoperability**: Enable AI agents to work across different platforms
- **Configuration Management**: Flexible configuration system for different environments

## Quick Start

### Installation

```bash
pip install -e .
```

### Initialize Configuration

```bash
ai-time-machines init-config
```

This creates a configuration file with sample integrations. Edit `ai_time_machines.json` to add your API keys and URLs.

### Deploy Your First Agent

```bash
# Deploy a Web3AI agent
ai-time-machines deploy-agent web3ai my_web3_agent "Web3 AI Agent"

# Deploy a repository agent
ai-time-machines deploy-agent repository my_repo_agent "Repository Agent"
```

### Check Status

```bash
ai-time-machines status
```

## Integration Examples

### Web3AI Integration

```python
from ai_time_machines import TimeMachine, Config
from ai_time_machines.agents import create_default_web3ai_agent

# Load configuration
config = Config()
config.create_web3ai_integration(
    "web3ai_main",
    web3ai_url="http://your-web3ai-instance:8080",
    blockchain_rpc="http://your-blockchain-rpc:8545"
)

# Create Time Machine
machine = TimeMachine("production")

# Deploy Web3AI agent
agent = create_default_web3ai_agent()
machine.register_agent(agent)

# Execute Web3 capabilities
result = await machine.execute_capability("deploy_contract", {
    "contract_code": "your_smart_contract_code",
    "constructor_args": []
})
```

### Repository Integration

```python
from ai_time_machines.agents import create_default_repository_agent

# Create repository integration
config.create_repository_integration(
    "github_main",
    "github",
    base_url="https://api.github.com",
    api_key="your_github_token"
)

# Deploy repository agent
repo_agent = create_default_repository_agent()
machine.register_agent(repo_agent)

# Analyze code in a repository
result = await machine.execute_capability("analyze_code", {
    "repository": "owner/repo-name",
    "type": "security"
})
```

## Architecture

### Time Machine

The Time Machine is the central coordinator that manages multiple AI agents and their integrations. It provides:

- Agent registration and lifecycle management
- Integration management and sharing
- Capability routing and execution
- Event handling and coordination

### AI Agents

AI Agents are specialized components with specific capabilities:

- **Web3AIAgent**: Handles blockchain interactions, smart contract deployment, and Web3AI integration
- **RepositoryAgent**: Manages code analysis, pull requests, and repository operations

### Integrations

Integrations provide connectivity to external systems:

- **Web3AIIntegration**: Connects to Web3AI instances and blockchain networks
- **RepositoryIntegration**: Connects to GitHub, GitLab, and other repository platforms

## Configuration

Configuration is managed through JSON files and environment variables:

```json
{
  "time_machines": {
    "default": {
      "machine_id": "default",
      "name": "Default Time Machine",
      "enabled": true,
      "max_agents": 100
    }
  },
  "integrations": {
    "web3ai_main": {
      "enabled": true,
      "timeout": 30,
      "config": {
        "web3ai_url": "http://localhost:8080",
        "blockchain_rpc": "http://localhost:8545",
        "contract_addresses": {}
      }
    }
  }
}
```

## API Reference

### Core Classes

- `TimeMachine`: Central coordination system
- `AIAgent`: Base class for AI agents
- `AgentCapability`: Defines what an agent can do
- `BaseIntegration`: Base class for system integrations

### CLI Commands

- `ai-time-machines status`: Show system status
- `ai-time-machines deploy-agent`: Deploy a new agent
- `ai-time-machines execute`: Execute a capability
- `ai-time-machines list-capabilities`: List available capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

GPL v3 - See LICENSE file for details 
