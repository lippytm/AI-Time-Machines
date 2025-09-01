"""Test configuration for pytest."""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "system": {
            "name": "AI Time Machines Test",
            "version": "1.0.0",
            "environment": "test",
            "debug": True
        },
        "agents": {
            "standard_agents": {"count": 2},
            "synthetic_agents": {"count": 1},
            "intelligence_engines": {"count": 1},
            "database_engines": {"count": 1}
        },
        "education": {
            "programming_languages": ["python", "javascript"],
            "blockchain": {"platforms": ["ethereum"]},
            "sandboxes": {"environments": ["coding", "blockchain"]}
        },
        "autonomous_learning": {
            "enabled": True,
            "self_improvement_interval": "1h",
            "experience_sharing": True
        },
        "database": {
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "name": "test_db"
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }