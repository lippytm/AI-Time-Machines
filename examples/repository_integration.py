"""
Example: Repository Integration with AI-Time-Machines
This example shows how to set up and use repository integration for code analysis and PR creation.
"""

import asyncio
from ai_time_machines import TimeMachine, Config
from ai_time_machines.integrations import RepositoryIntegration
from ai_time_machines.agents import create_default_repository_agent


async def main():
    print("📁 Starting Repository Integration Example")
    
    # 1. Create configuration
    config = Config()
    
    # Create GitHub integration configuration
    github_config = config.create_repository_integration(
        "github_example",
        "github",
        base_url="https://api.github.com",
        # Note: In real usage, set GITHUB_API_KEY environment variable
        api_key="your_github_token_here"  # Replace with your token
    )
    
    print(f"✓ Created GitHub integration: {github_config.name}")
    
    # 2. Create Time Machine
    machine = TimeMachine("repo_example")
    
    # 3. Set up repository integration
    repo_integration = RepositoryIntegration(github_config)
    
    # Try to connect (this will fail without a valid token, but that's OK for demo)
    try:
        connected = await repo_integration.connect()
        if connected:
            print("✓ Connected to GitHub successfully")
            machine.add_integration("github_example", repo_integration)
        else:
            print("⚠️  Could not connect to GitHub (check your API token)")
            # Add integration anyway for demonstration
            machine.add_integration("github_example", repo_integration)
    except Exception as e:
        print(f"⚠️  GitHub connection failed: {str(e)} (continuing with demo)")
        machine.add_integration("github_example", repo_integration)
    
    # 4. Create and register repository agent
    repo_agent = create_default_repository_agent("repo_demo", "Repository Demo Agent")
    machine.register_agent(repo_agent)
    
    print(f"✓ Registered agent: {repo_agent.name}")
    
    # 5. Show available capabilities
    print("\n📋 Available capabilities:")
    for agent in machine.agents.values():
        for cap_name, capability in agent.capabilities.items():
            status = "✓" if agent.can_execute(cap_name) else "✗"
            print(f"  {status} {cap_name}: {capability.description}")
    
    # 6. Example: Analyze code in a repository (simulation)
    print("\n🔍 Example: Analyzing code in a repository")
    
    try:
        result = await machine.execute_capability("analyze_code", {
            "repository": "octocat/Hello-World",  # Public repo for testing
            "type": "security"
        })
        
        print(f"✓ Code analysis result: {result}")
        
    except Exception as e:
        print(f"⚠️  Code analysis simulation failed: {str(e)}")
        print("   This is expected without a valid GitHub token")
    
    # 7. Example: Create a pull request (simulation)
    print("\n🔄 Example: Creating a pull request")
    
    try:
        result = await machine.execute_capability("create_pr", {
            "repository": "your-username/your-repo",  # Replace with your repo
            "title": "AI-generated improvements from Time Machine",
            "description": "This PR was created by an AI agent from AI-Time-Machines",
            "source_branch": "ai-improvements",
            "target_branch": "main"
        })
        
        print(f"✓ Pull request result: {result}")
        
    except Exception as e:
        print(f"⚠️  Pull request simulation failed: {str(e)}")
        print("   This is expected without a valid GitHub token and repository")
    
    # 8. Example: Sync repository (simulation)
    print("\n🔄 Example: Syncing with repository")
    
    try:
        result = await machine.execute_capability("sync_repository", {
            "repository": "your-username/your-repo",
            "type": "pull"
        })
        
        print(f"✓ Repository sync result: {result}")
        
    except Exception as e:
        print(f"⚠️  Repository sync simulation failed: {str(e)}")
        print("   This is expected without a valid GitHub token")
    
    # 9. Example: Deploy AI agent to repository (simulation)
    print("\n🚀 Example: Deploying AI agent to repository")
    
    try:
        result = await machine.execute_capability("deploy_ai_to_repo", {
            "repository": "your-username/your-repo",
            "deployment_type": "github_action",
            "agent_config": {
                "triggers": ["push", "pull_request"],
                "capabilities": ["analyze_code", "create_pr"]
            }
        })
        
        print(f"✓ AI deployment result: {result}")
        
    except Exception as e:
        print(f"⚠️  AI deployment simulation failed: {str(e)}")
        print("   This is expected without a valid GitHub token")
    
    # 10. Cleanup
    try:
        await repo_integration.disconnect()
        print("✓ Disconnected from GitHub")
    except:
        pass
    
    print("\n🎉 Repository integration example completed!")
    print("\nTo run with a real GitHub integration:")
    print("1. Get a GitHub personal access token")
    print("2. Set GITHUB_API_KEY environment variable")
    print("3. Update repository names in the examples")
    print("4. Run this example again")


async def demonstrate_cross_integration():
    """Demonstrate how AI-Time-Machines can work across multiple integrations"""
    print("\n🌐 Cross-Integration Example")
    
    config = Config()
    machine = TimeMachine("cross_integration_demo")
    
    # Set up multiple integrations
    github_config = config.create_repository_integration("github", "github")
    web3ai_config = config.create_web3ai_integration("web3ai")
    
    # Add integrations to machine
    github_integration = RepositoryIntegration(github_config)
    machine.add_integration("github", github_integration)
    
    # Create agents for different purposes
    repo_agent = create_default_repository_agent("repo_agent", "Repository Agent")
    machine.register_agent(repo_agent)
    
    print("✓ Set up cross-integration environment")
    
    # Simulate a workflow that uses both integrations
    print("📋 Simulated cross-integration workflow:")
    print("  1. Analyze repository code")
    print("  2. Deploy improvements as smart contract")
    print("  3. Create PR with integration details")
    print("  4. Sync results back to Web3AI")
    
    # This would be the actual implementation in a real scenario
    workflow_steps = [
        "analyze_code",
        "deploy_contract", 
        "create_pr",
        "sync_data"
    ]
    
    for step in workflow_steps:
        print(f"  ✓ Step: {step} (simulated)")
    
    print("🔗 Cross-integration workflow completed!")


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(demonstrate_cross_integration())