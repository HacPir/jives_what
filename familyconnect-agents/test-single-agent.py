#!/usr/bin/env python3
"""
Test a single FamilyConnect agent
"""

import sys
import os
import requests
import json
import time
import subprocess
import signal
from multiprocessing import Process

def start_agent(agent_file, port):
    """Start a single agent"""
    env = os.environ.copy()
    env.update({
        'GENAI_BACKEND_URL': 'http://localhost:8000',
        'AGENT_NAME': agent_file.split('_')[1].title(),
        'AGENT_PORT': str(port),
        'FAMILYCONNECT_URL': 'http://localhost:5000'
    })
    
    subprocess.run([sys.executable, agent_file], env=env)

def test_agent_health(port):
    """Test agent health endpoint"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Agent: {data.get('agent')}")
            print(f"   GenAI enabled: {data.get('genai_enabled', False)}")
            print(f"   OpenAI enabled: {data.get('openai_enabled', False)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_agent_chat(port, agent_name):
    """Test agent chat functionality"""
    try:
        payload = {
            "model": f"{agent_name.lower()}-agent",
            "messages": [
                {"role": "user", "content": f"Hello {agent_name}! Can you introduce yourself?"}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        response = requests.post(
            f"http://localhost:{port}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data["choices"][0]["message"]["content"]
            print(f"✅ Chat test successful")
            print(f"   Response: {message[:150]}...")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def main():
    """Test a single agent"""
    if len(sys.argv) != 2:
        print("Usage: python test-single-agent.py <alex|grace>")
        return 1
    
    agent_type = sys.argv[1].lower()
    
    if agent_type == "alex":
        agent_file = "standalone_alex_agent.py"
        port = 8002
        agent_name = "Alex"
    elif agent_type == "grace":
        agent_file = "standalone_grace_agent.py"
        port = 8001
        agent_name = "Grace"
    else:
        print("Invalid agent type. Use 'alex' or 'grace'")
        return 1
    
    print(f"🚀 Testing {agent_name} Agent...")
    print("=" * 50)
    
    # Start the agent
    print(f"1. Starting {agent_name} agent on port {port}...")
    agent_process = Process(target=start_agent, args=(agent_file, port))
    agent_process.start()
    
    # Wait for agent to start
    print("2. Waiting for agent to initialize...")
    time.sleep(3)
    
    # Test health
    print("3. Testing health endpoint...")
    health_ok = test_agent_health(port)
    
    if health_ok:
        # Test chat
        print("4. Testing chat functionality...")
        chat_ok = test_agent_chat(port, agent_name)
        
        if chat_ok:
            print(f"\n🎉 {agent_name} agent is working correctly!")
            print(f"Agent is available at: http://localhost:{port}")
            print("\nPress Ctrl+C to stop the agent")
            
            try:
                agent_process.join()
            except KeyboardInterrupt:
                print(f"\n\nStopping {agent_name} agent...")
                agent_process.terminate()
                agent_process.join()
                print("✅ Agent stopped")
        else:
            print(f"\n❌ {agent_name} agent chat test failed")
            agent_process.terminate()
            agent_process.join()
            return 1
    else:
        print(f"\n❌ {agent_name} agent health check failed")
        agent_process.terminate()
        agent_process.join()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())