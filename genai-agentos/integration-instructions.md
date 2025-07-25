# FamilyConnect GenAI OS Integration Guide

## Current Status
The FamilyConnect agents (Grace and Alex) are successfully running and responding to messages. They have been enhanced with:
- ✅ Inter-agent communication between Grace and Alex
- ✅ Voice interface with microphone permission handling  
- ✅ Real-time WebSocket communication
- ✅ Toast notifications for agent responses
- ✅ Voice announcements for agent communications

## Integration with GenAI OS

### Method 1: Direct API Integration (Recommended)
Since your GenAI OS is running, you can add the FamilyConnect agents as custom agents:

1. **Agent Endpoints:**
   - Grace: `http://localhost:5000/api/agents/message` (POST)
   - Alex: `http://localhost:5000/api/agents/message` (POST)

2. **Request Format:**
   ```json
   {
     "userId": 1,
     "agentId": "grace",  // or "alex"
     "message": "Your message here"
   }
   ```

3. **Response Format:**
   ```json
   {
     "message": "Agent response",
     "emotionalState": "neutral",
     "suggestedActions": ["action1", "action2"],
     "memoryTags": ["tag1", "tag2"]
   }
   ```

### Method 2: GenAI Protocol Bridge
If your GenAI OS requires OpenAI-compatible endpoints, use the bridge:

1. **Start the Bridge:**
   ```bash
   python3 genai-bridge.py
   ```

2. **OpenAI-Compatible Endpoints:**
   - Grace: `http://localhost:8080/v1/grace/chat/completions`
   - Alex: `http://localhost:8080/v1/alex/chat/completions`

3. **Request Format (OpenAI-compatible):**
   ```json
   {
     "model": "grace-familyconnect",
     "messages": [{"role": "user", "content": "Hello"}],
     "max_tokens": 500
   }
   ```

### Method 3: Docker Integration
Add FamilyConnect to your GenAI OS Docker Compose:

```yaml
services:
  familyconnect:
    image: familyconnect-agents:latest
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - genai-backend
```

## Agent Capabilities

### Grace Agent (Elderly Companion)
- **Personality:** Warm, patient, caring (like a grandmother)
- **Capabilities:**
  - Emotional support and companionship
  - Health monitoring and appointment reminders
  - Family connection facilitation
  - Voice interaction with speech recognition
  - Memory of conversations and preferences

### Alex Agent (Family Coordinator)
- **Personality:** Professional, organized, efficient
- **Capabilities:**
  - Care management and coordination
  - Family communication and updates
  - Emergency response coordination
  - Appointment scheduling and reminders
  - Health status monitoring

## Inter-Agent Communication
The agents can communicate with each other:
- Grace can alert Alex about health concerns
- Alex can coordinate family responses
- Both agents share context and memory
- Real-time notifications via WebSocket

## Voice Interface
Both agents support:
- Speech recognition for voice input
- Text-to-speech for voice responses
- Microphone permission handling
- Voice activity detection

## Next Steps

1. **Test the Integration:**
   - Open your GenAI OS dashboard
   - Try adding a custom agent with the FamilyConnect endpoints
   - Test communication with both Grace and Alex

2. **Configure Your GenAI OS:**
   - Add FamilyConnect as a custom provider
   - Configure the agent endpoints
   - Set up authentication if needed

3. **Monitor and Test:**
   - Check that agents appear in your dashboard
   - Test conversations with both agents
   - Verify inter-agent communication works

## Support
If you need help with the integration:
1. Check the FamilyConnect logs in the workflow console
2. Test the agent endpoints directly with curl
3. Verify your GenAI OS configuration
4. The agents will work locally even without GenAI OS integration

## Available Files
- `genai-bridge.py` - OpenAI-compatible bridge server
- `grace-agent-manifest.json` - Grace agent configuration
- `alex-agent-manifest.json` - Alex agent configuration
- `register-familyconnect-agents.py` - Registration script
- `integration-instructions.md` - This guide