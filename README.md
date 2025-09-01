# AI-Time-Machines

Adding AI Agents to everything with Time Machines

## lippytm ChatGPT.AI

A modular, extensible ChatGPT-like AI bot with time machine capabilities. This intelligent assistant can help users with various tasks, provide insightful responses, and engage in meaningful conversations while leveraging knowledge from different time periods.

### Features

- **Multi-Backend Support**: Works with OpenAI API, local Transformers models, or echo mode
- **Modular Architecture**: Extensible design for easy enhancement and customization
- **Interactive CLI**: Beautiful command-line interface with colored output
- **Configuration Management**: Flexible configuration via files or environment variables
- **Conversation Management**: Save, clear, and export conversation history
- **Time Machine Capabilities**: Historical context and knowledge integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

### Quick Start

1. **Installation**:
   ```bash
   git clone https://github.com/lippytm/AI-Time-Machines.git
   cd AI-Time-Machines
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Configuration**:
   ```bash
   # Copy example configuration
   cp config.example.yaml config.yaml
   cp .env.example .env
   
   # Edit config.yaml or .env with your API keys and preferences
   ```

3. **Run the Bot**:
   ```bash
   # Interactive mode (default)
   lippytm-chatgpt
   
   # Single message
   lippytm-chatgpt --message "Hello, how are you?"
   
   # Specify backend
   lippytm-chatgpt --backend openai --model gpt-4
   ```

### Configuration

#### Configuration File (config.yaml)

```yaml
backend: "openai"
openai_api_key: "your-api-key"
openai_model: "gpt-3.5-turbo"
max_tokens: 1000
temperature: 0.7
system_prompt: "You are lippytm ChatGPT.AI..."
```

#### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key"
export LIPPYTM_BACKEND="openai"
export LIPPYTM_MODEL="gpt-3.5-turbo"
```

### Usage Examples

#### Interactive Chat
```bash
$ lippytm-chatgpt
╔══════════════════════════════════════════════════╗
║              lippytm ChatGPT.AI                 ║
║         Intelligent AI with Time Machines       ║
╚══════════════════════════════════════════════════╝

You: Hello! What can you help me with?
AI: Hello! I'm lippytm ChatGPT.AI, your intelligent assistant with time machine capabilities...

You: /help
Available commands:
  help        - Show this help message
  clear       - Clear conversation history
  config      - Show current configuration
  summary     - Show conversation summary
  save        - Save conversation to file
  quit/exit   - Exit the application
```

#### Command Line Options
```bash
# Show help
lippytm-chatgpt --help

# Use specific backend
lippytm-chatgpt --backend transformers

# Single message with verbose output
lippytm-chatgpt --message "Explain quantum computing" --verbose

# Use custom config file
lippytm-chatgpt --config /path/to/config.yaml
```

### Architecture

```
lippytm_chatgpt/
├── __init__.py          # Package initialization
├── cli.py               # Command-line interface
├── core/                # Core AI functionality
│   └── __init__.py      # ChatGPT AI implementation
├── config/              # Configuration management
│   └── __init__.py      # ConfigManager class
├── ui/                  # User interface components
└── utils/               # Utility functions
    └── __init__.py      # Helper functions
```

### Supported Backends

#### OpenAI Backend
- Uses OpenAI's GPT models (GPT-3.5, GPT-4)
- Requires OpenAI API key
- Best performance and capabilities

#### Transformers Backend
- Uses local Hugging Face models
- No API key required
- Works offline
- Examples: DialoGPT, BlenderBot

#### Echo Backend
- Simple testing/demo mode
- No external dependencies
- Returns formatted echo responses

### API Reference

#### ChatGPTAI Class

```python
from lippytm_chatgpt.core import ChatGPTAI
from lippytm_chatgpt.config import ConfigManager

# Initialize
config_manager = ConfigManager()
ai_bot = ChatGPTAI(config_manager.get_config_dict())

# Generate response
response = ai_bot.generate_response("Hello!")

# Get conversation summary
summary = ai_bot.get_conversation_summary()

# Clear conversation
ai_bot.clear_conversation()
```

#### ConfigManager Class

```python
from lippytm_chatgpt.config import ConfigManager

# Initialize with custom config
config = ConfigManager("path/to/config.yaml")

# Get configuration values
backend = config.get("backend")
model = config.get("openai_model")

# Set configuration values
config.set("temperature", 0.8)

# Save configuration
config.save_config("new_config.yaml")
```

### Advanced Features

#### Custom System Prompts
```yaml
system_prompt: |
  You are a specialized assistant for software development.
  Focus on providing accurate, well-documented code examples
  and best practices for modern development.
```

#### Conversation Export
```bash
# In interactive mode, use the 'save' command
You: /save
Conversation saved to conversation_20231201_143022.txt
```

#### Multiple Configurations
```bash
# Development config
lippytm-chatgpt --config configs/dev.yaml

# Production config  
lippytm-chatgpt --config configs/prod.yaml
```

### Development

#### Project Structure
- **Core Module**: Main AI logic and conversation management
- **Config Module**: Configuration loading and management
- **CLI Module**: Command-line interface and interactive chat
- **Utils Module**: Helper functions and utilities

#### Adding New Backends
1. Extend the `ChatGPTAI` class in `core/__init__.py`
2. Add backend-specific configuration options
3. Implement the generation method for your backend
4. Update documentation

#### Running Tests
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests (if test infrastructure exists)
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### Support

For support, issues, or questions:
- Create an issue on GitHub
- Check the documentation
- Review configuration examples

### Changelog

#### v1.0.0
- Initial release
- Multi-backend support (OpenAI, Transformers, Echo)
- Interactive CLI interface
- Configuration management system
- Conversation history and export
- Comprehensive documentation
