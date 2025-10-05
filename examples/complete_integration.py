"""
Complete Integration Example: AI-Time-Machines working with multiple systems
This example demonstrates the complete integration workflow.
"""

import asyncio
import logging
from ai_time_machines import TimeMachine, Config
from ai_time_machines.integrations import Web3AIIntegration, RepositoryIntegration, IntegrationConfig
from ai_time_machines.agents import create_default_web3ai_agent, create_default_repository_agent

# Configure logging
logging.basicConfig(level=logging.INFO)


async def main():
    print("🌟 AI-Time-Machines Complete Integration Demo")
    print("=" * 50)
    
    # 1. Setup configuration
    print("\n1️⃣ Setting up configuration...")
    config = Config()
    
    # Add Web3AI integration
    web3ai_config = IntegrationConfig(
        name="demo_web3ai",
        enabled=True,
        timeout=30,
        config={
            "web3ai_url": "http://localhost:8080",
            "blockchain_rpc": "http://localhost:8545",
            "contract_addresses": {
                "AITimeToken": "0x1234567890123456789012345678901234567890"
            }
        }
    )
    
    # Add GitHub integration  
    github_config = IntegrationConfig(
        name="demo_github",
        enabled=True,
        timeout=30,
        config={
            "type": "github",
            "base_url": "https://api.github.com",
            "api_key": "demo_token"  # In real usage, use environment variable
        }
    )
    
    print("✓ Configuration prepared")
    
    # 2. Create Time Machine
    print("\n2️⃣ Creating Time Machine...")
    machine = TimeMachine("demo_machine")
    
    # Add integrations (they will fail to connect in demo, but that's OK)
    web3ai_integration = Web3AIIntegration(web3ai_config)
    github_integration = RepositoryIntegration(github_config)
    
    machine.add_integration("demo_web3ai", web3ai_integration)
    machine.add_integration("demo_github", github_integration)
    
    print("✓ Time Machine created with integrations")
    
    # 3. Deploy AI Agents
    print("\n3️⃣ Deploying AI Agents...")
    
    # Deploy Web3AI agent
    web3ai_agent = create_default_web3ai_agent("blockchain_agent", "Blockchain AI Agent")
    machine.register_agent(web3ai_agent)
    print("✓ Deployed Blockchain AI Agent")
    
    # Deploy Repository agent
    repo_agent = create_default_repository_agent("code_agent", "Code Analysis AI Agent")
    machine.register_agent(repo_agent)
    print("✓ Deployed Code Analysis AI Agent")
    
    # 4. Show system status
    print("\n4️⃣ System Status:")
    print(f"   Time Machine ID: {machine.machine_id}")
    print(f"   Agents: {len(machine.agents)}")
    print(f"   Integrations: {len(machine.integrations)}")
    
    print("\n   Registered Agents:")
    for agent_id, agent in machine.agents.items():
        capabilities = list(agent.capabilities.keys())
        print(f"     • {agent.name} ({agent_id})")
        print(f"       Capabilities: {', '.join(capabilities)}")
    
    # 5. Demonstrate cross-system workflow
    print("\n5️⃣ Cross-System AI Workflow Simulation:")
    print("   This workflow shows how AI-Time-Machines enables AI agents")
    print("   to work seamlessly across Web3AI and repository systems.")
    
    workflow_steps = [
        {
            "step": "Repository Analysis",
            "description": "AI agent analyzes code repository for improvement opportunities",
            "capability": "analyze_code",
            "parameters": {"repository": "owner/defi-project", "type": "security"}
        },
        {
            "step": "Smart Contract Generation", 
            "description": "AI agent generates optimized smart contract based on analysis",
            "capability": "deploy_contract",
            "parameters": {"contract_code": "optimized_contract_bytecode"}
        },
        {
            "step": "Integration Testing",
            "description": "AI agent tests contract integration with existing codebase", 
            "capability": "execute_transaction",
            "parameters": {"contract_name": "AITimeToken", "method": "test_integration"}
        },
        {
            "step": "Pull Request Creation",
            "description": "AI agent creates PR with improvements and integration",
            "capability": "create_pr", 
            "parameters": {"repository": "owner/defi-project", "title": "AI-optimized smart contract integration"}
        },
        {
            "step": "Cross-System Sync",
            "description": "AI agent syncs results between Web3AI and repository",
            "capability": "sync_data",
            "parameters": {"time_machine_id": "demo_machine", "data": {"workflow_results": "success"}}
        }
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n   Step {i}: {step['step']}")
        print(f"   Description: {step['description']}")
        print(f"   Capability: {step['capability']}")
        
        # In a real implementation, you would execute:
        # result = await machine.execute_capability(step['capability'], step['parameters'])
        print(f"   Status: ✓ Simulated (would execute with real integrations)")
    
    # 6. Show integration benefits
    print("\n6️⃣ Integration Benefits:")
    benefits = [
        "🔗 Unified AI agent management across multiple platforms",
        "🤖 Seamless data flow between Web3AI and repository systems", 
        "⚡ Automated workflows spanning blockchain and code development",
        "📈 Enhanced AI capabilities through cross-system integration",
        "🛠️ Extensible framework for adding new integrations",
        "🔄 Event-driven coordination between different AI systems"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    
    # 7. Next steps
    print("\n7️⃣ Next Steps for Real Implementation:")
    next_steps = [
        "Configure Web3AI instance URL and credentials",
        "Set up GitHub/GitLab API tokens", 
        "Customize agent capabilities for your specific use case",
        "Implement custom integrations for other systems",
        "Set up monitoring and logging for production use",
        "Deploy Time Machine in your infrastructure"
    ]
    
    for i, step in enumerate(next_steps, 1):
        print(f"   {i}. {step}")
    
    print("\n🎉 AI-Time-Machines Integration Demo Complete!")
    print("\nThis demo shows how AI-Time-Machines enables seamless integration")
    print("between Web3AI and repository systems, creating a unified AI ecosystem.")


async def show_configuration_example():
    """Show how to configure the system for real use"""
    print("\n" + "=" * 50)
    print("📝 Configuration Example for Production")
    print("=" * 50)
    
    print("""
# Environment Variables for Production:
export WEB3AI_URL=https://your-web3ai-instance.com
export BLOCKCHAIN_RPC=https://mainnet.infura.io/v3/your-project-id
export GITHUB_API_KEY=ghp_your_github_token
export PRIVATE_KEY=your_wallet_private_key

# ai_time_machines.json Configuration:
{
  "time_machines": {
    "production": {
      "machine_id": "production",
      "name": "Production Time Machine",
      "max_agents": 50
    }
  },
  "integrations": {
    "web3ai_prod": {
      "enabled": true,
      "config": {
        "web3ai_url": "${WEB3AI_URL}",
        "blockchain_rpc": "${BLOCKCHAIN_RPC}",
        "contract_addresses": {
          "MainContract": "0x...",
          "TokenContract": "0x..."
        }
      }
    },
    "github_prod": {
      "enabled": true,
      "config": {
        "base_url": "https://api.github.com",
        "api_key": "${GITHUB_API_KEY}"
      }
    }
  }
}
""")


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(show_configuration_example())