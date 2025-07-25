#!/bin/bash

# Start FamilyConnect GenAI Agents
echo "Starting FamilyConnect GenAI Agents..."

# Create agents directory if it doesn't exist
mkdir -p familyconnect-agents/logs

# Start Grace Agent
echo "Starting Grace Agent on port 8001..."
cd familyconnect-agents
python3 standalone_grace_agent.py --port 8001 > logs/grace.log 2>&1 &
GRACE_PID=$!
echo "Grace Agent started with PID: $GRACE_PID"

# Start Alex Agent
echo "Starting Alex Agent on port 8002..."
python3 standalone_alex_agent.py --port 8002 > logs/alex.log 2>&1 &
ALEX_PID=$!
echo "Alex Agent started with PID: $ALEX_PID"

# Wait a moment for agents to start
sleep 5

# Check if agents are running
echo "Checking agent status..."
curl -s http://localhost:8001/health && echo "Grace Agent is running" || echo "Grace Agent failed to start"
curl -s http://localhost:8002/health && echo "Alex Agent is running" || echo "Alex Agent failed to start"

# Save PIDs for later cleanup
echo $GRACE_PID > logs/grace.pid
echo $ALEX_PID > logs/alex.pid

echo "Agents are starting up..."
echo "Grace Agent: http://localhost:8001"
echo "Alex Agent: http://localhost:8002"
echo "Logs are in familyconnect-agents/logs/"

# Try to register with GenAI OS (if available)
echo "Attempting to register with GenAI OS..."
python3 register-local-genai.py

echo "FamilyConnect agents are now running!"