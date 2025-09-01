#!/usr/bin/env python3
"""
Demonstration script for lippytm ChatGPT.AI
Shows various features and capabilities of the bot
"""

import sys
import os
import time

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from lippytm_chatgpt.config import ConfigManager
from lippytm_chatgpt.core import ChatGPTAI

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    HAS_COLOR = True
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""
    HAS_COLOR = False


def print_colored(text, color="", style=""):
    """Print colored text if available"""
    if HAS_COLOR:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print_colored(f"  {title}", Fore.CYAN, Style.BRIGHT)
    print("="*60)


def demo_basic_conversation():
    """Demonstrate basic conversation"""
    print_section("Basic Conversation Demo")
    
    config_manager = ConfigManager()
    ai_bot = ChatGPTAI(config_manager.get_config_dict())
    
    print_colored(f"Backend: {ai_bot.ai_backend}", Fore.YELLOW)
    print()
    
    demo_messages = [
        "Hello! What is lippytm ChatGPT.AI?",
        "Tell me about time machines in science fiction",
        "What year was the first computer invented?",
        "How might AI change in the future?"
    ]
    
    for msg in demo_messages:
        print_colored(f"User: {msg}", Fore.GREEN)
        response = ai_bot.generate_response(msg)
        print_colored(f"AI: {response}", Fore.BLUE)
        print()
        time.sleep(1)  # Brief pause for readability
    
    return ai_bot


def demo_conversation_management(ai_bot):
    """Demonstrate conversation management features"""
    print_section("Conversation Management Demo")
    
    # Show conversation summary
    summary = ai_bot.get_conversation_summary()
    print_colored("Conversation Summary:", Fore.MAGENTA, Style.BRIGHT)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print()
    
    # Add a few more messages
    ai_bot.generate_response("Save this conversation for later")
    ai_bot.generate_response("Clear history when done")
    
    # Show updated summary
    summary = ai_bot.get_conversation_summary()
    print_colored(f"Updated: {summary['total_messages']} total messages", Fore.YELLOW)
    print()


def demo_configuration():
    """Demonstrate configuration features"""
    print_section("Configuration Demo")
    
    config_manager = ConfigManager()
    
    print_colored("Current Configuration:", Fore.CYAN, Style.BRIGHT)
    config = config_manager.get_config_dict()
    
    important_settings = [
        'backend', 'openai_model', 'max_tokens', 'temperature', 
        'max_conversation_history', 'system_prompt'
    ]
    
    for setting in important_settings:
        value = config.get(setting, "Not set")
        if setting == 'system_prompt' and len(str(value)) > 100:
            value = str(value)[:100] + "..."
        print(f"  {setting}: {value}")
    print()
    
    # Demonstrate dynamic configuration
    print_colored("Dynamic Configuration Changes:", Fore.YELLOW, Style.BRIGHT)
    config_manager.set('temperature', 0.9)
    config_manager.set('max_tokens', 500)
    print("  ✓ Updated temperature to 0.9")
    print("  ✓ Updated max_tokens to 500")
    print()


def demo_time_machine_features():
    """Demonstrate time machine themed features"""
    print_section("Time Machine Features Demo")
    
    # Create config with time machine system prompt
    time_machine_config = {
        'backend': 'echo',
        'system_prompt': (
            "You are lippytm ChatGPT.AI, an AI with time machine capabilities. "
            "You can discuss historical events, predict future trends, and provide "
            "perspectives from different time periods. You have knowledge spanning "
            "from ancient history to speculative future scenarios."
        ),
        'max_tokens': 1000,
        'temperature': 0.8
    }
    
    time_bot = ChatGPTAI(time_machine_config)
    
    time_messages = [
        "Take me to ancient Rome. What would daily life be like?",
        "Fast forward to the year 2050. How might cities look?",
        "What was the most important invention of the 20th century?",
        "If you could prevent one historical disaster, which would it be?"
    ]
    
    for msg in time_messages:
        print_colored(f"Time Traveler: {msg}", Fore.MAGENTA)
        response = time_bot.generate_response(msg)
        print_colored(f"Time Machine AI: {response}", Fore.CYAN)
        print()
        time.sleep(1)


def demo_error_handling():
    """Demonstrate error handling"""
    print_section("Error Handling Demo")
    
    config_manager = ConfigManager()
    ai_bot = ChatGPTAI(config_manager.get_config_dict())
    
    print_colored("Testing error handling with various scenarios:", Fore.YELLOW)
    
    # Test with empty input
    try:
        response = ai_bot.generate_response("")
        print(f"  ✓ Empty input handled: '{response[:50]}...'")
    except Exception as e:
        print(f"  ✗ Empty input error: {e}")
    
    # Test with very long input
    try:
        long_input = "This is a very long message. " * 100
        response = ai_bot.generate_response(long_input)
        print(f"  ✓ Long input handled: '{response[:50]}...'")
    except Exception as e:
        print(f"  ✗ Long input error: {e}")
    
    print()


def demo_utilities():
    """Demonstrate utility functions"""
    print_section("Utility Functions Demo")
    
    from lippytm_chatgpt.utils import (
        format_message, get_timestamp, estimate_tokens,
        validate_api_key, extract_code_blocks
    )
    
    # Test message formatting
    long_text = "This is a very long message that should be wrapped properly to demonstrate the formatting utility function working correctly."
    formatted = format_message(long_text, max_width=40)
    print_colored("Message Formatting:", Fore.GREEN, Style.BRIGHT)
    print(f"Original: {long_text}")
    print(f"Formatted:\n{formatted}")
    print()
    
    # Test timestamp
    timestamp = get_timestamp()
    print_colored(f"Current timestamp: {timestamp}", Fore.YELLOW)
    
    # Test token estimation
    tokens = estimate_tokens(long_text)
    print_colored(f"Estimated tokens: {tokens}", Fore.BLUE)
    
    # Test API key validation
    test_keys = ["sk-1234567890abcdef1234567890", "invalid", ""]
    for key in test_keys:
        valid = validate_api_key(key)
        print(f"Key '{key[:10]}...': {'✓' if valid else '✗'}")
    
    print()


def main():
    """Run the complete demonstration"""
    print_colored("🤖 lippytm ChatGPT.AI - Comprehensive Demonstration", Fore.WHITE, Style.BRIGHT)
    print_colored("=" * 60, Fore.WHITE)
    
    try:
        # Run all demonstrations
        ai_bot = demo_basic_conversation()
        demo_conversation_management(ai_bot)
        demo_configuration()
        demo_time_machine_features()
        demo_error_handling()
        demo_utilities()
        
        print_section("Demonstration Complete")
        print_colored("✨ All features demonstrated successfully!", Fore.GREEN, Style.BRIGHT)
        print_colored("🚀 lippytm ChatGPT.AI is ready for use!", Fore.CYAN, Style.BRIGHT)
        
        print("\nNext steps:")
        print("1. Configure your API keys in config.yaml or .env")
        print("2. Run: ./lippytm-chatgpt --backend openai")
        print("3. Start chatting with your AI assistant!")
        
    except Exception as e:
        print_colored(f"❌ Demonstration failed: {e}", Fore.RED, Style.BRIGHT)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())