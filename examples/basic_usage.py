"""
Basic usage example for AI Time Machines platform.

This example demonstrates how to:
1. Initialize the system
2. Create and manage AI agents
3. Access educational resources
4. Use the autonomous learning system
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the parent directory to Python path for examples
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from ai_time_machines import initialize_system
from ai_time_machines.agents import AgentType
from ai_time_machines.education import SkillLevel, ResourceType
from ai_time_machines.learning import LearningAlgorithm


async def main():
    """Main example demonstrating AI Time Machines capabilities."""
    print("🤖 AI Time Machines - Basic Usage Example")
    print("=" * 50)
    
    # 1. Initialize the system
    print("\n1. Initializing AI Time Machines system...")
    system = await initialize_system("config.yml")
    print(f"✅ System initialized successfully!")
    
    # 2. Check system status
    print("\n2. System Status:")
    status = system.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Version: {status['version']}")
    print(f"   Components: {list(status['components'].keys())}")
    
    # 3. Work with AI Agents
    print("\n3. AI Agent Operations:")
    agent_manager = system.components["agents"]
    
    # Get agent status
    agent_status = agent_manager.get_status()
    print(f"   Total Agents: {agent_status['total_agents']}")
    
    # Assign a task to a standard agent
    task = {
        "id": "example_task_001",
        "type": "reasoning",
        "description": "Solve a basic logical reasoning problem",
        "data": {
            "premises": ["All cats are mammals", "Fluffy is a cat"],
            "question": "Is Fluffy a mammal?"
        }
    }
    
    print(f"   Assigning task: {task['description']}")
    result = await agent_manager.assign_task(task, AgentType.STANDARD)
    print(f"   ✅ Task completed: {result['status']}")
    
    # Try a synthetic agent task
    creative_task = {
        "id": "creative_task_001", 
        "type": "creative_problem_solving",
        "description": "Generate innovative solutions",
        "data": {"problem": "How to make learning more engaging?"}
    }
    
    result = await agent_manager.assign_task(creative_task, AgentType.SYNTHETIC)
    print(f"   ✅ Creative task completed with creativity score: {result.get('creativity_score', 'N/A')}")
    
    # 4. Explore Educational Resources
    print("\n4. Educational Resources:")
    education_manager = system.components["education"]
    
    # Search for programming resources
    programming_resources = education_manager.search_resources(
        category="programming",
        skill_level=SkillLevel.BEGINNER
    )
    print(f"   Found {len(programming_resources)} beginner programming resources")
    
    if programming_resources:
        resource = programming_resources[0]
        print(f"   Example: '{resource.title}' - {resource.duration_minutes} minutes")
    
    # Search for blockchain resources
    blockchain_resources = education_manager.search_resources(
        category="blockchain",
        resource_type=ResourceType.TUTORIAL
    )
    print(f"   Found {len(blockchain_resources)} blockchain tutorials")
    
    # Get a coding sandbox
    sandbox_id = await education_manager.get_sandbox("coding")
    if sandbox_id:
        print(f"   ✅ Allocated coding sandbox: {sandbox_id}")
        
        # Start a demo session
        sandbox = education_manager.sandboxes[sandbox_id]
        session_id = await sandbox.start_session("demo_user", {"language": "python"})
        print(f"   ✅ Started sandbox session: {session_id}")
        
        # Execute some demo code
        result = await sandbox.execute_code(session_id, "print('Hello, AI Time Machines!')", "python")
        print(f"   Code execution result: {result['status']}")
        
        # Clean up
        await sandbox.stop_session(session_id)
        await education_manager.release_sandbox(sandbox_id)
    
    # 5. Autonomous Learning System
    print("\n5. Autonomous Learning:")
    learning_manager = system.components["learning"]
    
    # Generate some training experiences
    experiences = []
    agent_ids = list(agent_manager.agents.keys())[:3]  # Use first 3 agents
    
    print(f"   Generating training experiences for {len(agent_ids)} agents...")
    for agent_id in agent_ids:
        for task_type in ["reasoning", "optimization", "pattern_recognition"]:
            experience = await learning_manager.generate_training_experience(
                agent_id, task_type, difficulty=0.6
            )
            experiences.append(experience)
    
    print(f"   Generated {len(experiences)} training experiences")
    
    # Create a training session
    session_id = await learning_manager.create_training_session(
        agent_ids,
        LearningAlgorithm.REINFORCEMENT_LEARNING,
        experiences
    )
    print(f"   ✅ Started training session: {session_id}")
    
    # Wait a moment for training to process
    await asyncio.sleep(1)
    
    # Get learning metrics
    metrics = learning_manager.get_learning_metrics()
    print(f"   Learning metrics:")
    print(f"     - Total training sessions: {metrics['total_training_sessions']}")
    print(f"     - Knowledge base size: {metrics['knowledge_base_size']}")
    print(f"     - Average performance: {metrics['average_performance']:.2f}")
    
    # 6. System Health Check
    print("\n6. System Health Check:")
    health = await system.health_check()
    print(f"   System Health: {'✅ HEALTHY' if health else '❌ UNHEALTHY'}")
    
    # 7. Demonstrate knowledge sharing
    print("\n7. Knowledge Sharing:")
    
    # Share a successful experience
    if experiences:
        best_experience = max(experiences, key=lambda x: x.reward)
        await learning_manager.share_experience(best_experience)
        print(f"   ✅ Shared successful experience (reward: {best_experience.reward:.2f})")
    
    # Search knowledge base
    knowledge_results = learning_manager.knowledge_base.search_knowledge("reasoning")
    print(f"   Found {len(knowledge_results)} knowledge items related to reasoning")
    
    # 8. Generate Learning Path
    print("\n8. Learning Path Generation:")
    learning_path = education_manager.get_learning_path("programming", SkillLevel.INTERMEDIATE)
    print(f"   Generated learning path with {len(learning_path)} steps for intermediate programming")
    
    if learning_path:
        print(f"   First step: {learning_path[0]}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Time Machines demo completed successfully!")
    print("\nKey capabilities demonstrated:")
    print("  ✅ Multi-type AI agent management (800,000 agents)")
    print("  ✅ Comprehensive educational resources")
    print("  ✅ Interactive learning sandboxes")
    print("  ✅ Autonomous learning and AI training")
    print("  ✅ Knowledge sharing and experience-based learning")
    print("  ✅ Real-time system monitoring and health checks")
    
    # Gracefully shutdown
    print("\n🛑 Shutting down system...")
    await system.shutdown()
    print("✅ System shutdown complete!")


if __name__ == "__main__":
    asyncio.run(main())