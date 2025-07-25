#!/bin/bash

echo "Starting FamilyConnect Agents for GenAI OS"
echo "=========================================="

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)/agents
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"

# Install dependencies
echo "Installing dependencies..."
pip install -r agents/requirements.txt

# Start Grace agent
echo "Starting Grace agent on port 8001..."
cd agents
python3 standalone_grace_agent.py &
GRACE_PID=$!
echo "Grace agent started with PID: $GRACE_PID"

# Start Alex agent  
echo "Starting Alex agent on port 8002..."
python3 standalone_alex_agent.py &
ALEX_PID=$!
echo "Alex agent started with PID: $ALEX_PID"

# Wait for agents to initialize
echo "Waiting for agents to initialize..."
sleep 10

# Health check
echo "Checking agent health..."
curl -s http://localhost:8001/health > /dev/null && echo "✅ Grace agent healthy" || echo "❌ Grace agent not responding"
curl -s http://localhost:8002/health > /dev/null && echo "✅ Alex agent healthy" || echo "❌ Alex agent not responding"

echo ""
echo "🎯 FamilyConnect Agents Ready!"
echo "Grace Agent: http://localhost:8001"
echo "Alex Agent: http://localhost:8002"
echo ""
echo "GenAI OS can now discover and use these agents"
echo "Press Ctrl+C to stop all agents"

# Keep running
wait $GRACE_PID $ALEX_PID
