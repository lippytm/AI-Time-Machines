#!/usr/bin/env python3
"""Setup script for AI Time Machines."""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def setup_environment():
    """Set up environment configuration."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example) as f:
            content = f.read()
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your actual credentials")
        return False
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ .env.example not found")
        return False


def validate_configuration():
    """Validate basic configuration."""
    print("🔍 Validating configuration...")
    
    try:
        from src.ai_time_machines.config import config
        
        issues = []
        
        # Check GitHub token
        if not config.github.token or config.github.token == "your_github_personal_access_token_here":
            issues.append("GitHub token not configured")
        
        # Check OpenAI API key
        if not config.openai.api_key or config.openai.api_key == "your_openai_api_key_here":
            issues.append("OpenAI API key not configured")
        
        # Check email password
        if not config.email.password or config.email.password == "your_app_password_here":
            issues.append("Email password not configured")
        
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
            print("   Please update your .env file with actual credentials")
            return False
        else:
            print("✅ Configuration looks good")
            return True
            
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


def test_installation():
    """Test the installation."""
    print("🧪 Testing installation...")
    
    try:
        from src.ai_time_machines import AITimeMachines
        app = AITimeMachines()
        results = app.test_integrations()
        
        print("Test Results:")
        for service, result in results.items():
            status_emoji = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
            print(f"  {status_emoji} {service.title()}: {result['message']}")
        
        # Check if all tests passed
        all_passed = all(r["status"] in ["success", "warning"] for r in results.values())
        
        if all_passed:
            print("✅ Installation test completed successfully")
            return True
        else:
            print("⚠️  Some tests failed - check configuration and credentials")
            return False
            
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 AI Time Machines Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    env_setup = setup_environment()
    
    # Validate configuration
    if env_setup:
        config_valid = validate_configuration()
        
        # Test installation
        if config_valid:
            test_installation()
            print("\n🎉 Setup completed!")
            print("\nNext steps:")
            print("1. Try: python -m src.ai_time_machines --test")
            print("2. Process a query: python -m src.ai_time_machines --query 'Hello AI!'")
            print("3. Check repository health: python -m src.ai_time_machines --health")
        else:
            print("\n⚠️  Setup completed with configuration issues")
            print("Please update your .env file and run setup again")
    else:
        print("\n⚠️  Please configure your .env file and run setup again")


if __name__ == "__main__":
    main()