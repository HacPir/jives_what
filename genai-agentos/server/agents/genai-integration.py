#!/usr/bin/env python3
"""
GenAI Integration Helper - Registers agents with GenAI software
"""

import requests
import json
import time
import os

class GenAIIntegration:
    def __init__(self, genai_url="http://localhost:3000"):
        self.genai_url = genai_url
        self.agents = [
            {
                "name": "Grace",
                "description": "Elderly companion AI agent",
                "endpoint": "http://localhost:8001",
                "model": "grace-agent",
                "capabilities": ["emotional_support", "health_monitoring", "companionship"]
            },
            {
                "name": "Alex", 
                "description": "Family coordinator AI agent",
                "endpoint": "http://localhost:8002",
                "model": "alex-agent",
                "capabilities": ["family_coordination", "care_management", "emergency_response"]
            }
        ]
    
    def check_agent_health(self, agent):
        """Check if an agent is healthy"""
        try:
            response = requests.get(f"{agent['endpoint']}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def register_agent_with_genai(self, agent):
        """Register an agent with GenAI software"""
        try:
            # Check if GenAI software is available
            genai_response = requests.get(f"{self.genai_url}/api/health", timeout=5)
            if genai_response.status_code != 200:
                print(f"❌ GenAI software not available at {self.genai_url}")
                return False
            
            # Register the agent
            registration_data = {
                "name": agent["name"],
                "description": agent["description"],
                "endpoint": agent["endpoint"],
                "model": agent["model"],
                "capabilities": agent["capabilities"],
                "type": "openai_compatible"
            }
            
            response = requests.post(
                f"{self.genai_url}/api/agents/register",
                json=registration_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ {agent['name']} registered with GenAI software")
                return True
            else:
                print(f"❌ Failed to register {agent['name']}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error registering {agent['name']}: {e}")
            return False
    
    def test_agent_communication(self, agent):
        """Test communication with an agent"""
        try:
            test_message = {
                "model": agent["model"],
                "messages": [
                    {"role": "user", "content": "Hello, please introduce yourself"}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"{agent['endpoint']}/v1/chat/completions",
                json=test_message,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print(f"✅ {agent['name']} communication test passed")
                print(f"   Response: {message[:100]}...")
                return True
            else:
                print(f"❌ {agent['name']} communication test failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing {agent['name']}: {e}")
            return False
    
    def integrate_all_agents(self):
        """Integrate all agents with GenAI software"""
        print("🔗 Integrating FamilyConnect Agents with GenAI Software")
        print("=" * 55)
        
        # Wait for agents to be ready
        print("⏳ Waiting for agents to be ready...")
        time.sleep(5)
        
        # Check agent health
        healthy_agents = []
        for agent in self.agents:
            if self.check_agent_health(agent):
                print(f"✅ {agent['name']} agent is healthy")
                healthy_agents.append(agent)
            else:
                print(f"❌ {agent['name']} agent is not responding")
        
        if not healthy_agents:
            print("❌ No healthy agents found. Make sure Docker containers are running.")
            return False
        
        # Test communication
        print("\n🔍 Testing agent communication...")
        working_agents = []
        for agent in healthy_agents:
            if self.test_agent_communication(agent):
                working_agents.append(agent)
        
        if not working_agents:
            print("❌ No agents responding to communication tests")
            return False
        
        # Register with GenAI
        print("\n📡 Registering agents with GenAI software...")
        registered_agents = []
        for agent in working_agents:
            if self.register_agent_with_genai(agent):
                registered_agents.append(agent)
        
        # Summary
        print(f"\n🎯 Integration Summary:")
        print(f"   Total agents: {len(self.agents)}")
        print(f"   Healthy agents: {len(healthy_agents)}")
        print(f"   Working agents: {len(working_agents)}")
        print(f"   Registered agents: {len(registered_agents)}")
        
        if registered_agents:
            print("\n✅ Success! Your agents are now available in GenAI software")
            print("   Navigate to your GenAI dashboard to see and interact with them")
            return True
        else:
            print("\n❌ No agents were successfully registered")
            print("   Check your GenAI software status and agent endpoints")
            return False

def main():
    # Allow custom GenAI URL
    genai_url = os.getenv("GENAI_URL", "http://localhost:3000")
    
    integrator = GenAIIntegration(genai_url)
    success = integrator.integrate_all_agents()
    
    if success:
        print("\n🎉 Integration complete! Your agents are ready to use.")
    else:
        print("\n⚠️  Integration failed. Check logs and try again.")

if __name__ == "__main__":
    main()