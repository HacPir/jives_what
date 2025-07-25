#!/bin/bash

echo "🚀 Quick Deploy to GenAI AgentOS"
echo "================================="

# Check if GenAI AgentOS is running
echo "🔍 Checking GenAI AgentOS availability..."
if curl -s -f http://localhost:3000/health > /dev/null; then
    echo "✅ GenAI AgentOS is running"
else
    echo "❌ GenAI AgentOS is not running at http://localhost:3000"
    echo "   Please start GenAI AgentOS first"
    exit 1
fi

# Install Python dependencies if needed
if ! python3 -c "import fastapi, uvicorn, httpx" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Deploy Grace Agent
echo "🤖 Deploying Grace Agent..."
curl -s -X POST http://localhost:3000/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grace",
    "description": "Warm, patient elderly companion AI agent",
    "type": "elderly_companion",
    "url": "http://localhost:8001",
    "capabilities": ["emotional_support", "health_monitoring", "companionship"],
    "metadata": {
      "personality": "warm_grandmother",
      "target_audience": "elderly_users",
      "communication_style": "patient_caring"
    }
  }' | python3 -m json.tool

# Deploy Alex Agent
echo "🤖 Deploying Alex Agent..."
curl -s -X POST http://localhost:3000/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex",
    "description": "Professional family coordinator AI agent",
    "type": "family_coordinator",
    "url": "http://localhost:8002",
    "capabilities": ["care_coordination", "family_management", "health_tracking"],
    "metadata": {
      "personality": "professional_coordinator",
      "target_audience": "caregivers_family",
      "communication_style": "efficient_organized"
    }
  }' | python3 -m json.tool

echo ""
echo "🎉 Deployment complete!"
echo "   Check your GenAI AgentOS dashboard for the deployed agents"
echo "   You can now test them through the FamilyConnect interface"