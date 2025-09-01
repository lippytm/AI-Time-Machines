"""Core AI bot implementation for lippytm ChatGPT.AI"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


@dataclass
class Message:
    """Represents a conversation message"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class ChatGPTAI:
    """Main ChatGPT AI bot implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the ChatGPT AI bot
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config
        self.conversation_history: List[Message] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI backend
        self.ai_backend = self._initialize_backend()
        
        # Set system prompt
        self.system_prompt = config.get('system_prompt', 
            "You are lippytm ChatGPT.AI, an intelligent assistant with time machine capabilities. "
            "You can help users with various tasks and provide insightful responses.")
    
    def _initialize_backend(self) -> str:
        """Initialize the AI backend based on configuration"""
        backend_type = self.config.get('backend', 'openai')
        
        if backend_type == 'openai' and OPENAI_AVAILABLE:
            api_key = self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                self.logger.info("Initialized OpenAI backend")
                return 'openai'
            else:
                self.logger.warning("OpenAI API key not found, falling back to local model")
        
        if TRANSFORMERS_AVAILABLE:
            self.logger.info("Initialized local Transformers backend")
            self._init_local_model()
            return 'transformers'
        
        self.logger.warning("No AI backend available, using echo mode")
        return 'echo'
    
    def _init_local_model(self):
        """Initialize local transformer model"""
        try:
            model_name = self.config.get('local_model', 'microsoft/DialoGPT-medium')
            self.local_pipeline = pipeline(
                'conversational',
                model=model_name,
                device=-1  # Use CPU
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize local model: {e}")
            self.ai_backend = 'echo'
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.conversation_history.append(message)
        
        # Keep only last N messages to manage context length
        max_history = self.config.get('max_conversation_history', 50)
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]
    
    def generate_response(self, user_input: str) -> str:
        """Generate AI response to user input"""
        # Add user message to history
        self.add_message('user', user_input)
        
        try:
            if self.ai_backend == 'openai':
                response = self._generate_openai_response(user_input)
            elif self.ai_backend == 'transformers':
                response = self._generate_transformers_response(user_input)
            else:
                response = self._generate_echo_response(user_input)
            
            # Add assistant response to history
            self.add_message('assistant', response)
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            error_response = "I apologize, but I encountered an error while processing your request. Please try again."
            self.add_message('assistant', error_response)
            return error_response
    
    def _generate_openai_response(self, user_input: str) -> str:
        """Generate response using OpenAI API"""
        messages = []
        
        # Add system prompt
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Add conversation history
        for msg in self.conversation_history[-10:]:  # Last 10 messages
            if msg.role in ['user', 'assistant']:
                messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = openai.ChatCompletion.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=self.config.get('max_tokens', 1000),
                temperature=self.config.get('temperature', 0.7)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    def _generate_transformers_response(self, user_input: str) -> str:
        """Generate response using local transformer model"""
        try:
            # For conversational pipeline, we need to maintain conversation state
            if not hasattr(self, '_conversation'):
                from transformers import Conversation
                self._conversation = Conversation()
            
            self._conversation.add_user_input(user_input)
            response = self.local_pipeline(self._conversation)
            return response.generated_responses[-1]
        except Exception as e:
            self.logger.error(f"Transformers error: {e}")
            raise
    
    def _generate_echo_response(self, user_input: str) -> str:
        """Simple echo response for testing/fallback"""
        responses = [
            f"I understand you said: '{user_input}'. I'm currently in echo mode.",
            f"Thank you for your message: '{user_input}'. Please configure an AI backend for intelligent responses.",
            f"Message received: '{user_input}'. I'm lippytm ChatGPT.AI in demonstration mode."
        ]
        return responses[len(self.conversation_history) % len(responses)]
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        if hasattr(self, '_conversation'):
            delattr(self, '_conversation')
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        return {
            'total_messages': len(self.conversation_history),
            'user_messages': len([m for m in self.conversation_history if m.role == 'user']),
            'assistant_messages': len([m for m in self.conversation_history if m.role == 'assistant']),
            'backend': self.ai_backend,
            'start_time': self.conversation_history[0].timestamp.isoformat() if self.conversation_history else None,
            'last_activity': self.conversation_history[-1].timestamp.isoformat() if self.conversation_history else None
        }