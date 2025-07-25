#!/usr/bin/env python3
"""
Register FamilyConnect agents with local GenAI OS
"""

import requests
import time
import json
import os

def register_agents():
    """Register agents with local GenAI OS backend"""
    
    # Local GenAI OS endpoint
    backend_url = "http://localhost:3000"
    
    print("Registering agents with local GenAI OS...")
    
    # Agent configurations for local deployment
    agents = [
        {
            "name": "Grace",
            "description": "Elderly companion AI agent for FamilyConnect - warm, patient, caring companion designed for seniors",
            "endpoint": "http://localhost:8001",
            "model": "grace-agent",
            "capabilities": ["emotional_support", "health_monitoring", "companionship", "family_coordination"],
            "personality": "warm_grandmother",
            "target_users": ["elderly", "seniors"],
            "status": "active",
            "version": "1.0.0",
            "provider": "FamilyConnect"
        },
        {
            "name": "Alex",
            "description": "Family coordinator AI agent for FamilyConnect - professional coordinator for caregivers and family members", 
            "endpoint": "http://localhost:8002",
            "model": "alex-agent",
            "capabilities": ["family_coordination", "care_management", "emergency_response", "appointment_scheduling"],
            "personality": "professional_coordinator",
            "target_users": ["caregivers", "family_members"],
            "status": "active",
            "version": "1.0.0",
            "provider": "FamilyConnect"
        }
    ]
    
    # Test GenAI OS connectivity
    try:
        health_response = requests.get(f"{backend_url}/api/health", timeout=5)
        print(f"GenAI OS connectivity: {health_response.status_code}")
    except Exception as e:
        print(f"GenAI OS not accessible at {backend_url}: {e}")
        print("Please ensure GenAI OS is running on port 3000")
        return
    
    # Register each agent
    for agent in agents:
        try:
            # Try different registration endpoints
            endpoints_to_try = [
                f"{backend_url}/api/agents/register",
                f"{backend_url}/api/agents",
                f"{backend_url}/agents/register",
                f"{backend_url}/register"
            ]
            
            success = False
            for endpoint in endpoints_to_try:
                try:
                    response = requests.post(
                        endpoint,
                        json=agent,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ {agent['name']} registered successfully at {endpoint}")
                        success = True
                        break
                    else:
                        print(f"⚠️  {endpoint} returned {response.status_code}: {response.text}")
                        
                except Exception as e:
                    print(f"⚠️  {endpoint} failed: {e}")
                    
            if not success:
                print(f"❌ Failed to register {agent['name']} at any endpoint")
                
        except Exception as e:
            print(f"❌ {agent['name']} registration error: {e}")
    
    print("Agent registration complete!")
    
    # Verify registration
    print("\nVerifying agent registration...")
    try:
        response = requests.get(f"{backend_url}/api/agents", timeout=5)
        if response.status_code == 200:
            agents_data = response.json()
            print(f"Found {len(agents_data)} registered agents")
            for agent in agents_data:
                print(f"  - {agent.get('name', 'Unknown')}")
        else:
            print(f"Could not verify agents: {response.status_code}")
    except Exception as e:
        print(f"Could not verify agents: {e}")

if __name__ == "__main__":
    register_agents()