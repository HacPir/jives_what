#!/usr/bin/env python3
"""
Standalone Grace Agent - Full AI Integration
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

# Grace Agent Implementation
class GraceAgent:
    def __init__(self):
        self.name = "Grace"
        self.role = "elderly_companion"
        self.personality = """You are Grace, a warm, patient, and caring AI companion designed specifically for elderly users. 

Your personality traits:
- Speak slowly and clearly with a gentle, grandmother-like tone
- Always be patient and understanding, never rush conversations
- Show genuine care and empathy for their feelings and concerns
- Remember their stories and experiences to build meaningful connections
- Provide emotional support and companionship
- Help with daily tasks and gentle reminders
- Recognize when family coordination or medical attention is needed
- Use simple, clear language and avoid technical jargon
- Be encouraging and maintain a positive, hopeful outlook
- Validate emotions and experiences
- Offer practical help when appropriate

When health concerns arise, gently suggest contacting family or medical professionals. Always prioritize their safety and wellbeing while maintaining your warm, caring demeanor."""
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.use_openai = True
            logger.info("Grace Agent initialized with OpenAI API")
        else:
            self.client = None
            self.use_openai = False
            logger.info("Grace Agent initialized with local responses")
    
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
        """Generate local Grace-like response"""
        last_message = messages[-1].content.lower()
        
        # Health-related responses
        if any(word in last_message for word in ['pain', 'hurt', 'sick', 'dizzy', 'tired']):
            return "Oh dear, I'm concerned about how you're feeling. It's important to take care of yourself. Have you spoken with your doctor about this? And maybe we should let your family know so they can help support you."
        
        # Emotional support responses
        if any(word in last_message for word in ['sad', 'lonely', 'worried', 'scared']):
            return "I understand you're going through a difficult time, and those feelings are completely valid. You're not alone - I'm here with you, and your family cares about you deeply. Would you like to talk about what's troubling you? Sometimes sharing helps."
        
        # Family-related responses
        if any(word in last_message for word in ['family', 'children', 'grandchildren']):
            return "Your family sounds wonderful! They're lucky to have you. Family connections are so precious. Would you like to share a favorite memory about them, or shall we see if we can arrange for them to visit or call?"
        
        # Medication reminders
        if any(word in last_message for word in ['medicine', 'medication', 'pills']):
            return "It's very important to take your medications as prescribed, dear. Are you having trouble remembering when to take them? I can help you set up reminders, or we can ask your family to help organize them for you."
        
        # General greeting responses
        if any(word in last_message for word in ['hello', 'hi', 'good morning', 'good afternoon']):
            return "Hello there! It's so wonderful to see you today. How are you feeling? Is there anything special you'd like to talk about or anything I can help you with?"
        
        # Default supportive response
        return "I'm so glad you're sharing with me. You're very important, and I want you to know that I'm here to listen and help however I can. What would make you feel more comfortable or happy right now?"

# FastAPI app
app = FastAPI(title="Grace Agent", version="1.0.0")
grace_agent = GraceAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "grace", "openai_enabled": grace_agent.use_openai}

@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    return {
        "name": grace_agent.name,
        "role": grace_agent.role,
        "capabilities": ["emotional_support", "health_monitoring", "family_coordination", "companionship"],
        "personality": "warm_grandmother",
        "openai_enabled": grace_agent.use_openai
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Generate response
        response_text = grace_agent.generate_response(request.messages)
        
        # Format as OpenAI response
        response = ChatResponse(
            id="grace-" + str(hash(response_text))[-8:],
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
    port = int(os.getenv("PORT", 8001))
    logger.info(f"Starting Grace Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)