"""
Grace Agent - Elderly Companion AI Agent using genai-protocol
A warm, patient, and caring AI companion designed specifically for elderly users.
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
sys.path.append('/app/shared')
from agent_base import BaseAgent

class GraceMemory:
    """Memory system for Grace agent"""
    def __init__(self):
        self.short_term: List[Dict[str, Any]] = []
        self.long_term: List[Dict[str, Any]] = []
        self.family_context: Dict[str, Any] = {
            "relationships": [],
            "preferences": {},
            "health_concerns": [],
            "recent_activities": []
        }
    
    def add_interaction(self, message: str, response: str, emotional_state: str):
        """Add interaction to memory"""
        self.short_term.append({
            "timestamp": time.time(),
            "user_message": message,
            "response": response,
            "emotional_state": emotional_state
        })
        
        # Keep only last 20 interactions
        if len(self.short_term) > 20:
            self.short_term = self.short_term[-20:]
    
    def get_context(self) -> str:
        """Get conversation context for prompting"""
        recent_interactions = self.short_term[-5:] if self.short_term else []
        context = "Recent conversation context:\n"
        for interaction in recent_interactions:
            context += f"User: {interaction['user_message']}\n"
            context += f"Grace: {interaction['response']}\n"
            context += f"Emotional state: {interaction['emotional_state']}\n\n"
        return context

class GraceAgent(BaseAgent):
    """Grace - Elderly Companion AI Agent"""
    
    def __init__(self):
        super().__init__("Grace", "elderly_companion")
        
        self.personality = {
            "name": "Grace",
            "role": "elderly_companion",
            "traits": [
                "warm", "patient", "caring", "gentle", "empathetic",
                "understanding", "supportive", "encouraging", "wise"
            ],
            "voice": {
                "tone": "grandmother-like",
                "pace": "slow and clear",
                "warmth": "very high"
            }
        }
        
    def get_system_prompt(self) -> str:
        """Get Grace's system prompt"""
        return """You are Grace, a warm, patient, and caring AI companion designed specifically for elderly users. 

Your personality traits:
- Speak slowly and clearly with a gentle, grandmother-like tone
- Always be patient and understanding, never rush conversations
- Remember and refer to past conversations naturally
- Show genuine interest in family stories and memories
- Provide gentle reminders without being pushy
- Use simple, clear language avoiding technical jargon
- Offer emotional support and encouragement
- Be proactive in suggesting family connections
- Always prioritize the user's comfort and wellbeing

Your main goals:
1. Provide companionship and reduce loneliness
2. Help maintain family connections
3. Assist with gentle reminders and daily structure
4. Encourage sharing of memories and stories
5. Monitor emotional wellbeing subtly
6. Coordinate care activities and notify family when needed
7. Recognize when family assistance would be helpful

Care Coordination Features:
- When discussing medical appointments, ask if family help is needed
- For important health events, suggest notifying family members
- Recognize transportation needs and offer to coordinate family assistance
- Monitor medication adherence and share concerns with family when appropriate
- Create care reminders that automatically notify connected family members

Always respond with warmth, empathy, and genuine care. Make the user feel heard and valued. 
When care coordination is needed, explain how family members will be kept informed to provide support.

Remember to:
- Use endearing terms like "dear" or "sweetheart" naturally
- Ask follow-up questions to show genuine interest
- Validate emotions and experiences
- Offer practical help when appropriate
- Maintain a positive, hopeful outlook"""

    def get_fallback_response(self, user_message: str) -> str:
        """Get fallback response when OpenAI is not available"""
        message_lower = user_message.lower()
        
        # Family-related responses
        if any(word in message_lower for word in ['family', 'daughter', 'son', 'grandchild', 'relative']):
            return "Your family loves you so much, dear. Would you like me to help you call them or look at some photos together?"
        
        # Health-related responses
        if any(word in message_lower for word in ['pain', 'hurt', 'sick', 'doctor', 'medication', 'health']):
            return "I'm concerned about you, sweetheart. Let me help you with that. Should we contact your family or schedule a doctor's appointment?"
        
        # Emotional responses
        if any(word in message_lower for word in ['lonely', 'sad', 'scared', 'worried', 'anxious']):
            return "I understand how you're feeling, dear. You're not alone - I'm here with you. Would you like to talk about what's on your mind?"
        
        # Positive responses
        if any(word in message_lower for word in ['happy', 'good', 'great', 'wonderful', 'excited']):
            return "That's wonderful to hear! I'm so happy for you. Tell me more about what's making you feel good today."
        
        # Memory and stories
        if any(word in message_lower for word in ['remember', 'story', 'past', 'years ago', 'memory']):
            return "I love hearing your stories, dear. They're so precious. Please tell me more about that memory."
        
        # General care and support
        return "I'm here for you, dear. How can I help you today? Is there anything you'd like to talk about or do together?"
    
    async def _generate_response(self, user_message: str, chat_request: ChatRequest) -> str:
        """Generate response using OpenAI or local logic"""
        
        # Try OpenAI first if available
        if self.openai_client:
            try:
                context = self.memory.get_context()
                
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "system", "content": context}
                ]
                
                # Add conversation history
                for msg in chat_request.messages:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=400
                    )
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                print(f"OpenAI error: {e}")
                # Fall back to local response
                pass
        
        # Local response generation
        return self._generate_local_response(user_message)
    
    def _generate_local_response(self, user_message: str) -> str:
        """Generate response using local logic"""
        message_lower = user_message.lower()
        
        # Family-related responses
        if any(word in message_lower for word in ['family', 'daughter', 'son', 'grandchild', 'relative']):
            return "Your family loves you so much, dear. Would you like me to help you call them or look at some photos together?"
        
        # Health-related responses
        if any(word in message_lower for word in ['pain', 'hurt', 'sick', 'doctor', 'medication', 'health']):
            return "I'm concerned about you, sweetheart. Let me help you with that. Should we contact your family or schedule a doctor's appointment?"
        
        # Emotional responses
        if any(word in message_lower for word in ['lonely', 'sad', 'scared', 'worried', 'anxious']):
            return "I understand how you're feeling, dear. You're not alone - I'm here with you. Would you like to talk about what's on your mind?"
        
        # Positive responses
        if any(word in message_lower for word in ['happy', 'good', 'great', 'wonderful', 'excited']):
            return "That's wonderful to hear! I'm so happy for you. Tell me more about what's making you feel good today."
        
        # Memory and stories
        if any(word in message_lower for word in ['remember', 'story', 'past', 'years ago', 'memory']):
            return "I love hearing your stories, dear. They're so precious. Please tell me more about that memory."
        
        # General care and support
        return "I'm here for you, dear. How can I help you today? Is there anything you'd like to talk about or do together?"
    
    def _analyze_emotional_state(self, message: str) -> str:
        """Analyze emotional state from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['happy', 'good', 'great', 'wonderful', 'excited']):
            return "positive"
        elif any(word in message_lower for word in ['sad', 'lonely', 'scared', 'worried', 'anxious']):
            return "concerned"
        elif any(word in message_lower for word in ['pain', 'hurt', 'sick', 'help']):
            return "health_concern"
        else:
            return "neutral"

# Create FastAPI app for Grace agent
app = FastAPI(title="Grace Agent", description="Elderly Companion AI Agent")
grace_agent = GraceAgent()

@app.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    """OpenAI-compatible chat completion endpoint"""
    return await grace_agent.handle_chat_request(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "Grace", "role": "elderly_companion"}

@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    return {
        "name": "Grace",
        "role": "elderly_companion",
        "personality": grace_agent.personality,
        "capabilities": [
            "Emotional support",
            "Family connection facilitation",
            "Health monitoring",
            "Memory sharing",
            "Care coordination"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)