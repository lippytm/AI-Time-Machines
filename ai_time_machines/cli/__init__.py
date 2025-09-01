"""Command-line interface for AI Time Machines."""

import asyncio
import argparse
import json
from pathlib import Path

from ..core import initialize_system, get_system
from ..agents import AgentType
from ..education import ResourceType, SkillLevel


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AI Time Machines - Advanced AI Agent Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # System commands
    system_parser = subparsers.add_parser("system", help="System management")
    system_parser.add_argument("action", choices=["start", "stop", "status", "health"])
    system_parser.add_argument("--config", help="Configuration file path")
    
    # Agent commands
    agent_parser = subparsers.add_parser("agents", help="Agent management")
    agent_parser.add_argument("action", choices=["list", "status", "task"])
    agent_parser.add_argument("--type", choices=[t.value for t in AgentType], help="Agent type")
    agent_parser.add_argument("--task", help="Task definition (JSON)")
    
    # Education commands
    edu_parser = subparsers.add_parser("education", help="Education management")
    edu_parser.add_argument("action", choices=["list", "search", "sandbox"])
    edu_parser.add_argument("--category", help="Resource category")
    edu_parser.add_argument("--level", choices=[l.value for l in SkillLevel], help="Skill level")
    edu_parser.add_argument("--type", choices=[t.value for t in ResourceType], help="Resource type")
    
    # Learning commands
    learning_parser = subparsers.add_parser("learning", help="Learning management")
    learning_parser.add_argument("action", choices=["status", "train", "metrics"])
    learning_parser.add_argument("--agents", nargs="+", help="Agent IDs to train")
    learning_parser.add_argument("--algorithm", help="Learning algorithm to use")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "system":
            await handle_system_command(args)
        elif args.command == "agents":
            await handle_agent_command(args)
        elif args.command == "education":
            await handle_education_command(args)
        elif args.command == "learning":
            await handle_learning_command(args)
    except Exception as e:
        print(f"Error: {e}")


async def handle_system_command(args):
    """Handle system management commands."""
    if args.action == "start":
        print("Starting AI Time Machines system...")
        system = await initialize_system(args.config)
        print("System started successfully!")
        print(json.dumps(system.get_status(), indent=2))
        
    elif args.action == "status":
        system = get_system()
        status = system.get_status()
        print("System Status:")
        print(json.dumps(status, indent=2))
        
    elif args.action == "health":
        system = get_system()
        health = await system.health_check()
        print(f"System Health: {'HEALTHY' if health else 'UNHEALTHY'}")
        
    elif args.action == "stop":
        system = get_system()
        await system.shutdown()
        print("System stopped successfully!")


async def handle_agent_command(args):
    """Handle agent management commands."""
    system = get_system()
    agent_manager = system.components.get("agents")
    
    if not agent_manager:
        print("Agent system not initialized")
        return
    
    if args.action == "list":
        status = agent_manager.get_status()
        print("Agent Status:")
        print(json.dumps(status, indent=2))
        
    elif args.action == "status":
        status = agent_manager.get_status()
        print(f"Total Agents: {status['total_agents']}")
        for agent_type, counts in status['status_by_type'].items():
            print(f"  {agent_type}: {counts['total']} total, {counts['idle']} idle, {counts['active']} active")
            
    elif args.action == "task":
        if not args.task:
            print("Task definition required (--task)")
            return
            
        try:
            task_data = json.loads(args.task)
            agent_type = AgentType(args.type) if args.type else None
            result = await agent_manager.assign_task(task_data, agent_type)
            print("Task Result:")
            print(json.dumps(result, indent=2))
        except json.JSONDecodeError:
            print("Invalid task JSON format")
        except Exception as e:
            print(f"Task execution failed: {e}")


async def handle_education_command(args):
    """Handle education management commands."""
    system = get_system()
    education_manager = system.components.get("education")
    
    if not education_manager:
        print("Education system not initialized")
        return
    
    if args.action == "list":
        status = education_manager.get_status()
        print("Education System Status:")
        print(json.dumps(status, indent=2))
        
    elif args.action == "search":
        skill_level = SkillLevel(args.level) if args.level else None
        resource_type = ResourceType(args.type) if args.type else None
        
        resources = education_manager.search_resources(
            category=args.category,
            skill_level=skill_level,
            resource_type=resource_type
        )
        
        print(f"Found {len(resources)} resources:")
        for resource in resources[:10]:  # Show first 10
            print(f"  - {resource.title} ({resource.category}/{resource.skill_level.value})")
            
    elif args.action == "sandbox":
        env_type = args.type or "coding"
        sandbox_id = await education_manager.get_sandbox(env_type)
        
        if sandbox_id:
            print(f"Allocated sandbox: {sandbox_id}")
            # Start a demo session
            session_id = await education_manager.sandboxes[sandbox_id].start_session(
                "demo_user", {"environment": env_type}
            )
            print(f"Demo session started: {session_id}")
        else:
            print(f"No available sandboxes for environment: {env_type}")


async def handle_learning_command(args):
    """Handle learning management commands."""
    system = get_system()
    learning_manager = system.components.get("learning")
    
    if not learning_manager:
        print("Learning system not initialized")
        return
    
    if args.action == "status":
        status = learning_manager.get_status()
        print("Learning System Status:")
        print(json.dumps(status, indent=2))
        
    elif args.action == "metrics":
        metrics = learning_manager.get_learning_metrics()
        print("Learning Metrics:")
        print(json.dumps(metrics, indent=2))
        
    elif args.action == "train":
        if not args.agents:
            print("Agent IDs required (--agents)")
            return
            
        from ..learning import LearningAlgorithm
        algorithm = LearningAlgorithm.REINFORCEMENT_LEARNING
        if args.algorithm:
            try:
                algorithm = LearningAlgorithm(args.algorithm)
            except ValueError:
                print(f"Invalid algorithm: {args.algorithm}")
                return
        
        # Generate sample training experiences
        experiences = []
        for agent_id in args.agents:
            for _ in range(5):  # 5 experiences per agent
                exp = await learning_manager.generate_training_experience(
                    agent_id, "demonstration_task"
                )
                experiences.append(exp)
        
        session_id = await learning_manager.create_training_session(
            args.agents, algorithm, experiences
        )
        
        print(f"Training session created: {session_id}")
        print(f"Training {len(args.agents)} agents with {len(experiences)} experiences")


if __name__ == "__main__":
    asyncio.run(main())