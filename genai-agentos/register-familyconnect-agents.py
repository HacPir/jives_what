#!/usr/bin/env python3
"""
Register FamilyConnect agents with GenAI OS using the new protocol endpoints
"""

import requests
import json
import sys
from datetime import datetime

def find_genai_os():
    """Find the GenAI OS instance"""
    
    # Check common GenAI OS ports and configurations
    test_configs = [
        {"url": "http://localhost:8000", "name": "Local GenAI OS (port 8000)"},
        {"url": "http://localhost:3000", "name": "Local GenAI OS (port 3000)"},
        {"url": "http://genai-os:8000", "name": "Docker GenAI OS"},
        {"url": "http://genai-backend:8000", "name": "Docker Backend"},
        {"url": "http://localhost:7860", "name": "Local GenAI OS (port 7860)"},
        {"url": "http://localhost:11434", "name": "Local GenAI OS (port 11434)"},
    ]
    
    for config in test_configs:
        try:
            # Test basic connectivity
            response = requests.get(f"{config['url']}/health", timeout=3)
            if response.status_code == 200:
                print(f"✅ Found GenAI OS: {config['name']}")
                return config['url']
        except:
            continue
        
        # Also try checking for API endpoints
        try:
            response = requests.get(f"{config['url']}/api/health", timeout=3)
            if response.status_code == 200:
                print(f"✅ Found GenAI OS: {config['name']}")
                return config['url']
        except:
            continue
    
    return None

def register_agents(genai_url):
    """Register FamilyConnect agents with GenAI OS"""
    
    # Updated agent definitions with new protocol endpoints
    agents = [
        {
            "name": "Grace",
            "id": "grace-familyconnect",
            "description": "FamilyConnect elderly companion - warm, caring AI designed for seniors",
            "endpoint": "http://localhost:5000/api/agents/grace/v1/chat/completions",
            "model": "grace-familyconnect",
            "capabilities": ["companionship", "health_monitoring", "family_coordination", "voice_interaction"],
            "personality": "warm_grandmother",
            "status": "active",
            "provider": "FamilyConnect",
            "version": "1.0.0",
            "created": datetime.now().isoformat()
        },
        {
            "name": "Alex",
            "id": "alex-familyconnect", 
            "description": "FamilyConnect family coordinator - professional care management",
            "endpoint": "http://localhost:5000/api/agents/alex/v1/chat/completions",
            "model": "alex-familyconnect",
            "capabilities": ["care_management", "family_coordination", "emergency_response", "scheduling"],
            "personality": "professional_coordinator",
            "status": "active",
            "provider": "FamilyConnect",
            "version": "1.0.0",
            "created": datetime.now().isoformat()
        }
    ]
    
    # Test the new protocol endpoints first
    print("Testing GenAI protocol endpoints...")
    
    for agent in agents:
        try:
            # Test the chat completion endpoint
            test_response = requests.post(
                agent["endpoint"],
                json={
                    "model": agent["model"],
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 50
                },
                timeout=10
            )
            
            if test_response.status_code == 200:
                print(f"✅ {agent['name']} protocol endpoint is working")
            else:
                print(f"⚠️  {agent['name']} protocol endpoint returned {test_response.status_code}")
                
        except Exception as e:
            print(f"❌ {agent['name']} protocol endpoint failed: {e}")
    
    # Try different registration endpoints for GenAI OS
    registration_endpoints = [
        f"{genai_url}/api/agents/register",
        f"{genai_url}/api/agents",
        f"{genai_url}/agents/register",
        f"{genai_url}/register",
        f"{genai_url}/api/models/register",
        f"{genai_url}/api/v1/agents/register",
        f"{genai_url}/v1/agents/register"
    ]
    
    success_count = 0
    
    for agent in agents:
        registered = False
        
        for endpoint in registration_endpoints:
            try:
                response = requests.post(
                    endpoint,
                    json=agent,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    print(f"✅ {agent['name']} registered successfully at {endpoint}")
                    registered = True
                    success_count += 1
                    break
                else:
                    print(f"⚠️  {endpoint} returned {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                continue
                
        if not registered:
            print(f"❌ Failed to register {agent['name']}")
    
    return success_count

def main():
    print("🚀 FamilyConnect GenAI Agent Registration")
    print("========================================")
    
    # Test FamilyConnect backend
    try:
        response = requests.get("http://localhost:5000/api/agents/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ FamilyConnect backend ready with {len(models['data'])} models")
        else:
            print("❌ FamilyConnect backend not ready")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to FamilyConnect backend: {e}")
        sys.exit(1)
    
    # Find GenAI OS
    genai_url = find_genai_os()
    if not genai_url:
        print("❌ GenAI OS not found. Please ensure it's running.")
        print("Common GenAI OS locations:")
        print("  - http://localhost:3000")
        print("  - http://localhost:8000")
        print("  - http://localhost:7860")
        print("  - http://localhost:11434")
        sys.exit(1)
    
    # Register agents
    success_count = register_agents(genai_url)
    
    if success_count > 0:
        print(f"\n🎉 Successfully registered {success_count} agents!")
        print("The FamilyConnect agents should now appear in your GenAI OS dashboard.")
        print("\nAgent endpoints:")
        print("  - Grace: http://localhost:5000/api/agents/grace/v1/chat/completions")
        print("  - Alex: http://localhost:5000/api/agents/alex/v1/chat/completions")
    else:
        print("\n❌ No agents were successfully registered.")
        print("Please check your GenAI OS configuration and try again.")

if __name__ == "__main__":
    main()