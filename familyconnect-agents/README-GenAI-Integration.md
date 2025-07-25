# FamilyConnect GenAI Network Integration

This guide shows how to integrate FamilyConnect agents with your GenAI OS Docker setup.

## Overview

The FamilyConnect agents (Grace and Alex) are now configured to:
1. **Connect to GenAI network first** - Primary integration with your GenAI OS
2. **Fallback to OpenAI API** - If GenAI network is unavailable
3. **Use local responses** - Final fallback for offline operation

## Quick Start

### 1. Ensure GenAI OS is Running
```bash
# Your GenAI OS should be running on port 8000
curl http://localhost:8000/health
```

### 2. Start FamilyConnect App
```bash
# Start your FamilyConnect app on port 5000
npm run dev
```

### 3. Launch FamilyConnect Agents
```bash
# Use the quick start script
./quick-start-genai.sh

# Or manually with Docker Compose
docker-compose -f docker-compose.familyconnect.yml up -d
```

### 4. Test Integration
```bash
# Run integration tests
python test-genai-integration.py
```

## Agent Configuration

### Grace Agent (Port 8001)
- **Primary**: GenAI network connection via Docker networking
- **Fallback**: OpenAI API when GenAI unavailable
- **Final**: Local elderly-friendly responses for offline operation
- **GenAI URL**: `http://genai-backend:8000` (Docker network)

### Alex Agent (Port 8002)
- **Primary**: GenAI network connection via Docker networking
- **Fallback**: OpenAI API when GenAI unavailable
- **Final**: Local family coordination responses for offline operation
- **GenAI URL**: `http://genai-backend:8000` (Docker network)

## Environment Variables

Set these in your Docker environment:

```bash
# Required for GenAI network integration
GENAI_BACKEND_URL=http://genai-backend:8000

# Optional fallback
OPENAI_API_KEY=your_openai_key_here

# Agent configuration
AGENT_NAME=Grace|Alex
AGENT_PORT=8001|8002
FAMILYCONNECT_URL=http://host.docker.internal:5000
```

## Integration Priority

1. **GenAI Network**: Agents connect to GenAI OS via Docker network (`genai-backend:8000`)
2. **OpenAI API**: Seamless fallback when GenAI network experiences issues
3. **Local Responses**: Offline operation with maintained agent personalities

The Docker host handles all network connectivity, ensuring smooth integration with your GenAI OS setup.

## Testing

### Health Check
```bash
# Check Grace agent
curl http://localhost:8001/health

# Check Alex agent  
curl http://localhost:8002/health
```

### Chat Test
```bash
# Test Grace conversation
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grace-agent",
    "messages": [{"role": "user", "content": "Hello Grace!"}],
    "temperature": 0.7,
    "max_tokens": 200
  }'

# Test Alex conversation
curl -X POST http://localhost:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "alex-agent", 
    "messages": [{"role": "user", "content": "Hello Alex!"}],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

## Registration with GenAI OS

The agents automatically register with your GenAI OS when they start. You should see them in your GenAI OS dashboard.

### Manual Registration
If automatic registration fails:

```bash
# Run the registration script
python register-with-genai.py
```

## Troubleshooting

### Agents Not Connecting to GenAI
1. Check if GenAI OS is running: `curl http://localhost:8000/health`
2. Verify Docker network: `docker network ls | grep genai`
3. Check agent logs: `docker-compose -f docker-compose.familyconnect.yml logs`

### Agents Not Registered in GenAI OS
1. Check registration service: `docker-compose -f docker-compose.familyconnect.yml logs agent-registrar`
2. Manually register: `python register-with-genai.py`
3. Verify GenAI OS API: `curl http://localhost:8000/api/agents`

### Performance Issues
1. Check if OpenAI API key is needed: Set `OPENAI_API_KEY` environment variable
2. Monitor GenAI OS performance: Check GenAI OS logs
3. Adjust agent timeout settings in the code

## Architecture

```
FamilyConnect App (Port 5000)
      ↓
Docker Network (local-genai-network)
      ↓
┌─────────────────────┐    ┌─────────────────────┐
│   Grace Agent       │    │   Alex Agent        │
│   (Port 8001)       │    │   (Port 8002)       │
│                     │    │                     │
│ 1. GenAI Network    │    │ 1. GenAI Network    │
│ 2. OpenAI API       │    │ 2. OpenAI API       │
│ 3. Local Responses  │    │ 3. Local Responses  │
└─────────────────────┘    └─────────────────────┘
            ↓                          ↓
      ┌─────────────────────────────────────────┐
      │        GenAI OS Backend                 │
      │        (Port 8000)                      │
      └─────────────────────────────────────────┘
```

## Success Indicators

✅ **GenAI Integration Working**:
- Agents connect to GenAI network on startup
- Health checks show `"genai_enabled": true`
- Agents appear in GenAI OS dashboard
- Chat requests route through GenAI network

✅ **Fallback System Working**:
- Agents fall back to OpenAI when GenAI unavailable
- Local responses work when both services are down
- No service interruption during failover

✅ **Registration Success**:
- Agents automatically appear in GenAI OS
- Registration logs show successful API calls
- GenAI OS dashboard shows FamilyConnect agents

## Next Steps

1. **Test with GenAI OS**: Use the GenAI OS dashboard to interact with agents
2. **Monitor Performance**: Watch agent logs and GenAI OS metrics
3. **Customize Configuration**: Adjust agent personalities and capabilities
4. **Scale as Needed**: Add more agents or modify existing ones

Your FamilyConnect agents are now fully integrated with the GenAI network!