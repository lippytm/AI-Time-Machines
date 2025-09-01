"""
Example AI Agents for various integrations
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .core import AIAgent, AgentCapability
from .integrations import Web3AIIntegration, RepositoryIntegration, IntegrationResponse


class Web3AIAgent(AIAgent):
    """AI Agent specialized for Web3AI integration"""
    
    def __init__(self, agent_id: str, name: str, capabilities: List[AgentCapability]):
        super().__init__(agent_id, name, capabilities)
        
    async def _execute_capability(self, capability_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Web3AI specific capabilities"""
        
        if capability_name == "deploy_contract":
            return await self._deploy_contract(parameters)
        elif capability_name == "execute_transaction":
            return await self._execute_transaction(parameters)
        elif capability_name == "analyze_blockchain":
            return await self._analyze_blockchain(parameters)
        elif capability_name == "sync_data":
            return await self._sync_data(parameters)
        else:
            raise ValueError(f"Unknown capability: {capability_name}")
            
    async def _deploy_contract(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a smart contract via Web3AI"""
        web3ai = self.integrations.get("web3ai") or self.integrations.get("web3ai_main")
        if not web3ai:
            raise ValueError("Web3AI integration not available")
            
        contract_code = parameters.get("contract_code")
        constructor_args = parameters.get("constructor_args", [])
        
        if not contract_code:
            raise ValueError("contract_code is required")
            
        agent_config = {
            "type": "contract_deployer",
            "contract_code": contract_code,
            "constructor_args": constructor_args,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        response = await web3ai.deploy_ai_agent(agent_config)
        
        return {
            "success": response.success,
            "contract_address": response.data.get("contract_address") if response.success else None,
            "transaction_hash": response.data.get("transaction_hash") if response.success else None,
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _execute_transaction(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a blockchain transaction via Web3AI"""
        web3ai = self.integrations.get("web3ai") or self.integrations.get("web3ai_main")
        if not web3ai:
            raise ValueError("Web3AI integration not available")
            
        contract_name = parameters.get("contract_name")
        method = parameters.get("method")
        method_args = parameters.get("args", [])
        
        if not contract_name or not method:
            raise ValueError("contract_name and method are required")
            
        response = await web3ai.execute_smart_contract(contract_name, method, method_args)
        
        return {
            "success": response.success,
            "result": response.data.get("result") if response.success else None,
            "transaction_hash": response.data.get("transaction_hash") if response.success else None,
            "gas_used": response.data.get("gas_used") if response.success else None,
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _analyze_blockchain(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze blockchain data via Web3AI"""
        web3ai = self.integrations.get("web3ai") or self.integrations.get("web3ai_main")
        if not web3ai:
            raise ValueError("Web3AI integration not available")
            
        analysis_type = parameters.get("type", "general")
        target = parameters.get("target")  # address, transaction, block, etc.
        
        agent_config = {
            "type": "blockchain_analyzer",
            "analysis_type": analysis_type,
            "target": target,
            "agent_id": self.agent_id,
            "parameters": parameters
        }
        
        response = await web3ai.deploy_ai_agent(agent_config)
        
        return {
            "success": response.success,
            "analysis_result": response.data.get("analysis") if response.success else None,
            "insights": response.data.get("insights", []) if response.success else [],
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _sync_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize data with Web3AI"""
        web3ai = self.integrations.get("web3ai") or self.integrations.get("web3ai_main")
        if not web3ai:
            raise ValueError("Web3AI integration not available")
            
        time_machine_id = parameters.get("time_machine_id", "default")
        sync_data = parameters.get("data", {})
        
        response = await web3ai.sync_with_time_machine(time_machine_id, sync_data)
        
        return {
            "success": response.success,
            "sync_status": response.data.get("status") if response.success else None,
            "synced_items": response.data.get("synced_items", 0) if response.success else 0,
            "error": response.error,
            "timestamp": response.timestamp
        }


class RepositoryAgent(AIAgent):
    """AI Agent specialized for repository integration"""
    
    def __init__(self, agent_id: str, name: str, capabilities: List[AgentCapability]):
        super().__init__(agent_id, name, capabilities)
        
    async def _execute_capability(self, capability_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute repository specific capabilities"""
        
        if capability_name == "analyze_code":
            return await self._analyze_code(parameters)
        elif capability_name == "create_pr":
            return await self._create_pr(parameters)
        elif capability_name == "sync_repository":
            return await self._sync_repository(parameters)
        elif capability_name == "deploy_ai_to_repo":
            return await self._deploy_ai_to_repo(parameters)
        else:
            raise ValueError(f"Unknown capability: {capability_name}")
            
    async def _analyze_code(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code in a repository"""
        repo_integration = self.integrations.get("repository") or self.integrations.get("github_main")
        if not repo_integration:
            raise ValueError("Repository integration not available")
            
        repo_path = parameters.get("repository")
        analysis_type = parameters.get("type", "general")
        
        if not repo_path:
            raise ValueError("repository parameter is required")
            
        # Get repository info first
        repo_response = await repo_integration.get_repository_info(repo_path)
        if not repo_response.success:
            return {
                "success": False,
                "error": f"Failed to access repository: {repo_response.error}",
                "timestamp": datetime.now()
            }
            
        # Execute analysis action
        analysis_params = {
            "repository": repo_path,
            "analysis_type": analysis_type,
            "agent_id": self.agent_id,
            **parameters
        }
        
        response = await repo_integration.execute_action("analyze_code", analysis_params)
        
        return {
            "success": response.success,
            "analysis_result": response.data.get("analysis") if response.success else None,
            "file_count": response.data.get("file_count", 0) if response.success else 0,
            "languages": response.data.get("languages", []) if response.success else [],
            "recommendations": response.data.get("recommendations", []) if response.success else [],
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _create_pr(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a pull request"""
        repo_integration = self.integrations.get("repository") or self.integrations.get("github_main")
        if not repo_integration:
            raise ValueError("Repository integration not available")
            
        repo_path = parameters.get("repository")
        title = parameters.get("title")
        description = parameters.get("description")
        source_branch = parameters.get("source_branch")
        target_branch = parameters.get("target_branch", "main")
        
        if not all([repo_path, title, source_branch]):
            raise ValueError("repository, title, and source_branch are required")
            
        pr_params = {
            "repository": repo_path,
            "title": title,
            "description": description,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "agent_id": self.agent_id
        }
        
        response = await repo_integration.execute_action("create_pull_request", pr_params)
        
        return {
            "success": response.success,
            "pr_number": response.data.get("pr_number") if response.success else None,
            "pr_url": response.data.get("pr_url") if response.success else None,
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _sync_repository(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize with a repository"""
        repo_integration = self.integrations.get("repository") or self.integrations.get("github_main")
        if not repo_integration:
            raise ValueError("Repository integration not available")
            
        repo_path = parameters.get("repository")
        sync_type = parameters.get("type", "pull")  # pull, push, bidirectional
        
        if not repo_path:
            raise ValueError("repository parameter is required")
            
        sync_params = {
            "repository": repo_path,
            "sync_type": sync_type,
            "agent_id": self.agent_id,
            **parameters
        }
        
        response = await repo_integration.execute_action("sync_repository", sync_params)
        
        return {
            "success": response.success,
            "sync_status": response.data.get("status") if response.success else None,
            "files_synced": response.data.get("files_synced", 0) if response.success else 0,
            "commits_synced": response.data.get("commits_synced", 0) if response.success else 0,
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    async def _deploy_ai_to_repo(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy AI agent capabilities to a repository"""
        repo_integration = self.integrations.get("repository") or self.integrations.get("github_main")
        if not repo_integration:
            raise ValueError("Repository integration not available")
            
        repo_path = parameters.get("repository")
        agent_config = parameters.get("agent_config", {})
        deployment_type = parameters.get("deployment_type", "github_action")  # github_action, webhook, etc.
        
        if not repo_path:
            raise ValueError("repository parameter is required")
            
        deploy_params = {
            "repository": repo_path,
            "deployment_type": deployment_type,
            "agent_config": {
                "agent_id": self.agent_id,
                "capabilities": list(self.capabilities.keys()),
                "time_machine_id": parameters.get("time_machine_id", "default"),
                **agent_config
            },
            "source_agent_id": self.agent_id
        }
        
        response = await repo_integration.execute_action("deploy_ai_agent", deploy_params)
        
        return {
            "success": response.success,
            "deployment_id": response.data.get("deployment_id") if response.success else None,
            "webhook_url": response.data.get("webhook_url") if response.success else None,
            "action_file": response.data.get("action_file") if response.success else None,
            "error": response.error,
            "timestamp": response.timestamp
        }


def create_default_web3ai_agent(agent_id: str = "web3ai_default", name: str = "Web3AI Agent") -> Web3AIAgent:
    """Create a default Web3AI agent with standard capabilities"""
    capabilities = [
        AgentCapability(
            name="deploy_contract",
            description="Deploy smart contracts to blockchain",
            required_integrations=["web3ai"],
            parameters={
                "contract_code": {"type": "string", "required": True},
                "constructor_args": {"type": "array", "default": []}
            }
        ),
        AgentCapability(
            name="execute_transaction",
            description="Execute smart contract transactions",
            required_integrations=["web3ai"],
            parameters={
                "contract_name": {"type": "string", "required": True},
                "method": {"type": "string", "required": True},
                "args": {"type": "array", "default": []}
            }
        ),
        AgentCapability(
            name="analyze_blockchain",
            description="Analyze blockchain data and transactions",
            required_integrations=["web3ai"],
            parameters={
                "type": {"type": "string", "default": "general"},
                "target": {"type": "string", "required": True}
            }
        ),
        AgentCapability(
            name="sync_data",
            description="Synchronize data with Web3AI",
            required_integrations=["web3ai"],
            parameters={
                "time_machine_id": {"type": "string", "default": "default"},
                "data": {"type": "object", "required": True}
            }
        )
    ]
    
    return Web3AIAgent(agent_id, name, capabilities)


def create_default_repository_agent(agent_id: str = "repo_default", name: str = "Repository Agent") -> RepositoryAgent:
    """Create a default repository agent with standard capabilities"""
    capabilities = [
        AgentCapability(
            name="analyze_code",
            description="Analyze code in repositories",
            required_integrations=["repository"],
            parameters={
                "repository": {"type": "string", "required": True},
                "type": {"type": "string", "default": "general"}
            }
        ),
        AgentCapability(
            name="create_pr",
            description="Create pull requests",
            required_integrations=["repository"],
            parameters={
                "repository": {"type": "string", "required": True},
                "title": {"type": "string", "required": True},
                "source_branch": {"type": "string", "required": True},
                "target_branch": {"type": "string", "default": "main"}
            }
        ),
        AgentCapability(
            name="sync_repository",
            description="Synchronize with repositories",
            required_integrations=["repository"],
            parameters={
                "repository": {"type": "string", "required": True},
                "type": {"type": "string", "default": "pull"}
            }
        ),
        AgentCapability(
            name="deploy_ai_to_repo",
            description="Deploy AI capabilities to repositories",
            required_integrations=["repository"],
            parameters={
                "repository": {"type": "string", "required": True},
                "deployment_type": {"type": "string", "default": "github_action"}
            }
        )
    ]
    
    return RepositoryAgent(agent_id, name, capabilities)