"""Complete example demonstrating AI Time Machines integration."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Import core components
from ai_time_machines.core.base import Component
from ai_time_machines.communication.event_bus import EventBus
from ai_time_machines.utils.registry import ComponentRegistry, ComponentDiscovery
from ai_time_machines.config.manager import ConfigManager, save_default_config
from ai_time_machines.utils.helpers import setup_logging

# Import example implementations
from ai_time_machines.agents.examples import SimpleTaskAgent, CollaborativeAgent, LearningAgent
from ai_time_machines.time_machines.examples import SimpleTimeMachine, AdvancedTimeMachine


class SystemOrchestrator(Component):
    """Orchestrates the entire AI Time Machines system."""
    
    def __init__(self):
        super().__init__(component_id="system_orchestrator", component_type="orchestrator")
        self.agents = {}
        self.time_machines = {}
        self.discovery = None
        
    async def _on_initialize(self) -> None:
        """Initialize the system orchestrator."""
        self.discovery = ComponentDiscovery()
        
        # Register for system events
        self.register_event_handler("component_registered", self._handle_component_registered)
        self.register_event_handler("task_request", self._handle_task_request)
        self.register_event_handler("time_travel_request", self._handle_time_travel_request)
    
    async def setup_demo_environment(self) -> None:
        """Set up a demonstration environment with various components."""
        self._logger.info("Setting up demo environment...")
        
        # Create and register agents
        simple_agent = SimpleTaskAgent("simple_agent_1", "Calculator Agent")
        collab_agent1 = CollaborativeAgent("collab_agent_1", "Research Agent")
        collab_agent2 = CollaborativeAgent("collab_agent_2", "Analysis Agent")
        learning_agent = LearningAgent("learning_agent_1", "Adaptive Agent")
        
        # Create and register time machines
        simple_tm = SimpleTimeMachine("simple_tm_1", "Basic Time Machine")
        advanced_tm = AdvancedTimeMachine("advanced_tm_1", "Quantum Time Machine")
        
        # Get registry and register all components
        registry = await ComponentRegistry.get_instance()
        
        components = [simple_agent, collab_agent1, collab_agent2, learning_agent, simple_tm, advanced_tm]
        
        for component in components:
            await component.initialize()
            await registry.register_component(component)
            
            if hasattr(component, 'agent_name'):
                self.agents[component.component_id] = component
            elif hasattr(component, 'machine_name'):
                self.time_machines[component.component_id] = component
        
        self._logger.info(f"Registered {len(components)} components")
    
    async def run_integration_demo(self) -> Dict[str, Any]:
        """Run a comprehensive demonstration of system integration."""
        demo_results = {
            "start_time": datetime.now().isoformat(),
            "tasks_completed": [],
            "time_travels": [],
            "collaborations": [],
            "learning_events": [],
            "errors": []
        }
        
        try:
            # Demo 1: Simple task processing
            self._logger.info("=== Demo 1: Simple Task Processing ===")
            task_results = await self._demo_simple_tasks()
            demo_results["tasks_completed"].extend(task_results)
            
            # Demo 2: Agent collaboration
            self._logger.info("=== Demo 2: Agent Collaboration ===")
            collab_results = await self._demo_collaboration()
            demo_results["collaborations"].extend(collab_results)
            
            # Demo 3: Time travel operations
            self._logger.info("=== Demo 3: Time Travel Operations ===")
            travel_results = await self._demo_time_travel()
            demo_results["time_travels"].extend(travel_results)
            
            # Demo 4: Learning and adaptation
            self._logger.info("=== Demo 4: Learning and Adaptation ===")
            learning_results = await self._demo_learning()
            demo_results["learning_events"].extend(learning_results)
            
            # Demo 5: Cross-component integration
            self._logger.info("=== Demo 5: Cross-Component Integration ===")
            integration_results = await self._demo_integration()
            demo_results["integration_events"] = integration_results
            
        except Exception as e:
            self._logger.error(f"Demo error: {e}")
            demo_results["errors"].append(str(e))
        
        demo_results["end_time"] = datetime.now().isoformat()
        return demo_results
    
    async def _demo_simple_tasks(self) -> list:
        """Demonstrate simple task processing."""
        results = []
        
        # Find a simple agent
        agents = await self.discovery.find_agents()
        simple_agents = [a for a in agents if isinstance(a, SimpleTaskAgent)]
        
        if not simple_agents:
            self._logger.warning("No simple agents available")
            return results
        
        agent = simple_agents[0]
        
        # Process various types of tasks
        tasks = [
            {"id": "calc_1", "type": "calculation", "data": {"operation": "add", "numbers": [10, 20, 30]}},
            {"id": "text_1", "type": "text_analysis", "data": {"text": "Hello world! This is a test sentence."}},
            {"id": "calc_2", "type": "calculation", "data": {"operation": "multiply", "numbers": [5, 6, 7]}},
        ]
        
        for task in tasks:
            try:
                result = await agent.process_task(task)
                results.append(result)
                self._logger.info(f"Task {task['id']} completed: {result['result']}")
            except Exception as e:
                self._logger.error(f"Task {task['id']} failed: {e}")
        
        return results
    
    async def _demo_collaboration(self) -> list:
        """Demonstrate agent collaboration."""
        results = []
        
        # Find collaborative agents
        agents = await self.discovery.find_agents()
        collab_agents = [a for a in agents if isinstance(a, CollaborativeAgent)]
        
        if len(collab_agents) < 2:
            self._logger.warning("Need at least 2 collaborative agents")
            return results
        
        agent = collab_agents[0]
        
        # Create a complex collaborative task
        complex_task = {
            "id": "complex_1",
            "type": "collaborative",
            "complexity": "high",
            "data": {
                "description": "Analyze large dataset and generate insights",
                "dataset_size": "1TB",
                "analysis_type": "machine_learning"
            }
        }
        
        try:
            result = await agent.process_task(complex_task)
            results.append(result)
            self._logger.info(f"Collaborative task completed: {result}")
        except Exception as e:
            self._logger.error(f"Collaborative task failed: {e}")
        
        return results
    
    async def _demo_time_travel(self) -> list:
        """Demonstrate time travel operations."""
        results = []
        
        # Find time machines
        machines = await self.discovery.find_time_machines()
        
        if not machines:
            self._logger.warning("No time machines available")
            return results
        
        # Test simple time travel
        simple_machines = [m for m in machines if isinstance(m, SimpleTimeMachine)]
        if simple_machines:
            machine = simple_machines[0]
            target_time = datetime.now() + timedelta(hours=1)
            
            try:
                success = await machine.travel_to_time(target_time)
                status = await machine.get_status()
                results.append({
                    "machine": machine.component_id,
                    "travel_success": success,
                    "target_time": target_time.isoformat(),
                    "status": status
                })
                self._logger.info(f"Time travel result: {success}, Status: {status}")
            except Exception as e:
                self._logger.error(f"Time travel failed: {e}")
        
        # Test advanced time travel with branching
        advanced_machines = [m for m in machines if isinstance(m, AdvancedTimeMachine)]
        if advanced_machines:
            machine = advanced_machines[0]
            
            try:
                # Create a timeline branch
                branch_point = datetime.now() + timedelta(minutes=30)
                branch_success = await machine.create_timeline_branch(branch_point, "demo_branch")
                
                # Switch to the new branch
                switch_success = await machine.switch_to_branch("demo_branch")
                
                # Get branch information
                branches = await machine.list_branches()
                
                results.append({
                    "machine": machine.component_id,
                    "branch_created": branch_success,
                    "branch_switched": switch_success,
                    "branches": branches
                })
                
                self._logger.info(f"Advanced time travel demo completed: {len(branches)} branches")
            except Exception as e:
                self._logger.error(f"Advanced time travel failed: {e}")
        
        return results
    
    async def _demo_learning(self) -> list:
        """Demonstrate learning and adaptation."""
        results = []
        
        # Find learning agents
        agents = await self.discovery.find_agents()
        learning_agents = [a for a in agents if isinstance(a, LearningAgent)]
        
        if not learning_agents:
            self._logger.warning("No learning agents available")
            return results
        
        agent = learning_agents[0]
        
        # Process multiple similar tasks to trigger learning
        tasks = [
            {"id": f"learn_{i}", "type": "optimization", "data": {"complexity": i}} 
            for i in range(1, 8)
        ]
        
        for task in tasks:
            try:
                result = await agent.process_task(task)
                
                # Provide feedback
                feedback = {
                    "type": "positive" if task["data"]["complexity"] < 5 else "negative",
                    "task_type": "optimization",
                    "rating": 1.0 - (task["data"]["complexity"] / 10.0),
                    "message": f"Task complexity {task['data']['complexity']} feedback"
                }
                
                await agent.learn_from_feedback(feedback)
                
                results.append({
                    "task": task,
                    "result": result,
                    "feedback": feedback
                })
                
            except Exception as e:
                self._logger.error(f"Learning task {task['id']} failed: {e}")
        
        # Get learning statistics
        try:
            stats = await agent.get_learning_statistics()
            results.append({"learning_statistics": stats})
            self._logger.info(f"Learning stats: {stats}")
        except Exception as e:
            self._logger.error(f"Failed to get learning stats: {e}")
        
        return results
    
    async def _demo_integration(self) -> dict:
        """Demonstrate cross-component integration."""
        integration_events = {
            "registry_health": {},
            "event_bus_stats": {},
            "component_interactions": []
        }
        
        try:
            # Check registry health
            registry = await ComponentRegistry.get_instance()
            health = await registry.health_check()
            integration_events["registry_health"] = health
            self._logger.info(f"Registry health: {health}")
            
            # Demonstrate event broadcasting
            await self.broadcast_event(
                "integration_test",
                {"message": "Testing cross-component communication", "timestamp": datetime.now().isoformat()}
            )
            
            # Coordinate time travel across all machines
            target_time = datetime.now() + timedelta(minutes=5)
            travel_results = await self.discovery.coordinate_time_travel(target_time)
            integration_events["coordinated_time_travel"] = travel_results
            self._logger.info(f"Coordinated time travel: {travel_results}")
            
            # Send task to best available agent
            test_task = {
                "id": "integration_task",
                "type": "integration_test",
                "data": {"source": "system_orchestrator"}
            }
            
            task_result = await self.discovery.send_task_to_best_agent(test_task)
            if task_result:
                integration_events["distributed_task"] = task_result
                self._logger.info(f"Distributed task result: {task_result}")
            
        except Exception as e:
            self._logger.error(f"Integration demo error: {e}")
            integration_events["error"] = str(e)
        
        return integration_events
    
    async def _handle_component_registered(self, message) -> None:
        """Handle component registration events."""
        component_id = message.payload.get("component_id")
        self._logger.info(f"Component registered: {component_id}")
    
    async def _handle_task_request(self, message) -> None:
        """Handle task requests from other components."""
        task = message.payload.get("task")
        self._logger.info(f"Task request received: {task}")
    
    async def _handle_time_travel_request(self, message) -> None:
        """Handle time travel requests."""
        target_time = message.payload.get("target_time")
        self._logger.info(f"Time travel request received: {target_time}")


async def main():
    """Main function to run the comprehensive demo."""
    # Setup logging
    setup_logging("INFO")
    logger = logging.getLogger("Demo")
    
    logger.info("Starting AI Time Machines Integration Demo")
    
    try:
        # Create default configuration
        save_default_config()
        
        # Initialize system components
        event_bus = await EventBus.get_instance()
        registry = await ComponentRegistry.get_instance()
        
        # Create and initialize orchestrator
        orchestrator = SystemOrchestrator()
        await orchestrator.initialize()
        await registry.register_component(orchestrator)
        
        # Setup demo environment
        await orchestrator.setup_demo_environment()
        
        # Run comprehensive demo
        demo_results = await orchestrator.run_integration_demo()
        
        logger.info("=== DEMO RESULTS ===")
        logger.info(f"Demo completed in {(datetime.fromisoformat(demo_results['end_time']) - datetime.fromisoformat(demo_results['start_time'])).total_seconds():.2f} seconds")
        logger.info(f"Tasks completed: {len(demo_results['tasks_completed'])}")
        logger.info(f"Collaborations: {len(demo_results['collaborations'])}")
        logger.info(f"Time travels: {len(demo_results['time_travels'])}")
        logger.info(f"Learning events: {len(demo_results['learning_events'])}")
        logger.info(f"Errors: {len(demo_results['errors'])}")
        
        if demo_results['errors']:
            logger.warning(f"Errors encountered: {demo_results['errors']}")
        
        # Final system health check
        final_health = await registry.health_check()
        logger.info(f"Final system health: {final_health}")
        
        # Cleanup
        logger.info("Shutting down system...")
        components = await registry.list_components()
        for component in components:
            try:
                await component.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down {component.component_id}: {e}")
        
        await event_bus.stop()
        
        logger.info("Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())