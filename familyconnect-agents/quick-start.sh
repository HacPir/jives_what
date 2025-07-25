#!/bin/bash
# Quick start script for FamilyConnect × GenAI OS integration

echo "🚀 FamilyConnect × GenAI OS Quick Start"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ] || [ ! -d "familyconnect-agents" ]; then
    echo "❌ Please run this script from your genai-agentos directory"
    echo "   Make sure you have both docker-compose.yml and familyconnect-agents/ folder"
    exit 1
fi

echo "📋 Prerequisites Check:"
echo "✅ In genai-agentos directory"
echo "✅ familyconnect-agents folder found"

# Check if FamilyConnect is running
echo ""
echo "🔍 Checking if FamilyConnect is running on port 5000..."
if curl -s -f "http://localhost:5000/api/agents/message" > /dev/null 2>&1; then
    echo "✅ FamilyConnect is running on port 5000"
else
    echo "⚠️  FamilyConnect not detected on port 5000"
    echo "   Please start your FamilyConnect app first:"
    echo "   - In Replit: npm run dev"
    echo "   - Locally: npm run dev"
    echo ""
    echo "   Press Enter when FamilyConnect is running..."
    read -r
fi

echo ""
echo "▶️  Step 1: Starting GenAI OS..."
docker compose up -d

echo ""
echo "⏳ Waiting for GenAI OS to be ready..."
sleep 15

echo ""
echo "▶️  Step 2: Starting FamilyConnect agents..."
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml up -d

echo ""
echo "⏳ Waiting for agents to be ready..."
sleep 10

echo ""
echo "📝 Step 3: Registering agents with GenAI OS..."
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml run --rm agent-registrar

echo ""
echo "🎉 Integration Complete!"
echo ""
echo "🎯 What's Available:"
echo "- GenAI OS Dashboard: http://localhost:3000"
echo "- GenAI OS API: http://localhost:8000"
echo "- Grace Agent: http://localhost:8001"
echo "- Alex Agent: http://localhost:8002"
echo "- FamilyConnect Backend: http://localhost:5000"
echo ""
echo "🧪 Test the Integration:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Look for Grace and Alex agents in the agent list"
echo "3. Send test messages to each agent"
echo ""
echo "📋 Logs:"
echo "- GenAI OS: docker compose logs -f"
echo "- FamilyConnect Agents: docker compose -f familyconnect-agents/docker-compose.familyconnect.yml logs -f"
echo ""
echo "🛑 Stop All Services:"
echo "- docker compose down"
echo "- docker compose -f familyconnect-agents/docker-compose.familyconnect.yml down"