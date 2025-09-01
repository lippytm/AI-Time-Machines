# AI-Time-Machines

A modular framework for integrating AI Agents with Time Machine concepts, providing robust communication mechanisms and seamless component integration.

## Features

- **Modular Architecture**: Clean separation between agents, time machines, and communication systems
- **Event-Driven Communication**: Robust event bus for inter-component messaging
- **Component Registry**: Automatic discovery and management of system components
- **Configuration Management**: Flexible configuration system with environment support
- **Time Travel & Branching**: Advanced timeline management with paradox detection
- **Learning Agents**: AI agents that adapt and improve over time
- **Collaborative Processing**: Multi-agent coordination for complex tasks

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from ai_time_machines import Component, EventBus, ComponentRegistry
from ai_time_machines.agents import SimpleTaskAgent
from ai_time_machines.time_machines import SimpleTimeMachine

async def main():
    # Initialize core systems
    event_bus = await EventBus.get_instance()
    registry = await ComponentRegistry.get_instance()
    
    # Create and register components
    agent = SimpleTaskAgent("my_agent", "Calculator Agent")
    time_machine = SimpleTimeMachine("my_tm", "Basic Time Machine")
    
    await agent.initialize()
    await time_machine.initialize()
    
    await registry.register_component(agent)
    await registry.register_component(time_machine)
    
    # Process a task
    task = {
        "type": "calculation",
        "data": {"operation": "add", "numbers": [10, 20, 30]}
    }
    result = await agent.process_task(task)
    print(f"Task result: {result}")
    
    # Time travel
    from datetime import datetime, timedelta
    target_time = datetime.now() + timedelta(hours=1)
    success = await time_machine.travel_to_time(target_time)
    print(f"Time travel successful: {success}")
    
    # Cleanup
    await agent.shutdown()
    await time_machine.shutdown()
    await event_bus.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Running the Integration Demo

```bash
python -m ai_time_machines.examples.integration_demo
```

## Architecture

### Core Components

- **Component Base Classes**: Abstract interfaces and implementations for all system components
- **Event Bus**: Centralized message routing and event handling
- **Component Registry**: Service discovery and lifecycle management
- **Configuration Manager**: Unified configuration with file and environment support

### AI Agents

- **SimpleTaskAgent**: Basic task processing capabilities
- **CollaborativeAgent**: Multi-agent coordination and collaboration
- **LearningAgent**: Adaptive behavior based on feedback and experience

### Time Machines

- **SimpleTimeMachine**: Basic time travel with energy management
- **AdvancedTimeMachine**: Timeline branching and paradox detection

### Communication Features

- **Message Routing**: Intelligent message delivery between components
- **Event Broadcasting**: System-wide event notifications
- **Request-Response Patterns**: Synchronous communication support
- **Rate Limiting**: Built-in protection against message flooding

## Configuration

Create a `config.yaml` file:

```yaml
system:
  log_level: "INFO"
  event_bus_queue_size: 1000
  component_timeout: 30
  max_retries: 3
  enable_metrics: true

components:
  example_agent:
    type: "agent"
    name: "Example AI Agent"
    enabled: true
    parameters:
      model: "gpt-3.5-turbo"
      temperature: 0.7
      max_tokens: 1000

  example_time_machine:
    type: "time_machine"
    name: "Example Time Machine"
    enabled: true
    parameters:
      time_resolution: "seconds"
      max_time_range: "1 year"
      enable_branching: true
```

## Integration Patterns

### Component Discovery

```python
from ai_time_machines.utils import ComponentDiscovery

discovery = ComponentDiscovery()

# Find all agents
agents = await discovery.find_agents()

# Find specific agent types
calc_agents = await discovery.find_agents("calculator")

# Send task to best available agent
result = await discovery.send_task_to_best_agent(task)
```

### Event Handling

```python
from ai_time_machines.core import Component

class MyComponent(Component):
    async def _on_initialize(self):
        # Register event handlers
        self.register_event_handler("task_completed", self.handle_task_completion)
        self.register_event_handler("time_travel", self.handle_time_travel)
    
    async def handle_task_completion(self, message):
        print(f"Task completed: {message.payload}")
    
    async def handle_time_travel(self, message):
        print(f"Time travel event: {message.payload}")
```

### Cross-Component Communication

```python
# Send direct messages
await component.send_message(
    receiver_id="target_component",
    event_type="custom_request",
    payload={"data": "important_info"}
)

# Broadcast events
await component.broadcast_event(
    event_type="system_notification",
    payload={"message": "System update available"}
)
```

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Code Formatting

```bash
black ai_time_machines/
flake8 ai_time_machines/
```

### Type Checking

```bash
mypy ai_time_machines/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
