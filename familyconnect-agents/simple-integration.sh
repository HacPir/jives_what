#!/bin/bash
# Simple integration script for FamilyConnect agents with GenAI OS

echo "🚀 Starting FamilyConnect Agent Integration"
echo "=========================================="

# Check if in genai-agentos directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from your genai-agentos directory"
    exit 1
fi

# Check if FamilyConnect agents directory exists
if [ ! -d "familyconnect-agents" ]; then
    echo "❌ familyconnect-agents directory not found"
    exit 1
fi

echo "📋 Integration Steps:"
echo "1. Make sure your FamilyConnect app is running on port 5000"
echo "2. Start GenAI OS: docker compose up -d"
echo "3. Start FamilyConnect agents: docker compose -f familyconnect-agents/docker-compose.familyconnect.yml up -d"
echo "4. Register agents with GenAI OS"

# Start the integration
echo ""
echo "▶️  Starting GenAI OS..."
docker compose up -d

echo ""
echo "⏳ Waiting for GenAI OS to be ready..."
sleep 10

echo ""
echo "▶️  Starting FamilyConnect agents..."
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml up -d

echo ""
echo "⏳ Waiting for agents to be ready..."
sleep 10

echo ""
echo "📝 Registering agents with GenAI OS..."
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml run --rm agent-registrar

echo ""
echo "✅ Integration complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Open GenAI OS dashboard: http://localhost:3000"
echo "2. Look for Grace and Alex agents in the agent list"
echo "3. Test the agents by sending messages"
echo ""
echo "📋 Service URLs:"
echo "- GenAI OS Dashboard: http://localhost:3000"
echo "- GenAI OS API: http://localhost:8000"
echo "- Grace Agent: http://localhost:8001"
echo "- Alex Agent: http://localhost:8002"
echo "- FamilyConnect Backend: http://localhost:5000"