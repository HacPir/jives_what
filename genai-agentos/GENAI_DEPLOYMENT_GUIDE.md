# FamilyConnect GenAI OS Deployment Guide

## Quick Start (Recommended)

The FamilyConnect agents are working and ready to integrate with your GenAI OS dashboard.

### Option 1: Add as Custom Agents in GenAI OS Dashboard

1. **Access your GenAI OS dashboard** (the one you showed in the screenshot)

2. **Add Custom Agent - Grace:**
   - Name: `Grace`
   - Description: `FamilyConnect elderly companion - warm, caring AI for seniors`
   - API Endpoint: `http://localhost:5000/api/agents/message`
   - Method: `POST`
   - Request format:
     ```json
     {
       "userId": 1,
       "agentId": "grace",
       "message": "{{user_message}}"
     }
     ```

3. **Add Custom Agent - Alex:**
   - Name: `Alex`
   - Description: `FamilyConnect family coordinator - professional care management`
   - API Endpoint: `http://localhost:5000/api/agents/message`
   - Method: `POST`
   - Request format:
     ```json
     {
       "userId": 1,
       "agentId": "alex",
       "message": "{{user_message}}"
     }
     ```

### Option 2: Docker Integration (Advanced)

If you're using Docker Compose for your GenAI OS:

1. **Add to your existing docker-compose.yml:**
   ```yaml
   services:
     familyconnect:
       image: familyconnect-agents:latest
       ports:
         - "5000:5000"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - DATABASE_URL=${DATABASE_URL}
       networks:
         - genai-network
   ```

2. **Build the FamilyConnect image:**
   ```bash
   docker build -t familyconnect-agents .
   ```

3. **Add to your GenAI OS networks:**
   ```yaml
   networks:
     genai-network:
       driver: bridge
   ```

## Testing the Integration

1. **Test Grace Agent:**
   ```bash
   curl -X POST http://localhost:5000/api/agents/message \
     -H "Content-Type: application/json" \
     -d '{
       "userId": 1,
       "agentId": "grace",
       "message": "Hello, how are you today?"
     }'
   ```

2. **Test Alex Agent:**
   ```bash
   curl -X POST http://localhost:5000/api/agents/message \
     -H "Content-Type: application/json" \
     -d '{
       "userId": 1,
       "agentId": "alex",
       "message": "Can you help coordinate care for my elderly parent?"
     }'
   ```

## Agent Capabilities

### Grace (Elderly Companion)
- Warm, patient, caring personality
- Emotional support and companionship
- Health monitoring and reminders
- Family connection facilitation
- Voice interaction support
- Memory of conversations

### Alex (Family Coordinator)
- Professional, organized personality
- Care management and coordination
- Family communication and updates
- Emergency response coordination
- Appointment scheduling
- Health status monitoring

## Advanced Features

### Inter-Agent Communication
- Grace can alert Alex about health concerns
- Alex can coordinate family responses
- Both agents share context and memory
- Real-time notifications via WebSocket

### Voice Interface
- Speech recognition for voice input
- Text-to-speech for voice responses
- Microphone permission handling
- Voice activity detection

### Real-time Updates
- WebSocket-based communication
- Live family status updates
- Inter-agent messaging
- Toast notifications

## Troubleshooting

1. **Agents not appearing in GenAI OS:**
   - Check that FamilyConnect is running on port 5000
   - Verify your GenAI OS can reach localhost:5000
   - Test the endpoints directly with curl

2. **Connection issues:**
   - Ensure both services are on the same network
   - Check firewall settings
   - Verify environment variables are set

3. **Agent responses not working:**
   - Check the FamilyConnect logs
   - Verify OpenAI API key is configured
   - Test with local AI fallback

## Next Steps

1. **Configure in GenAI OS:**
   - Add the agents as custom endpoints
   - Test communication with both Grace and Alex
   - Set up any authentication if needed

2. **Test Features:**
   - Try voice interaction
   - Test inter-agent communication
   - Verify real-time updates

3. **Production Deployment:**
   - Set up proper authentication
   - Configure SSL/TLS
   - Set up monitoring and logging

## Support

The FamilyConnect agents are fully functional and ready for integration. They work independently and don't require GenAI OS to function, but they can be easily integrated into your existing setup.

For additional help:
- Check the integration-instructions.md file
- Review the agent manifest files
- Test the endpoints directly
- Monitor the FamilyConnect logs