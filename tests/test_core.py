"""Unit tests for AI Time Machines core functionality."""

import asyncio
import pytest
from unittest.mock import Mock, patch

from ai_time_machines.core import SystemManager
from ai_time_machines.agents import AgentManager, AgentType
from ai_time_machines.education import EducationManager, SkillLevel
from ai_time_machines.learning import LearningManager, LearningAlgorithm


class TestSystemManager:
    """Test cases for SystemManager."""
    
    @pytest.mark.asyncio
    async def test_system_initialization(self):
        """Test system initialization."""
        config = {
            "system": {"name": "Test System"},
            "agents": {"standard_agents": {"count": 5}},
            "education": {"programming_languages": ["python"]},
            "autonomous_learning": {"enabled": True}
        }
        
        with patch('ai_time_machines.utils.config.ConfigManager') as mock_config:
            mock_config.return_value.get.side_effect = lambda key, default=None: config.get(key, default)
            
            system = SystemManager()
            result = await system.initialize()
            
            assert result is True
            assert system.status == "running"
            assert len(system.components) == 4  # database, agents, education, learning
    
    @pytest.mark.asyncio
    async def test_system_health_check(self):
        """Test system health check."""
        system = SystemManager()
        system.status = "running"
        
        # Mock components with health_check methods
        for name in ["database", "agents", "education", "learning"]:
            mock_component = Mock()
            mock_component.health_check = asyncio.coroutine(lambda: True)
            system.components[name] = mock_component
        
        health = await system.health_check()
        assert health is True
    
    def test_system_status(self):
        """Test system status reporting."""
        system = SystemManager()
        system.status = "running"
        
        status = system.get_status()
        
        assert "status" in status
        assert "uptime" in status
        assert "version" in status
        assert status["status"] == "running"


class TestAgentManager:
    """Test cases for AgentManager."""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self):
        """Test agent creation and initialization."""
        config = {
            "standard_agents": {"count": 2},
            "synthetic_agents": {"count": 2},
            "intelligence_engines": {"count": 1},
            "database_engines": {"count": 1}
        }
        
        manager = AgentManager(config)
        await manager.initialize()
        
        assert len(manager.agents) == 6  # 2+2+1+1
        
        # Check agent types
        standard_count = sum(1 for agent in manager.agents.values() 
                           if agent.agent_type == AgentType.STANDARD)
        assert standard_count == 2
    
    @pytest.mark.asyncio
    async def test_task_assignment(self):
        """Test task assignment to agents."""
        config = {"standard_agents": {"count": 1}}
        manager = AgentManager(config)
        await manager.initialize()
        
        task = {"id": "test_task", "type": "reasoning", "data": "test"}
        result = await manager.assign_task(task)
        
        assert result["status"] == "completed"
        assert result["task_id"] == "test_task"
    
    def test_agent_status(self):
        """Test agent status reporting."""
        config = {"standard_agents": {"count": 2}}
        manager = AgentManager(config)
        
        status = manager.get_status()
        
        assert "total_agents" in status
        assert "status_by_type" in status


class TestEducationManager:
    """Test cases for EducationManager."""
    
    @pytest.mark.asyncio
    async def test_education_initialization(self):
        """Test education system initialization."""
        config = {
            "programming_languages": ["python", "javascript"],
            "blockchain": {"platforms": ["ethereum"]},
            "sandboxes": {"environments": ["coding"]}
        }
        
        manager = EducationManager(config)
        await manager.initialize()
        
        assert len(manager.programming_modules) == 2
        assert len(manager.blockchain_modules) == 1
        assert len(manager.sandboxes) > 0
        assert len(manager.resources) > 0
    
    def test_resource_search(self):
        """Test educational resource search."""
        config = {"programming_languages": ["python"]}
        manager = EducationManager(config)
        
        # Manually add a test resource
        from ai_time_machines.education import LearningResource, ResourceType
        resource = LearningResource(
            id="test_resource",
            title="Test Resource",
            description="Test",
            resource_type=ResourceType.TUTORIAL,
            category="programming",
            subcategory="python",
            skill_level=SkillLevel.BEGINNER,
            duration_minutes=60
        )
        manager.resources["test_resource"] = resource
        
        results = manager.search_resources(category="programming")
        assert len(results) == 1
        assert results[0].id == "test_resource"
    
    def test_learning_path(self):
        """Test learning path generation."""
        config = {"programming_languages": ["python"]}
        manager = EducationManager(config)
        
        path = manager.get_learning_path("programming", SkillLevel.INTERMEDIATE)
        assert isinstance(path, list)


class TestLearningManager:
    """Test cases for LearningManager."""
    
    @pytest.mark.asyncio
    async def test_learning_initialization(self):
        """Test learning system initialization."""
        config = {
            "enabled": True,
            "self_improvement_interval": "1h",
            "experience_sharing": True
        }
        
        manager = LearningManager(config)
        await manager.initialize()
        
        assert manager.learning_enabled is True
        assert len(manager.knowledge_base.knowledge_items) > 0
        assert len(manager.algorithms) > 0
    
    @pytest.mark.asyncio
    async def test_training_experience_generation(self):
        """Test training experience generation."""
        config = {"enabled": True}
        manager = LearningManager(config)
        
        experience = await manager.generate_training_experience(
            "test_agent", "reasoning", 0.5
        )
        
        assert experience.agent_id == "test_agent"
        assert experience.task_type == "reasoning"
        assert 0.0 <= experience.reward <= 1.0
    
    @pytest.mark.asyncio
    async def test_training_session_creation(self):
        """Test training session creation."""
        config = {"enabled": True}
        manager = LearningManager(config)
        await manager.initialize()
        
        experiences = []
        for _ in range(3):
            exp = await manager.generate_training_experience("agent1", "test_task")
            experiences.append(exp)
        
        session_id = await manager.create_training_session(
            ["agent1"], LearningAlgorithm.REINFORCEMENT_LEARNING, experiences
        )
        
        assert session_id in manager.training_sessions
        assert manager.training_sessions[session_id].agent_ids == ["agent1"]
    
    def test_learning_metrics(self):
        """Test learning metrics collection."""
        config = {"enabled": True}
        manager = LearningManager(config)
        
        metrics = manager.get_learning_metrics()
        
        assert "total_training_sessions" in metrics
        assert "knowledge_base_size" in metrics
        assert "autonomous_learning_enabled" in metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v"])