#!/usr/bin/env python3
"""
Complete GenAI AgentOS Integration Guide for FamilyConnect Agents
Creates proper genai-protocol compatible agents for registration
"""

import json
import os
import requests
from datetime import datetime

def create_genai_compatible_agents():
    """Create genai-protocol compatible agent files for Grace and Alex"""
    
    # Grace Agent - Elderly Companion
    grace_agent = '''import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import httpx

# Agent JWT will be provided after registration
AGENT_JWT = "YOUR_AGENT_JWT_HERE"
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(name="Grace", description="FamilyConnect elderly companion - warm, caring AI for seniors")
async def grace_agent(
    agent_context: GenAIContext,
    message: Annotated[str, "User message to Grace"]
):
    """
    Grace - Elderly Companion Agent
    Provides warm, caring interaction for elderly users
    """
    try:
        # Forward to FamilyConnect backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://host.docker.internal:5000/api/agents/message",
                json={
                    "userId": 1,
                    "agentId": "grace", 
                    "message": message
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('message', 'Hello dear, how can I help you today?')}"
            else:
                return "Hello dear, I'm here to help. How are you feeling today?"
                
    except Exception as e:
        return f"Hello dear, I'm experiencing some technical difficulties, but I'm here to listen. How can I support you today?"

async def main():
    print(f"Grace Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
'''

    # Alex Agent - Family Coordinator
    alex_agent = '''import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import httpx

# Agent JWT will be provided after registration
AGENT_JWT = "YOUR_AGENT_JWT_HERE"
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(name="Alex", description="FamilyConnect family coordinator - professional care management")
async def alex_agent(
    agent_context: GenAIContext,
    message: Annotated[str, "User message to Alex"]
):
    """
    Alex - Family Coordinator Agent
    Provides professional care management and family coordination
    """
    try:
        # Forward to FamilyConnect backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://host.docker.internal:5000/api/agents/message",
                json={
                    "userId": 1,
                    "agentId": "alex",
                    "message": message
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('message', 'Hello, I can help coordinate care for your family.')}"
            else:
                return "Hello, I can help coordinate care for your family. What do you need assistance with?"
                
    except Exception as e:
        return f"Hello, I'm experiencing some technical difficulties, but I'm here to help coordinate care. What can I assist you with?"

async def main():
    print(f"Alex Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
'''

    # Create agents directory
    os.makedirs("familyconnect-agents", exist_ok=True)
    
    # Save agent files
    with open("familyconnect-agents/grace_agent.py", "w") as f:
        f.write(grace_agent)
    
    with open("familyconnect-agents/alex_agent.py", "w") as f:
        f.write(alex_agent)
    
    # Create pyproject.toml for agent dependencies
    pyproject_content = '''[project]
name = "familyconnect-agents"
version = "1.0.0"
description = "FamilyConnect Agents for GenAI OS"
dependencies = [
    "genai-protocol>=1.0.9",
    "httpx>=0.25.0",
    "asyncio-mqtt>=0.13.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''
    
    with open("familyconnect-agents/pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    print("✅ Created GenAI-compatible agent files:")
    print("  - familyconnect-agents/grace_agent.py")
    print("  - familyconnect-agents/alex_agent.py")
    print("  - familyconnect-agents/pyproject.toml")
    
    return "familyconnect-agents"

def create_registration_script():
    """Create registration script for GenAI CLI"""
    
    registration_script = '''#!/bin/bash
# FamilyConnect Agent Registration Script for GenAI OS
# This script registers Grace and Alex agents with your GenAI OS

echo "🚀 FamilyConnect Agent Registration for GenAI OS"
echo "================================================"

# Check if GenAI CLI is available
if ! command -v genai &> /dev/null; then
    echo "❌ GenAI CLI not found. Please install it first:"
    echo "   cd /path/to/genai-agentos/cli"
    echo "   ./install_cli.sh"
    exit 1
fi

# Check if user is logged in
echo "📋 Checking authentication..."
if ! genai list_agents &> /dev/null; then
    echo "❌ Not logged in to GenAI OS. Please login first:"
    echo "   genai login -u <username> -p <password>"
    echo "   Or signup: genai signup -u <username>"
    exit 1
fi

echo "✅ Authentication successful"

# Register Grace Agent
echo "📝 Registering Grace agent..."
GRACE_OUTPUT=$(genai register_agent --name "Grace" --description "FamilyConnect elderly companion - warm, caring AI for seniors")
echo "$GRACE_OUTPUT"

