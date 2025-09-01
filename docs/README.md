# AI-Time-Machines Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [Architecture](#architecture)
3. [Integrations](#integrations)
4. [Agent Development](#agent-development)
5. [Configuration](#configuration)
6. [API Reference](#api-reference)

## Getting Started

### Prerequisites

- Python 3.8+
- Access to Web3AI instance (optional)
- Repository API access (GitHub/GitLab tokens)

### Installation

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Install dependencies
pip install -e .

# Initialize configuration
ai-time-machines init-config
```

### Basic Usage

1. **Configure Integrations**: Edit `ai_time_machines.json` to add your API keys
2. **Deploy Agents**: Use CLI or Python API to deploy agents
3. **Execute Capabilities**: Run AI capabilities across integrated systems

## Architecture

### Time Machine Pattern

The Time Machine acts as a temporal coordination layer that:
- Manages agent lifecycles
- Routes capabilities to appropriate agents
- Handles cross-system synchronization
- Provides event-driven coordination

### Agent Framework

```python
from ai_time_machines import AIAgent, AgentCapability

class CustomAgent(AIAgent):
    async def _execute_capability(self, capability_name: str, parameters: dict):
        # Implement your capability logic
        pass
```

### Integration Pattern

```python
from ai_time_machines.integrations import BaseIntegration

class CustomIntegration(BaseIntegration):
    async def connect(self) -> bool:
        # Implement connection logic
        pass
```

## Integrations

### Web3AI Integration

Enables AI agents to interact with blockchain systems and Web3AI instances:

```python
# Deploy a smart contract
result = await machine.execute_capability("deploy_contract", {
    "contract_code": contract_bytecode,
    "constructor_args": [param1, param2]
})

# Execute contract method
result = await machine.execute_capability("execute_transaction", {
    "contract_name": "MyContract",
    "method": "transfer",
    "args": [recipient_address, amount]
})
```

### Repository Integration

Connects AI agents with code repositories:

```python
# Analyze repository code
result = await machine.execute_capability("analyze_code", {
    "repository": "owner/repo",
    "type": "security"
})

# Create pull request
result = await machine.execute_capability("create_pr", {
    "repository": "owner/repo",
    "title": "AI-generated improvements",
    "source_branch": "ai-improvements",
    "description": "Automated code improvements"
})
```

## Agent Development

### Creating Custom Agents

```python
from ai_time_machines import AIAgent, AgentCapability

class MyCustomAgent(AIAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="my_capability",
                description="Does something useful",
                required_integrations=["my_integration"]
            )
        ]
        super().__init__("my_agent", "My Agent", capabilities)
    
    async def _execute_capability(self, capability_name: str, parameters: dict):
        if capability_name == "my_capability":
            return await self._do_something(parameters)
    
    async def _do_something(self, parameters: dict):
        # Your implementation here
        return {"result": "success"}
```

### Agent Best Practices

1. **Capability Design**: Make capabilities atomic and reusable
2. **Error Handling**: Always handle integration failures gracefully
3. **Logging**: Use the built-in logger for debugging
4. **Parameters**: Validate input parameters before processing

## Configuration

### Environment Variables

```bash
# Web3AI Configuration
export WEB3AI_URL=http://your-web3ai-instance:8080
export BLOCKCHAIN_RPC=http://your-blockchain-rpc:8545
export PRIVATE_KEY=your_private_key

# Repository Configuration
export GITHUB_URL=https://api.github.com
export GITHUB_API_KEY=your_github_token
```

### Configuration File Structure

```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  },
  "time_machines": {
    "production": {
      "machine_id": "production",
      "name": "Production Time Machine",
      "max_agents": 50
    }
  },
  "integrations": {
    "web3ai_prod": {
      "enabled": true,
      "config": {
        "web3ai_url": "${WEB3AI_URL}",
        "blockchain_rpc": "${BLOCKCHAIN_RPC}"
      }
    }
  }
}
```

## API Reference

### Core Classes

#### TimeMachine

```python
class TimeMachine:
    def __init__(self, machine_id: str)
    def register_agent(self, agent: AIAgent)
    def add_integration(self, name: str, integration: BaseIntegration)
    async def execute_capability(self, capability_name: str, parameters: dict)
```

#### AIAgent

```python
class AIAgent:
    def __init__(self, agent_id: str, name: str, capabilities: List[AgentCapability])
    def add_integration(self, name: str, integration: BaseIntegration)
    async def execute_task(self, task: AgentTask)
```

#### AgentCapability

```python
class AgentCapability:
    name: str
    description: str
    parameters: Dict[str, Any]
    required_integrations: List[str]
```

### Integration Classes

#### Web3AIIntegration

```python
async def deploy_ai_agent(self, agent_config: dict) -> IntegrationResponse
async def execute_smart_contract(self, contract_name: str, method: str, parameters: list)
async def sync_with_time_machine(self, time_machine_id: str, data: dict)
```

#### RepositoryIntegration

```python
async def get_repository_info(self, repo_path: str) -> IntegrationResponse
async def execute_action(self, action: str, parameters: dict) -> IntegrationResponse
```

### CLI Reference

```bash
# Initialize configuration
ai-time-machines init-config

# Check system status
ai-time-machines status [--machine MACHINE_ID]

# Deploy an agent
ai-time-machines deploy-agent TYPE AGENT_ID NAME [--machine MACHINE_ID]

# Execute a capability
ai-time-machines execute CAPABILITY [--parameters JSON] [--agent-id AGENT_ID]

# List available capabilities
ai-time-machines list-capabilities [--machine MACHINE_ID]
```