#!/bin/bash

echo "Stopping GenAI Protocol Agents..."

# Stop Grace agent
if [ -f grace_agent.pid ]; then
    PID=$(cat grace_agent.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "Grace agent stopped (PID: $PID)"
    fi
    rm grace_agent.pid
fi

# Stop Alex agent
if [ -f alex_agent.pid ]; then
    PID=$(cat alex_agent.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "Alex agent stopped (PID: $PID)"
    fi
    rm alex_agent.pid
fi

# Stop Agent Manager
if [ -f agent_manager.pid ]; then
    PID=$(cat agent_manager.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "Agent Manager stopped (PID: $PID)"
    fi
    rm agent_manager.pid
fi

echo "All agents stopped successfully!"