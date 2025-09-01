"""Core system management for AI Time Machines platform."""

import asyncio
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..utils.config import ConfigManager
from ..utils.logger import setup_logging


class SystemManager:
    """Central management system for the AI Time Machines platform."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the system manager.
        
        Args:
            config_path: Path to configuration file. Defaults to config.yml
        """
        self.config_path = config_path or "config.yml"
        self.config = ConfigManager(self.config_path)
        self.logger = setup_logging(self.config.get("logging", {}))
        
        self.start_time = datetime.now()
        self.status = "initializing"
        self.components = {}
        
    async def initialize(self) -> bool:
        """Initialize all system components.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing AI Time Machines system...")
            
            # Initialize core components
            await self._initialize_database()
            await self._initialize_agents()
            await self._initialize_education()
            await self._initialize_learning()
            
            self.status = "running"
            self.logger.info("System initialization complete")
            return True
            
        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            self.status = "error"
            return False
    
    async def _initialize_database(self):
        """Initialize database connections and schemas."""
        from ..database import DatabaseManager
        
        db_config = self.config.get("database", {})
        self.components["database"] = DatabaseManager(db_config)
        await self.components["database"].initialize()
        self.logger.info("Database manager initialized")
    
    async def _initialize_agents(self):
        """Initialize AI agent systems."""
        from ..agents import AgentManager
        
        agent_config = self.config.get("agents", {})
        self.components["agents"] = AgentManager(agent_config)
        await self.components["agents"].initialize()
        self.logger.info("Agent manager initialized")
    
    async def _initialize_education(self):
        """Initialize educational resources."""
        from ..education import EducationManager
        
        edu_config = self.config.get("education", {})
        self.components["education"] = EducationManager(edu_config)
        await self.components["education"].initialize()
        self.logger.info("Education manager initialized")
    
    async def _initialize_learning(self):
        """Initialize autonomous learning system."""
        from ..learning import LearningManager
        
        learning_config = self.config.get("autonomous_learning", {})
        self.components["learning"] = LearningManager(learning_config)
        await self.components["learning"].initialize()
        self.logger.info("Learning manager initialized")
    
    async def shutdown(self):
        """Gracefully shutdown all system components."""
        self.logger.info("Shutting down AI Time Machines system...")
        
        for name, component in self.components.items():
            try:
                if hasattr(component, 'shutdown'):
                    await component.shutdown()
                    self.logger.info(f"{name} component shutdown complete")
            except Exception as e:
                self.logger.error(f"Error shutting down {name}: {e}")
        
        self.status = "stopped"
        self.logger.info("System shutdown complete")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status and metrics.
        
        Returns:
            Dict containing system status information
        """
        uptime = datetime.now() - self.start_time
        
        status_info = {
            "status": self.status,
            "uptime": str(uptime),
            "start_time": self.start_time.isoformat(),
            "version": "1.0.0",
            "components": {}
        }
        
        for name, component in self.components.items():
            if hasattr(component, 'get_status'):
                status_info["components"][name] = component.get_status()
            else:
                status_info["components"][name] = "running"
        
        return status_info
    
    async def health_check(self) -> bool:
        """Perform system health check.
        
        Returns:
            bool: True if all components are healthy, False otherwise
        """
        if self.status != "running":
            return False
            
        for name, component in self.components.items():
            try:
                if hasattr(component, 'health_check'):
                    if not await component.health_check():
                        self.logger.warning(f"Health check failed for {name}")
                        return False
            except Exception as e:
                self.logger.error(f"Health check error for {name}: {e}")
                return False
        
        return True


# Global system instance
_system_instance: Optional[SystemManager] = None


def get_system() -> SystemManager:
    """Get the global system instance."""
    global _system_instance
    if _system_instance is None:
        _system_instance = SystemManager()
    return _system_instance


async def initialize_system(config_path: Optional[str] = None) -> SystemManager:
    """Initialize and return the global system instance."""
    global _system_instance
    _system_instance = SystemManager(config_path)
    await _system_instance.initialize()
    return _system_instance