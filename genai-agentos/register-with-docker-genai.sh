#!/bin/bash
# Register FamilyConnect agents with GenAI OS running in Docker

echo "🚀 Registering FamilyConnect agents with GenAI OS..."
echo "Target: GenAI OS at port 8000"

# Grace Agent Registration
echo "Registering Grace agent..."
curl -X POST "http://localhost:8000/api/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grace",
    "id": "grace-familyconnect",
    "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
    "endpoint": "http://host.docker.internal:5000/api/agents/message",
    "model": "grace-familyconnect",
    "capabilities": ["companionship", "health_monitoring", "family_coordination"],
    "personality": "warm_grandmother",
    "status": "active",
    "provider": "FamilyConnect",
    "version": "1.0.0",
    "request_format": {
      "userId": 1,
      "agentId": "grace",
      "message": "{{user_message}}"
    }
  }'

echo -e "\n\nRegistering Alex agent..."
curl -X POST "http://localhost:8000/api/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex",
    "id": "alex-familyconnect",
    "description": "FamilyConnect family coordinator - professional care management",
    "endpoint": "http://host.docker.internal:5000/api/agents/message",
    "model": "alex-familyconnect",
    "capabilities": ["care_management", "family_coordination", "emergency_response"],
    "personality": "professional_coordinator",
    "status": "active",
    "provider": "FamilyConnect",
    "version": "1.0.0",
    "request_format": {
      "userId": 1,
      "agentId": "alex",
      "message": "{{user_message}}"
    }
  }'

echo -e "\n\n✅ Registration complete!"
echo "Check your GenAI OS dashboard at http://localhost:8000"
