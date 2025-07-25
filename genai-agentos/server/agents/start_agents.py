#!/usr/bin/env python3
"""
Start all genai-protocol agents
Launches Grace, Alex, and the Agent Manager
"""

import asyncio
import subprocess
import sys
import time
import os
from pathlib import Path

def start_agent_process(agent_script: str, port: int, name: str):
    """Start an agent process"""
    print(f"Starting {name} agent on port {port}...")
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    agent_path = script_dir / agent_script
    
    # Start the process
    process = subprocess.Popen([
        sys.executable, str(agent_path)
    ], env={**os.environ, "PORT": str(port)})
    
    return process

def main():
    """Start all agents"""
    agents = [
        ("grace_agent.py", 8001, "Grace"),
        ("alex_agent.py", 8002, "Alex"),
        ("agent_manager.py", 8000, "Agent Manager")
    ]
    
    processes = []
    
    try:
        # Start all agents
        for script, port, name in agents:
            process = start_agent_process(script, port, name)
            processes.append((process, name))
            time.sleep(2)  # Wait between starts
        
        print("\nAll agents started successfully!")
        print("Grace Agent: http://localhost:8001")
        print("Alex Agent: http://localhost:8002")
        print("Agent Manager: http://localhost:8000")
        print("\nPress Ctrl+C to stop all agents...")
        
        # Wait for all processes
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping all agents...")
        
        # Terminate all processes
        for process, name in processes:
            print(f"Stopping {name}...")
            process.terminate()
            process.wait()
        
        print("All agents stopped.")

if __name__ == "__main__":
    main()