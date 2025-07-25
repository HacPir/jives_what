# FamilyConnect × GenAI OS Integration Guide

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
curl -X POST "http://localhost:8000/api/agents/message" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "grace-agent-id",
    "message": "Hello Grace, how are you?"
  }'

# Test Alex agent
curl -X POST "http://localhost:8000/api/agents/message" \
  -H "Content-Type: application/json" \
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
