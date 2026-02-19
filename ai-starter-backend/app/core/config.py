from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_starter"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production-min-32-characters"
    JWT_EXPIRES_IN: int = 3600  # seconds
    JWT_ALGORITHM: str = "HS256"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    
    # Development
    USE_LOCAL_MODEL: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
