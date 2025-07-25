# Docker Deployment Guide for FamilyConnect AI Agents

## Complete Docker-Ready Agent System

This folder contains everything needed to deploy the FamilyConnect AI agents in Docker containers. Once deployed, the agents will automatically integrate with your software and show up in the GenAI dashboard.

## Files Overview

### Agent Files
- `standalone_grace_agent.py` - Complete Grace elderly companion agent
- `standalone_alex_agent.py` - Complete Alex family coordinator agent  
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Container orchestration

### Docker Files
- `Dockerfile.grace` - Grace agent container definition
- `Dockerfile.alex` - Alex agent container definition

### Deployment Scripts
- `start-docker-agents.sh` - Quick deployment script
- `deploy-to-genai.py` - GenAI server integration

## Quick Deploy to Docker

### Option 1: Using Docker Compose (Recommended)
```bash
# Set your OpenAI API key (optional)
export OPENAI_API_KEY="your-api-key-here"

# Deploy all agents
docker-compose up --build -d

# Check status
docker-compose ps
```

### Option 2: Manual Docker Build
```bash
# Build Grace agent
docker build -f Dockerfile.grace -t grace-agent .

# Build Alex agent  
docker build -f Dockerfile.alex -t alex-agent .

# Run Grace agent
docker run -d -p 8001:8001 -e OPENAI_API_KEY="$OPENAI_API_KEY" grace-agent

# Run Alex agent
docker run -d -p 8002:8002 -e OPENAI_API_KEY="$OPENAI_API_KEY" alex-agent
```

### Option 3: Using the Start Script
```bash
chmod +x start-docker-agents.sh
./start-docker-agents.sh
```

## After Deployment

### 1. Verify Agents Are Running
```bash
# Check Grace agent
curl http://localhost:8001/health

# Check Alex agent  
curl http://localhost:8002/health
```

### 2. Test Agent Communication
```bash
# Test Grace agent
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grace-agent",
    "messages": [{"role": "user", "content": "Hello Grace, how are you?"}],
    "temperature": 0.7
  }'

# Test Alex agent
curl -X POST http://localhost:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "alex-agent", 
    "messages": [{"role": "user", "content": "Show me family status"}],
    "temperature": 0.7
  }'
```

### 3. Integration with FamilyConnect

Once the Docker containers are running, the agents will automatically:

1. **Show up in the GenAI Dashboard** - Navigate to Alex Dashboard → GenAI Protocol Agent Dashboard
2. **Provide OpenAI-compatible endpoints** - Full v1/chat/completions API compatibility
3. **Integrate with existing features** - Voice interface, family coordination, care management
4. **Use intelligent fallback** - OpenAI API when available, local AI responses otherwise

## Agent Capabilities

### Grace Agent (Port 8001)
- **Role**: Elderly companion
- **Personality**: Warm, patient, caring grandmother-like
- **Capabilities**: 
  - Emotional support and companionship
  - Health monitoring and family coordination
  - Memory assistance and gentle reminders
  - Voice interaction with speech synthesis

### Alex Agent (Port 8002)
- **Role**: Family coordinator
- **Personality**: Professional, organized, efficient
- **Capabilities**:
  - Family coordination and care management
  - Medical appointment scheduling
  - Emergency response and health monitoring
  - Communication facilitation between family members

## Environment Variables

- `OPENAI_API_KEY` - Optional OpenAI API key for enhanced AI responses
- `PORT` - Agent port (8001 for Grace, 8002 for Alex)

## Health Monitoring

Each agent includes:
- Health check endpoints at `/health`
- Agent information at `/agent/info`
- Docker health checks with automatic restart
- Real-time status monitoring in the dashboard

## Networking

- **Grace Agent**: http://localhost:8001
- **Alex Agent**: http://localhost:8002
- **Internal Network**: `agent-network` for inter-container communication
- **External Access**: All agents accessible from host machine

## Logs and Monitoring

```bash
# View logs
docker-compose logs grace-agent
docker-compose logs alex-agent

# Follow logs in real-time
docker-compose logs -f grace-agent
docker-compose logs -f alex-agent

# Check container status
docker-compose ps
```

## Stopping Agents

```bash
# Stop all agents
docker-compose down

# Stop and remove everything
docker-compose down -v --rmi all
```

## Integration with GenAI AgentOS

The agents are designed to work seamlessly with GenAI AgentOS:

1. **Auto-Discovery**: Your GenAI dashboard will automatically detect the running agents
2. **API Compatibility**: Full OpenAI v1/chat/completions API compatibility
3. **Registration**: Use the "Deploy to GenAI" button in the dashboard for automatic registration
4. **Health Monitoring**: Real-time agent status and health checks

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Stop existing processes: `docker-compose down`
   - Check for running processes: `docker ps`

2. **Build Failures**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild without cache: `docker-compose build --no-cache`

3. **Agent Not Responding**
   - Check logs: `docker-compose logs [agent-name]`
   - Verify health: `curl http://localhost:[port]/health`

4. **OpenAI API Issues**
   - Verify API key: `echo $OPENAI_API_KEY`
   - Agents work without API key (local responses)

### Support

The agents are designed to work with or without OpenAI API keys:
- **With API Key**: Full OpenAI GPT-4 powered responses
- **Without API Key**: Local AI simulation with agent personalities

Both configurations provide full OpenAI API compatibility for integration with your GenAI AgentOS system.