"""Component registry for discovery and management."""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Any
from datetime import datetime

from ai_time_machines.core.interfaces import IComponent, IRegistry, Message


class ComponentRegistry(IRegistry):
    """Registry for component registration and discovery."""
    
    _instance: Optional['ComponentRegistry'] = None
    _lock = asyncio.Lock()
    
    def __init__(self):
        self._components: Dict[str, IComponent] = {}
        self._components_by_type: Dict[str, Set[str]] = {}
        self._component_metadata: Dict[str, Dict[str, Any]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @classmethod
    async def get_instance(cls) -> 'ComponentRegistry':
        """Get the singleton instance of the component registry."""
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    async def register_component(self, component: IComponent) -> bool:
        """Register a component."""
        try:
            component_id = component.component_id
            component_type = component.component_type
            
            if component_id in self._components:
                self._logger.warning(f"Component {component_id} already registered")
                return False
            
            # Register the component
            self._components[component_id] = component
            
            # Add to type index
            if component_type not in self._components_by_type:
                self._components_by_type[component_type] = set()
            self._components_by_type[component_type].add(component_id)
            
            # Store metadata
            self._component_metadata[component_id] = {
                "registered_at": datetime.now(),
                "type": component_type,
                "status": "registered"
            }
            
            self._logger.info(f"Registered component {component_id} of type {component_type}")
            
            # Subscribe component to event bus if it's an event handler
            from ai_time_machines.communication.event_bus import EventBus
            event_bus = await EventBus.get_instance()
            await event_bus.subscribe(component)
            
            return True
            
        except Exception as e:
            self._logger.error(f"Error registering component: {e}")
            return False
    
    async def unregister_component(self, component_id: str) -> bool:
        """Unregister a component."""
        try:
            if component_id not in self._components:
                self._logger.warning(f"Component {component_id} not found")
                return False
            
            component = self._components[component_id]
            component_type = component.component_type
            
            # Unsubscribe from event bus
            from ai_time_machines.communication.event_bus import EventBus
            event_bus = await EventBus.get_instance()
            await event_bus.unsubscribe(component)
            
            # Shutdown component if it's running
            if hasattr(component, 'is_running') and component.is_running:
                await component.shutdown()
            
            # Remove from registry
            del self._components[component_id]
            
            # Remove from type index
            if component_type in self._components_by_type:
                self._components_by_type[component_type].discard(component_id)
                if not self._components_by_type[component_type]:
                    del self._components_by_type[component_type]
            
            # Remove metadata
            if component_id in self._component_metadata:
                del self._component_metadata[component_id]
            
            self._logger.info(f"Unregistered component {component_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error unregistering component {component_id}: {e}")
            return False
    
    async def get_component(self, component_id: str) -> Optional[IComponent]:
        """Get a component by ID."""
        return self._components.get(component_id)
    
    async def list_components(self, component_type: Optional[str] = None) -> List[IComponent]:
        """List all components, optionally filtered by type."""
        if component_type is None:
            return list(self._components.values())
        
        if component_type not in self._components_by_type:
            return []
        
        component_ids = self._components_by_type[component_type]
        return [self._components[cid] for cid in component_ids if cid in self._components]
    
    async def get_component_metadata(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a component."""
        return self._component_metadata.get(component_id)
    
    async def list_component_types(self) -> List[str]:
        """List all registered component types."""
        return list(self._components_by_type.keys())
    
    async def get_components_count(self) -> int:
        """Get total number of registered components."""
        return len(self._components)
    
    async def find_components_by_name(self, name_pattern: str) -> List[IComponent]:
        """Find components whose names match a pattern."""
        matching_components = []
        for component in self._components.values():
            if hasattr(component, 'agent_name') and name_pattern.lower() in component.agent_name.lower():
                matching_components.append(component)
            elif hasattr(component, 'machine_name') and name_pattern.lower() in component.machine_name.lower():
                matching_components.append(component)
        return matching_components
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all registered components."""
        health_status = {
            "total_components": len(self._components),
            "components_by_type": {t: len(ids) for t, ids in self._components_by_type.items()},
            "unhealthy_components": []
        }
        
        for component_id, component in self._components.items():
            try:
                # Check if component is still responsive
                if hasattr(component, 'is_running') and not component.is_running:
                    health_status["unhealthy_components"].append({
                        "component_id": component_id,
                        "issue": "not_running"
                    })
            except Exception as e:
                health_status["unhealthy_components"].append({
                    "component_id": component_id,
                    "issue": str(e)
                })
        
        return health_status


class ComponentDiscovery:
    """Helper class for component discovery and interaction."""
    
    def __init__(self, registry: Optional[ComponentRegistry] = None):
        self.registry = registry
        self._logger = logging.getLogger(self.__class__.__name__)
    
    async def _get_registry(self) -> ComponentRegistry:
        """Get the registry instance."""
        if self.registry is None:
            self.registry = await ComponentRegistry.get_instance()
        return self.registry
    
    async def find_agents(self, agent_type: Optional[str] = None) -> List[IComponent]:
        """Find all agent components."""
        registry = await self._get_registry()
        agents = await registry.list_components("agent")
        
        if agent_type is None:
            return agents
        
        # Filter by specific agent type if provided
        return [agent for agent in agents if getattr(agent, 'agent_name', '').lower() == agent_type.lower()]
    
    async def find_time_machines(self, machine_type: Optional[str] = None) -> List[IComponent]:
        """Find all time machine components."""
        registry = await self._get_registry()
        machines = await registry.list_components("time_machine")
        
        if machine_type is None:
            return machines
        
        # Filter by specific machine type if provided
        return [machine for machine in machines if getattr(machine, 'machine_name', '').lower() == machine_type.lower()]
    
    async def send_task_to_best_agent(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a task to the most suitable agent."""
        agents = await self.find_agents()
        
        if not agents:
            self._logger.warning("No agents available to process task")
            return None
        
        # Simple selection: use the first available agent
        # In a real implementation, this could use more sophisticated selection logic
        selected_agent = agents[0]
        
        try:
            if hasattr(selected_agent, 'process_task'):
                result = await selected_agent.process_task(task)
                self._logger.info(f"Task processed by agent {selected_agent.component_id}")
                return result
        except Exception as e:
            self._logger.error(f"Error processing task with agent {selected_agent.component_id}: {e}")
        
        return None
    
    async def coordinate_time_travel(self, target_time: datetime) -> Dict[str, bool]:
        """Coordinate time travel across all time machines."""
        machines = await self.find_time_machines()
        results = {}
        
        for machine in machines:
            try:
                if hasattr(machine, 'travel_to_time'):
                    success = await machine.travel_to_time(target_time)
                    results[machine.component_id] = success
                    self._logger.info(f"Time travel to {target_time} for machine {machine.component_id}: {success}")
            except Exception as e:
                self._logger.error(f"Error with time travel for machine {machine.component_id}: {e}")
                results[machine.component_id] = False
        
        return results