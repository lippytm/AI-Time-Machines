"""AI Time Machines - Advanced AI Agent and Educational Platform"""

__version__ = "1.0.0"
__author__ = "AI Time Machines Team"

from .core import SystemManager, initialize_system
from .agents import AgentManager
from .education import EducationManager
from .learning import LearningManager

__all__ = [
    "SystemManager",
    "initialize_system",
    "AgentManager", 
    "EducationManager",
    "LearningManager",
]