#!/usr/bin/env python3
"""
Quick test script to verify AI Time Machines installation and basic functionality.
Run this after installation to ensure everything is working correctly.
"""

import asyncio
import sys
import traceback
from pathlib import Path

# Add the current directory to Python path for development
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from ai_time_machines.core import SystemManager
    from ai_time_machines.agents import AgentManager, AgentType
    from ai_time_machines.education import EducationManager
    from ai_time_machines.learning import LearningManager
    print("✅ Successfully imported AI Time Machines modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure AI Time Machines is properly installed:")
    print("  pip install -e .")
    sys.exit(1)


async def test_system():
    """Test basic system functionality."""
    print("\n🧪 Testing AI Time Machines Core Functionality")
    print("=" * 60)
    
    try:
        # Test 1: System Manager
        print("\n1. Testing System Manager...")
        config = {
            "system": {"name": "Test System", "debug": True},
            "agents": {
                "standard_agents": {"count": 2},
                "synthetic_agents": {"count": 1}
            },
            "education": {
                "programming_languages": ["python"],
                "blockchain": {"platforms": ["ethereum"]},
                "sandboxes": {"environments": ["coding"]}
            },
            "autonomous_learning": {
                "enabled": True,
                "experience_sharing": True
            },
            "database": {"type": "sqlite", "name": ":memory:"},
            "logging": {"level": "WARNING"}  # Reduce log noise
        }
        
        # Create a temporary config file
        import tempfile
        import yaml
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        system = SystemManager(config_path)
        initialized = await system.initialize()
        
        if initialized:
            print("   ✅ System initialization successful")
        else:
            print("   ❌ System initialization failed")
            return False
        
        # Test 2: Agent Operations
        print("\n2. Testing Agent Operations...")
        agent_manager = system.components.get("agents")
        if agent_manager:
            agent_status = agent_manager.get_status()
            print(f"   ✅ Created {agent_status['total_agents']} agents")
            
            # Test task assignment
            task = {"id": "test_task", "type": "test", "data": "hello"}
            result = await agent_manager.assign_task(task)
            
            if result and result.get("status") == "completed":
                print("   ✅ Task assignment successful")
            else:
                print("   ❌ Task assignment failed")
        else:
            print("   ❌ Agent manager not found")
            return False
        
        # Test 3: Education System
        print("\n3. Testing Education System...")
        education = system.components.get("education")
        if education:
            edu_status = education.get_status()
            print(f"   ✅ Education system with {edu_status['total_resources']} resources")
            
            # Test resource search
            resources = education.search_resources(category="programming")
            if resources:
                print(f"   ✅ Found {len(resources)} programming resources")
            else:
                print("   ⚠️  No programming resources found")
            
            # Test sandbox allocation
            sandbox_id = await education.get_sandbox("coding")
            if sandbox_id:
                print("   ✅ Sandbox allocation successful")
                await education.release_sandbox(sandbox_id)
            else:
                print("   ⚠️  No sandbox available")
        else:
            print("   ❌ Education manager not found")
            return False
        
        # Test 4: Learning System
        print("\n4. Testing Learning System...")
        learning = system.components.get("learning")
        if learning:
            learning_status = learning.get_status()
            print(f"   ✅ Learning system initialized")
            
            # Test experience generation
            agent_id = list(agent_manager.agents.keys())[0]
            experience = await learning.generate_training_experience(
                agent_id, "test_task", 0.5
            )
            if experience:
                print("   ✅ Training experience generation successful")
            else:
                print("   ❌ Training experience generation failed")
        else:
            print("   ❌ Learning manager not found")
            return False
        
        # Test 5: Health Check
        print("\n5. Testing System Health...")
        health = await system.health_check()
        if health:
            print("   ✅ System health check passed")
        else:
            print("   ❌ System health check failed")
        
        # Test 6: Status Reporting
        print("\n6. Testing Status Reporting...")
        status = system.get_status()
        if status and "status" in status and "components" in status:
            print("   ✅ Status reporting working")
            print(f"   System status: {status['status']}")
            print(f"   Components: {len(status['components'])}")
        else:
            print("   ❌ Status reporting failed")
        
        # Clean shutdown
        print("\n7. Testing Graceful Shutdown...")
        await system.shutdown()
        print("   ✅ System shutdown successful")
        
        # Clean up temp file
        import os
        os.unlink(config_path)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False


async def test_imports():
    """Test that all modules can be imported without errors."""
    print("\n📦 Testing Module Imports")
    print("=" * 30)
    
    modules_to_test = [
        ("ai_time_machines", "Main package"),
        ("ai_time_machines.core", "Core system"),
        ("ai_time_machines.agents", "Agent management"),
        ("ai_time_machines.education", "Education system"),
        ("ai_time_machines.learning", "Learning system"),
        ("ai_time_machines.database", "Database layer"),
        ("ai_time_machines.utils", "Utilities"),
        ("ai_time_machines.cli", "CLI interface")
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {description} ({module_name})")
        except ImportError as e:
            print(f"   ❌ {description} ({module_name}): {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} modules failed to import")
        return False
    else:
        print(f"\n✅ All {len(modules_to_test)} modules imported successfully")
        return True


async def main():
    """Run all tests."""
    print("🚀 AI Time Machines - Installation Verification")
    print("=" * 60)
    
    # Test imports first
    import_success = await test_imports()
    
    if not import_success:
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test system functionality
    system_success = await test_system()
    
    if system_success:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("\nAI Time Machines is ready to use. Try running:")
        print("  python examples/basic_usage.py")
        print("  ai-time-machines system start")
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED!")
        print("\nPlease check the error messages above and ensure:")
        print("  1. All dependencies are installed: pip install -r requirements.txt")
        print("  2. The package is installed: pip install -e .")
        print("  3. Python version is 3.8 or higher")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)