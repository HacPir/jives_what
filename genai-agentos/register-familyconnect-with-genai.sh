#!/bin/bash
# FamilyConnect Agent Registration Script for GenAI OS
# This script registers Grace and Alex agents with your GenAI OS

echo "🚀 FamilyConnect Agent Registration for GenAI OS"
echo "================================================"

# Check if GenAI CLI is available
if ! command -v genai &> /dev/null; then
    echo "❌ GenAI CLI not found. Please install it first:"
    echo "   cd /path/to/genai-agentos/cli"
    echo "   ./install_cli.sh"
    exit 1
fi

# Check if user is logged in
echo "📋 Checking authentication..."
if ! genai list_agents &> /dev/null; then
    echo "❌ Not logged in to GenAI OS. Please login first:"
    echo "   genai login -u <username> -p <password>"
    echo "   Or signup: genai signup -u <username>"
    exit 1
fi

echo "✅ Authentication successful"

# Register Grace Agent
echo "📝 Registering Grace agent..."
GRACE_OUTPUT=$(genai register_agent --name "Grace" --description "FamilyConnect elderly companion - warm, caring AI for seniors")
echo "$GRACE_OUTPUT"

# Register Alex Agent  
echo "📝 Registering Alex agent..."
ALEX_OUTPUT=$(genai register_agent --name "Alex" --description "FamilyConnect family coordinator - professional care management")
echo "$ALEX_OUTPUT"

echo "✅ Agent registration complete!"
echo ""
echo "🎯 Next steps:"
echo "1. The agent files have been created in the 'agents/' directory"
echo "2. Update the JWT tokens in the agent files"
echo "3. Set up virtual environments for each agent:"
echo "   cd agents/Grace && uv venv && uv sync"
echo "   cd agents/Alex && uv venv && uv sync"
echo "4. Run the agents:"
echo "   genai run_agents"
echo ""
echo "📋 Make sure FamilyConnect is running on port 5000 before starting agents"
