"""
Agent Manager - Centralized coordination for Grace and Alex agents
"""

import asyncio
import json
import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn

class AgentManagerConfig(BaseModel):
    grace_agent_url: str = "http://localhost:8001"
    alex_agent_url: str = "http://localhost:8002"
    port: int = 8000

class InterAgentMessage(BaseModel):
    from_agent: str
    to_agent: str
    message: str
    priority: str = "medium"
    context: Optional[Dict[str, Any]] = None

class AgentManager:
    """Centralized agent coordination"""
    
    def __init__(self, config: AgentManagerConfig):
        self.config = config
        self.agents = {
            "grace": config.grace_agent_url,
            "alex": config.alex_agent_url
        }
        self.communication_log: List[Dict[str, Any]] = []
    
    async def check_agent_health(self, agent_id: str) -> bool:
        """Check if an agent is healthy"""
        try:
            agent_url = self.agents.get(agent_id)
            if not agent_url:
                return False
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{agent_url}/health", timeout=5.0)
                return response.status_code == 200
        except:
            return False
    
    async def send_message_to_agent(self, agent_id: str, message: str, context: Dict[str, Any] = None) -> str:
        """Send message to specific agent"""
        agent_url = self.agents.get(agent_id)
        if not agent_url:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        payload = {
            "model": f"{agent_id}-agent",
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 400
        }
        
        if context:
            payload["messages"].insert(0, {
                "role": "system",
                "content": f"Context: {json.dumps(context)}"
            })
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{agent_url}/v1/chat/completions",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    raise HTTPException(status_code=response.status_code, detail="Agent communication failed")
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Agent timeout")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Agent communication error: {str(e)}")
    
    async def facilitate_inter_agent_communication(self, inter_message: InterAgentMessage) -> Dict[str, Any]:
        """Facilitate communication between agents"""
        # Add inter-agent context
        context = inter_message.context or {}
        context.update({
            "inter_agent_communication": True,
            "from_agent": inter_message.from_agent,
            "priority": inter_message.priority,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Send message to target agent
        response = await self.send_message_to_agent(
            inter_message.to_agent,
            inter_message.message,
            context
        )
        
        # Log the communication
        communication_entry = {
            "id": len(self.communication_log) + 1,
            "from_agent": inter_message.from_agent,
            "to_agent": inter_message.to_agent,
            "message": inter_message.message,
            "response": response,
            "priority": inter_message.priority,
            "timestamp": asyncio.get_event_loop().time(),
            "context": context
        }
        
        self.communication_log.append(communication_entry)
        
        return communication_entry
    
    async def get_all_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        
        for agent_id, agent_url in self.agents.items():
            try:
                is_healthy = await self.check_agent_health(agent_id)
                
                if is_healthy:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{agent_url}/agent/info", timeout=5.0)
                        if response.status_code == 200:
                            status[agent_id] = response.json()
                        else:
                            status[agent_id] = {"status": "error", "name": agent_id.title()}
                else:
                    status[agent_id] = {"status": "offline", "name": agent_id.title()}
            except Exception as e:
                status[agent_id] = {"status": "error", "name": agent_id.title(), "error": str(e)}
        
        return status

# Initialize FastAPI app
app = FastAPI(title="GenAI Agent Manager", version="1.0.0")

# Initialize agent manager
config = AgentManagerConfig(
    grace_agent_url=os.getenv("GRACE_AGENT_URL", "http://localhost:8001"),
    alex_agent_url=os.getenv("ALEX_AGENT_URL", "http://localhost:8002"),
    port=int(os.getenv("PORT", 8000))
)

agent_manager = AgentManager(config)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agent_manager"}

@app.get("/agent/info")
async def agent_info():
    """Get agent manager information"""
    return {
        "name": "Agent Manager",
        "role": "agent_coordinator",
        "status": "running",
        "capabilities": [
            "inter_agent_communication",
            "agent_health_monitoring",
            "message_routing",
            "communication_logging"
        ],
        "managed_agents": list(agent_manager.agents.keys())
    }

@app.post("/agent/message")
async def send_message(agent_id: str, message: str, context: Optional[Dict[str, Any]] = None):
    """Send message to specific agent"""
    response = await agent_manager.send_message_to_agent(agent_id, message, context)
    return {"agent_id": agent_id, "response": response}

@app.post("/agent/communicate")
async def inter_agent_communication(inter_message: InterAgentMessage):
    """Facilitate inter-agent communication"""
    result = await agent_manager.facilitate_inter_agent_communication(inter_message)
    return result

@app.get("/agent/status")
async def get_agent_status():
    """Get status of all agents"""
    return await agent_manager.get_all_agent_status()

@app.get("/agent/communications")
async def get_communications():
    """Get communication log"""
    return {"communications": agent_manager.communication_log}

if __name__ == "__main__":
    port = config.port
    print(f"Starting Agent Manager on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)