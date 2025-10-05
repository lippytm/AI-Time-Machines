"""
Basic tests for AI-Time-Machines core functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from ai_time_machines.core import TimeMachine, AIAgent, AgentCapability, AgentTask
from ai_time_machines.integrations import IntegrationConfig, Web3AIIntegration, RepositoryIntegration
from ai_time_machines.config import Config
from ai_time_machines.agents import Web3AIAgent, RepositoryAgent


class TestAIAgent(AIAgent):
    """Test implementation of AIAgent"""
    
    def __init__(self, agent_id: str, name: str, capabilities: list):
        super().__init__(agent_id, name, capabilities)
    
    async def _execute_capability(self, capability_name: str, parameters: dict):
        if capability_name == "test_capability":
            return {"result": "test_success", "parameters": parameters}
        else:
            raise ValueError(f"Unknown capability: {capability_name}")


@pytest.fixture
def test_capability():
    return AgentCapability(
        name="test_capability",
        description="Test capability",
        required_integrations=["test_integration"]
    )


@pytest.fixture
def test_agent(test_capability):
    return TestAIAgent("test_agent", "Test Agent", [test_capability])


@pytest.fixture
def time_machine():
    return TimeMachine("test_machine")


@pytest.fixture
def mock_integration():
    integration = Mock()
    integration.connect = AsyncMock(return_value=True)
    integration.health_check = AsyncMock(return_value=True)
    integration.disconnect = AsyncMock()
    return integration


class TestTimeMachine:
    
    def test_creation(self):
        machine = TimeMachine("test")
        assert machine.machine_id == "test"
        assert len(machine.agents) == 0
        assert len(machine.integrations) == 0
    
    def test_register_agent(self, time_machine, test_agent):
        time_machine.register_agent(test_agent)
        assert test_agent.agent_id in time_machine.agents
        assert time_machine.agents[test_agent.agent_id] == test_agent
    
    def test_add_integration(self, time_machine, mock_integration):
        time_machine.add_integration("test_integration", mock_integration)
        assert "test_integration" in time_machine.integrations
        assert time_machine.integrations["test_integration"] == mock_integration
    
    def test_get_agents_with_capability(self, time_machine, test_agent):
        time_machine.register_agent(test_agent)
        agents = time_machine.get_agents_with_capability("test_capability")
        assert len(agents) == 1
        assert agents[0] == test_agent
        
        agents = time_machine.get_agents_with_capability("nonexistent")
        assert len(agents) == 0
    
    @pytest.mark.asyncio
    async def test_execute_capability(self, time_machine, test_agent, mock_integration):
        # Set up machine with agent and integration
        time_machine.add_integration("test_integration", mock_integration)
        time_machine.register_agent(test_agent)
        
        # Execute capability
        result = await time_machine.execute_capability("test_capability", {"param": "value"})
        
        assert result["result"] == "test_success"
        assert result["parameters"]["param"] == "value"


class TestAIAgent:
    
    def test_creation(self, test_capability):
        agent = TestAIAgent("test", "Test", [test_capability])
        assert agent.agent_id == "test"
        assert agent.name == "Test"
        assert "test_capability" in agent.capabilities
    
    def test_has_capability(self, test_agent):
        assert test_agent.has_capability("test_capability")
        assert not test_agent.has_capability("nonexistent")
    
    def test_can_execute_without_integration(self, test_agent):
        assert not test_agent.can_execute("test_capability")
    
    def test_can_execute_with_integration(self, test_agent, mock_integration):
        test_agent.add_integration("test_integration", mock_integration)
        assert test_agent.can_execute("test_capability")
    
    @pytest.mark.asyncio
    async def test_execute_task(self, test_agent, mock_integration):
        test_agent.add_integration("test_integration", mock_integration)
        
        task = AgentTask(
            id="test_task",
            capability="test_capability",
            parameters={"test": "value"}
        )
        
        result = await test_agent.execute_task(task)
        assert result["result"] == "test_success"
        assert task.status == "completed"


class TestConfig:
    
    def test_default_config(self):
        config = Config("nonexistent_file.json")
        assert "default" in config.time_machines
        assert config.logging_config.level == "INFO"
    
    def test_create_web3ai_integration(self):
        config = Config("nonexistent_file.json")
        integration_config = config.create_web3ai_integration(
            "test_web3ai",
            web3ai_url="http://test.com"
        )
        
        assert integration_config.name == "test_web3ai"
        assert integration_config.config["web3ai_url"] == "http://test.com"
        assert "test_web3ai" in config.integrations
    
    def test_create_repository_integration(self):
        config = Config("nonexistent_file.json")
        integration_config = config.create_repository_integration(
            "test_repo",
            "github",
            base_url="https://api.github.com"
        )
        
        assert integration_config.name == "test_repo"
        assert integration_config.config["base_url"] == "https://api.github.com"
        assert integration_config.config["type"] == "github"


class TestIntegrations:
    
    def test_integration_config_creation(self):
        config = IntegrationConfig(
            name="test",
            enabled=True,
            timeout=30,
            config={"url": "http://test.com"}
        )
        
        assert config.name == "test"
        assert config.enabled
        assert config.timeout == 30
        assert config.config["url"] == "http://test.com"
    
    @pytest.mark.asyncio
    async def test_web3ai_integration_creation(self):
        config = IntegrationConfig(
            name="web3ai_test",
            config={
                "web3ai_url": "http://localhost:8080",
                "blockchain_rpc": "http://localhost:8545"
            }
        )
        
        integration = Web3AIIntegration(config)
        assert integration.config.name == "web3ai_test"
        assert integration.web3ai_url == "http://localhost:8080"
        assert integration.blockchain_rpc == "http://localhost:8545"
    
    @pytest.mark.asyncio
    async def test_repository_integration_creation(self):
        config = IntegrationConfig(
            name="repo_test",
            config={
                "base_url": "https://api.github.com",
                "type": "github"
            }
        )
        
        integration = RepositoryIntegration(config)
        assert integration.config.name == "repo_test"
        assert integration.base_url == "https://api.github.com"
        assert integration.repository_type == "github"


class TestAgents:
    
    def test_web3ai_agent_creation(self):
        from ai_time_machines.agents import create_default_web3ai_agent
        
        agent = create_default_web3ai_agent("test_web3ai", "Test Web3AI Agent")
        assert agent.agent_id == "test_web3ai"
        assert agent.name == "Test Web3AI Agent"
        assert "deploy_contract" in agent.capabilities
        assert "execute_transaction" in agent.capabilities
    
    def test_repository_agent_creation(self):
        from ai_time_machines.agents import create_default_repository_agent
        
        agent = create_default_repository_agent("test_repo", "Test Repo Agent")
        assert agent.agent_id == "test_repo"
        assert agent.name == "Test Repo Agent"
        assert "analyze_code" in agent.capabilities
        assert "create_pr" in agent.capabilities


if __name__ == "__main__":
    pytest.main([__file__, "-v"])