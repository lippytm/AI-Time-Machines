"""Utility functions for lippytm ChatGPT.AI"""

import re
import json
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict


def format_message(message: str, max_width: int = 80) -> str:
    """Format message with proper line wrapping
    
    Args:
        message: Message to format
        max_width: Maximum line width
        
    Returns:
        Formatted message
    """
    words = message.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) > max_width:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)


def get_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """Get current timestamp as string
    
    Args:
        format_str: Timestamp format string
        
    Returns:
        Formatted timestamp string
    """
    return datetime.datetime.now().strftime(format_str)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe filesystem usage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing whitespace and periods
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    
    return sanitized


def parse_api_response(response: Dict[str, Any]) -> Optional[str]:
    """Parse API response and extract message content
    
    Args:
        response: API response dictionary
        
    Returns:
        Extracted message content or None
    """
    try:
        # OpenAI format
        if 'choices' in response and response['choices']:
            choice = response['choices'][0]
            if 'message' in choice:
                return choice['message'].get('content', '').strip()
            elif 'text' in choice:
                return choice['text'].strip()
        
        # Generic format
        if 'content' in response:
            return response['content'].strip()
        
        if 'text' in response:
            return response['text'].strip()
        
        return None
    
    except (KeyError, IndexError, TypeError):
        return None


def estimate_tokens(text: str) -> int:
    """Estimate token count for text (rough approximation)
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Rough estimation: ~4 characters per token for English text
    return len(text) // 4


def truncate_conversation_history(history: List[Dict], max_tokens: int = 4000) -> List[Dict]:
    """Truncate conversation history to fit within token limit
    
    Args:
        history: List of message dictionaries
        max_tokens: Maximum token limit
        
    Returns:
        Truncated history list
    """
    if not history:
        return []
    
    # Calculate tokens for each message
    message_tokens = []
    for msg in history:
        content = msg.get('content', '')
        tokens = estimate_tokens(content)
        message_tokens.append((msg, tokens))
    
    # Keep adding messages from the end until we hit the limit
    total_tokens = 0
    result = []
    
    for msg, tokens in reversed(message_tokens):
        if total_tokens + tokens > max_tokens:
            break
        total_tokens += tokens
        result.insert(0, msg)
    
    return result


def validate_api_key(api_key: str) -> bool:
    """Validate API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # OpenAI API key format: sk-...
    if api_key.startswith('sk-') and len(api_key) > 20:
        return True
    
    # Generic validation: non-empty string with reasonable length
    return 10 <= len(api_key.strip()) <= 200


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string with fallback
    
    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump object to JSON string with fallback
    
    Args:
        obj: Object to serialize
        default: Default JSON string if serialization fails
        
    Returns:
        JSON string or default value
    """
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return default


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown-formatted text
    
    Args:
        text: Input text with potential code blocks
        
    Returns:
        List of dictionaries with 'language' and 'code' keys
    """
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for language, code in matches:
        code_blocks.append({
            'language': language or 'text',
            'code': code.strip()
        })
    
    return code_blocks


def mask_sensitive_data(text: str) -> str:
    """Mask sensitive data in text for logging
    
    Args:
        text: Input text
        
    Returns:
        Text with sensitive data masked
    """
    # Mask API keys
    text = re.sub(r'sk-[a-zA-Z0-9]{20,}', 'sk-***MASKED***', text)
    
    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***EMAIL***', text)
    
    # Mask potential passwords/tokens (sequences of 16+ alphanumeric chars)
    text = re.sub(r'\b[A-Za-z0-9]{16,}\b', '***TOKEN***', text)
    
    return text


class ConversationExporter:
    """Export conversations to various formats"""
    
    @staticmethod
    def to_json(conversation_history: List, metadata: Optional[Dict] = None) -> str:
        """Export conversation to JSON format"""
        export_data = {
            'metadata': metadata or {},
            'export_timestamp': datetime.datetime.now().isoformat(),
            'conversation': []
        }
        
        for msg in conversation_history:
            if hasattr(msg, '__dict__'):
                # Convert dataclass to dict
                msg_dict = asdict(msg)
                # Convert datetime to string
                if 'timestamp' in msg_dict and hasattr(msg_dict['timestamp'], 'isoformat'):
                    msg_dict['timestamp'] = msg_dict['timestamp'].isoformat()
                export_data['conversation'].append(msg_dict)
            else:
                export_data['conversation'].append(msg)
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_markdown(conversation_history: List, metadata: Optional[Dict] = None) -> str:
        """Export conversation to Markdown format"""
        lines = ["# lippytm ChatGPT.AI Conversation Log", ""]
        
        if metadata:
            lines.extend(["## Metadata", ""])
            for key, value in metadata.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        lines.extend(["## Conversation", ""])
        
        for msg in conversation_history:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                role = msg.role.title()
                content = msg.content
                timestamp = ""
                
                if hasattr(msg, 'timestamp'):
                    timestamp = f" _{msg.timestamp.strftime('%H:%M:%S')}_"
                
                lines.append(f"### {role}{timestamp}")
                lines.append("")
                lines.append(content)
                lines.append("")
        
        return "\n".join(lines)