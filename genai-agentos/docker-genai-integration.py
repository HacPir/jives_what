#!/usr/bin/env python3
"""
Docker-based GenAI OS Integration for FamilyConnect
This script creates the integration files for your GenAI OS running in Docker
"""

import json
import os
from datetime import datetime

def create_docker_integration_files():
    """Create Docker integration files for GenAI OS"""
    
    # Create agent configuration for Docker GenAI OS
    docker_agents = {
        "agents": [
            {
                "name": "Grace",
                "id": "grace-familyconnect",
                "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
                "endpoint": "http://host.docker.internal:5000/api/agents/message",
                "model": "grace-familyconnect",
                "capabilities": ["companionship", "health_monitoring", "family_coordination"],
                "personality": "warm_grandmother",
                "status": "active",
                "provider": "FamilyConnect",
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "request_format": {
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "userId": 1,
                        "agentId": "grace",
                        "message": "{{user_message}}"
                    }
                },
                "response_format": {
                    "message": "string",
                    "emotionalState": "string",
                    "suggestedActions": ["string"],
                    "memoryTags": ["string"]
                }
            },
            {
                "name": "Alex",
                "id": "alex-familyconnect",
                "description": "FamilyConnect family coordinator - professional care management",
                "endpoint": "http://host.docker.internal:5000/api/agents/message",
                "model": "alex-familyconnect",
                "capabilities": ["care_management", "family_coordination", "emergency_response"],
                "personality": "professional_coordinator",
                "status": "active",
                "provider": "FamilyConnect",
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "request_format": {
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "userId": 1,
                        "agentId": "alex",
                        "message": "{{user_message}}"
                    }
                },
                "response_format": {
                    "message": "string",
                    "emotionalState": "string",
                    "suggestedActions": ["string"],
                    "memoryTags": ["string"]
                }
            }
        ]
    }
    
    # Save Docker agent configuration
    with open("familyconnect-docker-agents.json", "w") as f:
        json.dump(docker_agents, f, indent=2)
    
    return docker_agents

def create_curl_registration_script():
    """Create curl script to register agents with GenAI OS"""
    
    curl_script = '''#!/bin/bash
# Register FamilyConnect agents with GenAI OS running in Docker

echo "🚀 Registering FamilyConnect agents with GenAI OS..."
echo "Target: GenAI OS at port 8000"

# Grace Agent Registration
echo "Registering Grace agent..."
curl -X POST "http://localhost:8000/api/agents/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Grace",
    "id": "grace-familyconnect",
    "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
    "endpoint": "http://host.docker.internal:5000/api/agents/message",
    "model": "grace-familyconnect",
    "capabilities": ["companionship", "health_monitoring", "family_coordination"],
    "personality": "warm_grandmother",
    "status": "active",
    "provider": "FamilyConnect",
    "version": "1.0.0",
    "request_format": {
      "userId": 1,
      "agentId": "grace",
      "message": "{{user_message}}"
    }
  }'

echo -e "\\n\\nRegistering Alex agent..."
curl -X POST "http://localhost:8000/api/agents/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Alex",
    "id": "alex-familyconnect",
    "description": "FamilyConnect family coordinator - professional care management",
    "endpoint": "http://host.docker.internal:5000/api/agents/message",
    "model": "alex-familyconnect",
    "capabilities": ["care_management", "family_coordination", "emergency_response"],
    "personality": "professional_coordinator",
    "status": "active",
    "provider": "FamilyConnect",
    "version": "1.0.0",
    "request_format": {
      "userId": 1,
      "agentId": "alex",
      "message": "{{user_message}}"
    }
  }'

echo -e "\\n\\n✅ Registration complete!"
echo "Check your GenAI OS dashboard at http://localhost:8000"
'''
    
    with open("register-with-docker-genai.sh", "w") as f:
        f.write(curl_script)
    
    os.chmod("register-with-docker-genai.sh", 0o755)
    
    return "register-with-docker-genai.sh"