# Register Alex Agent  
echo "📝 Registering Alex agent..."
ALEX_OUTPUT=$(genai register_agent --name "Alex" --description "FamilyConnect family coordinator - professional care management")
echo "$ALEX_OUTPUT"

echo "✅ Agent registration complete!"
echo ""
echo "🎯 Next steps:"
echo "1. The agent files have been created in the 'agents/' directory"
echo "2. Update the JWT tokens in the agent files"
echo "3. Set up virtual environments for each agent:"
echo "   cd agents/Grace && uv venv && uv sync"
echo "   cd agents/Alex && uv venv && uv sync"
echo "4. Run the agents:"
echo "   genai run_agents"
echo ""
echo "📋 Make sure FamilyConnect is running on port 5000 before starting agents"
'''
    
    with open("register-familyconnect-with-genai.sh", "w") as f:
        f.write(registration_script)
    
    os.chmod("register-familyconnect-with-genai.sh", 0o755)
    return "register-familyconnect-with-genai.sh"

def create_docker_integration():
    """Create Docker integration for GenAI OS"""
    
    docker_compose_addition = '''# Add this to your GenAI OS docker-compose.yml
  
  # FamilyConnect Service
  familyconnect:
    build: 
      context: ./familyconnect-agents
      dockerfile: Dockerfile
    container_name: familyconnect-service
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - NODE_ENV=production
    networks:
      - local-genai-network
    depends_on:
      - backend
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/agents/message"]
      interval: 30s
      timeout: 10s
      retries: 5

# Make sure to update the volumes section to include FamilyConnect data
volumes:
  postgres-volume:
  shared-files-volume:
  redis-data:
  familyconnect-data:  # Add this line
'''
    
    with open("docker-compose-addition.yml", "w") as f:
        f.write(docker_compose_addition)
    
    # Create Dockerfile for FamilyConnect
    dockerfile = '''FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 5000

# Start the application
CMD ["npm", "start"]
'''
    
    os.makedirs("familyconnect-agents", exist_ok=True)
    with open("familyconnect-agents/Dockerfile", "w") as f:
        f.write(dockerfile)
    
    return "docker-compose-addition.yml"

def create_comprehensive_guide():
    """Create comprehensive integration guide"""
    
    guide = '''# FamilyConnect × GenAI OS Integration Guide

## Overview
This guide helps you integrate FamilyConnect's Grace and Alex agents with your GenAI OS setup.

## Prerequisites
- GenAI OS running with Docker (`docker compose up`)
- GenAI CLI installed and configured
- FamilyConnect running on port 5000

## Integration Steps

### 1. Install GenAI CLI
```bash
cd /path/to/genai-agentos/cli
./install_cli.sh
```

### 2. Create GenAI Account
```bash
# Create new account
genai signup -u <username>

# Or login if you have an account
genai login -u <username> -p <password>
```

### 3. Register FamilyConnect Agents
```bash
# Run the registration script
./register-familyconnect-with-genai.sh
```

### 4. Set Up Agent Environments
```bash
# Navigate to agents directory (created by GenAI CLI)
cd agents/Grace
uv venv
uv sync

cd ../Alex  
uv venv
uv sync
```

### 5. Update Agent JWT Tokens
After registration, update the JWT tokens in the agent files:
- `agents/Grace/grace_agent.py` - Replace `YOUR_AGENT_JWT_HERE`
- `agents/Alex/alex_agent.py` - Replace `YOUR_AGENT_JWT_HERE`

### 6. Start FamilyConnect Service
```bash
# Make sure FamilyConnect is running
npm run dev  # or your preferred method
```

### 7. Run GenAI Agents
```bash
# Run all agents
genai run_agents

# Or run individually
cd agents/Grace && python grace_agent.py
cd agents/Alex && python alex_agent.py
```

## Testing the Integration

### Test via GenAI OS Dashboard
1. Open http://localhost:3000
2. Look for Grace and Alex agents in the agent list
3. Send test messages to each agent
4. Verify responses come from FamilyConnect

### Test via API
```bash
# Test Grace agent
curl -X POST "http://localhost:8000/api/agents/message" \\
  -H "Content-Type: application/json" \\
  -d '{
    "agent_id": "grace-agent-id",
    "message": "Hello Grace, how are you?"
  }'

# Test Alex agent
curl -X POST "http://localhost:8000/api/agents/message" \\
  -H "Content-Type: application/json" \\
  -d '{
    "agent_id": "alex-agent-id", 
    "message": "Hello Alex, can you help coordinate care?"
  }'
```

## Architecture

