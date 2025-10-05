"""Configuration management utilities."""

import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages system configuration from YAML files."""
    
    def __init__(self, config_path: str):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to the main configuration file
        """
        self.config_path = Path(config_path)
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                # Create default config if none exists
                self._config = self._get_default_config()
                self.save_config()
        except Exception as e:
            raise ValueError(f"Failed to load config from {self.config_path}: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "system": {
                "name": "AI Time Machines",
                "version": "1.0.0",
                "environment": "development",
                "debug": True
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'system.name')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to save config to {self.config_path}: {e}")
    
    def reload(self):
        """Reload configuration from file."""
        self._load_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()
    
    def update(self, config_dict: Dict[str, Any]):
        """Update configuration with provided dictionary.
        
        Args:
            config_dict: Dictionary of configuration updates
        """
        self._deep_update(self._config, config_dict)
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Recursively update nested dictionaries."""
        for key, value in update_dict.items():
            if (key in base_dict and 
                isinstance(base_dict[key], dict) and 
                isinstance(value, dict)):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value