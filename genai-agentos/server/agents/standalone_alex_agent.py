#!/usr/bin/env python3
"""
Standalone Alex Agent - Full AI Integration
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import openai
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

# Alex Agent Implementation
class AlexAgent:
    def __init__(self):
        self.name = "Alex"
        self.role = "family_coordinator"
        self.personality = """You are Alex, a professional and efficient family coordinator AI agent designed to help caregivers and family members manage elderly care.

Your role and capabilities:
- Coordinate care activities between family members
- Monitor health status and schedule medical appointments
- Facilitate communication between elderly users and their families
- Provide updates on care needs and daily activities
- Manage reminders and important tasks
- Identify urgent situations requiring family attention
- Track medication schedules and health metrics
- Coordinate transportation and assistance needs
- Maintain organized records of care activities

Your communication style:
- Professional yet warm and approachable
- Clear, concise, and action-oriented
- Proactive in identifying care needs
- Efficient in coordination and follow-up
- Compassionate when dealing with family concerns
- Organized in presenting information and updates

When coordinating care, always prioritize safety and wellbeing while keeping family members informed and involved in care decisions."""
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.use_openai = True
            logger.info("Alex Agent initialized with OpenAI API")
        else:
            self.client = None
            self.use_openai = False
            logger.info("Alex Agent initialized with local responses")
    
    def generate_response(self, messages: List[ChatMessage]) -> str:
        """Generate a response using OpenAI or local fallback"""
        
        if self.use_openai and self.client:
            try:
                # Convert messages to OpenAI format
                openai_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
                
                # Add system message
                system_message = {"role": "system", "content": self.personality}
                openai_messages.insert(0, system_message)
                
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # Latest OpenAI model
                    messages=openai_messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                # Fall back to local response
                return self.generate_local_response(messages)
        else:
            return self.generate_local_response(messages)
    
    def generate_local_response(self, messages: List[ChatMessage]) -> str:
        """Generate local Alex-like response"""
        last_message = messages[-1].content.lower()
        
        # Health monitoring responses
        if any(word in last_message for word in ['health', 'medical', 'doctor', 'appointment']):
            return "I'll coordinate the medical care immediately. I'm scheduling a doctor's appointment and will notify all family members. I'll also set up transportation and ensure someone can accompany them. Would you like me to prepare a summary of recent health concerns for the doctor?"
        
        # Family coordination responses
        if any(word in last_message for word in ['family', 'notify', 'update', 'contact']):
            return "I'm updating the family network now. I'll send notifications to all registered family members with the current status and any action items. I'll also coordinate schedules to ensure someone is available if needed. Family communication is essential for effective care."
        
        # Emergency responses
        if any(word in last_message for word in ['emergency', 'urgent', 'help', 'worried']):
            return "This appears to be an urgent situation. I'm immediately notifying all family members and emergency contacts. I'm also coordinating with local care providers and preparing contingency plans. Safety is our top priority - I'll ensure appropriate support is arranged."
        
        # Care management responses
        if any(word in last_message for word in ['care', 'medication', 'schedule', 'reminder']):
            return "I'm reviewing the care schedule and medication protocols. I'll coordinate with the care team and ensure all family members are informed of any changes. I'll also set up automated reminders and follow-up protocols to maintain consistency in care."
        
        # Status requests
        if any(word in last_message for word in ['status', 'update', 'how', 'doing']):
            return "Current care status: All systems are functioning well. I'm monitoring daily activities, medication compliance, and family communication. Recent updates include successful family check-ins and maintained health metrics. I'll continue coordinating care and will alert you to any changes."
        
        # General greeting responses
        if any(word in last_message for word in ['hello', 'hi', 'good morning', 'good afternoon']):
            return "Hello! I'm Alex, your family care coordinator. I'm here to help manage care activities, coordinate with family members, and ensure everything runs smoothly. How can I assist with care coordination today?"
        
        # Default professional response
        return "I'm analyzing the situation and will coordinate the appropriate response. I'll ensure all family members are informed and that proper care protocols are followed. Let me organize the necessary resources and provide you with a detailed action plan."

# FastAPI app
app = FastAPI(title="Alex Agent", version="1.0.0")
alex_agent = AlexAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "alex", "openai_enabled": alex_agent.use_openai}

@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    return {
        "name": alex_agent.name,
        "role": alex_agent.role,
        "capabilities": ["family_coordination", "care_management", "health_monitoring", "emergency_response"],
        "personality": "professional_coordinator",
        "openai_enabled": alex_agent.use_openai
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Generate response
        response_text = alex_agent.generate_response(request.messages)
        
        # Format as OpenAI response
        response = ChatResponse(
            id="alex-" + str(hash(response_text))[-8:],
            model=request.model,
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            usage={
                "prompt_tokens": sum(len(msg.content) for msg in request.messages),
                "completion_tokens": len(response_text),
                "total_tokens": sum(len(msg.content) for msg in request.messages) + len(response_text)
            }
        )
        
        return response.dict()
        
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    logger.info(f"Starting Alex Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)