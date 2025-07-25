#!/usr/bin/env python3
"""
Create GenAI-compatible agent definitions for FamilyConnect
"""

import json
import os
import requests
from datetime import datetime

def create_agent_manifests():
    """Create agent manifest files for GenAI OS"""
    
    # Grace Agent Manifest
    grace_manifest = {
        "name": "Grace",
        "id": "grace-familyconnect",
        "version": "1.0.0",
        "description": "FamilyConnect elderly companion - warm, caring AI designed for seniors",
        "author": "FamilyConnect Team",
        "license": "MIT",
        "tags": ["elderly-care", "companionship", "health", "family"],
        "capabilities": [
            "emotional_support",
            "health_monitoring", 
            "companionship",
            "family_coordination",
            "voice_interaction"
        ],
        "personality": {
            "type": "warm_grandmother",
            "traits": ["patient", "caring", "supportive", "gentle"],
            "voice": "warm_female"
        },
        "endpoints": {
            "chat": "http://localhost:5000/api/agents/grace/chat",
            "health": "http://localhost:5000/api/agents/grace/health",
            "status": "http://localhost:5000/api/agents/grace/status"
        },
        "model": "grace-familyconnect",
        "provider": "FamilyConnect",
        "created": datetime.now().isoformat(),
        "status": "active"
    }
    
    # Alex Agent Manifest
    alex_manifest = {
        "name": "Alex",
        "id": "alex-familyconnect", 
        "version": "1.0.0",
        "description": "FamilyConnect family coordinator - professional care management and family coordination",
        "author": "FamilyConnect Team",
        "license": "MIT",
        "tags": ["family-coordination", "care-management", "emergency-response", "scheduling"],
        "capabilities": [
            "care_management",
            "family_coordination",
            "emergency_response",
            "appointment_scheduling",
            "health_monitoring"
        ],
        "personality": {
            "type": "professional_coordinator",
            "traits": ["organized", "efficient", "reliable", "proactive"],
            "voice": "professional_male"
        },
        "endpoints": {
            "chat": "http://localhost:5000/api/agents/alex/chat",
            "health": "http://localhost:5000/api/agents/alex/health", 
            "status": "http://localhost:5000/api/agents/alex/status"
        },
        "model": "alex-familyconnect",
        "provider": "FamilyConnect",
        "created": datetime.now().isoformat(),
        "status": "active"
    }
    
    # Save manifests
    with open("grace-agent-manifest.json", "w") as f:
        json.dump(grace_manifest, f, indent=2)
    
    with open("alex-agent-manifest.json", "w") as f:
        json.dump(alex_manifest, f, indent=2)
        
    print("✅ Agent manifests created:")
    print("   - grace-agent-manifest.json")
    print("   - alex-agent-manifest.json")
    
    return grace_manifest, alex_manifest

def test_familyconnect_agents():
    """Test that FamilyConnect agents are responding"""
    
    print("\n🔍 Testing FamilyConnect agent connectivity...")
    
    # Test Grace
    try:
        response = requests.get("http://localhost:5000/api/agents/grace/health", timeout=5)
        if response.status_code == 200:
            print("✅ Grace agent is responding")
        else:
            print(f"⚠️  Grace agent returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Grace agent not responding: {e}")
    
    # Test Alex
    try:
        response = requests.get("http://localhost:5000/api/agents/alex/health", timeout=5)
        if response.status_code == 200:
            print("✅ Alex agent is responding")
        else:
            print(f"⚠️  Alex agent returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Alex agent not responding: {e}")

def create_genai_registration_script():
    """Create a script to register agents with GenAI OS"""
    
    script = '''#!/bin/bash
# Register FamilyConnect agents with GenAI OS

echo "🚀 Registering FamilyConnect agents with GenAI OS..."

# Test if GenAI OS is running
GENAI_PORTS=(3000 8000 7860 11434)
GENAI_URL=""

for port in "${GENAI_PORTS[@]}"; do
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        GENAI_URL="http://localhost:$port"
        echo "✅ Found GenAI OS at $GENAI_URL"
        break
    fi
done

if [ -z "$GENAI_URL" ]; then
    echo "❌ GenAI OS not found on common ports"
    echo "Please ensure GenAI OS is running and accessible"
    exit 1
fi

# Register Grace agent
echo "Registering Grace agent..."
curl -X POST "$GENAI_URL/api/agents/register" \\
    -H "Content-Type: application/json" \\
    -d @grace-agent-manifest.json

# Register Alex agent  
echo "Registering Alex agent..."
curl -X POST "$GENAI_URL/api/agents/register" \\
    -H "Content-Type: application/json" \\
    -d @alex-agent-manifest.json

echo "✅ Registration complete!"
echo "Your FamilyConnect agents should now appear in the GenAI OS dashboard"
'''
    
    with open("register-with-genai-os.sh", "w") as f:
        f.write(script)
    
    os.chmod("register-with-genai-os.sh", 0o755)
    print("✅ Registration script created: register-with-genai-os.sh")

def main():
    print("🔧 FamilyConnect GenAI Agent Setup")
    print("==================================")
    
    # Test FamilyConnect agents
    test_familyconnect_agents()
    
    # Create manifests
    grace_manifest, alex_manifest = create_agent_manifests()
    
    # Create registration script
    create_genai_registration_script()
    
    print("\n📋 Next steps:")
    print("1. Make sure your GenAI OS is running")
    print("2. Run: ./register-with-genai-os.sh")
    print("3. Check your GenAI OS dashboard for the agents")
    print("4. The agents will communicate through: http://localhost:5000")
    
    print("\n🎯 Agent URLs:")
    print("   - Grace: http://localhost:5000/api/agents/grace")
    print("   - Alex: http://localhost:5000/api/agents/alex")

if __name__ == "__main__":
    main()