#!/usr/bin/env python3
"""
Start FamilyConnect agents in standalone mode for testing
"""

import os
import sys
import subprocess
import time
import signal
import requests
from multiprocessing import Process

def start_alex_agent():
    """Start Alex agent in standalone mode"""
    os.environ['GENAI_BACKEND_URL'] = 'http://localhost:8000'
    os.environ['AGENT_NAME'] = 'Alex'
    os.environ['AGENT_PORT'] = '8002'
    os.environ['FAMILYCONNECT_URL'] = 'http://localhost:5000'
    
    subprocess.run([sys.executable, 'standalone_alex_agent.py'])

def start_grace_agent():
    """Start Grace agent in standalone mode"""
    os.environ['GENAI_BACKEND_URL'] = 'http://localhost:8000'
    os.environ['AGENT_NAME'] = 'Grace'
    os.environ['AGENT_PORT'] = '8001'
    os.environ['FAMILYCONNECT_URL'] = 'http://localhost:5000'
    
    subprocess.run([sys.executable, 'standalone_grace_agent.py'])

def test_agent_connection(agent_name, port):
    """Test if agent is responding"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {agent_name} agent is healthy")
            print(f"   GenAI enabled: {data.get('genai_enabled', False)}")
            print(f"   OpenAI enabled: {data.get('openai_enabled', False)}")
            return True
        else:
            print(f"❌ {agent_name} agent returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {agent_name} agent connection failed: {e}")
        return False

def main():
    """Start agents and test connectivity"""
    print("🚀 Starting FamilyConnect Agents in Standalone Mode...")
    
    # Start agents in separate processes
    print("\n1. Starting Grace Agent on port 8001...")
    grace_process = Process(target=start_grace_agent)
    grace_process.start()
    
    print("2. Starting Alex Agent on port 8002...")
    alex_process = Process(target=start_alex_agent)
    alex_process.start()
    
    # Wait for agents to start
    print("\n3. Waiting for agents to initialize...")
    time.sleep(5)
    
    # Test connections
    print("\n4. Testing agent connectivity...")
    grace_ok = test_agent_connection("Grace", 8001)
    alex_ok = test_agent_connection("Alex", 8002)
    
    if grace_ok and alex_ok:
        print("\n🎉 Both agents are running successfully!")
        print("Access them at:")
        print("- Grace: http://localhost:8001")
        print("- Alex: http://localhost:8002")
        print("\nPress Ctrl+C to stop agents")
        
        try:
            # Keep processes running
            grace_process.join()
            alex_process.join()
        except KeyboardInterrupt:
            print("\n\nStopping agents...")
            grace_process.terminate()
            alex_process.terminate()
            grace_process.join()
            alex_process.join()
            print("✅ Agents stopped")
    else:
        print("\n❌ Some agents failed to start")
        grace_process.terminate()
        alex_process.terminate()
        grace_process.join()
        alex_process.join()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())