"""
Integration interfaces for connecting with external systems
"""

import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field


class IntegrationConfig(BaseModel):
    """Base configuration for integrations"""
    name: str
    enabled: bool = True
    timeout: int = 30
    retry_attempts: int = 3
    config: Dict[str, Any] = Field(default_factory=dict)


class IntegrationResponse(BaseModel):
    """Response from an integration"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    integration_name: str


class BaseIntegration(ABC):
    """Base class for all integrations"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.logger = logging.getLogger(f"ai_time_machines.integration.{config.name}")
        self._session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._session:
            await self._session.close()
            self._session = None
            
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the external system"""
        pass
        
    @abstractmethod
    async def disconnect(self):
        """Close connection to the external system"""
        pass
        
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the integration is healthy"""
        pass


class RepositoryIntegration(BaseIntegration):
    """Integration for connecting with other repositories"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = config.config.get("base_url")
        self.api_key = config.config.get("api_key")
        self.repository_type = config.config.get("type", "generic")  # github, gitlab, etc.
        
    async def connect(self) -> bool:
        """Connect to repository API"""
        try:
            if not self.base_url:
                raise ValueError("base_url is required for repository integration")
                
            async with self:
                response = await self.health_check()
                self.logger.info(f"Connected to repository: {self.base_url}")
                return response
        except Exception as e:
            self.logger.error(f"Failed to connect to repository: {str(e)}")
            return False
            
    async def disconnect(self):
        """Disconnect from repository"""
        if self._session:
            await self._session.close()
            self._session = None
            
    async def health_check(self) -> bool:
        """Check repository health"""
        try:
            if not self._session:
                return False
                
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            async with self._session.get(f"{self.base_url}/health", headers=headers) as response:
                return response.status == 200
        except:
            return False
            
    async def get_repository_info(self, repo_path: str) -> IntegrationResponse:
        """Get information about a repository"""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            async with self._session.get(f"{self.base_url}/repos/{repo_path}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )
            
    async def execute_action(self, action: str, parameters: Dict[str, Any]) -> IntegrationResponse:
        """Execute an action on the repository"""
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            payload = {
                "action": action,
                "parameters": parameters,
                "timestamp": datetime.now().isoformat()
            }
            
            async with self._session.post(f"{self.base_url}/actions", 
                                        json=payload, headers=headers) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )


class Web3AIIntegration(BaseIntegration):
    """Specialized integration for Web3AI repositories"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.web3ai_url = config.config.get("web3ai_url")
        self.blockchain_rpc = config.config.get("blockchain_rpc")
        self.contract_addresses = config.config.get("contract_addresses", {})
        self.private_key = config.config.get("private_key")
        
    async def connect(self) -> bool:
        """Connect to Web3AI system"""
        try:
            if not self.web3ai_url:
                raise ValueError("web3ai_url is required for Web3AI integration")
                
            async with self:
                # Check Web3AI API health
                web3ai_health = await self._check_web3ai_health()
                
                # Check blockchain connection if configured
                blockchain_health = True
                if self.blockchain_rpc:
                    blockchain_health = await self._check_blockchain_health()
                    
                success = web3ai_health and blockchain_health
                if success:
                    self.logger.info("Connected to Web3AI system")
                return success
                
        except Exception as e:
            self.logger.error(f"Failed to connect to Web3AI: {str(e)}")
            return False
            
    async def disconnect(self):
        """Disconnect from Web3AI"""
        if self._session:
            await self._session.close()
            self._session = None
            
    async def health_check(self) -> bool:
        """Check Web3AI integration health"""
        web3ai_health = await self._check_web3ai_health()
        blockchain_health = True
        
        if self.blockchain_rpc:
            blockchain_health = await self._check_blockchain_health()
            
        return web3ai_health and blockchain_health
        
    async def _check_web3ai_health(self) -> bool:
        """Check Web3AI API health"""
        try:
            if not self._session:
                return False
                
            async with self._session.get(f"{self.web3ai_url}/health") as response:
                return response.status == 200
        except:
            return False
            
    async def _check_blockchain_health(self) -> bool:
        """Check blockchain RPC health"""
        try:
            if not self._session:
                return False
                
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }
            
            async with self._session.post(self.blockchain_rpc, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return "result" in data
                return False
        except:
            return False
            
    async def deploy_ai_agent(self, agent_config: Dict[str, Any]) -> IntegrationResponse:
        """Deploy an AI agent to Web3AI"""
        try:
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "agent_config": agent_config,
                "timestamp": datetime.now().isoformat(),
                "integration_source": "ai_time_machines"
            }
            
            async with self._session.post(f"{self.web3ai_url}/agents/deploy", 
                                        json=payload, headers=headers) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )
            
    async def execute_smart_contract(self, contract_name: str, method: str, 
                                   parameters: List[Any]) -> IntegrationResponse:
        """Execute a smart contract method"""
        try:
            if contract_name not in self.contract_addresses:
                return IntegrationResponse(
                    success=False,
                    error=f"Contract {contract_name} not configured",
                    integration_name=self.config.name
                )
                
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "contract_address": self.contract_addresses[contract_name],
                "method": method,
                "parameters": parameters,
                "timestamp": datetime.now().isoformat()
            }
            
            async with self._session.post(f"{self.web3ai_url}/contracts/execute", 
                                        json=payload, headers=headers) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )
            
    async def get_agent_status(self, agent_id: str) -> IntegrationResponse:
        """Get status of a deployed agent"""
        try:
            async with self._session.get(f"{self.web3ai_url}/agents/{agent_id}/status") as response:
                if response.status == 200:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )
            
    async def sync_with_time_machine(self, time_machine_id: str, data: Dict[str, Any]) -> IntegrationResponse:
        """Synchronize data with AI-Time-Machines"""
        try:
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "time_machine_id": time_machine_id,
                "sync_data": data,
                "timestamp": datetime.now().isoformat()
            }
            
            async with self._session.post(f"{self.web3ai_url}/sync/time_machine", 
                                        json=payload, headers=headers) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return IntegrationResponse(
                        success=True,
                        data=data,
                        integration_name=self.config.name
                    )
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"HTTP {response.status}",
                        integration_name=self.config.name
                    )
        except Exception as e:
            return IntegrationResponse(
                success=False,
                error=str(e),
                integration_name=self.config.name
            )