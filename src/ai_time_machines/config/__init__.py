"""Configuration management for AI Time Machines."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GitHubConfig(BaseModel):
    """GitHub integration configuration."""
    token: str = Field(..., description="GitHub personal access token")
    repository_owner: str = Field(default="lippytm", description="GitHub repository owner")
    repository_name: str = Field(default="AI-Time-Machines", description="GitHub repository name")


class EmailConfig(BaseModel):
    """Email service configuration."""
    smtp_server: str = Field(default="smtp.gmail.com", description="SMTP server address")
    smtp_port: int = Field(default=587, description="SMTP server port")
    use_tls: bool = Field(default=True, description="Use TLS encryption")
    email_address: str = Field(default="lippytimemachines@gmail.com", description="Email address for notifications")
    password: str = Field(..., description="Email account password or app password")


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""
    api_key: str = Field(..., description="OpenAI API key")


class AppConfig(BaseModel):
    """Main application configuration."""
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="development", description="Application environment")


class Config(BaseModel):
    """Main configuration class."""
    github: GitHubConfig
    email: EmailConfig
    openai: OpenAIConfig
    app: AppConfig

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            github=GitHubConfig(
                token=os.getenv("GITHUB_TOKEN", ""),
                repository_owner=os.getenv("GITHUB_REPOSITORY_OWNER", "lippytm"),
                repository_name=os.getenv("GITHUB_REPOSITORY_NAME", "AI-Time-Machines"),
            ),
            email=EmailConfig(
                smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                smtp_port=int(os.getenv("SMTP_PORT", "587")),
                use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
                email_address=os.getenv("EMAIL_ADDRESS", "lippytimemachines@gmail.com"),
                password=os.getenv("EMAIL_PASSWORD", ""),
            ),
            openai=OpenAIConfig(
                api_key=os.getenv("OPENAI_API_KEY", ""),
            ),
            app=AppConfig(
                log_level=os.getenv("LOG_LEVEL", "INFO"),
                environment=os.getenv("ENVIRONMENT", "development"),
            ),
        )


# Global configuration instance
config = Config.from_env()