def create_docker_compose_integration():
    """Create Docker Compose configuration for GenAI OS integration"""
    
    docker_compose = '''# Add this to your existing GenAI OS docker-compose.yml
version: '3.8'

services:
  # Add FamilyConnect to your existing GenAI OS setup
  familyconnect:
    build: .
    container_name: familyconnect-agents
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - NODE_ENV=production
    networks:
      - genai-network
    depends_on:
      - genai-backend  # Replace with your GenAI OS backend service name
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/agents/message"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

networks:
  genai-network:
    external: true  # Use your existing GenAI OS network

# If you need to expose the FamilyConnect agents to other containers:
# The agents will be available at:
# - http://familyconnect:5000/api/agents/message (from within Docker network)
# - http://localhost:5000/api/agents/message (from host)
# - http://host.docker.internal:5000/api/agents/message (from GenAI OS containers)
'''
    
    with open("docker-compose.familyconnect.yml", "w") as f:
        f.write(docker_compose)
    
    return "docker-compose.familyconnect.yml"

def create_manual_registration_guide():
    """Create manual registration guide for GenAI OS dashboard"""
    
    guide = '''# Manual Registration Guide for GenAI OS Dashboard

## Step 1: Access GenAI OS Dashboard
Open your browser and go to: http://localhost:8000

## Step 2: Add Custom Agent - Grace
In your GenAI OS dashboard, add a new agent with these details:

**Agent Name:** Grace
**Description:** FamilyConnect elderly companion - warm, caring AI for seniors
**Endpoint:** http://host.docker.internal:5000/api/agents/message
**Method:** POST
**Content-Type:** application/json

**Request Body Format:**
```json
{
  "userId": 1,
  "agentId": "grace",
  "message": "{{user_message}}"
}
```

**Expected Response:**
```json
{
  "message": "Agent response here",
  "emotionalState": "neutral",
  "suggestedActions": ["action1", "action2"],
  "memoryTags": ["tag1", "tag2"]
}
```

## Step 3: Add Custom Agent - Alex
Add another agent with these details:

**Agent Name:** Alex
**Description:** FamilyConnect family coordinator - professional care management
**Endpoint:** http://host.docker.internal:5000/api/agents/message
**Method:** POST
**Content-Type:** application/json

**Request Body Format:**
```json
{
  "userId": 1,
  "agentId": "alex",
  "message": "{{user_message}}"
}
```

## Step 4: Test the Integration
After adding both agents, test them by:
1. Sending a message to Grace: "Hello, how are you today?"
2. Sending a message to Alex: "Can you help coordinate care?"

## Troubleshooting

**If agents don't respond:**
- Ensure FamilyConnect is running on port 5000
- Check that your GenAI OS can reach host.docker.internal:5000
- Verify the request format matches exactly

**If endpoint is unreachable:**
- Try using "localhost:5000" instead of "host.docker.internal:5000"
- Or use the actual IP address of your host machine

**Test the endpoint directly:**
```bash
curl -X POST http://localhost:5000/api/agents/message \\
  -H "Content-Type: application/json" \\
  -d '{"userId": 1, "agentId": "grace", "message": "Hello test"}'
```

## Agent Capabilities

**Grace (Elderly Companion):**
- Warm, patient, caring personality
- Emotional support and companionship
- Health monitoring and reminders
- Family connection facilitation
- Voice interaction support

**Alex (Family Coordinator):**
- Professional, organized personality
- Care management and coordination
- Family communication updates
- Emergency response coordination
- Appointment scheduling
'''
    
    with open("MANUAL_REGISTRATION_GUIDE.md", "w") as f:
        f.write(guide)
    
    return "MANUAL_REGISTRATION_GUIDE.md"

def main():
    print("🚀 Creating GenAI OS Integration Files for Docker")
    print("=" * 50)
    
    # Create integration files
    docker_agents = create_docker_integration_files()
    print(f"✅ Created familyconnect-docker-agents.json")
    
    curl_script = create_curl_registration_script()
    print(f"✅ Created {curl_script}")
    
    docker_compose = create_docker_compose_integration()
    print(f"✅ Created {docker_compose}")
    
    manual_guide = create_manual_registration_guide()
    print(f"✅ Created {manual_guide}")
    
    print("\n🎯 Next Steps:")
    print("1. Try running: ./register-with-docker-genai.sh")
    print("2. Or manually add agents in your GenAI OS dashboard")
    print("3. Read MANUAL_REGISTRATION_GUIDE.md for detailed instructions")
    print("4. Use docker-compose.familyconnect.yml to add to your Docker setup")
    
    print("\n📋 Agent Endpoints:")
    print("- Grace & Alex: http://host.docker.internal:5000/api/agents/message")
    print("- From host: http://localhost:5000/api/agents/message")
    
    print(f"\n🔧 Created {len(docker_agents['agents'])} agent configurations")

if __name__ == "__main__":
    main()