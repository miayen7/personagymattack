#!/bin/bash

# PersonaGym-R AgentBeats Deployment Script
# Quick deployment helper for AgentBeats platform

set -e

echo "🚀 PersonaGym-R AgentBeats Deployment Helper"
echo "=============================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

if ! command_exists docker; then
    echo "⚠️  Docker not found. Docker deployment will not be available."
    DOCKER_AVAILABLE=false
else
    echo "✅ Docker found"
    DOCKER_AVAILABLE=true
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python version: $PYTHON_VERSION"

echo ""
echo "Select deployment mode:"
echo "1) Local testing (run on localhost:8000)"
echo "2) Docker build and test"
echo "3) Deploy to Docker registry"
echo "4) Generate submission package"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🔧 Installing dependencies..."
        pip install -e .
        pip install -r agentbeats/requirements.txt
        
        echo ""
        echo "🚀 Starting green agent on http://localhost:8000"
        echo "Press Ctrl+C to stop"
        echo ""
        python -m agentbeats.green_agent
        ;;
    
    2)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "❌ Docker not available"
            exit 1
        fi
        
        echo ""
        echo "🐳 Building Docker image..."
        docker build -t personagym-green-agent:latest .
        
        echo ""
        echo "✅ Image built successfully!"
        echo ""
        echo "🧪 Testing image..."
        docker run -d -p 8000:8000 --name personagym-test personagym-green-agent:latest
        
        echo "Waiting for service to start..."
        sleep 5
        
        echo ""
        echo "Testing health endpoint..."
        curl -s http://localhost:8000/health | python -m json.tool
        
        echo ""
        echo "Testing agent card..."
        curl -s http://localhost:8000/a2a/card | python -m json.tool
        
        echo ""
        echo "🧹 Cleaning up test container..."
        docker stop personagym-test
        docker rm personagym-test
        
        echo ""
        echo "✅ Docker image is ready: personagym-green-agent:latest"
        ;;
    
    3)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "❌ Docker not available"
            exit 1
        fi
        
        echo ""
        read -p "Enter your Docker Hub username: " DOCKER_USERNAME
        read -p "Enter image tag [latest]: " IMAGE_TAG
        IMAGE_TAG=${IMAGE_TAG:-latest}
        
        echo ""
        echo "🏗️  Building image..."
        docker build -t personagym-green-agent:$IMAGE_TAG .
        
        echo ""
        echo "🏷️  Tagging image..."
        docker tag personagym-green-agent:$IMAGE_TAG $DOCKER_USERNAME/personagym-green-agent:$IMAGE_TAG
        
        echo ""
        echo "📤 Pushing to Docker Hub..."
        docker push $DOCKER_USERNAME/personagym-green-agent:$IMAGE_TAG
        
        echo ""
        echo "✅ Image pushed successfully!"
        echo "Image name: $DOCKER_USERNAME/personagym-green-agent:$IMAGE_TAG"
        echo ""
        echo "Use this image name when submitting to AgentBeats in Hosted Mode"
        ;;
    
    4)
        echo ""
        echo "📦 Generating submission package..."
        
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        PACKAGE_DIR="agentbeats_submission_$TIMESTAMP"
        
        mkdir -p "$PACKAGE_DIR"
        
        # Copy essential files
        echo "Copying files..."
        cp -r agentbeats "$PACKAGE_DIR/"
        cp -r src "$PACKAGE_DIR/"
        cp -r tasks "$PACKAGE_DIR/"
        cp pyproject.toml "$PACKAGE_DIR/"
        cp README.md "$PACKAGE_DIR/"
        cp AGENTBEATS_INTEGRATION.md "$PACKAGE_DIR/"
        cp Dockerfile "$PACKAGE_DIR/"
        
        # Create submission info
        cat > "$PACKAGE_DIR/SUBMISSION_INFO.txt" << EOF
PersonaGym-R AgentBeats Submission Package
=========================================

Generated: $(date)

Deployment Options:
-------------------

1. Remote Mode:
   - Deploy green agent on your server
   - Run: python -m agentbeats.green_agent
   - Submit URL: https://your-domain.com:8000

2. Docker Hosted Mode:
   - Build: docker build -t personagym-green-agent .
   - Push to registry (see AGENTBEATS_INTEGRATION.md)
   - Submit image name to AgentBeats

3. GitHub Mode:
   - Push this repository to GitHub
   - Submit repository URL to AgentBeats
   - Platform will clone and deploy

Required Information for Submission:
-----------------------------------
- Name: PersonaGym-R
- Type: Green Agent (Hosting/Evaluator)
- Version: 1.0.0
- Protocol: A2A-1.0
- Available Tasks: 6 persona scenarios
- Metrics: P (persona), B (break), S (safety), E (efficiency), R (overall)

Contact:
--------
- Email: sec+agentbeats@berkeley.edu
- GitHub: https://github.com/miayen7/personagym

Next Steps:
-----------
1. Review AGENTBEATS_INTEGRATION.md for detailed instructions
2. Choose your deployment mode
3. Test locally first
4. Submit to AgentBeats platform

Good luck! 🚀
EOF
        
        # Create archive
        tar -czf "$PACKAGE_DIR.tar.gz" "$PACKAGE_DIR"
        
        echo ""
        echo "✅ Submission package created!"
        echo "Directory: $PACKAGE_DIR"
        echo "Archive: $PACKAGE_DIR.tar.gz"
        echo ""
        echo "Next steps:"
        echo "1. Review $PACKAGE_DIR/SUBMISSION_INFO.txt"
        echo "2. Read $PACKAGE_DIR/AGENTBEATS_INTEGRATION.md"
        echo "3. Test locally or build Docker image"
        echo "4. Submit to AgentBeats platform"
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Done! 🎉"
