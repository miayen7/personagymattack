#!/bin/bash
# Install dependencies for PersonaGym-R AgentBeats

echo "📦 Installing dependencies..."
echo "================================"

# Upgrade pip
pip install --upgrade pip

# Install PersonaGym-R package
echo ""
echo "Installing PersonaGym-R..."
pip install -e .

# Install requirements
echo ""
echo "Installing AgentBeats dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "Now you can run: ./start_codespaces.sh"
