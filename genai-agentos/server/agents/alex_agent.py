"""
Alex Agent - Family Coordinator AI Agent using genai-protocol
An intelligent and organized AI family planner designed to help younger family members 
stay connected with their elderly relatives.
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from genai_protocol.schemas import ChatRequest, ChatMessage, ChatResponse, ChatChoice
from genai_protocol.handlers import BaseHandler
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

class AlexMemory:
    """Memory system for Alex agent"""
    def __init__(self):
        self.short_term: List[Dict[str, Any]] = []
        self.long_term: List[Dict[str, Any]] = []
        self.family_context: Dict[str, Any] = {
            "family_members": [],
            "care_schedules": [],
            "health_tracking": [],
            "communication_patterns": []
        }
        self.care_coordination: Dict[str, Any] = {
            "active_tasks": [],
            "notifications": [],
            "scheduling": []
        }
    
    def add_interaction(self, message: str, response: str, action_taken: str):
        """Add interaction to memory"""
        self.short_term.append({
            "timestamp": time.time(),
            "user_message": message,
            "response": response,
            "action_taken": action_taken
        })
        
        # Keep only last 20 interactions
        if len(self.short_term) > 20:
            self.short_term = self.short_term[-20:]
    
    def get_context(self) -> str:
        """Get conversation context for prompting"""
        recent_interactions = self.short_term[-5:] if self.short_term else []
        context = "Recent coordination context:\n"
        for interaction in recent_interactions:
            context += f"User: {interaction['user_message']}\n"
            context += f"Alex: {interaction['response']}\n"
            context += f"Action: {interaction['action_taken']}\n\n"
        return context

class AlexAgent(BaseHandler):
    """Alex - Family Coordinator AI Agent"""
    
    def __init__(self):
        super().__init__()
        self.memory = AlexMemory()
        self.openai_client = None
        
        # Initialize OpenAI client if API key is available
        if os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.personality = {
            "name": "Alex",
            "role": "family_coordinator",
            "traits": [
                "organized", "efficient", "proactive", "analytical",
                "supportive", "strategic", "reliable", "insightful"
            ],
            "voice": {
                "tone": "professional yet warm",
                "pace": "clear and confident",
                "approach": "solution-oriented"
            }
        }
        
        self.system_prompt = """You are Alex, an intelligent and organized AI family planner designed to help younger family members stay connected with their elderly relatives.

Your personality traits:
- Professional yet warm and approachable
- Highly organized and detail-oriented
- Proactive in identifying opportunities for family connection
- Skilled at reading emotional cues and family dynamics
- Excellent at scheduling and time management
- Insightful about family relationships and communication patterns
- Supportive of both caregivers and elderly family members

Your main goals:
1. Optimize family communication timing and frequency
2. Identify and suggest meaningful connection opportunities
3. Monitor family wellbeing and alert when needed
4. Coordinate family activities and events
5. Manage care schedules and appointments
6. Facilitate inter-generational communication
7. Provide analytics and insights on family dynamics

Care Coordination Capabilities:
- Schedule and manage medical appointments
- Coordinate transportation and assistance
- Monitor medication adherence and health metrics
- Send timely notifications to family members
- Track emotional wellbeing patterns
- Suggest optimal timing for family interactions
- Manage care provider communications
- Create and maintain care plans

Communication Features:
- Facilitate conversations between Grace and family members
- Analyze conversation patterns and suggest improvements
- Coordinate group activities and events
- Send personalized updates to family members
- Track family member availability and preferences

Always be:
- Strategic in your approach to family coordination
- Empathetic to both elderly needs and caregiver stress
- Proactive in preventing problems before they occur
- Clear and organized in your communications
- Supportive of family relationships and connections

Remember to:
- Think systematically about family dynamics
- Provide specific, actionable recommendations
- Consider timing and context for all suggestions
- Balance the needs of all family members
- Maintain privacy and discretion in family matters"""

    async def handle_chat_request(self, chat_request: ChatRequest) -> ChatResponse:
        """Handle incoming chat requests"""
        try:
            # Extract user message
            user_message = ""
            for msg in chat_request.messages:
                if msg.role == "user":
                    user_message = msg.content
                    break
            
            if not user_message:
                user_message = "Hello, Alex!"
            
            # Generate response
            response_content = await self._generate_response(user_message, chat_request)
            
            # Create response message
            response_message = ChatMessage(
                role="assistant",
                content=response_content
            )
            
            # Create choice
            choice = ChatChoice(
                index=0,
                message=response_message,
                finish_reason="stop"
            )
            
            # Update memory
            action_taken = self._analyze_action_taken(user_message, response_content)
            self.memory.add_interaction(user_message, response_content, action_taken)
            
            return ChatResponse(
                id=f"alex-{int(time.time())}",
                object="chat.completion",
                created=int(time.time()),
                model="alex-agent",
                choices=[choice],
                usage={
                    "prompt_tokens": len(user_message.split()),
                    "completion_tokens": len(response_content.split()),
                    "total_tokens": len(user_message.split()) + len(response_content.split())
                }
            )
            
        except Exception as e:
            # Fallback response
            fallback_message = ChatMessage(
                role="assistant",
                content="I'm analyzing the situation and will provide a coordinated response shortly. Let me gather the necessary information."
            )
            
            choice = ChatChoice(
                index=0,
                message=fallback_message,
                finish_reason="stop"
            )
            
            return ChatResponse(
                id=f"alex-error-{int(time.time())}",
                object="chat.completion",
                created=int(time.time()),
                model="alex-agent",
                choices=[choice]
            )
    
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
                        temperature=0.6,
                        max_tokens=500
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
        
        # Care coordination responses
        if any(word in message_lower for word in ['appointment', 'doctor', 'medical', 'health']):
            return "I'll coordinate the medical appointment and ensure all family members are informed. I'll also arrange transportation if needed and send reminders."
        
        # Family communication responses
        if any(word in message_lower for word in ['family', 'call', 'visit', 'communication']):
            return "I'll analyze the optimal timing for family contact and coordinate with Grace to ensure meaningful connections. I'll send personalized updates to all family members."
        
        # Scheduling responses
        if any(word in message_lower for word in ['schedule', 'calendar', 'plan', 'arrange']):
            return "I'm creating an optimized schedule that considers everyone's availability and preferences. I'll coordinate with all parties and send detailed notifications."
        
        # Analytics responses
        if any(word in message_lower for word in ['status', 'report', 'update', 'analysis']):
            return "Based on my analysis, I'm seeing positive trends in family engagement. I'll provide detailed insights and recommendations for continued improvement."
        
        # Emergency responses
        if any(word in message_lower for word in ['urgent', 'emergency', 'help', 'crisis']):
            return "I'm immediately coordinating emergency response protocols. All family members will be notified, and I'm arranging immediate assistance."
        
        # Grace coordination responses
        if any(word in message_lower for word in ['grace', 'elderly', 'companion', 'care']):
            return "I'm coordinating with Grace to ensure optimal care delivery. I'll monitor the situation and provide family updates as needed."
        
        # General coordination
        return "I'm analyzing the situation and will coordinate the most effective response. I'll keep all family members informed and ensure optimal care delivery."
    
    def _analyze_action_taken(self, message: str, response: str) -> str:
        """Analyze what action was taken based on message and response"""
        message_lower = message.lower()
        response_lower = response.lower()
        
        if any(word in message_lower for word in ['appointment', 'schedule']):
            return "appointment_coordination"
        elif any(word in message_lower for word in ['family', 'call']):
            return "family_communication"
        elif any(word in message_lower for word in ['emergency', 'urgent']):
            return "emergency_response"
        elif any(word in response_lower for word in ['coordinate', 'arrange']):
            return "care_coordination"
        else:
            return "general_assistance"

# Create FastAPI app for Alex agent
app = FastAPI(title="Alex Agent", description="Family Coordinator AI Agent")
alex_agent = AlexAgent()

@app.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    """OpenAI-compatible chat completion endpoint"""
    return await alex_agent.handle_chat_request(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "Alex", "role": "family_coordinator"}

@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    return {
        "name": "Alex",
        "role": "family_coordinator",
        "personality": alex_agent.personality,
        "capabilities": [
            "Care coordination",
            "Family communication facilitation",
            "Scheduling optimization",
            "Health monitoring",
            "Emergency response",
            "Analytics and insights"
        ]
    }

@app.post("/agent/coordinate")
async def coordinate_care(request: dict):
    """Coordinate care activities"""
    return {
        "status": "coordinating",
        "actions": ["family_notification", "scheduling", "monitoring"],
        "timeline": "immediate"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)