#!/usr/bin/env python3
"""
Simple agent startup script for immediate testing
"""

import sys
import os
import subprocess
import time

def start_agent(script_name, port):
    """Start a single agent"""
    env = os.environ.copy()
    env['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
    env['PORT'] = str(port)
    
    print(f"Starting {script_name} on port {port}...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, script_name],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's still running
        if process.poll() is None:
            print(f"✅ {script_name} started successfully (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {script_name} failed to start")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting {script_name}: {e}")
        return None

def main():
    print("🚀 Starting FamilyConnect Agents")
    print("=" * 40)
    
    # Start agents
    agents = [
        ('grace_agent.py', 8001),
        ('alex_agent.py', 8002),
        ('agent_manager.py', 8000)
    ]
    
    processes = []
    for script, port in agents:
        process = start_agent(script, port)
        if process:
            processes.append(process)
    
    print(f"\n🎯 Started {len(processes)} agents")
    print("   Grace Agent: http://localhost:8001")
    print("   Alex Agent: http://localhost:8002") 
    print("   Agent Manager: http://localhost:8000")
    
    # Test connectivity
    print("\n🔍 Testing connectivity...")
    import requests
    
    for name, port in [('Grace', 8001), ('Alex', 8002), ('Manager', 8000)]:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} agent responding")
            else:
                print(f"❌ {name} agent not responding ({response.status_code})")
        except Exception as e:
            print(f"❌ {name} agent connection failed: {e}")
    
    print("\n🎉 Agents are ready for integration!")
    print("   Your GenAI dashboard can now communicate with these agents")
    print("   They provide full OpenAI-compatible endpoints")

if __name__ == "__main__":
    main()