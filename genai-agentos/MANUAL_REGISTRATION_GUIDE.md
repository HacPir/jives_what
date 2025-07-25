# Manual Registration Guide for GenAI OS Dashboard

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
curl -X POST http://localhost:5000/api/agents/message \
  -H "Content-Type: application/json" \
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
