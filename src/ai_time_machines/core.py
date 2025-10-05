"""
Core AI Agent and Time Machine implementations
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from pydantic import BaseModel, Field


class AgentCapability(BaseModel):
    """Represents a capability that an AI Agent can perform"""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    required_integrations: List[str] = Field(default_factory=list)


class AgentTask(BaseModel):
    """Represents a task for an AI Agent to execute"""
    id: str
    capability: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 1
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "pending"  # pending, running, completed, failed


class AIAgent(ABC):
    """
    Abstract base class for AI Agents in the Time Machine ecosystem
    """
    
    def __init__(self, agent_id: str, name: str, capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = {cap.name: cap for cap in capabilities}
        self.integrations: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"ai_time_machines.agent.{agent_id}")
        self._task_queue: List[AgentTask] = []
        
    def add_integration(self, integration_name: str, integration_instance: Any):
        """Add an integration to this agent"""
        self.integrations[integration_name] = integration_instance
        self.logger.info(f"Added integration: {integration_name}")
        
    def has_capability(self, capability_name: str) -> bool:
        """Check if agent has a specific capability"""
        return capability_name in self.capabilities
        
    def get_required_integrations(self, capability_name: str) -> List[str]:
        """Get required integrations for a capability"""
        if capability_name in self.capabilities:
            return self.capabilities[capability_name].required_integrations
        return []
        
    def can_execute(self, capability_name: str) -> bool:
        """Check if agent can execute a capability (has required integrations)"""
        if not self.has_capability(capability_name):
            return False
            
        required = self.get_required_integrations(capability_name)
        return all(integration in self.integrations for integration in required)
        
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task"""
        if not self.can_execute(task.capability):
            raise ValueError(f"Cannot execute capability: {task.capability}")
            
        task.status = "running"
        self.logger.info(f"Executing task {task.id}: {task.capability}")
        
        try:
            result = await self._execute_capability(task.capability, task.parameters)
            task.status = "completed"
            self.logger.info(f"Completed task {task.id}")
            return result
        except Exception as e:
            task.status = "failed"
            self.logger.error(f"Failed task {task.id}: {str(e)}")
            raise
            
    @abstractmethod
    async def _execute_capability(self, capability_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific capability - must be implemented by subclasses"""
        pass


class TimeMachine:
    """
    Core Time Machine class that manages AI Agents and their interactions
    """
    
    def __init__(self, machine_id: str):
        self.machine_id = machine_id
        self.agents: Dict[str, AIAgent] = {}
        self.integrations: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"ai_time_machines.machine.{machine_id}")
        self._event_handlers: Dict[str, List[Callable]] = {}
        
    def register_agent(self, agent: AIAgent):
        """Register an AI Agent with this Time Machine"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.name} ({agent.agent_id})")
        
        # Share integrations with the agent
        for name, integration in self.integrations.items():
            if name in agent.get_all_required_integrations():
                agent.add_integration(name, integration)
                
    def add_integration(self, name: str, integration: Any):
        """Add an integration to this Time Machine"""
        self.integrations[name] = integration
        self.logger.info(f"Added integration: {name}")
        
        # Share with relevant agents
        for agent in self.agents.values():
            if name in agent.get_all_required_integrations():
                agent.add_integration(name, integration)
                
    def get_agents_with_capability(self, capability_name: str) -> List[AIAgent]:
        """Get all agents that have a specific capability"""
        return [agent for agent in self.agents.values() 
                if agent.has_capability(capability_name)]
                
    def get_available_agents_for_capability(self, capability_name: str) -> List[AIAgent]:
        """Get all agents that can currently execute a specific capability"""
        return [agent for agent in self.agents.values() 
                if agent.can_execute(capability_name)]
                
    async def execute_capability(self, capability_name: str, parameters: Dict[str, Any], 
                               preferred_agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute a capability, optionally specifying a preferred agent"""
        
        if preferred_agent_id and preferred_agent_id in self.agents:
            agent = self.agents[preferred_agent_id]
            if agent.can_execute(capability_name):
                task = AgentTask(
                    id=f"task_{datetime.now().timestamp()}",
                    capability=capability_name,
                    parameters=parameters
                )
                return await agent.execute_task(task)
                
        # Find available agents
        available_agents = self.get_available_agents_for_capability(capability_name)
        if not available_agents:
            raise ValueError(f"No agents available for capability: {capability_name}")
            
        # Use first available agent (could implement more sophisticated selection)
        agent = available_agents[0]
        task = AgentTask(
            id=f"task_{datetime.now().timestamp()}",
            capability=capability_name,
            parameters=parameters
        )
        
        return await agent.execute_task(task)
        
    def on_event(self, event_name: str, handler: Callable):
        """Register an event handler"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)
        
    async def emit_event(self, event_name: str, data: Any):
        """Emit an event to all registered handlers"""
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {str(e)}")


# Extension method for AIAgent
def get_all_required_integrations(self) -> List[str]:
    """Get all required integrations across all capabilities"""
    integrations = set()
    for capability in self.capabilities.values():
        integrations.update(capability.required_integrations)
    return list(integrations)

AIAgent.get_all_required_integrations = get_all_required_integrations