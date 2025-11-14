#!/bin/bash
# Start script for GitHub Codespaces

echo "🚀 Starting PersonaGym-R AgentBeats Controller..."
echo "================================================"
echo ""
echo "This will start the earthshaker controller with your green agent."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Set environment variables
export HOST=${HOST:-"0.0.0.0"}
export AGENT_PORT=${AGENT_PORT:-8000}

echo "📡 Controller will listen on $HOST:$AGENT_PORT"
echo ""
echo "Once started, your agent will be accessible at:"
echo "https://<your-codespace-name>-8000.app.github.dev"
echo ""
echo "Starting controller..."
echo "================================================"
echo ""

# Start the controller
agentbeats run_ctrl
