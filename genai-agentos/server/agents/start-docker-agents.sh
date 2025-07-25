#!/bin/bash

echo "🚀 Starting FamilyConnect Docker Agents"
echo "======================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OpenAI API key not set. Agents will use local AI responses."
    echo "   Export OPENAI_API_KEY to enable full AI integration."
else
    echo "✅ OpenAI API key detected"
fi

# Build and start the containers
echo "🏗️  Building Docker containers..."
docker-compose up --build -d

# Wait for agents to be ready
echo "⏳ Waiting for agents to start..."
sleep 10

# Check agent health
echo "🏥 Checking agent health..."

# Grace Agent
if curl -s -f http://localhost:8001/health > /dev/null; then
    echo "✅ Grace Agent running on port 8001"
else
    echo "❌ Grace Agent not responding"
fi

# Alex Agent
if curl -s -f http://localhost:8002/health > /dev/null; then
    echo "✅ Alex Agent running on port 8002"
else
    echo "❌ Alex Agent not responding"
fi

# Agent Manager
if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "✅ Agent Manager running on port 8000"
else
    echo "❌ Agent Manager not responding"
fi

echo ""
echo "🎉 Docker agents are running!"
echo "   Grace Agent: http://localhost:8001"
echo "   Alex Agent: http://localhost:8002"
echo "   Agent Manager: http://localhost:8000"
echo ""
echo "💡 Test the agents:"
echo "   curl -X POST http://localhost:8001/v1/chat/completions -H 'Content-Type: application/json' -d '{\"model\":\"grace-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello Grace!\"}]}'"
echo ""
echo "🔗 Integration:"
echo "   Your GenAI dashboard can now communicate with these containerized agents"
echo "   The agents are fully independent and OpenAI-compatible"