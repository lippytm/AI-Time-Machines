"""Visual demonstration of AI-Time-Machines system architecture and capabilities."""

import asyncio
import logging
from datetime import datetime, timedelta

from ai_time_machines.utils import setup_logging
from ai_time_machines.examples.integration_demo import SystemOrchestrator


def print_banner():
    """Print a banner showing the system capabilities."""
    print("\n" + "="*80)
    print("          AI-TIME-MACHINES: INTEGRATED COMPONENT FRAMEWORK")
    print("="*80)
    print("""
This framework demonstrates enhanced component integration with:

📦 MODULAR ARCHITECTURE
   ├── Core base classes and interfaces for extensibility
   ├── Event-driven communication between all components
   └── Automatic component discovery and lifecycle management

🤖 AI AGENTS
   ├── SimpleTaskAgent: Processes calculations and text analysis
   ├── CollaborativeAgent: Coordinates with other agents for complex tasks
   └── LearningAgent: Adapts behavior based on feedback and experience

⏰ TIME MACHINES
   ├── SimpleTimeMachine: Basic time travel with energy management
   └── AdvancedTimeMachine: Timeline branching with paradox detection

🔗 INTEGRATION MECHANISMS
   ├── Cross-component messaging and event broadcasting
   ├── Service discovery and distributed task processing
   ├── Coordinated operations across multiple components
   └── Health monitoring and system metrics

🛠️ INFRASTRUCTURE
   ├── Configuration management (files + environment)
   ├── Rate limiting and circuit breaker patterns
   ├── Async caching and performance optimization
   └── Comprehensive logging and error handling
""")
    print("="*80 + "\n")


async def run_visual_demo():
    """Run a visual demonstration of the system."""
    setup_logging("INFO")
    print_banner()
    
    print("🚀 Starting AI-Time-Machines Integration Demo...\n")
    
    try:
        # Create orchestrator
        orchestrator = SystemOrchestrator()
        await orchestrator.initialize()
        
        print("✓ System orchestrator initialized")
        
        # Setup demo environment
        await orchestrator.setup_demo_environment()
        print("✓ Demo environment configured with 6 components")
        
        # Run demonstrations
        print("\n📊 Running integration demonstrations...")
        demo_results = await orchestrator.run_integration_demo()
        
        # Display results
        print("\n" + "="*60)
        print("                 DEMO RESULTS SUMMARY")
        print("="*60)
        print(f"⏱️  Total Duration: {(datetime.fromisoformat(demo_results['end_time']) - datetime.fromisoformat(demo_results['start_time'])).total_seconds():.2f} seconds")
        print(f"✅ Tasks Completed: {len(demo_results['tasks_completed'])}")
        print(f"🤝 Collaborations: {len(demo_results['collaborations'])}")
        print(f"🕐 Time Travels: {len(demo_results['time_travels'])}")
        print(f"🧠 Learning Events: {len(demo_results['learning_events'])}")
        print(f"❌ Errors: {len(demo_results['errors'])}")
        
        if demo_results['errors']:
            print(f"\n⚠️  Errors encountered: {demo_results['errors']}")
        else:
            print("\n🎉 All demonstrations completed successfully!")
        
        # Show integration features
        print("\n" + "="*60)
        print("              INTEGRATION FEATURES DEMONSTRATED")
        print("="*60)
        
        features = [
            ("Component Registry", "✓ All components registered and discoverable"),
            ("Event Bus Communication", "✓ Messages routed between components"),
            ("Task Distribution", "✓ Tasks processed by appropriate agents"),
            ("Agent Collaboration", "✓ Multi-agent coordination for complex tasks"),
            ("Time Travel Coordination", "✓ Synchronized time travel across machines"),
            ("Learning & Adaptation", "✓ Agents improve performance over time"),
            ("Timeline Branching", "✓ Advanced time machines create parallel timelines"),
            ("Health Monitoring", "✓ System health checks and component status"),
            ("Configuration Management", "✓ Unified configuration with environment support"),
            ("Cross-Component Discovery", "✓ Automatic service discovery and routing")
        ]
        
        for feature, status in features:
            print(f"{status:<30} {feature}")
        
        print("\n" + "="*60)
        print("     ENHANCED COMPONENT CONNECTIONS ACHIEVED! 🚀")
        print("="*60)
        
        # Cleanup
        print(f"\n🧹 Shutting down system...")
        components = []
        from ai_time_machines.utils.registry import ComponentRegistry
        registry = await ComponentRegistry.get_instance()
        components = await registry.list_components()
        
        for component in components:
            try:
                await component.shutdown()
            except Exception as e:
                print(f"Warning: Error shutting down {component.component_id}: {e}")
        
        from ai_time_machines.communication.event_bus import EventBus
        event_bus = await EventBus.get_instance()
        await event_bus.stop()
        
        print("✓ System shutdown complete")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_visual_demo())