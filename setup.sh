#!/usr/bin/env bash
# Quick setup script for lippytm ChatGPT.AI

set -e

echo "🤖 Setting up lippytm ChatGPT.AI..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Copy example config files
if [ ! -f "config.yaml" ]; then
    cp config.example.yaml config.yaml
    echo "✓ Created config.yaml from example"
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env from example"
fi

# Make scripts executable
chmod +x lippytm-chatgpt
chmod +x demo.py
echo "✓ Made scripts executable"
echo ""

# Test installation
echo "Testing installation..."
python3 test_installation.py
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.yaml or .env with your API keys"
echo "2. Run: ./lippytm-chatgpt --help"
echo "3. Try: ./demo.py"
echo "4. Start chatting: ./lippytm-chatgpt --backend echo"
echo ""
echo "For OpenAI backend, set your API key:"
echo "  export OPENAI_API_KEY='your-api-key-here'"
echo "  ./lippytm-chatgpt --backend openai"