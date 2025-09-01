"""Core interfaces for AI Time Machines components."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    """Standard message format for component communication."""
    id: str
    sender_id: str
    receiver_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = {}


class TimelineEvent(BaseModel):
    """Represents an event in a timeline."""
    id: str
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    source_component: str


class IComponent(ABC):
    """Base interface for all components in the system."""
    
    @property
    @abstractmethod
    def component_id(self) -> str:
        """Unique identifier for this component."""
        pass
    
    @property
    @abstractmethod
    def component_type(self) -> str:
        """Type classification for this component."""
        pass
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the component."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup and shutdown the component."""
        pass
    
    @abstractmethod
    async def handle_message(self, message: Message) -> Optional[Message]:
        """Handle incoming messages."""
        pass


class IAgent(IComponent):
    """Interface for AI agents."""
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a given task and return results."""
        pass
    
    @abstractmethod
    async def learn_from_feedback(self, feedback: Dict[str, Any]) -> None:
        """Learn and adapt from feedback."""
        pass


class ITimeMachine(IComponent):
    """Interface for time machine components."""
    
    @abstractmethod
    async def travel_to_time(self, target_time: datetime) -> bool:
        """Attempt to travel to a specific time."""
        pass
    
    @abstractmethod
    async def get_timeline_events(self, start_time: datetime, end_time: datetime) -> List[TimelineEvent]:
        """Retrieve events from a time range."""
        pass
    
    @abstractmethod
    async def create_timeline_branch(self, branch_point: datetime, branch_id: str) -> bool:
        """Create a new timeline branch."""
        pass


class IEventHandler(ABC):
    """Interface for handling events."""
    
    @abstractmethod
    async def handle_event(self, event: Message) -> None:
        """Handle an incoming event."""
        pass


class IRegistry(ABC):
    """Interface for component registration and discovery."""
    
    @abstractmethod
    async def register_component(self, component: IComponent) -> bool:
        """Register a component."""
        pass
    
    @abstractmethod
    async def unregister_component(self, component_id: str) -> bool:
        """Unregister a component."""
        pass
    
    @abstractmethod
    async def get_component(self, component_id: str) -> Optional[IComponent]:
        """Get a component by ID."""
        pass
    
    @abstractmethod
    async def list_components(self, component_type: Optional[str] = None) -> List[IComponent]:
        """List all components, optionally filtered by type."""
        pass