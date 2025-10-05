"""
Example: Basic Web3AI Integration with AI-Time-Machines
This example shows how to set up and use the Web3AI integration.
"""

import asyncio
from ai_time_machines import TimeMachine, Config
from ai_time_machines.integrations import Web3AIIntegration, IntegrationConfig
from ai_time_machines.agents import create_default_web3ai_agent


async def main():
    print("🚀 Starting Web3AI Integration Example")
    
    # 1. Create configuration
    config = Config()
    
    # Create Web3AI integration configuration
    web3ai_config = config.create_web3ai_integration(
        "web3ai_example",
        web3ai_url="http://localhost:8080",  # Replace with your Web3AI URL
        blockchain_rpc="http://localhost:8545",  # Replace with your blockchain RPC
        contract_addresses={
            "MyToken": "0x1234567890123456789012345678901234567890",
            "MyDApp": "0x0987654321098765432109876543210987654321"
        }
    )
    
    print(f"✓ Created Web3AI integration: {web3ai_config.name}")
    
    # 2. Create Time Machine
    machine = TimeMachine("web3ai_example")
    
    # 3. Set up Web3AI integration
    web3ai_integration = Web3AIIntegration(web3ai_config)
    
    # Try to connect (this will fail if Web3AI is not running, but that's OK for demo)
    try:
        connected = await web3ai_integration.connect()
        if connected:
            print("✓ Connected to Web3AI successfully")
            machine.add_integration("web3ai_example", web3ai_integration)
        else:
            print("⚠️  Could not connect to Web3AI (this is normal if not running)")
            # Add integration anyway for demonstration
            machine.add_integration("web3ai_example", web3ai_integration)
    except Exception as e:
        print(f"⚠️  Web3AI connection failed: {str(e)} (continuing with demo)")
        machine.add_integration("web3ai_example", web3ai_integration)
    
    # 4. Create and register Web3AI agent
    web3ai_agent = create_default_web3ai_agent("web3ai_demo", "Web3AI Demo Agent")
    machine.register_agent(web3ai_agent)
    
    print(f"✓ Registered agent: {web3ai_agent.name}")
    
    # 5. Show available capabilities
    print("\n📋 Available capabilities:")
    for agent in machine.agents.values():
        for cap_name, capability in agent.capabilities.items():
            status = "✓" if agent.can_execute(cap_name) else "✗"
            print(f"  {status} {cap_name}: {capability.description}")
    
    # 6. Example: Deploy a smart contract (simulation)
    print("\n🔧 Example: Deploying a smart contract")
    
    contract_code = """
    pragma solidity ^0.8.0;
    
    contract ExampleToken {
        string public name = "AI Time Machine Token";
        string public symbol = "AITM";
        uint256 public totalSupply = 1000000;
        
        mapping(address => uint256) public balances;
        
        constructor() {
            balances[msg.sender] = totalSupply;
        }
    }
    """
    
    try:
        result = await machine.execute_capability("deploy_contract", {
            "contract_code": contract_code,
            "constructor_args": []
        })
        
        print(f"✓ Contract deployment result: {result}")
        
    except Exception as e:
        print(f"⚠️  Contract deployment simulation failed: {str(e)}")
        print("   This is expected if Web3AI is not running")
    
    # 7. Example: Execute a transaction (simulation)
    print("\n💸 Example: Executing a transaction")
    
    try:
        result = await machine.execute_capability("execute_transaction", {
            "contract_name": "MyToken",
            "method": "transfer",
            "args": ["0x742d35Cc6634C0532925a3b8D404E682DB4e6e54", 100]
        })
        
        print(f"✓ Transaction result: {result}")
        
    except Exception as e:
        print(f"⚠️  Transaction simulation failed: {str(e)}")
        print("   This is expected if Web3AI is not running")
    
    # 8. Example: Analyze blockchain data (simulation)
    print("\n🔍 Example: Analyzing blockchain data")
    
    try:
        result = await machine.execute_capability("analyze_blockchain", {
            "type": "transaction_analysis",
            "target": "0x1234567890123456789012345678901234567890"
        })
        
        print(f"✓ Analysis result: {result}")
        
    except Exception as e:
        print(f"⚠️  Blockchain analysis simulation failed: {str(e)}")
        print("   This is expected if Web3AI is not running")
    
    # 9. Cleanup
    try:
        await web3ai_integration.disconnect()
        print("✓ Disconnected from Web3AI")
    except:
        pass
    
    print("\n🎉 Web3AI integration example completed!")
    print("\nTo run with a real Web3AI instance:")
    print("1. Start your Web3AI server on http://localhost:8080")
    print("2. Update the web3ai_url in the configuration")
    print("3. Run this example again")


if __name__ == "__main__":
    asyncio.run(main())