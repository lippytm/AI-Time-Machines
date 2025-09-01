"""AI Time Machines - A framework for integrating AI Agents with Time Machine concepts.

This package provides a modular architecture for building AI systems that can
interact across time, with robust communication mechanisms and component integration.
"""

__version__ = "0.1.0"
__author__ = "AI-Time-Machines Team"

# Core imports for easy access
from ai_time_machines.core.base import Component
from ai_time_machines.core.interfaces import IAgent, ITimeMachine
from ai_time_machines.communication.event_bus import EventBus
from ai_time_machines.utils.registry import ComponentRegistry

__all__ = [
    "Component",
    "IAgent", 
    "ITimeMachine",
    "EventBus",
    "ComponentRegistry",
]