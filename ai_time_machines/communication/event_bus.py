"""Event bus for component communication."""

import asyncio
import logging
from typing import Dict, Set, Optional, Callable, Any
from collections import defaultdict

from ai_time_machines.core.interfaces import Message, IEventHandler


class EventBus:
    """Central event bus for component communication."""
    
    _instance: Optional['EventBus'] = None
    _lock = asyncio.Lock()
    
    def __init__(self):
        self._subscribers: Dict[str, Set[IEventHandler]] = defaultdict(set)
        self._global_subscribers: Set[IEventHandler] = set()
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._logger = logging.getLogger(self.__class__.__name__)
        self._processor_task: Optional[asyncio.Task] = None
        
    @classmethod
    async def get_instance(cls) -> 'EventBus':
        """Get the singleton instance of the event bus."""
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    await cls._instance.start()
        return cls._instance
    
    async def start(self) -> None:
        """Start the event bus message processing."""
        if self._running:
            return
            
        self._running = True
        self._processor_task = asyncio.create_task(self._process_messages())
        self._logger.info("Event bus started")
    
    async def stop(self) -> None:
        """Stop the event bus."""
        if not self._running:
            return
            
        self._running = False
        if self._processor_task:
            self._processor_task.cancel()
            try:
                await self._processor_task
            except asyncio.CancelledError:
                pass
        
        self._logger.info("Event bus stopped")
    
    async def subscribe(self, handler: IEventHandler, event_types: Optional[Set[str]] = None) -> None:
        """Subscribe a handler to specific event types or all events."""
        if event_types is None:
            # Subscribe to all events
            self._global_subscribers.add(handler)
            self._logger.debug(f"Handler {handler} subscribed to all events")
        else:
            # Subscribe to specific event types
            for event_type in event_types:
                self._subscribers[event_type].add(handler)
            self._logger.debug(f"Handler {handler} subscribed to events: {event_types}")
    
    async def unsubscribe(self, handler: IEventHandler, event_types: Optional[Set[str]] = None) -> None:
        """Unsubscribe a handler from specific event types or all events."""
        if event_types is None:
            # Unsubscribe from all events
            self._global_subscribers.discard(handler)
            # Also remove from all specific event types
            for subscribers in self._subscribers.values():
                subscribers.discard(handler)
            self._logger.debug(f"Handler {handler} unsubscribed from all events")
        else:
            # Unsubscribe from specific event types
            for event_type in event_types:
                self._subscribers[event_type].discard(handler)
            self._logger.debug(f"Handler {handler} unsubscribed from events: {event_types}")
    
    async def publish(self, message: Message) -> None:
        """Publish a message to the event bus."""
        await self._message_queue.put(message)
        self._logger.debug(f"Message {message.id} published to event bus")
    
    async def _process_messages(self) -> None:
        """Process messages from the queue."""
        while self._running:
            try:
                # Wait for message with timeout to allow checking _running flag
                message = await asyncio.wait_for(self._message_queue.get(), timeout=1.0)
                await self._deliver_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self._logger.error(f"Error processing message: {e}")
    
    async def _deliver_message(self, message: Message) -> None:
        """Deliver a message to all relevant subscribers."""
        handlers = set()
        
        # Add global subscribers
        handlers.update(self._global_subscribers)
        
        # Add event-specific subscribers
        if message.event_type in self._subscribers:
            handlers.update(self._subscribers[message.event_type])
        
        # If message has specific receiver, filter handlers
        if message.receiver_id:
            handlers = {h for h in handlers if hasattr(h, 'component_id') and h.component_id == message.receiver_id}
        
        # Deliver to all relevant handlers
        for handler in handlers:
            try:
                await handler.handle_event(message)
            except Exception as e:
                self._logger.error(f"Error delivering message {message.id} to handler {handler}: {e}")
        
        self._logger.debug(f"Message {message.id} delivered to {len(handlers)} handlers")


class MessageRouter:
    """Routes messages between components based on patterns and rules."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._routing_rules: Dict[str, Callable[[Message], Optional[str]]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def add_routing_rule(self, rule_name: str, rule_func: Callable[[Message], Optional[str]]) -> None:
        """Add a routing rule that determines message destination."""
        self._routing_rules[rule_name] = rule_func
        self._logger.debug(f"Added routing rule: {rule_name}")
    
    def remove_routing_rule(self, rule_name: str) -> None:
        """Remove a routing rule."""
        if rule_name in self._routing_rules:
            del self._routing_rules[rule_name]
            self._logger.debug(f"Removed routing rule: {rule_name}")
    
    async def route_message(self, message: Message) -> None:
        """Apply routing rules to determine message destination."""
        for rule_name, rule_func in self._routing_rules.items():
            try:
                destination = rule_func(message)
                if destination:
                    # Create a new message with the determined destination
                    routed_message = message.model_copy()
                    routed_message.receiver_id = destination
                    routed_message.metadata["routed_by"] = rule_name
                    await self.event_bus.publish(routed_message)
                    self._logger.debug(f"Message {message.id} routed to {destination} by rule {rule_name}")
                    return
            except Exception as e:
                self._logger.error(f"Error in routing rule {rule_name}: {e}")
        
        # If no routing rule matched, publish as-is
        await self.event_bus.publish(message)