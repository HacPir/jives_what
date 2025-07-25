#!/usr/bin/env python3
"""
Create deployment package for GenAI OS integration
"""

import os
import shutil
import json
from pathlib import Path

def create_genai_deployment_package():
    """Create a complete deployment package for GenAI OS"""
    
    # Create package directory
    package_dir = Path("./genai-os-deployment")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Create agents directory
    agents_dir = package_dir / "agents"
    agents_dir.mkdir()
    
    # Copy agent files
    files_to_copy = [
        "standalone_grace_agent.py",
        "standalone_alex_agent.py", 
        "requirements.txt"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, agents_dir)
    
    # Create GenAI OS configuration
    genai_config = {
        "agents": [
            {
                "name": "Grace",
                "description": "Elderly companion AI agent for FamilyConnect",
                "version": "1.0.0",
                "author": "FamilyConnect AI",
                "endpoint": "http://localhost:8001",
                "health_check": "http://localhost:8001/health",
                "api_type": "openai_compatible",
                "capabilities": [
                    "emotional_support",
                    "health_monitoring", 
                    "companionship",
                    "elderly_care"
                ],
                "model": "grace-agent",
                "personality": "warm_grandmother",
                "target_users": ["elderly", "seniors"],
                "integration": {
                    "chat_completions": "/v1/chat/completions",
                    "health": "/health",
                    "info": "/agent/info"
                }
            },
            {
                "name": "Alex",
                "description": "Family coordinator AI agent for FamilyConnect",
                "version": "1.0.0", 
                "author": "FamilyConnect AI",
                "endpoint": "http://localhost:8002",
                "health_check": "http://localhost:8002/health",
                "api_type": "openai_compatible",
                "capabilities": [
                    "family_coordination",
                    "care_management",
                    "emergency_response",
                    "health_monitoring"
                ],
                "model": "alex-agent",
                "personality": "professional_coordinator",
                "target_users": ["caregivers", "family_members"],
                "integration": {
                    "chat_completions": "/v1/chat/completions",
                    "health": "/health", 
                    "info": "/agent/info"
                }
            }
        ]
    }
    
    # Save configuration
    with open(package_dir / "agents.json", "w") as f:
        json.dump(genai_config, f, indent=2)
    
    # Create startup script
    startup_script = '''#!/bin/bash

echo "Starting FamilyConnect Agents for GenAI OS"
echo "=========================================="

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)/agents
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"

# Install dependencies
echo "Installing dependencies..."
pip install -r agents/requirements.txt

# Start Grace agent
echo "Starting Grace agent on port 8001..."
cd agents
python3 standalone_grace_agent.py &
GRACE_PID=$!
echo "Grace agent started with PID: $GRACE_PID"

# Start Alex agent  
echo "Starting Alex agent on port 8002..."
python3 standalone_alex_agent.py &
ALEX_PID=$!
echo "Alex agent started with PID: $ALEX_PID"

# Wait for agents to initialize
echo "Waiting for agents to initialize..."
sleep 10

# Health check
echo "Checking agent health..."
curl -s http://localhost:8001/health > /dev/null && echo "✅ Grace agent healthy" || echo "❌ Grace agent not responding"
curl -s http://localhost:8002/health > /dev/null && echo "✅ Alex agent healthy" || echo "❌ Alex agent not responding"

echo ""
echo "🎯 FamilyConnect Agents Ready!"
echo "Grace Agent: http://localhost:8001"
echo "Alex Agent: http://localhost:8002"
echo ""
echo "GenAI OS can now discover and use these agents"
echo "Press Ctrl+C to stop all agents"

# Keep running
wait $GRACE_PID $ALEX_PID
'''
    
    with open(package_dir / "start-agents.sh", "w") as f:
        f.write(startup_script)
    
    # Make startup script executable
    os.chmod(package_dir / "start-agents.sh", 0o755)
    
    # Create integration guide
    integration_guide = '''# FamilyConnect Agents - GenAI OS Integration

## Quick Setup

1. **Deploy agents to your GenAI OS environment**:
   ```bash
   ./start-agents.sh
   ```

2. **Verify agents are running**:
   ```bash
   curl http://localhost:8001/health  # Grace Agent
   curl http://localhost:8002/health  # Alex Agent
   ```

3. **Configure GenAI OS**:
   - Import the `agents.json` configuration into your GenAI OS
   - Agents will automatically appear in your dashboard
   - Test communication through the GenAI OS interface

## Agent Endpoints

### Grace Agent (Port 8001)
- **Health**: `GET /health`
- **Info**: `GET /agent/info`  
- **Chat**: `POST /v1/chat/completions`

### Alex Agent (Port 8002)
- **Health**: `GET /health`
- **Info**: `GET /agent/info`
- **Chat**: `POST /v1/chat/completions`

## OpenAI API Compatibility

Both agents provide full OpenAI v1/chat/completions compatibility:

```bash
curl -X POST http://localhost:8001/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "grace-agent",
    "messages": [{"role": "user", "content": "Hello Grace"}],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

## Integration with GenAI OS

The agents are designed to work seamlessly with GenAI OS:

1. **Auto-Discovery**: GenAI OS will automatically detect running agents
2. **Configuration**: Use the provided `agents.json` for automatic setup
3. **Monitoring**: Built-in health checks and status endpoints
4. **API Compatibility**: Full OpenAI API compatibility for easy integration

## Environment Variables

- `OPENAI_API_KEY`: Optional OpenAI API key for enhanced responses
- `PORT`: Override default ports (8001 for Grace, 8002 for Alex)

## Troubleshooting

- **Port conflicts**: Modify ports in the startup script if needed
- **Dependencies**: Ensure all Python packages are installed
- **Health checks**: Use `/health` endpoints to verify agent status
- **Logs**: Check Python process logs for debugging

The agents work with or without OpenAI API keys, providing local AI responses when the API is unavailable.
'''
    
    with open(package_dir / "README.md", "w") as f:
        f.write(integration_guide)
    
    # Create systemd service file for production deployment
    systemd_service = '''[Unit]
Description=FamilyConnect Agents for GenAI OS
After=network.target

[Service]
Type=simple
User=genai
WorkingDirectory=/opt/familyconnect-agents
ExecStart=/opt/familyconnect-agents/start-agents.sh
Restart=always
RestartSec=10
Environment=OPENAI_API_KEY=
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
'''
    
    with open(package_dir / "familyconnect-agents.service", "w") as f:
        f.write(systemd_service)
    
    return package_dir

