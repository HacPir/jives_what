import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import httpx

# Agent JWT will be provided after registration
AGENT_JWT = "YOUR_AGENT_JWT_HERE"
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(name="Grace", description="FamilyConnect elderly companion - warm, caring AI for seniors")
async def grace_agent(
    agent_context: GenAIContext,
    message: Annotated[str, "User message to Grace"]
):
    """
    Grace - Elderly Companion Agent
    Provides warm, caring interaction for elderly users
    """
    try:
        # Forward to FamilyConnect backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://host.docker.internal:5000/api/agents/message",
                json={
                    "userId": 1,
                    "agentId": "grace", 
                    "message": message
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('message', 'Hello dear, how can I help you today?')}"
            else:
                return "Hello dear, I'm here to help. How are you feeling today?"
                
    except Exception as e:
        return f"Hello dear, I'm experiencing some technical difficulties, but I'm here to listen. How can I support you today?"

async def main():
    print(f"Grace Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