```
GenAI OS (port 8000) → GenAI Agents → FamilyConnect (port 5000)
                     ↓
                 Grace Agent (elderly companion)
                 Alex Agent (family coordinator)
```

## Agent Capabilities

### Grace Agent
- Warm, caring personality for elderly users
- Emotional support and companionship
- Health monitoring and gentle reminders
- Family connection facilitation
- Voice interaction support

### Alex Agent
- Professional care coordination
- Family communication management
- Medical appointment scheduling
- Emergency response coordination
- Care activity tracking

## Troubleshooting

### Agents Not Responding
- Check FamilyConnect is running on port 5000
- Verify JWT tokens are correctly set
- Ensure virtual environments are activated
- Check network connectivity to host.docker.internal:5000

### Registration Issues
- Ensure GenAI CLI is installed and authenticated
- Check that GenAI OS is running (docker compose up)
- Verify user permissions in GenAI OS

### Connection Issues
- Check Docker network configuration
- Verify host.docker.internal is accessible
- Test FamilyConnect endpoint manually

## Additional Resources

- [GenAI OS Documentation](https://github.com/genai-works-org/genai-agentos)
- [GenAI Protocol Documentation](https://pypi.org/project/genai-protocol/)
- [FamilyConnect AI Documentation](./README.md)

## Support

For issues specific to:
- GenAI OS: Check the official repository
- FamilyConnect: Refer to the project documentation
- Integration: Follow this guide or check the troubleshooting section
'''
    
    with open("GENAI_INTEGRATION_GUIDE.md", "w") as f:
        f.write(guide)
    
    return "GENAI_INTEGRATION_GUIDE.md"

def create_agent_package():
    """Create a complete agent package for deployment"""
    
    # Create the package structure
    package_structure = {
        "familyconnect-agents/": {
            "grace_agent.py": "Grace agent file",
            "alex_agent.py": "Alex agent file", 
            "pyproject.toml": "Dependencies",
            "Dockerfile": "Docker configuration",
            "README.md": "Agent documentation"
        }
    }
    
    # Create README for the agent package
    agent_readme = '''# FamilyConnect Agents for GenAI OS

This package contains Grace and Alex agents compatible with GenAI OS.

## Setup

1. Install dependencies:
   ```bash
   uv venv
   uv sync
   ```

2. Update JWT tokens in agent files after registration

3. Run agents:
   ```bash
   python grace_agent.py
   python alex_agent.py
   ```

## Agent Details

### Grace Agent
- **Purpose**: Elderly companion
- **Personality**: Warm, caring, patient
- **Capabilities**: Emotional support, health monitoring, family connections

### Alex Agent  
- **Purpose**: Family coordinator
- **Personality**: Professional, organized, efficient
- **Capabilities**: Care management, family communication, emergency response

## Integration

These agents forward messages to the FamilyConnect backend at:
- Endpoint: http://host.docker.internal:5000/api/agents/message
- Format: {"userId": 1, "agentId": "grace|alex", "message": "user_message"}
'''
    
    with open("familyconnect-agents/README.md", "w") as f:
        f.write(agent_readme)
    
    return package_structure

def main():
    print("🚀 Creating GenAI OS Integration for FamilyConnect")
    print("=" * 50)
    
    # Create all integration files
    agents_dir = create_genai_compatible_agents()
    registration_script = create_registration_script()
    docker_integration = create_docker_integration()
    guide = create_comprehensive_guide()
    package = create_agent_package()
    
    print(f"✅ Created {registration_script}")
    print(f"✅ Created {docker_integration}")
    print(f"✅ Created {guide}")
    print(f"✅ Created agent package in {agents_dir}/")
    
    print("\n🎯 Next Steps:")
    print("1. Install GenAI CLI in your genai-agentos project")
    print("2. Run: ./register-familyconnect-with-genai.sh")
    print("3. Follow the GENAI_INTEGRATION_GUIDE.md")
    print("4. Test agents in GenAI OS dashboard at http://localhost:3000")
    
    print("\n📋 Files Created:")
    print("- register-familyconnect-with-genai.sh (registration script)")
    print("- GENAI_INTEGRATION_GUIDE.md (comprehensive guide)")
    print("- docker-compose-addition.yml (Docker integration)")
    print("- familyconnect-agents/ (agent package)")
    
    print("\n🔧 Agent Configuration:")
    print("- Grace: FamilyConnect elderly companion")
    print("- Alex: FamilyConnect family coordinator")
    print("- Endpoint: http://host.docker.internal:5000/api/agents/message")

if __name__ == "__main__":
    main()