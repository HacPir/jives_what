#!/bin/bash

echo "🐳 Starting FamilyConnect Agents with Docker"
echo "============================================"

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Remove any existing images to force rebuild
echo "Cleaning up old images..."
docker rmi $(docker images -q -f "dangling=true") 2>/dev/null || true

# Set OpenAI API key if available
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OpenAI API key found"
    export OPENAI_API_KEY="$OPENAI_API_KEY"
else
    echo "⚠️  No OpenAI API key - agents will use local responses"
    export OPENAI_API_KEY=""
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up --build -d

# Wait for containers to start
echo "Waiting for containers to initialize..."
sleep 10

# Check container status
echo "Checking container status..."
docker-compose ps

# Test agent connectivity
echo "Testing agent connectivity..."

# Test Grace Agent
echo -n "Grace Agent (8001): "
if curl -s -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Healthy"
else
    echo "❌ Not responding"
fi

# Test Alex Agent
echo -n "Alex Agent (8002): "
if curl -s -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Healthy"
else
    echo "❌ Not responding"
fi

echo ""
echo "🎯 Agent Endpoints:"
echo "   Grace Agent: http://localhost:8001"
echo "   Alex Agent: http://localhost:8002"
echo ""
echo "📡 GenAI Integration:"
echo "   Both agents provide OpenAI-compatible endpoints"
echo "   Your GenAI software should now detect them automatically"
echo ""
echo "🔍 Test Commands:"
echo "   curl -X POST http://localhost:8001/v1/chat/completions \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"model\":\"grace-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'"
echo ""
echo "   curl -X POST http://localhost:8002/v1/chat/completions \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"model\":\"alex-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Status\"}]}'"
echo ""
echo "📊 View logs: docker-compose logs grace-agent"
echo "📊 View logs: docker-compose logs alex-agent"
echo "🛑 Stop agents: docker-compose down"