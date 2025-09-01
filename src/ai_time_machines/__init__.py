"""
AI-Time-Machines: Core package for AI Agent integration
"""

__version__ = "0.1.0"
__author__ = "AI-Time-Machines Team"

from .core import AIAgent, TimeMachine
from .integrations import Web3AIIntegration, RepositoryIntegration
from .config import Config

__all__ = [
    "AIAgent",
    "TimeMachine", 
    "Web3AIIntegration",
    "RepositoryIntegration",
    "Config",
]