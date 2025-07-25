import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import httpx

# Agent JWT will be provided after registration
AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4MTg3NmI0MS1hMjYzLTRjODYtYjJmZS1hOWNlMzQ1OGI5NTciLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImJhYzkyZWRhLTAzOTQtNDUwZi1iNjBhLWMyY2RkMDEwOTc0ZSJ9.7XZK5MzYMr9oOoWXHWQkOHTT8eO69xSqfL-tqFk5z70"
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(name="Alex", description="FamilyConnect family coordinator - professional care management")
async def alex_agent(
    agent_context: GenAIContext,
    message: Annotated[str, "User message to Alex"]
):
    """
    Alex - Family Coordinator Agent
    Provides professional care management and family coordination
    """
    try:
        # Forward to FamilyConnect backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://host.docker.internal:5000/api/agents/message",
                json={
                    "userId": 1,
                    "agentId": "alex",
                    "message": message
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('message', 'Hello, I can help coordinate care for your family.')}"
            else:
                return "Hello, I can help coordinate care for your family. What do you need assistance with?"
                
    except Exception as e:
        return f"Hello, I'm experiencing some technical difficulties, but I'm here to help coordinate care. What can I assist you with?"

async def main():
    print(f"Alex Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
