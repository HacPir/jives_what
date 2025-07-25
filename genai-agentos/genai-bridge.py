#!/usr/bin/env python3
"""
GenAI Protocol Bridge for FamilyConnect Agents
This creates GenAI protocol-compliant endpoints for Grace and Alex agents
"""

import asyncio
import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Request/Response models matching GenAI protocol
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

# Create FastAPI app
app = FastAPI(title="FamilyConnect GenAI Bridge", version="1.0.0")

# FamilyConnect backend URL
FAMILYCONNECT_URL = "http://localhost:5000"

class GenAIBridge:
    def __init__(self):
        self.familyconnect_url = FAMILYCONNECT_URL
        
    async def call_familyconnect_agent(self, agent_id: str, message: str) -> Dict[str, Any]:
        """Call FamilyConnect agent via its API"""
        try:
            # Use requests to call the FamilyConnect agent
            response = requests.post(
                f"{self.familyconnect_url}/api/agents/message",
                json={
                    "userId": 1,
                    "agentId": agent_id,
                    "message": message
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"message": f"Error: {response.status_code}", "error": True}
                
        except Exception as e:
            return {"message": f"Agent communication error: {str(e)}", "error": True}

# Initialize bridge
bridge = GenAIBridge()

# Grace Agent Endpoint
@app.post("/v1/grace/chat/completions")
async def grace_chat_completions(request: ChatRequest):
    """Grace agent chat completions endpoint"""
    
    # Get the last user message
    user_message = None
    for msg in reversed(request.messages):
        if msg.role == "user":
            user_message = msg.content
            break
    
    if not user_message:
        raise HTTPException(status_code=400, detail="No user message found")
    
    # Call Grace agent
    result = await bridge.call_familyconnect_agent("grace", user_message)
    
    # Format response
    response_content = result.get("message", "I'm here to help you.")
    
    return ChatResponse(
        id=f"grace-{datetime.now().timestamp()}",
        created=int(datetime.now().timestamp()),
        model="grace-familyconnect",
        choices=[{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response_content
            },
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": len(user_message.split()),
            "completion_tokens": len(response_content.split()),
            "total_tokens": len(user_message.split()) + len(response_content.split())
        }
    )

# Alex Agent Endpoint
@app.post("/v1/alex/chat/completions")
async def alex_chat_completions(request: ChatRequest):
    """Alex agent chat completions endpoint"""
    
    # Get the last user message
    user_message = None
    for msg in reversed(request.messages):
        if msg.role == "user":
            user_message = msg.content
            break
    
    if not user_message:
        raise HTTPException(status_code=400, detail="No user message found")
    
    # Call Alex agent
    result = await bridge.call_familyconnect_agent("alex", user_message)
    
    # Format response
    response_content = result.get("message", "I'm here to help coordinate care.")
    
    return ChatResponse(
        id=f"alex-{datetime.now().timestamp()}",
        created=int(datetime.now().timestamp()),
        model="alex-familyconnect",
        choices=[{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response_content
            },
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": len(user_message.split()),
            "completion_tokens": len(response_content.split()),
            "total_tokens": len(user_message.split()) + len(response_content.split())
        }
    )

# Health check endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FamilyConnect GenAI Bridge"}

@app.get("/v1/models")
async def list_models():
    """List available models"""
    return {
        "object": "list",
        "data": [
            {
                "id": "grace-familyconnect",
                "object": "model",
                "created": int(datetime.now().timestamp()),
                "owned_by": "familyconnect",
                "permission": [],
                "root": "grace-familyconnect",
                "parent": None
            },
            {
                "id": "alex-familyconnect", 
                "object": "model",
                "created": int(datetime.now().timestamp()),
                "owned_by": "familyconnect",
                "permission": [],
                "root": "alex-familyconnect",
                "parent": None
            }
        ]
    }

# Registration with GenAI OS
async def register_with_genai_os():
    """Register agents with GenAI OS"""
    
    # Try different GenAI OS endpoints - prioritize port 8000
    genai_endpoints = [
        "http://localhost:8000",
        "http://localhost:3000", 
        "http://genai-os:8000",
        "http://genai-backend:8000",
        "http://localhost:7860",
        "http://localhost:11434"
    ]
    
    agents = [
        {
            "name": "Grace",
            "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
            "endpoint": "http://localhost:8080/v1/grace/chat/completions",
            "model": "grace-familyconnect",
            "capabilities": ["companionship", "health_monitoring", "family_coordination"],
            "status": "active",
            "provider": "FamilyConnect"
        },
        {
            "name": "Alex",
            "description": "FamilyConnect family coordinator - professional care management",
            "endpoint": "http://localhost:8080/v1/alex/chat/completions", 
            "model": "alex-familyconnect",
            "capabilities": ["care_management", "family_coordination", "emergency_response"],
            "status": "active",
            "provider": "FamilyConnect"
        }
    ]
    
    for genai_url in genai_endpoints:
        try:
            # Test connection
            response = requests.get(f"{genai_url}/health", timeout=2)
            if response.status_code == 200:
                print(f"Found GenAI OS at {genai_url}")
                
                # Register agents
                for agent in agents:
                    try:
                        reg_response = requests.post(
                            f"{genai_url}/api/agents/register",
                            json=agent,
                            timeout=10
                        )
                        
                        if reg_response.status_code in [200, 201]:
                            print(f"✅ {agent['name']} registered with GenAI OS")
                        else:
                            print(f"⚠️  {agent['name']} registration failed: {reg_response.text}")
                            
                    except Exception as e:
                        print(f"⚠️  Error registering {agent['name']}: {e}")
                
                return True
                
        except Exception:
            continue
            
    print("GenAI OS not found - agents running locally")
    return False

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 FamilyConnect GenAI Bridge starting...")
    print("   - Grace agent: http://localhost:8080/v1/grace/chat/completions")
    print("   - Alex agent: http://localhost:8080/v1/alex/chat/completions")
    
    # Try to register with GenAI OS
    await register_with_genai_os()

if __name__ == "__main__":
    print("Starting FamilyConnect GenAI Bridge on port 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080)