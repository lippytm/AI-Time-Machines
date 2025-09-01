"""
AI Time Machines - Adding AI Agents to everything with Time Machines

This package provides capabilities for:
- Git repository cloning and management
- Web scraping and data extraction
- Educational resources and tutorials
"""

__version__ = "0.1.0"
__author__ = "AI Time Machines Team"

from .cloning import RepositoryCloner
from .scraping import WebScraper

__all__ = ["RepositoryCloner", "WebScraper"]