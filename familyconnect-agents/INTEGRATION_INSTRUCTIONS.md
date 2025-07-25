# FamilyConnect × GenAI OS Integration Instructions

## Your Setup
You have a `genai-agentos` directory with a `familyconnect-agents` folder containing:
- Standalone Grace and Alex agents with genai-protocol
- Docker configurations for both agents
- Registration scripts for GenAI OS

## Integration Steps

### Step 1: Start Your FamilyConnect App
Make sure your FamilyConnect app is running on port 5000 (in Replit or locally):
```bash
# In your FamilyConnect project
npm run dev
```

### Step 2: Start GenAI OS
In your `genai-agentos` directory:
```bash
# Start the full GenAI OS stack
docker compose up -d
```

### Step 3: Start FamilyConnect Agents
```bash
# Start Grace and Alex agents
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml up -d
```

### Step 4: Register Agents (Automatic)
The registration happens automatically, but you can also run it manually:
```bash
# Register agents with GenAI OS
docker compose -f familyconnect-agents/docker-compose.familyconnect.yml run --rm agent-registrar
```

### Step 5: Test Integration
1. Open GenAI OS dashboard: http://localhost:3000
2. Look for Grace and Alex agents in the agent list
3. Send test messages to each agent

## Service URLs
- GenAI OS Dashboard: http://localhost:3000
- GenAI OS API: http://localhost:8000
- Grace Agent: http://localhost:8001
- Alex Agent: http://localhost:8002
- FamilyConnect Backend: http://localhost:5000

## How It Works
1. GenAI OS (port 8000) manages agent discovery and routing
2. Grace Agent (port 8001) handles elderly companion interactions
3. Alex Agent (port 8002) handles family coordination
4. Both agents forward messages to your FamilyConnect app (port 5000)
5. Your FamilyConnect app processes the messages and returns responses

## Troubleshooting

### Agents Not Appearing in GenAI OS
- Check that GenAI OS is running: `docker compose ps`
- Check agent logs: `docker compose -f familyconnect-agents/docker-compose.familyconnect.yml logs`
- Manually register: `docker compose -f familyconnect-agents/docker-compose.familyconnect.yml run --rm agent-registrar`

### Agents Not Responding
- Verify FamilyConnect app is running on port 5000
- Check agent health: `curl http://localhost:8001/health` and `curl http://localhost:8002/health`
- Check agent logs for connection errors

### Connection Issues
- Ensure Docker networks are connected
- Check host.docker.internal connectivity
- Verify firewall settings

## Manual Alternative
If you prefer to run agents individually:
```bash
# In familyconnect-agents directory
python standalone_grace_agent.py &
python standalone_alex_agent.py &
python register-with-genai.py
```

## Expected Result
After successful integration:
- Grace and Alex appear in your GenAI OS dashboard
- Messages sent to agents are forwarded to your FamilyConnect app
- Responses maintain the agents' personalities and capabilities
- Full integration with GenAI OS features like conversation history and management