#!/bin/bash

echo "Starting GenAI Protocol Agents..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start Grace agent in background
echo "Starting Grace agent on port 8001..."
python3 grace_agent.py &
GRACE_PID=$!
echo "Grace agent started with PID: $GRACE_PID"

# Start Alex agent in background
echo "Starting Alex agent on port 8002..."
python3 alex_agent.py &
ALEX_PID=$!
echo "Alex agent started with PID: $ALEX_PID"

# Start agent manager
echo "Starting Agent Manager on port 8000..."
python3 agent_manager.py &
MANAGER_PID=$!
echo "Agent Manager started with PID: $MANAGER_PID"

# Save PIDs to file for cleanup
echo "$GRACE_PID" > grace_agent.pid
echo "$ALEX_PID" > alex_agent.pid
echo "$MANAGER_PID" > agent_manager.pid

echo "All agents started successfully!"
echo "Grace Agent: http://localhost:8001"
echo "Alex Agent: http://localhost:8002"
echo "Agent Manager: http://localhost:8000"

# Keep script running
wait