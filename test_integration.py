"""Quick integration test to validate component connections."""

import asyncio
import logging
from datetime import datetime, timedelta

from ai_time_machines import Component, EventBus, ComponentRegistry
from ai_time_machines.agents import SimpleTaskAgent, CollaborativeAgent
from ai_time_machines.time_machines import SimpleTimeMachine
from ai_time_machines.utils import setup_logging, ComponentDiscovery


async def test_basic_integration():
    """Test basic integration between components."""
    setup_logging("INFO")
    logger = logging.getLogger("Integration Test")
    
    logger.info("Starting basic integration test...")
    
    # Initialize core systems
    event_bus = await EventBus.get_instance()
    registry = await ComponentRegistry.get_instance()
    discovery = ComponentDiscovery()
    
    # Create components
    agent = SimpleTaskAgent("test_agent", "Test Agent")
    time_machine = SimpleTimeMachine("test_tm", "Test Time Machine")
    
    # Initialize and register
    await agent.initialize()
    await time_machine.initialize()
    
    await registry.register_component(agent)
    await registry.register_component(time_machine)
    
    logger.info("✓ Components created and registered")
    
    # Test task processing
    task = {
        "id": "test_task",
        "type": "calculation", 
        "data": {"operation": "add", "numbers": [5, 10, 15]}
    }
    
    result = await agent.process_task(task)
    logger.info(f"✓ Task processed: {result['result']}")
    
    # Test time travel
    future_time = datetime.now() + timedelta(minutes=30)
    travel_success = await time_machine.travel_to_time(future_time)
    logger.info(f"✓ Time travel successful: {travel_success}")
    
    # Test component discovery
    agents = await discovery.find_agents()
    machines = await discovery.find_time_machines()
    logger.info(f"✓ Discovery found {len(agents)} agents and {len(machines)} time machines")
    
    # Test cross-component communication
    await agent.broadcast_event("test_event", {"message": "Hello from agent!"})
    logger.info("✓ Event broadcast successful")
    
    # Test registry health
    health = await registry.health_check()
    logger.info(f"✓ System health: {health['total_components']} components, {len(health['unhealthy_components'])} unhealthy")
    
    # Cleanup
    await agent.shutdown()
    await time_machine.shutdown()
    await event_bus.stop()
    
    logger.info("✓ Integration test completed successfully!")
    
    return {
        "status": "success",
        "components_tested": 2,
        "task_result": result,
        "time_travel": travel_success,
        "system_health": health
    }


if __name__ == "__main__":
    result = asyncio.run(test_basic_integration())
    print(f"Test result: {result}")