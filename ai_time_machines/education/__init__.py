"""Educational resources and learning management system."""

import asyncio
import uuid
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..utils.logger import LoggerMixin


class ResourceType(Enum):
    """Types of educational resources."""
    TUTORIAL = "tutorial"
    GUIDE = "guide"
    SANDBOX = "sandbox"
    EXERCISE = "exercise"
    PROJECT = "project"
    ASSESSMENT = "assessment"


class SkillLevel(Enum):
    """Skill levels for educational content."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class LearningResource:
    """Educational learning resource."""
    id: str
    title: str
    description: str
    resource_type: ResourceType
    category: str
    subcategory: str
    skill_level: SkillLevel
    duration_minutes: int
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    content: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ProgrammingLanguageModule:
    """Educational module for a programming language."""
    
    def __init__(self, language: str):
        """Initialize programming language module.
        
        Args:
            language: Programming language name
        """
        self.language = language
        self.resources = []
        self._create_resources()
    
    def _create_resources(self):
        """Create educational resources for the programming language."""
        base_id = self.language.lower().replace('+', 'plus').replace('#', 'sharp')
        
        # Basic tutorial
        self.resources.append(LearningResource(
            id=f"{base_id}_basics",
            title=f"{self.language} Basics",
            description=f"Introduction to {self.language} programming language fundamentals",
            resource_type=ResourceType.TUTORIAL,
            category="programming",
            subcategory=self.language.lower(),
            skill_level=SkillLevel.BEGINNER,
            duration_minutes=120,
            learning_objectives=[
                f"Understand {self.language} syntax",
                "Write basic programs",
                "Use variables and functions",
                "Handle errors and exceptions"
            ],
            content={
                "sections": [
                    "Introduction and Setup",
                    "Variables and Data Types", 
                    "Control Structures",
                    "Functions and Methods",
                    "Error Handling",
                    "Best Practices"
                ],
                "exercises": 15,
                "code_examples": 30
            },
            tags=[self.language.lower(), "basics", "fundamentals"]
        ))
        
        # Advanced concepts
        self.resources.append(LearningResource(
            id=f"{base_id}_advanced",
            title=f"Advanced {self.language}",
            description=f"Advanced concepts and patterns in {self.language}",
            resource_type=ResourceType.GUIDE,
            category="programming", 
            subcategory=self.language.lower(),
            skill_level=SkillLevel.ADVANCED,
            duration_minutes=240,
            prerequisites=[f"{base_id}_basics"],
            learning_objectives=[
                "Master advanced language features",
                "Implement design patterns",
                "Optimize performance",
                "Build complex applications"
            ],
            content={
                "topics": [
                    "Advanced Data Structures",
                    "Concurrency and Parallelism",
                    "Memory Management",
                    "Design Patterns",
                    "Performance Optimization",
                    "Testing and Debugging"
                ],
                "projects": 5,
                "case_studies": 10
            },
            tags=[self.language.lower(), "advanced", "patterns"]
        ))
        
        # Interactive sandbox
        self.resources.append(LearningResource(
            id=f"{base_id}_sandbox",
            title=f"{self.language} Interactive Sandbox",
            description=f"Hands-on coding environment for {self.language}",
            resource_type=ResourceType.SANDBOX,
            category="programming",
            subcategory=self.language.lower(),
            skill_level=SkillLevel.BEGINNER,
            duration_minutes=60,
            content={
                "environment": "containerized",
                "features": [
                    "Code editor with syntax highlighting",
                    "Real-time execution",
                    "Built-in debugger",
                    "Example projects",
                    "Performance profiler"
                ],
                "resource_limits": {
                    "cpu": "2 cores",
                    "memory": "4GB",
                    "storage": "10GB"
                }
            },
            tags=[self.language.lower(), "sandbox", "interactive"]
        ))


class BlockchainModule:
    """Educational module for blockchain technology."""
    
    def __init__(self, platform: str):
        """Initialize blockchain module.
        
        Args:
            platform: Blockchain platform name
        """
        self.platform = platform
        self.resources = []
        self._create_resources()
    
    def _create_resources(self):
        """Create blockchain educational resources."""
        base_id = self.platform.lower()
        
        # Blockchain fundamentals
        self.resources.append(LearningResource(
            id=f"{base_id}_fundamentals",
            title=f"{self.platform} Blockchain Fundamentals",
            description=f"Core concepts of {self.platform} blockchain technology",
            resource_type=ResourceType.TUTORIAL,
            category="blockchain",
            subcategory=self.platform.lower(),
            skill_level=SkillLevel.BEGINNER,
            duration_minutes=180,
            learning_objectives=[
                "Understand blockchain concepts",
                "Learn consensus mechanisms",
                "Explore cryptographic foundations",
                "Analyze network architecture"
            ],
            content={
                "modules": [
                    "What is Blockchain?",
                    "Cryptographic Hash Functions",
                    "Digital Signatures",
                    "Consensus Algorithms",
                    "Network Topology",
                    "Transaction Processing"
                ],
                "simulations": 8,
                "quizzes": 12
            },
            tags=[self.platform.lower(), "blockchain", "fundamentals"]
        ))
        
        # Smart contract development
        if self.platform.lower() in ['ethereum', 'solana', 'cardano']:
            self.resources.append(LearningResource(
                id=f"{base_id}_smart_contracts",
                title=f"{self.platform} Smart Contract Development",
                description=f"Building smart contracts on {self.platform}",
                resource_type=ResourceType.PROJECT,
                category="blockchain",
                subcategory=self.platform.lower(),
                skill_level=SkillLevel.INTERMEDIATE,
                duration_minutes=300,
                prerequisites=[f"{base_id}_fundamentals"],
                learning_objectives=[
                    "Write smart contracts",
                    "Deploy to testnet/mainnet",
                    "Test contract functionality",
                    "Implement security best practices"
                ],
                content={
                    "languages": ["solidity", "vyper"] if self.platform.lower() == 'ethereum' else ["rust"],
                    "projects": [
                        "Token Contract",
                        "NFT Marketplace",
                        "DeFi Protocol",
                        "DAO Governance"
                    ],
                    "tools": ["development framework", "testing suite", "deployment scripts"]
                },
                tags=[self.platform.lower(), "smart-contracts", "development"]
            ))
        
        # DeFi applications
        self.resources.append(LearningResource(
            id=f"{base_id}_defi",
            title=f"DeFi on {self.platform}",
            description=f"Decentralized Finance applications on {self.platform}",
            resource_type=ResourceType.GUIDE,
            category="blockchain",
            subcategory="defi",
            skill_level=SkillLevel.ADVANCED,
            duration_minutes=240,
            prerequisites=[f"{base_id}_fundamentals"],
            learning_objectives=[
                "Understand DeFi protocols",
                "Analyze liquidity pools",
                "Implement yield farming",
                "Build DeFi applications"
            ],
            content={
                "protocols": [
                    "Automated Market Makers (AMM)",
                    "Lending and Borrowing",
                    "Yield Farming",
                    "Synthetic Assets",
                    "Options and Derivatives"
                ],
                "case_studies": ["Uniswap", "Compound", "Aave", "Synthetix"],
                "hands_on": ["Build AMM", "Create lending protocol"]
            },
            tags=[self.platform.lower(), "defi", "finance"]
        ))


class InteractiveSandbox:
    """Interactive learning environment for hands-on practice."""
    
    def __init__(self, sandbox_id: str, environment_type: str):
        """Initialize sandbox.
        
        Args:
            sandbox_id: Unique sandbox identifier
            environment_type: Type of sandbox environment
        """
        self.sandbox_id = sandbox_id
        self.environment_type = environment_type
        self.status = "available"
        self.user_sessions = {}
        self.created_at = datetime.now()
    
    async def start_session(self, user_id: str, config: Dict[str, Any]) -> str:
        """Start a new user session in the sandbox.
        
        Args:
            user_id: User identifier
            config: Session configuration
            
        Returns:
            Session ID
        """
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "started_at": datetime.now(),
            "config": config,
            "status": "active",
            "resources_used": {
                "cpu_percent": 0,
                "memory_percent": 0,
                "storage_used": "0MB"
            }
        }
        
        self.user_sessions[session_id] = session
        return session_id
    
    async def execute_code(self, session_id: str, code: str, language: str) -> Dict[str, Any]:
        """Execute code in a sandbox session.
        
        Args:
            session_id: Session identifier
            code: Code to execute
            language: Programming language
            
        Returns:
            Execution result
        """
        if session_id not in self.user_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Simulate code execution
        await asyncio.sleep(0.1)
        
        return {
            "session_id": session_id,
            "language": language,
            "status": "success",
            "output": f"Executed {language} code successfully",
            "execution_time": "0.1s",
            "memory_used": "10MB"
        }
    
    async def stop_session(self, session_id: str):
        """Stop a user session.
        
        Args:
            session_id: Session to stop
        """
        if session_id in self.user_sessions:
            self.user_sessions[session_id]["status"] = "stopped"
            self.user_sessions[session_id]["stopped_at"] = datetime.now()


class EducationManager(LoggerMixin):
    """Manages educational resources and learning experiences."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize education manager.
        
        Args:
            config: Education configuration
        """
        self.config = config
        self.resources: Dict[str, LearningResource] = {}
        self.programming_modules = {}
        self.blockchain_modules = {}
        self.sandboxes: Dict[str, InteractiveSandbox] = {}
        
    async def initialize(self):
        """Initialize the education system."""
        self.logger.info("Initializing Education system...")
        
        # Create programming language modules
        await self._create_programming_modules()
        
        # Create blockchain modules
        await self._create_blockchain_modules()
        
        # Create interactive sandboxes
        await self._create_sandboxes()
        
        self.logger.info(f"Education system initialized with {len(self.resources)} resources")
    
    async def _create_programming_modules(self):
        """Create programming language educational modules."""
        languages = self.config.get("programming_languages", [])
        
        for language in languages[:10]:  # Limit for demonstration
            module = ProgrammingLanguageModule(language)
            self.programming_modules[language] = module
            
            # Add resources to main collection
            for resource in module.resources:
                self.resources[resource.id] = resource
        
        self.logger.info(f"Created {len(self.programming_modules)} programming language modules")
    
    async def _create_blockchain_modules(self):
        """Create blockchain educational modules."""
        platforms = self.config.get("blockchain", {}).get("platforms", [])
        
        for platform in platforms[:6]:  # Limit for demonstration
            module = BlockchainModule(platform)
            self.blockchain_modules[platform] = module
            
            # Add resources to main collection
            for resource in module.resources:
                self.resources[resource.id] = resource
        
        self.logger.info(f"Created {len(self.blockchain_modules)} blockchain modules")
    
    async def _create_sandboxes(self):
        """Create interactive sandbox environments."""
        environments = self.config.get("sandboxes", {}).get("environments", [])
        
        for env_type in environments:
            for i in range(5):  # Create 5 sandboxes per type
                sandbox_id = f"{env_type}_{uuid.uuid4().hex[:8]}"
                sandbox = InteractiveSandbox(sandbox_id, env_type)
                self.sandboxes[sandbox_id] = sandbox
        
        self.logger.info(f"Created {len(self.sandboxes)} interactive sandboxes")
    
    def search_resources(self, 
                        category: Optional[str] = None,
                        skill_level: Optional[SkillLevel] = None,
                        resource_type: Optional[ResourceType] = None,
                        tags: Optional[List[str]] = None) -> List[LearningResource]:
        """Search for educational resources.
        
        Args:
            category: Resource category filter
            skill_level: Skill level filter
            resource_type: Resource type filter
            tags: Tags filter
            
        Returns:
            List of matching resources
        """
        results = []
        
        for resource in self.resources.values():
            # Apply filters
            if category and resource.category != category:
                continue
            if skill_level and resource.skill_level != skill_level:
                continue
            if resource_type and resource.resource_type != resource_type:
                continue
            if tags and not any(tag in resource.tags for tag in tags):
                continue
                
            results.append(resource)
        
        return results
    
    async def get_sandbox(self, environment_type: str) -> Optional[str]:
        """Get an available sandbox for the specified environment.
        
        Args:
            environment_type: Type of sandbox needed
            
        Returns:
            Sandbox ID if available, None otherwise
        """
        for sandbox_id, sandbox in self.sandboxes.items():
            if (sandbox.environment_type == environment_type and 
                sandbox.status == "available"):
                sandbox.status = "in_use"
                return sandbox_id
        
        return None
    
    async def release_sandbox(self, sandbox_id: str):
        """Release a sandbox back to available pool.
        
        Args:
            sandbox_id: Sandbox to release
        """
        if sandbox_id in self.sandboxes:
            self.sandboxes[sandbox_id].status = "available"
            # Clean up any active sessions
            for session in self.sandboxes[sandbox_id].user_sessions.values():
                if session["status"] == "active":
                    await self.sandboxes[sandbox_id].stop_session(session["session_id"])
    
    def get_learning_path(self, category: str, skill_level: SkillLevel) -> List[str]:
        """Get a recommended learning path for a category and skill level.
        
        Args:
            category: Learning category
            skill_level: Target skill level
            
        Returns:
            List of resource IDs in recommended order
        """
        resources = self.search_resources(category=category)
        
        # Sort by skill level progression
        level_order = [SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE, SkillLevel.ADVANCED, SkillLevel.EXPERT]
        target_index = level_order.index(skill_level)
        
        path = []
        for level in level_order[:target_index + 1]:
            level_resources = [r for r in resources if r.skill_level == level]
            level_resources.sort(key=lambda x: x.duration_minutes)
            path.extend([r.id for r in level_resources])
        
        return path
    
    def get_status(self) -> Dict[str, Any]:
        """Get education system status."""
        resource_counts = {}
        for resource in self.resources.values():
            category = resource.category
            if category not in resource_counts:
                resource_counts[category] = 0
            resource_counts[category] += 1
        
        sandbox_status = {}
        for sandbox in self.sandboxes.values():
            env_type = sandbox.environment_type
            if env_type not in sandbox_status:
                sandbox_status[env_type] = {"total": 0, "available": 0, "in_use": 0}
            sandbox_status[env_type]["total"] += 1
            sandbox_status[env_type][sandbox.status] += 1
        
        return {
            "total_resources": len(self.resources),
            "resources_by_category": resource_counts,
            "programming_languages": len(self.programming_modules),
            "blockchain_platforms": len(self.blockchain_modules),
            "sandboxes": sandbox_status
        }
    
    async def shutdown(self):
        """Shutdown education system."""
        self.logger.info("Shutting down education system...")
        
        # Stop all active sandbox sessions
        for sandbox in self.sandboxes.values():
            for session in sandbox.user_sessions.values():
                if session["status"] == "active":
                    await sandbox.stop_session(session["session_id"])
        
        self.logger.info("Education system shutdown complete")