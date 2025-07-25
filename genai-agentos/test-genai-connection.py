#!/usr/bin/env python3
"""
Test connection to GenAI OS at port 8000 and register FamilyConnect agents
"""

import requests
import json
import sys
from datetime import datetime

def test_genai_os():
    """Test connection to GenAI OS at port 8000"""
    
    genai_url = "http://localhost:8000"
    
    print(f"Testing GenAI OS at {genai_url}")
    
    # Test different health endpoints
    health_endpoints = [
        "/health",
        "/api/health", 
        "/",
        "/api/status",
        "/status"
    ]
    
    for endpoint in health_endpoints:
        try:
            response = requests.get(f"{genai_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint} - Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
                return genai_url
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    return None

def register_agents_with_genai_8000():
    """Register FamilyConnect agents with GenAI OS at port 8000"""
    
    genai_url = "http://localhost:8000"
    
    # Agent definitions for GenAI OS
    agents = [
        {
            "name": "Grace",
            "id": "grace-familyconnect",
            "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
            "endpoint": "http://localhost:5000/api/agents/message",
            "model": "grace-familyconnect",
            "capabilities": ["companionship", "health_monitoring", "family_coordination"],
            "personality": "warm_grandmother",
            "status": "active",
            "provider": "FamilyConnect",
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "request_format": {
                "userId": 1,
                "agentId": "grace",
                "message": "{{user_message}}"
            }
        },
        {
            "name": "Alex",
            "id": "alex-familyconnect",
            "description": "FamilyConnect family coordinator - professional care management",
            "endpoint": "http://localhost:5000/api/agents/message",
            "model": "alex-familyconnect",
            "capabilities": ["care_management", "family_coordination", "emergency_response"],
            "personality": "professional_coordinator",
            "status": "active",
            "provider": "FamilyConnect",
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "request_format": {
                "userId": 1,
                "agentId": "alex",
                "message": "{{user_message}}"
            }
        }
    ]
    
    # Try different registration endpoints
    registration_endpoints = [
        "/api/agents/register",
        "/api/agents",
        "/agents/register",
        "/register",
        "/api/models/register",
        "/api/v1/agents/register",
        "/v1/agents/register",
        "/api/agents/create",
        "/agents/create"
    ]
    
    success_count = 0
    
    for agent in agents:
        print(f"\nRegistering {agent['name']} agent...")
        registered = False
        
        for endpoint in registration_endpoints:
            try:
                url = f"{genai_url}{endpoint}"
                response = requests.post(
                    url,
                    json=agent,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                print(f"  Trying {endpoint}: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    print(f"  ✅ {agent['name']} registered successfully!")
                    try:
                        print(f"  Response: {json.dumps(response.json(), indent=2)[:300]}...")
                    except:
                        print(f"  Response: {response.text[:300]}...")
                    registered = True
                    success_count += 1
                    break
                else:
                    print(f"  ❌ Failed: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                
        if not registered:
            print(f"  ❌ Failed to register {agent['name']} at any endpoint")
    
    return success_count

def main():
    print("🚀 FamilyConnect → GenAI OS Integration Test")
    print("=" * 50)
    
    # Test FamilyConnect agents first
    print("\n1. Testing FamilyConnect agents...")
    try:
        response = requests.post(
            "http://localhost:5000/api/agents/message",
            json={"userId": 1, "agentId": "grace", "message": "Hello test"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ FamilyConnect agents are working")
        else:
            print(f"❌ FamilyConnect agents error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to FamilyConnect: {e}")
        return
    
    # Test GenAI OS connection
    print("\n2. Testing GenAI OS connection...")
    genai_url = test_genai_os()
    if not genai_url:
        print("❌ Cannot connect to GenAI OS at port 8000")
        print("Make sure your GenAI OS Docker container is running and accessible")
        return
    
    # Register agents
    print("\n3. Registering agents with GenAI OS...")
    success_count = register_agents_with_genai_8000()
    
    print(f"\n🎉 Registration complete!")
    print(f"Successfully registered {success_count} agents with GenAI OS at port 8000")
    
    if success_count > 0:
        print("\n📋 Next steps:")
        print("1. Check your GenAI OS dashboard at http://localhost:8000")
        print("2. Look for Grace and Alex agents in the agent list")
        print("3. Test communication with the agents")
        print("4. The agents will respond via: http://localhost:5000/api/agents/message")

if __name__ == "__main__":
    main()