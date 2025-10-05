"""Logging utilities for the AI Time Machines platform."""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Dict, Any


def setup_logging(logging_config: Dict[str, Any]) -> logging.Logger:
    """Setup logging configuration for the system.
    
    Args:
        logging_config: Dictionary containing logging configuration
        
    Returns:
        Configured logger instance
    """
    log_level = logging_config.get("level", "INFO")
    log_format = logging_config.get("format", 
                                   "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_file = logging_config.get("file", "logs/ai_time_machines.log")
    max_size = logging_config.get("max_size", "100MB")
    backup_count = logging_config.get("backup_count", 5)
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger("ai_time_machines")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    max_bytes = _parse_size(max_size)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def _parse_size(size_str: str) -> int:
    """Parse size string to bytes.
    
    Args:
        size_str: Size string like '100MB', '1GB', etc.
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper()
    
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size_str)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"ai_time_machines.{name}")


class LoggerMixin:
    """Mixin class to add logging capabilities to other classes."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__module__)