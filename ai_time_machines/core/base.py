"""Base classes for AI Time Machines components."""

import asyncio
import logging
from typing import Dict, Any, Optional, Set
from datetime import datetime
import uuid

from ai_time_machines.core.interfaces import (
    IComponent, IEventHandler, Message, IAgent, ITimeMachine
)


class Component(IComponent, IEventHandler):
    """Base implementation for all components."""
    
    def __init__(self, component_id: Optional[str] = None, component_type: str = "component"):
        self._component_id = component_id or str(uuid.uuid4())
        self._component_type = component_type
        self._initialized = False
        self._running = False
        self._logger = logging.getLogger(f"{self.__class__.__name__}[{self._component_id}]")
        self._event_handlers: Dict[str, Set[callable]] = {}
        
    @property
    def component_id(self) -> str:
        return self._component_id
    
    @property
    def component_type(self) -> str:
        return self._component_type
    
    @property
    def is_initialized(self) -> bool:
        return self._initialized
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    async def initialize(self) -> None:
        """Initialize the component."""
        if self._initialized:
            return
        
        self._logger.info(f"Initializing component {self.component_id}")
        await self._on_initialize()
        self._initialized = True
        self._running = True
        
    async def shutdown(self) -> None:
        """Shutdown the component."""
        if not self._initialized:
            return
            
        self._logger.info(f"Shutting down component {self.component_id}")
        self._running = False
        await self._on_shutdown()
        self._initialized = False
    
    async def handle_message(self, message: Message) -> Optional[Message]:
        """Handle incoming messages."""
        self._logger.debug(f"Handling message {message.id} of type {message.event_type}")
        
        # Call registered event handlers
        if message.event_type in self._event_handlers:
            for handler in self._event_handlers[message.event_type]:
                try:
                    await handler(message)
                except Exception as e:
                    self._logger.error(f"Error in event handler: {e}")
        
        return await self._on_message(message)
    
    async def handle_event(self, event: Message) -> None:
        """Handle an incoming event."""
        await self.handle_message(event)
    
    def register_event_handler(self, event_type: str, handler: callable) -> None:
        """Register an event handler for a specific event type."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = set()
        self._event_handlers[event_type].add(handler)
    
    def unregister_event_handler(self, event_type: str, handler: callable) -> None:
        """Unregister an event handler."""
        if event_type in self._event_handlers:
            self._event_handlers[event_type].discard(handler)
    
    async def send_message(self, receiver_id: str, event_type: str, payload: Dict[str, Any], 
                          metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Send a message to another component."""
        from ai_time_machines.communication.event_bus import EventBus
        
        message = Message(
            id=str(uuid.uuid4()),
            sender_id=self.component_id,
            receiver_id=receiver_id,
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Get the global event bus and send the message
        event_bus = await EventBus.get_instance()
        await event_bus.publish(message)
        return message
    
    async def broadcast_event(self, event_type: str, payload: Dict[str, Any],
                             metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Broadcast an event to all listening components."""
        from ai_time_machines.communication.event_bus import EventBus
        
        message = Message(
            id=str(uuid.uuid4()),
            sender_id=self.component_id,
            receiver_id=None,  # Broadcast
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        event_bus = await EventBus.get_instance()
        await event_bus.publish(message)
        return message
    
    # Template methods for subclasses to override
    async def _on_initialize(self) -> None:
        """Called during initialization. Override in subclasses."""
        pass
    
    async def _on_shutdown(self) -> None:
        """Called during shutdown. Override in subclasses."""
        pass
    
    async def _on_message(self, message: Message) -> Optional[Message]:
        """Called when a message is received. Override in subclasses."""
        return None


class BaseAgent(Component, IAgent):
    """Base implementation for AI agents."""
    
    def __init__(self, agent_id: Optional[str] = None, agent_name: str = "BaseAgent"):
        super().__init__(component_id=agent_id, component_type="agent")
        self.agent_name = agent_name
        self._knowledge_base: Dict[str, Any] = {}
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a given task and return results."""
        self._logger.info(f"Processing task: {task.get('type', 'unknown')}")
        return await self._process_task_impl(task)
    
    async def learn_from_feedback(self, feedback: Dict[str, Any]) -> None:
        """Learn and adapt from feedback."""
        self._logger.info(f"Learning from feedback: {feedback.get('type', 'unknown')}")
        await self._learn_from_feedback_impl(feedback)
    
    async def _process_task_impl(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Override this method to implement task processing."""
        return {"status": "completed", "result": "Task processed by base agent"}
    
    async def _learn_from_feedback_impl(self, feedback: Dict[str, Any]) -> None:
        """Override this method to implement learning."""
        pass
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "agent_name": self.agent_name,
            "component_id": self.component_id,
            "knowledge_base_size": len(self._knowledge_base),
            "is_running": self.is_running
        }


class BaseTimeMachine(Component, ITimeMachine):
    """Base implementation for time machines."""
    
    def __init__(self, machine_id: Optional[str] = None, machine_name: str = "BaseTimeMachine"):
        super().__init__(component_id=machine_id, component_type="time_machine")
        self.machine_name = machine_name
        self._current_time = datetime.now()
        self._timeline_events: Dict[str, Any] = {}
        
    async def travel_to_time(self, target_time: datetime) -> bool:
        """Attempt to travel to a specific time."""
        self._logger.info(f"Traveling to time: {target_time}")
        return await self._travel_to_time_impl(target_time)
    
    async def get_timeline_events(self, start_time: datetime, end_time: datetime):
        """Retrieve events from a time range."""
        return await self._get_timeline_events_impl(start_time, end_time)
    
    async def create_timeline_branch(self, branch_point: datetime, branch_id: str) -> bool:
        """Create a new timeline branch."""
        self._logger.info(f"Creating timeline branch '{branch_id}' at {branch_point}")
        return await self._create_timeline_branch_impl(branch_point, branch_id)
    
    async def _travel_to_time_impl(self, target_time: datetime) -> bool:
        """Override this method to implement time travel."""
        self._current_time = target_time
        return True
    
    async def _get_timeline_events_impl(self, start_time: datetime, end_time: datetime):
        """Override this method to implement event retrieval."""
        return []
    
    async def _create_timeline_branch_impl(self, branch_point: datetime, branch_id: str) -> bool:
        """Override this method to implement timeline branching."""
        return True