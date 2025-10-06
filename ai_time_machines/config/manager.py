"""Configuration management for AI Time Machines."""

import os
import yaml
import json
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
from pydantic import BaseModel, Field


class ComponentConfig(BaseModel):
    """Configuration for a component."""
    id: Optional[str] = None
    type: str
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)
    dependencies: list[str] = Field(default_factory=list)


class SystemConfig(BaseModel):
    """System-wide configuration."""
    log_level: str = "INFO"
    event_bus_queue_size: int = 1000
    component_timeout: int = 30
    max_retries: int = 3
    enable_metrics: bool = True


class AITimeMachinesConfig(BaseModel):
    """Main configuration class."""
    system: SystemConfig = Field(default_factory=SystemConfig)
    components: Dict[str, ComponentConfig] = Field(default_factory=dict)
    custom: Dict[str, Any] = Field(default_factory=dict)


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.config_path = config_path or Path("config.yaml")
        self._config: Optional[AITimeMachinesConfig] = None
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def load_config(self, config_path: Optional[Union[str, Path]] = None) -> AITimeMachinesConfig:
        """Load configuration from file."""
        if config_path:
            self.config_path = Path(config_path)
        
        config_path = Path(self.config_path)
        
        if not config_path.exists():
            self._logger.warning(f"Config file {config_path} not found, using defaults")
            self._config = AITimeMachinesConfig()
            return self._config
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    config_data = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    config_data = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path.suffix}")
            
            self._config = AITimeMachinesConfig(**config_data)
            self._logger.info(f"Configuration loaded from {config_path}")
            return self._config
            
        except Exception as e:
            self._logger.error(f"Error loading configuration from {config_path}: {e}")
            self._config = AITimeMachinesConfig()
            return self._config
    
    def save_config(self, config_path: Optional[Union[str, Path]] = None) -> bool:
        """Save current configuration to file."""
        if self._config is None:
            self._logger.error("No configuration to save")
            return False
        
        if config_path:
            self.config_path = Path(config_path)
        
        config_path = Path(self.config_path)
        
        try:
            config_data = self._config.model_dump()
            
            with open(config_path, 'w', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
                elif config_path.suffix.lower() == '.json':
                    json.dump(config_data, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path.suffix}")
            
            self._logger.info(f"Configuration saved to {config_path}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error saving configuration to {config_path}: {e}")
            return False
    
    def get_config(self) -> AITimeMachinesConfig:
        """Get the current configuration."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def get_component_config(self, component_id: str) -> Optional[ComponentConfig]:
        """Get configuration for a specific component."""
        config = self.get_config()
        return config.components.get(component_id)
    
    def add_component_config(self, component_id: str, component_config: ComponentConfig) -> None:
        """Add or update component configuration."""
        config = self.get_config()
        config.components[component_id] = component_config
        self._logger.debug(f"Added configuration for component {component_id}")
    
    def remove_component_config(self, component_id: str) -> bool:
        """Remove component configuration."""
        config = self.get_config()
        if component_id in config.components:
            del config.components[component_id]
            self._logger.debug(f"Removed configuration for component {component_id}")
            return True
        return False
    
    def get_system_config(self) -> SystemConfig:
        """Get system configuration."""
        return self.get_config().system
    
    def update_system_config(self, **kwargs) -> None:
        """Update system configuration parameters."""
        config = self.get_config()
        for key, value in kwargs.items():
            if hasattr(config.system, key):
                setattr(config.system, key, value)
                self._logger.debug(f"Updated system config {key} = {value}")
    
    def get_custom_config(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        config = self.get_config()
        return config.custom.get(key, default)
    
    def set_custom_config(self, key: str, value: Any) -> None:
        """Set custom configuration value."""
        config = self.get_config()
        config.custom[key] = value
        self._logger.debug(f"Set custom config {key} = {value}")
    
    def load_from_env(self, prefix: str = "AITM_") -> None:
        """Load configuration values from environment variables."""
        config = self.get_config()
        
        # Load system config from environment
        for field_name in config.system.model_fields.keys():
            env_name = f"{prefix}SYSTEM_{field_name.upper()}"
            env_value = os.getenv(env_name)
            if env_value is not None:
                # Convert value to appropriate type
                field_info = config.system.model_fields[field_name]
                if field_info.annotation == bool:
                    value = env_value.lower() in ('true', '1', 'yes', 'on')
                elif field_info.annotation == int:
                    value = int(env_value)
                else:
                    value = env_value
                
                setattr(config.system, field_name, value)
                self._logger.debug(f"Loaded system config {field_name} from environment")
        
        # Load custom config from environment
        for env_name, env_value in os.environ.items():
            if env_name.startswith(f"{prefix}CUSTOM_"):
                key = env_name[len(f"{prefix}CUSTOM_"):].lower()
                config.custom[key] = env_value
                self._logger.debug(f"Loaded custom config {key} from environment")


def create_default_config() -> AITimeMachinesConfig:
    """Create a default configuration."""
    config = AITimeMachinesConfig()
    
    # Add some example component configurations
    config.components["example_agent"] = ComponentConfig(
        type="agent",
        name="Example AI Agent",
        enabled=True,
        parameters={
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )
    
    config.components["example_time_machine"] = ComponentConfig(
        type="time_machine",
        name="Example Time Machine",
        enabled=True,
        parameters={
            "time_resolution": "seconds",
            "max_time_range": "1 year",
            "enable_branching": True
        }
    )
    
    return config


def save_default_config(config_path: Union[str, Path] = "config.yaml") -> bool:
    """Save a default configuration file."""
    config = create_default_config()
    config_manager = ConfigManager(config_path)
    config_manager._config = config
    return config_manager.save_config()