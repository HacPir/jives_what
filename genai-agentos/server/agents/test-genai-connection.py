#!/usr/bin/env python3
"""
Test connection to GenAI AgentOS and register agents
"""

import requests
import json
import time

def test_genai_connection():
    """Test different possible GenAI AgentOS endpoints"""
    
    # Common ports and endpoints to try
    test_urls = [
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "https://localhost:3000"
    ]
    
    print("🔍 Testing GenAI AgentOS Connection...")
    
    for url in test_urls:
        try:
            # Try health check
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Found GenAI AgentOS at: {url}")
                return url
        except:
            pass
            
        try:
            # Try agents endpoint
            response = requests.get(f"{url}/agents", timeout=5)
            if response.status_code == 200:
                print(f"✅ Found GenAI AgentOS at: {url}")
                return url
        except:
            pass
            
        try:
            # Try API endpoint
            response = requests.get(f"{url}/api", timeout=5)
            if response.status_code == 200:
                print(f"✅ Found GenAI AgentOS at: {url}")
                return url
        except:
            pass
    
    print("❌ GenAI AgentOS not found on common ports")
    return None

def register_agent(base_url, agent_config):
    """Register an agent with GenAI AgentOS"""
    
    # Try different registration endpoints
    endpoints = [
        "/api/agents/register",
        "/api/agents",
        "/agents/register",
        "/agents"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.post(
                url,
                json=agent_config,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Registered {agent_config['name']} via {endpoint}")
                return True
            else:
                print(f"❌ Failed to register {agent_config['name']} via {endpoint}: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error with {endpoint}: {e}")
    
    return False

def main():
    print("🚀 GenAI AgentOS Connection Test")
    print("=" * 40)
    
    # Test connection
    genai_url = test_genai_connection()
    if not genai_url:
        print("\n💡 Manual connection test:")
        print("   1. Check if GenAI AgentOS is running")
        print("   2. Try different ports: 3000, 8080, 8000")
        print("   3. Check the GenAI AgentOS logs for the correct port")
        return
    
    # Agent configurations
    grace_config = {
        "name": "Grace",
        "description": "Warm, patient elderly companion AI agent",
        "type": "elderly_companion",
        "capabilities": ["emotional_support", "health_monitoring", "companionship"],
        "metadata": {
            "personality": "warm_grandmother",
            "target_audience": "elderly_users",
            "communication_style": "patient_caring"
        }
    }
    
    alex_config = {
        "name": "Alex",
        "description": "Professional family coordinator AI agent",
        "type": "family_coordinator",
        "capabilities": ["care_coordination", "family_management", "health_tracking"],
        "metadata": {
            "personality": "professional_coordinator",
            "target_audience": "caregivers_family",
            "communication_style": "efficient_organized"
        }
    }
    
    print(f"\n🤖 Registering agents with {genai_url}...")
    
    # Register agents
    grace_success = register_agent(genai_url, grace_config)
    alex_success = register_agent(genai_url, alex_config)
    
    # Summary
    print(f"\n📊 Registration Summary:")
    print(f"   Grace: {'✅ Success' if grace_success else '❌ Failed'}")
    print(f"   Alex: {'✅ Success' if alex_success else '❌ Failed'}")
    
    if grace_success and alex_success:
        print("\n🎉 All agents registered successfully!")
        print("   Check your GenAI AgentOS dashboard to see them")
    else:
        print("\n⚠️  Some agents failed to register")
        print("   Check the GenAI AgentOS documentation for the correct API format")

if __name__ == "__main__":
    main()