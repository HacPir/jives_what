#!/usr/bin/env python3
"""
Start FamilyConnect Agents for GenAI Integration
"""

import subprocess
import sys
import os
import time
import signal
import requests
import json
from pathlib import Path

class GenAIAgentManager:
    def __init__(self):
        self.processes = {}
        self.agents = [
            {
                'name': 'Grace',
                'script': 'standalone_grace_agent.py',
                'port': 8001,
                'description': 'Elderly companion AI agent',
                'capabilities': ['emotional_support', 'health_monitoring', 'companionship']
            },
            {
                'name': 'Alex',
                'script': 'standalone_alex_agent.py',
                'port': 8002,
                'description': 'Family coordinator AI agent',
                'capabilities': ['family_coordination', 'care_management', 'emergency_response']
            }
        ]
        
    def start_agent(self, agent):
        """Start a single agent"""
        print(f"Starting {agent['name']} agent on port {agent['port']}...")
        
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
        env['PORT'] = str(agent['port'])
        
        try:
            process = subprocess.Popen(
                [sys.executable, agent['script']],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path(__file__).parent
            )
            
            self.processes[agent['name']] = process
            print(f"✅ {agent['name']} agent started (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start {agent['name']} agent: {e}")
            return False
    
    def check_agent_health(self, agent):
        """Check if agent is responding"""
        try:
            response = requests.get(f"http://localhost:{agent['port']}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_agent_communication(self, agent):
        """Test agent communication"""
        try:
            test_message = {
                "model": f"{agent['name'].lower()}-agent",
                "messages": [
                    {"role": "user", "content": "Hello, please introduce yourself briefly"}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"http://localhost:{agent['port']}/v1/chat/completions",
                json=test_message,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print(f"✅ {agent['name']} communication test passed")
                print(f"   Response: {message[:80]}...")
                return True
            else:
                print(f"❌ {agent['name']} communication test failed")
                return False
                
        except Exception as e:
            print(f"❌ Error testing {agent['name']}: {e}")
            return False
    
    def register_with_genai(self, agent, genai_url="http://localhost:3000"):
        """Register agent with GenAI software"""
        try:
            registration_data = {
                "name": agent["name"],
                "description": agent["description"],
                "endpoint": f"http://localhost:{agent['port']}",
                "model": f"{agent['name'].lower()}-agent",
                "capabilities": agent["capabilities"],
                "type": "openai_compatible",
                "status": "active"
            }
            
            # Try to register with GenAI
            response = requests.post(
                f"{genai_url}/api/agents/register",
                json=registration_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ {agent['name']} registered with GenAI software")
                return True
            else:
                print(f"⚠️  GenAI registration endpoint not available (this is okay)")
                return False
                
        except Exception as e:
            print(f"⚠️  GenAI registration failed: {e} (this is okay)")
            return False
    
    def start_all_agents(self):
        """Start all agents and integrate with GenAI"""
        print("🚀 Starting FamilyConnect Agents for GenAI Integration")
        print("=" * 55)
        
        # Start agents
        started_agents = []
        for agent in self.agents:
            if self.start_agent(agent):
                started_agents.append(agent)
                time.sleep(2)  # Brief pause between starts
        
        if not started_agents:
            print("❌ No agents started successfully")
            return False
        
        # Wait for agents to initialize
        print("⏳ Waiting for agents to initialize...")
        time.sleep(8)
        
        # Health check
        print("🏥 Checking agent health...")
        healthy_agents = []
        for agent in started_agents:
            if self.check_agent_health(agent):
                print(f"✅ {agent['name']} agent healthy on port {agent['port']}")
                healthy_agents.append(agent)
            else:
                print(f"❌ {agent['name']} agent not responding")
        
        if not healthy_agents:
            print("❌ No healthy agents found")
            return False
        
        # Test communication
        print("\n🔍 Testing agent communication...")
        working_agents = []
        for agent in healthy_agents:
            if self.test_agent_communication(agent):
                working_agents.append(agent)
        
        # Try to register with GenAI
        print("\n📡 Attempting GenAI registration...")
        registered_count = 0
        for agent in working_agents:
            if self.register_with_genai(agent):
                registered_count += 1
        
        # Success summary
        print(f"\n🎯 Integration Summary:")
        print(f"   Started: {len(started_agents)}/{len(self.agents)} agents")
        print(f"   Healthy: {len(healthy_agents)} agents")
        print(f"   Working: {len(working_agents)} agents")
        print(f"   Registered: {registered_count} agents")
        
        if working_agents:
            print("\n✅ Success! Your agents are ready for GenAI integration")
            print("\n🔗 Agent Endpoints:")
            for agent in working_agents:
                print(f"   {agent['name']} Agent: http://localhost:{agent['port']}")
            
            print("\n💡 GenAI Integration:")
            print("   Your agents provide OpenAI-compatible endpoints")
            print("   They will work with any GenAI software that supports OpenAI API")
            print("   Test them with your GenAI dashboard or API calls")
            
            print("\n🧪 Quick Test:")
            print("   curl -X POST http://localhost:8001/v1/chat/completions \\")
            print("     -H 'Content-Type: application/json' \\")
            print("     -d '{\"model\":\"grace-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'")
            
            return True
        else:
            print("\n❌ No agents are working properly")
            return False
    
    def stop_all_agents(self):
        """Stop all running agents"""
        print("🛑 Stopping all agents...")
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name} agent")
            except:
                try:
                    process.kill()
                    print(f"🔪 Force killed {name} agent")
                except:
                    pass
        print("✅ All agents stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n⚠️  Received shutdown signal")
        self.stop_all_agents()
        sys.exit(0)

def main():
    manager = GenAIAgentManager()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Start all agents
    success = manager.start_all_agents()
    
    if success:
        print("\n⏳ Agents running in background for GenAI integration...")
        print("   Press Ctrl+C to stop all agents")
        
        try:
            # Keep running and monitor agents
            while True:
                time.sleep(30)
                # Optional: periodic health check
                healthy_count = sum(1 for agent in manager.agents if manager.check_agent_health(agent))
                print(f"📊 Health check: {healthy_count}/{len(manager.agents)} agents healthy")
        except KeyboardInterrupt:
            pass
    else:
        print("\n❌ Failed to start agents for GenAI integration")
        sys.exit(1)

if __name__ == "__main__":
    main()