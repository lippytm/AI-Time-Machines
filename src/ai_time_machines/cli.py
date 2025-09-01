"""
Command Line Interface for AI-Time-Machines
"""

import asyncio
import argparse
import json
import sys
from typing import Dict, Any

from .config import load_config
from .core import TimeMachine, AgentCapability
from .integrations import Web3AIIntegration, RepositoryIntegration
from .agents import Web3AIAgent, RepositoryAgent, create_default_web3ai_agent, create_default_repository_agent


async def create_time_machine(config_name: str = "default"):
    """Create and configure a Time Machine"""
    config = load_config()
    machine_config = config.get_time_machine_config(config_name)
    
    if not machine_config:
        print(f"Time Machine configuration '{config_name}' not found")
        return None
        
    machine = TimeMachine(machine_config.machine_id)
    
    # Add integrations
    for integration_name, integration_config in config.integrations.items():
        if not integration_config.enabled:
            continue
            
        if "web3ai" in integration_name.lower():
            integration = Web3AIIntegration(integration_config)
        else:
            integration = RepositoryIntegration(integration_config)
            
        connected = await integration.connect()
        if connected:
            machine.add_integration(integration_name, integration)
            print(f"✓ Connected integration: {integration_name}")
        else:
            print(f"✗ Failed to connect integration: {integration_name}")
            
    return machine


async def cmd_status(args):
    """Show status of Time Machine and integrations"""
    machine = await create_time_machine(args.machine)
    if not machine:
        return
        
    print(f"\nTime Machine: {machine.machine_id}")
    print(f"Agents: {len(machine.agents)}")
    print(f"Integrations: {len(machine.integrations)}")
    
    print("\nIntegrations:")
    for name, integration in machine.integrations.items():
        try:
            healthy = await integration.health_check()
            status = "✓ Healthy" if healthy else "✗ Unhealthy"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: ✗ Error - {str(e)}")
            
    print("\nAgents:")
    for agent_id, agent in machine.agents.items():
        capabilities = list(agent.capabilities.keys())
        print(f"  {agent.name} ({agent_id}): {', '.join(capabilities)}")


async def cmd_deploy_agent(args):
    """Deploy an AI agent"""
    machine = await create_time_machine(args.machine)
    if not machine:
        return
        
    # Create appropriate agent based on type
    if args.type == "web3ai":
        agent = create_default_web3ai_agent(args.agent_id, args.name)
    elif args.type == "repository":
        agent = create_default_repository_agent(args.agent_id, args.name)
    else:
        print(f"Unknown agent type: {args.type}")
        return
        
    machine.register_agent(agent)
    print(f"✓ Deployed agent: {agent.name} ({agent.agent_id})")


async def cmd_execute_capability(args):
    """Execute a capability"""
    machine = await create_time_machine(args.machine)
    if not machine:
        return
        
    # Parse parameters
    parameters = {}
    if args.parameters:
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError:
            print("Error: Invalid JSON parameters")
            return
            
    try:
        result = await machine.execute_capability(
            args.capability,
            parameters,
            args.agent_id
        )
        print("Result:")
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error executing capability: {str(e)}")


async def cmd_list_capabilities(args):
    """List available capabilities"""
    machine = await create_time_machine(args.machine)
    if not machine:
        return
        
    print("Available capabilities:")
    capabilities = set()
    for agent in machine.agents.values():
        for cap_name, capability in agent.capabilities.items():
            if agent.can_execute(cap_name):
                status = "✓"
            else:
                status = "✗"
            capabilities.add((cap_name, capability.description, status, agent.name))
            
    for cap_name, description, status, agent_name in sorted(capabilities):
        print(f"  {status} {cap_name}: {description} (via {agent_name})")


def cmd_init_config(args):
    """Initialize configuration file"""
    config = load_config()
    
    # Add sample integrations
    config.create_web3ai_integration(
        "web3ai_main",
        web3ai_url="http://localhost:8080",
        blockchain_rpc="http://localhost:8545"
    )
    
    config.create_repository_integration(
        "github_main",
        "github",
        base_url="https://api.github.com"
    )
    
    config.save_config()
    print(f"✓ Configuration initialized at {config.config_file}")
    print("Edit the configuration file to add your API keys and URLs")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="AI-Time-Machines CLI")
    parser.add_argument("--machine", default="default", help="Time Machine ID")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Show Time Machine status")
    
    # Deploy agent command
    deploy_parser = subparsers.add_parser("deploy-agent", help="Deploy an AI agent")
    deploy_parser.add_argument("type", choices=["web3ai", "repository"], help="Agent type")
    deploy_parser.add_argument("agent_id", help="Agent ID")
    deploy_parser.add_argument("name", help="Agent name")
    
    # Execute capability command
    exec_parser = subparsers.add_parser("execute", help="Execute a capability")
    exec_parser.add_argument("capability", help="Capability name")
    exec_parser.add_argument("--parameters", help="JSON parameters")
    exec_parser.add_argument("--agent-id", help="Preferred agent ID")
    
    # List capabilities command
    subparsers.add_parser("list-capabilities", help="List available capabilities")
    
    # Init config command
    subparsers.add_parser("init-config", help="Initialize configuration file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    # Map commands to functions
    commands = {
        "status": cmd_status,
        "deploy-agent": cmd_deploy_agent,
        "execute": cmd_execute_capability,
        "list-capabilities": cmd_list_capabilities,
        "init-config": cmd_init_config,
    }
    
    if args.command in commands:
        if args.command == "init-config":
            commands[args.command](args)
        else:
            asyncio.run(commands[args.command](args))
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()