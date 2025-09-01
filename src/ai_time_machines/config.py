"""
Configuration management for AI-Time-Machines
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .integrations import IntegrationConfig


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


class TimeMachineConfig(BaseModel):
    """Configuration for a Time Machine instance"""
    machine_id: str
    name: str = ""
    description: str = ""
    enabled: bool = True
    max_agents: int = 100
    event_retention_days: int = 30


class Config:
    """Main configuration class for AI-Time-Machines"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_config_file()
        self.data: Dict[str, Any] = {}
        self.integrations: Dict[str, IntegrationConfig] = {}
        self.time_machines: Dict[str, TimeMachineConfig] = {}
        self.logging_config: LoggingConfig = LoggingConfig()
        
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self._load_config()
        self._setup_logging()
        
    def _find_config_file(self) -> str:
        """Find configuration file in standard locations"""
        possible_files = [
            "ai_time_machines.json",
            "config/ai_time_machines.json",
            os.path.expanduser("~/.ai_time_machines.json"),
            "/etc/ai_time_machines.json"
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                return file_path
                
        # Return default location if none found
        return "ai_time_machines.json"
        
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.data = json.load(f)
                    
                self._parse_config()
                logging.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logging.warning(f"Failed to load config file {self.config_file}: {str(e)}")
                self._load_defaults()
        else:
            logging.info(f"Config file {self.config_file} not found, using defaults")
            self._load_defaults()
            
    def _load_defaults(self):
        """Load default configuration"""
        self.data = {
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "time_machines": {
                "default": {
                    "machine_id": "default",
                    "name": "Default Time Machine",
                    "description": "Default AI-Time-Machine instance",
                    "enabled": True,
                    "max_agents": 100
                }
            },
            "integrations": {}
        }
        self._parse_config()
        
    def _parse_config(self):
        """Parse loaded configuration data"""
        # Parse logging config
        logging_data = self.data.get("logging", {})
        self.logging_config = LoggingConfig(**logging_data)
        
        # Parse time machine configs
        time_machines_data = self.data.get("time_machines", {})
        for machine_id, machine_data in time_machines_data.items():
            if "machine_id" in machine_data:
                self.time_machines[machine_id] = TimeMachineConfig(**machine_data)
            else:
                self.time_machines[machine_id] = TimeMachineConfig(
                    machine_id=machine_id,
                    **machine_data
                )
            
        # Parse integration configs
        integrations_data = self.data.get("integrations", {})
        for integration_name, integration_data in integrations_data.items():
            if "name" in integration_data and integration_data["name"] != integration_name:
                # Handle case where name in data conflicts with key
                config_data = integration_data.copy()
                config_data["name"] = integration_name
                self.integrations[integration_name] = IntegrationConfig(**config_data)
            else:
                self.integrations[integration_name] = IntegrationConfig(
                    name=integration_name,
                    **{k: v for k, v in integration_data.items() if k != "name"}
                )
            
    def _setup_logging(self):
        """Setup logging based on configuration"""
        logging.basicConfig(
            level=getattr(logging, self.logging_config.level.upper()),
            format=self.logging_config.format,
            filename=self.logging_config.file
        )
        
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Ensure directory exists
            config_dir = os.path.dirname(self.config_file)
            if config_dir:  # Only create directory if there is one
                os.makedirs(config_dir, exist_ok=True)
            
            # Prepare data for saving
            save_data = {
                "logging": self.logging_config.dict(),
                "time_machines": {
                    machine_id: config.dict() 
                    for machine_id, config in self.time_machines.items()
                },
                "integrations": {
                    name: config.dict() 
                    for name, config in self.integrations.items()
                }
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
                
            logging.info(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to save configuration: {str(e)}")
            
    def get_integration_config(self, name: str) -> Optional[IntegrationConfig]:
        """Get integration configuration by name"""
        return self.integrations.get(name)
        
    def add_integration_config(self, config: IntegrationConfig):
        """Add integration configuration"""
        self.integrations[config.name] = config
        
    def get_time_machine_config(self, machine_id: str) -> Optional[TimeMachineConfig]:
        """Get time machine configuration by ID"""
        return self.time_machines.get(machine_id)
        
    def add_time_machine_config(self, config: TimeMachineConfig):
        """Add time machine configuration"""
        self.time_machines[config.machine_id] = config
        
    def get_env_var(self, key: str, default: Any = None) -> Any:
        """Get environment variable with fallback to config"""
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value
            
        # Try to find in config data
        return self._get_nested_value(self.data, key.lower().split('_'), default)
        
    def _get_nested_value(self, data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
        """Get nested value from dictionary"""
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
        
    def create_web3ai_integration(self, name: str = "web3ai", **kwargs) -> IntegrationConfig:
        """Create a Web3AI integration configuration"""
        config_data = {
            "enabled": True,
            "timeout": 30,
            "config": {
                "web3ai_url": kwargs.get("web3ai_url") or self.get_env_var("WEB3AI_URL"),
                "blockchain_rpc": kwargs.get("blockchain_rpc") or self.get_env_var("BLOCKCHAIN_RPC"),
                "contract_addresses": kwargs.get("contract_addresses", {}),
                "private_key": kwargs.get("private_key") or self.get_env_var("PRIVATE_KEY")
            }
        }
        config_data.update(kwargs)
        
        integration_config = IntegrationConfig(name=name, **config_data)
        self.add_integration_config(integration_config)
        return integration_config
        
    def create_repository_integration(self, name: str, repo_type: str = "github", **kwargs) -> IntegrationConfig:
        """Create a repository integration configuration"""
        config_data = {
            "enabled": True,
            "timeout": 30,
            "config": {
                "type": repo_type,
                "base_url": kwargs.get("base_url") or self.get_env_var(f"{repo_type.upper()}_URL"),
                "api_key": kwargs.get("api_key") or self.get_env_var(f"{repo_type.upper()}_API_KEY")
            }
        }
        config_data.update(kwargs)
        
        integration_config = IntegrationConfig(name=name, **config_data)
        self.add_integration_config(integration_config)
        return integration_config


def load_config(config_file: Optional[str] = None) -> Config:
    """Load configuration from file or defaults"""
    return Config(config_file)