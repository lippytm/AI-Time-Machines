"""Configuration management for lippytm ChatGPT.AI"""

import os
import yaml
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration for the ChatGPT AI bot"""
    
    DEFAULT_CONFIG = {
        'backend': 'openai',  # 'openai', 'transformers', 'echo'
        'openai_model': 'gpt-3.5-turbo',
        'local_model': 'microsoft/DialoGPT-medium',
        'max_tokens': 1000,
        'temperature': 0.7,
        'max_conversation_history': 50,
        'system_prompt': (
            "You are lippytm ChatGPT.AI, an intelligent assistant with time machine capabilities. "
            "You can help users with various tasks, provide insightful responses, and engage in "
            "meaningful conversations. You have access to knowledge from different time periods "
            "and can provide historical context when relevant."
        ),
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'ui': {
            'prompt_style': 'modern',
            'show_timestamps': True,
            'colorize_output': True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self._load_config()
        
        # Setup logging
        self._setup_logging()
    
    def _load_config(self):
        """Load configuration from various sources"""
        # 1. Load from file if provided
        if self.config_path and os.path.exists(self.config_path):
            self._load_config_file(self.config_path)
        
        # 2. Look for config files in standard locations
        else:
            config_locations = [
                'config.yaml',
                'config.yml',
                'lippytm_chatgpt.yaml',
                'lippytm_chatgpt.yml',
                os.path.expanduser('~/.lippytm_chatgpt.yaml'),
                '/etc/lippytm_chatgpt.yaml'
            ]
            
            for location in config_locations:
                if os.path.exists(location):
                    self._load_config_file(location)
                    break
        
        # 3. Override with environment variables
        self._load_env_config()
    
    def _load_config_file(self, filepath: str):
        """Load configuration from YAML or JSON file"""
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith(('.yaml', '.yml')):
                    file_config = yaml.safe_load(f)
                else:
                    file_config = json.load(f)
            
            if file_config:
                self._deep_update(self.config, file_config)
                self.logger.info(f"Loaded configuration from {filepath}")
        
        except Exception as e:
            self.logger.error(f"Failed to load config from {filepath}: {e}")
    
    def _load_env_config(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'LIPPYTM_OPENAI_API_KEY': 'openai_api_key',
            'OPENAI_API_KEY': 'openai_api_key',
            'LIPPYTM_BACKEND': 'backend',
            'LIPPYTM_MODEL': 'openai_model',
            'LIPPYTM_MAX_TOKENS': 'max_tokens',
            'LIPPYTM_TEMPERATURE': 'temperature',
            'LIPPYTM_LOG_LEVEL': 'logging.level'
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Handle nested keys like 'logging.level'
                if '.' in config_key:
                    keys = config_key.split('.')
                    target = self.config
                    for key in keys[:-1]:
                        target = target.setdefault(key, {})
                    target[keys[-1]] = self._convert_value(value)
                else:
                    self.config[config_key] = self._convert_value(value)
    
    def _convert_value(self, value: str) -> Any:
        """Convert string values to appropriate types"""
        # Try to convert to int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try to convert to float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Try to convert to boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Return as string
        return value
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO').upper())
        format_str = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(level=level, format=format_str)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        target = self.config
        
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        
        target[keys[-1]] = value
    
    def save_config(self, filepath: str):
        """Save current configuration to file"""
        try:
            with open(filepath, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            self.logger.info(f"Configuration saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save config to {filepath}: {e}")
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get complete configuration as dictionary"""
        return self.config.copy()
    
    def validate_config(self) -> bool:
        """Validate configuration and return True if valid"""
        valid = True
        
        # Check required fields based on backend
        backend = self.get('backend', 'echo')
        
        if backend == 'openai':
            if not self.get('openai_api_key'):
                self.logger.warning("OpenAI API key not configured")
                valid = False
        
        # Validate numeric values
        if not isinstance(self.get('max_tokens', 0), (int, float)) or self.get('max_tokens', 0) <= 0:
            self.logger.error("max_tokens must be a positive number")
            valid = False
        
        if not 0 <= self.get('temperature', 0.7) <= 2:
            self.logger.error("temperature must be between 0 and 2")
            valid = False
        
        return valid