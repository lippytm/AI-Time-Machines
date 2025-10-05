"""Configuration management for AI Time Machines automation."""

import os
from typing import Optional
from pydantic import Field, BaseModel


class Settings(BaseModel):
    """Application settings with environment variable support."""
    
    # GitHub Authentication
    github_token: Optional[str] = Field(None, description="GitHub API token")
    
    # Default repository settings
    default_repo_owner: Optional[str] = Field(None, description="Default repository owner")
    default_repo_name: Optional[str] = Field(None, description="Default repository name")
    
    # Automation settings
    auto_process_prs: bool = Field(True, description="Auto-process PRs")
    max_pr_batch_size: int = Field(10, description="Maximum PR batch size")
    
    def __init__(self, **kwargs):
        # Load from environment variables
        env_values = {
            'github_token': os.getenv('GITHUB_TOKEN'),
            'default_repo_owner': os.getenv('DEFAULT_REPO_OWNER'),
            'default_repo_name': os.getenv('DEFAULT_REPO_NAME'),
            'auto_process_prs': os.getenv('AUTO_PROCESS_PRS', 'true').lower() == 'true',
            'max_pr_batch_size': int(os.getenv('MAX_PR_BATCH_SIZE', '10'))
        }
        # Override with any provided kwargs
        env_values.update(kwargs)
        super().__init__(**env_values)


# Global settings instance
settings = Settings()


def validate_github_auth() -> bool:
    """Validate that GitHub authentication is properly configured."""
    return settings.github_token is not None and len(settings.github_token.strip()) > 0


def get_repo_info(repo_owner: Optional[str] = None, repo_name: Optional[str] = None) -> tuple[str, str]:
    """Get repository owner and name, using defaults if not provided."""
    owner = repo_owner or settings.default_repo_owner
    name = repo_name or settings.default_repo_name
    
    if not owner or not name:
        raise ValueError("Repository owner and name must be provided either as parameters or environment variables")
    
    return owner, name