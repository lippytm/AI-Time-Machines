"""Command Line Interface for lippytm ChatGPT.AI"""

import click
import logging
import sys
from typing import Optional
from pathlib import Path

try:
    from colorama import init as colorama_init, Fore, Style
    COLORAMA_AVAILABLE = True
    colorama_init()
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback for no colorama
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

from lippytm_chatgpt.core import ChatGPTAI
from lippytm_chatgpt.config import ConfigManager
from lippytm_chatgpt.utils import format_message, get_timestamp


class ChatInterface:
    """Interactive chat interface for the AI bot"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize chat interface
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.config = config_manager.get_config_dict()
        self.ai_bot = ChatGPTAI(self.config)
        self.logger = logging.getLogger(__name__)
        
        # UI settings
        self.colorize = self.config.get('ui', {}).get('colorize_output', True) and COLORAMA_AVAILABLE
        self.show_timestamps = self.config.get('ui', {}).get('show_timestamps', True)
    
    def print_colored(self, text: str, color: str = "", style: str = ""):
        """Print colored text if colorama is available"""
        if self.colorize:
            print(f"{style}{color}{text}{Style.RESET_ALL}")
        else:
            print(text)
    
    def print_welcome(self):
        """Print welcome message"""
        welcome_text = f"""
╔══════════════════════════════════════════════════╗
║              lippytm ChatGPT.AI                 ║
║         Intelligent AI with Time Machines       ║
╚══════════════════════════════════════════════════╝

Backend: {self.ai_bot.ai_backend}
Model: {self.config.get('openai_model', 'N/A')}

Type 'help' for commands or 'quit' to exit.
        """
        self.print_colored(welcome_text, Fore.CYAN, Style.BRIGHT)
    
    def print_help(self):
        """Print help information"""
        help_text = """
Available commands:
  help        - Show this help message
  clear       - Clear conversation history
  config      - Show current configuration
  summary     - Show conversation summary
  save        - Save conversation to file
  quit/exit   - Exit the application

Just type your message to chat with the AI!
        """
        self.print_colored(help_text, Fore.YELLOW)
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands
        
        Args:
            command: Command string
            
        Returns:
            True if should continue, False if should exit
        """
        command = command.lower().strip()
        
        if command in ['quit', 'exit']:
            self.print_colored("Goodbye! Thanks for using lippytm ChatGPT.AI", Fore.GREEN)
            return False
        
        elif command == 'help':
            self.print_help()
        
        elif command == 'clear':
            self.ai_bot.clear_conversation()
            self.print_colored("Conversation history cleared.", Fore.GREEN)
        
        elif command == 'config':
            self.show_config()
        
        elif command == 'summary':
            self.show_summary()
        
        elif command == 'save':
            self.save_conversation()
        
        else:
            self.print_colored(f"Unknown command: {command}. Type 'help' for available commands.", Fore.RED)
        
        return True
    
    def show_config(self):
        """Show current configuration"""
        config_info = f"""
Current Configuration:
  Backend: {self.ai_bot.ai_backend}
  Model: {self.config.get('openai_model', 'N/A')}
  Max Tokens: {self.config.get('max_tokens', 'N/A')}
  Temperature: {self.config.get('temperature', 'N/A')}
  History Length: {self.config.get('max_conversation_history', 'N/A')}
        """
        self.print_colored(config_info, Fore.BLUE)
    
    def show_summary(self):
        """Show conversation summary"""
        summary = self.ai_bot.get_conversation_summary()
        summary_text = f"""
Conversation Summary:
  Total Messages: {summary['total_messages']}
  User Messages: {summary['user_messages']}
  Assistant Messages: {summary['assistant_messages']}
  Backend: {summary['backend']}
  Start Time: {summary['start_time'] or 'N/A'}
  Last Activity: {summary['last_activity'] or 'N/A'}
        """
        self.print_colored(summary_text, Fore.MAGENTA)
    
    def save_conversation(self):
        """Save conversation to file"""
        if not self.ai_bot.conversation_history:
            self.print_colored("No conversation to save.", Fore.YELLOW)
            return
        
        filename = f"conversation_{get_timestamp()}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("lippytm ChatGPT.AI Conversation Log\n")
                f.write("=" * 40 + "\n\n")
                
                for msg in self.ai_bot.conversation_history:
                    timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {msg.role.upper()}: {msg.content}\n\n")
            
            self.print_colored(f"Conversation saved to {filename}", Fore.GREEN)
        
        except Exception as e:
            self.print_colored(f"Failed to save conversation: {e}", Fore.RED)
    
    def run_interactive(self):
        """Run interactive chat session"""
        self.print_welcome()
        
        try:
            while True:
                # Get user input
                if self.colorize:
                    prompt = f"{Fore.GREEN}You: {Style.RESET_ALL}"
                else:
                    prompt = "You: "
                
                try:
                    user_input = input(prompt).strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    self.print_colored("Goodbye! Thanks for using lippytm ChatGPT.AI", Fore.GREEN)
                    break
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/') or user_input in ['help', 'quit', 'exit', 'clear', 'config', 'summary', 'save']:
                    command = user_input.lstrip('/')
                    if not self.handle_command(command):
                        break
                    continue
                
                # Generate AI response
                try:
                    self.print_colored("AI: ", Fore.BLUE, Style.BRIGHT, end="")
                    response = self.ai_bot.generate_response(user_input)
                    
                    if self.colorize:
                        print(f"{Fore.WHITE}{response}{Style.RESET_ALL}")
                    else:
                        print(response)
                
                except Exception as e:
                    self.logger.error(f"Error in chat: {e}")
                    self.print_colored(f"Error: {e}", Fore.RED)
                
                print()  # Add spacing
        
        except Exception as e:
            self.logger.error(f"Unexpected error in interactive mode: {e}")
            self.print_colored(f"An unexpected error occurred: {e}", Fore.RED)


@click.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Path to configuration file')
@click.option('--backend', '-b', type=click.Choice(['openai', 'transformers', 'echo']), help='AI backend to use')
@click.option('--model', '-m', help='Model to use (e.g., gpt-3.5-turbo)')
@click.option('--interactive', '-i', is_flag=True, default=True, help='Run in interactive mode')
@click.option('--message', help='Single message to process (non-interactive)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(config: Optional[str], backend: Optional[str], model: Optional[str], 
         interactive: bool, message: Optional[str], verbose: bool):
    """lippytm ChatGPT.AI - Intelligent AI bot with time machine capabilities"""
    
    # Setup logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        # Initialize configuration
        config_manager = ConfigManager(config)
        
        # Override config with CLI options
        if backend:
            config_manager.set('backend', backend)
        if model:
            config_manager.set('openai_model', model)
        
        # Validate configuration
        if not config_manager.validate_config():
            click.echo("Configuration validation failed. Please check your settings.", err=True)
            sys.exit(1)
        
        # Create chat interface
        chat_interface = ChatInterface(config_manager)
        
        if message:
            # Single message mode
            try:
                response = chat_interface.ai_bot.generate_response(message)
                click.echo(f"AI: {response}")
            except Exception as e:
                click.echo(f"Error: {e}", err=True)
                sys.exit(1)
        
        elif interactive:
            # Interactive mode
            chat_interface.run_interactive()
        
        else:
            click.echo("Please specify either --interactive or --message")
            sys.exit(1)
    
    except Exception as e:
        if verbose:
            logging.exception("Application error")
        click.echo(f"Application error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()