def create_tar_package():
    """Create compressed package for deployment"""
    package_dir = create_genai_deployment_package()
    
    # Create tar.gz package
    import tarfile
    
    with tarfile.open("familyconnect-genai-deployment.tar.gz", "w:gz") as tar:
        tar.add(package_dir, arcname="familyconnect-agents")
    
    print("✅ GenAI OS deployment package created: familyconnect-genai-deployment.tar.gz")
    print()
    print("Package contents:")
    print("- agents/standalone_grace_agent.py")
    print("- agents/standalone_alex_agent.py") 
    print("- agents/requirements.txt")
    print("- agents.json (GenAI OS configuration)")
    print("- start-agents.sh (startup script)")
    print("- README.md (integration guide)")
    print("- familyconnect-agents.service (systemd service)")
    print()
    print("Deployment instructions:")
    print("1. Upload familyconnect-genai-deployment.tar.gz to your GenAI OS server")
    print("2. Extract: tar -xzf familyconnect-genai-deployment.tar.gz")
    print("3. Run: cd familyconnect-agents && ./start-agents.sh")
    print("4. Import agents.json into your GenAI OS dashboard")
    print("5. Agents will appear as Grace and Alex in your interface")
    
    return "familyconnect-genai-deployment.tar.gz"

if __name__ == "__main__":
    create_tar_package()