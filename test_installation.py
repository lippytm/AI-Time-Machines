#!/usr/bin/env python3
"""Quick test script for lippytm ChatGPT.AI"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from lippytm_chatgpt.config import ConfigManager
    from lippytm_chatgpt.core import ChatGPTAI
    
    print("✓ lippytm ChatGPT.AI modules imported successfully")
    
    # Test configuration
    config_manager = ConfigManager()
    print("✓ Configuration manager initialized")
    
    # Test AI bot initialization
    ai_bot = ChatGPTAI(config_manager.get_config_dict())
    print(f"✓ AI bot initialized with backend: {ai_bot.ai_backend}")
    
    # Test response generation
    test_message = "Hello, this is a test message."
    response = ai_bot.generate_response(test_message)
    print(f"✓ Response generated: {response[:50]}...")
    
    # Test conversation summary
    summary = ai_bot.get_conversation_summary()
    print(f"✓ Conversation summary: {summary['total_messages']} messages")
    
    print("\n🎉 All tests passed! lippytm ChatGPT.AI is working correctly.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Test failed: {e}")
    sys.exit(1)