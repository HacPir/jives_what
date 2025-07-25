# FamilyConnect Agents - GenAI OS Integration

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
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
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
