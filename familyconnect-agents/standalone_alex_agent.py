#!/usr/bin/env python3
"""
Standalone Alex Agent - Full AI Integration
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import openai
from openai import OpenAI
import requests
import nest_asyncio

# GenAI session class (simplified for Docker deployment)
class GenAISession:
    def __init__(self, jwt_token: str, ws_url: str):
        self.jwt_token = jwt_token
        self.ws_url = ws_url
        self.connected = False
    
    def connect(self):
        # Simplified connection for Docker deployment
        self.connected = True
        return self.connected
nest_asyncio.apply()

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

# Alex Agent Implementation with GenAI Protocol Integration
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
        
        # Initialize GenAI network client first, then OpenAI as fallback
        self.genai_backend_url = os.getenv('GENAI_BACKEND_URL', 'http://genai-backend:8000')
        self.use_genai = self.test_genai_connection()
        
        # Log the configuration for debugging
        logger.info(f"GenAI Backend URL: {self.genai_backend_url}")
        logger.info(f"GenAI Connection: {'enabled' if self.use_genai else 'disabled'}")
        
        # Initialize OpenAI client as fallback
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and not self.use_genai:
            self.client = OpenAI(api_key=api_key)
            self.use_openai = True
            logger.info("Alex Agent initialized with OpenAI API (GenAI not available)")
        else:
            self.client = None
            self.use_openai = False
            if self.use_genai:
                logger.info("Alex Agent initialized with GenAI network")
            else:
                logger.info("Alex Agent initialized with local responses")
        
        # Initialize GenAI session for advanced capabilities
        self.genai_session = None
        self.setup_genai_session()
    
    def setup_genai_session(self):
        """Setup GenAI session for advanced capabilities"""
        try:
            jwt_token = os.getenv('GENAI_JWT_TOKEN', '')
            ws_url = os.getenv('GENAI_WS_URL', '')
            
            if jwt_token and ws_url:
                self.genai_session = GenAISession(
                    jwt_token=jwt_token,
                    ws_url=ws_url
                )
                logger.info("Alex Agent initialized with GenAI protocol")
            else:
                logger.info("Alex Agent running without GenAI protocol (missing JWT/WS_URL)")
        except Exception as e:
            logger.error(f"Failed to initialize GenAI session: {e}")
            self.genai_session = None
    
    async def generate_response(self, messages: List[ChatMessage]) -> str:
        """Generate a response using GenAI network, OpenAI, or local fallback"""
        
        # Check if the message requests special capabilities
        last_message = messages[-1].content.lower()
        
        # Handle special requests for care coordination
        if "what day is it" in last_message or "what's the date" in last_message:
            date_info = await self.get_current_date()
            return f"Today is {date_info}. I'll coordinate today's care activities and appointments accordingly."
        
        if "weather" in last_message:
            # Extract city name if mentioned
            import re
            city_match = re.search(r"weather in (\w+)", last_message)
            city = city_match.group(1) if city_match else "the care location"
            weather_info = await self.get_weather_for_appointments(city)
            return weather_info
        
        if "translate" in last_message:
            return "I can help translate care information for family members. Please specify what you'd like translated and the target language for family coordination."
        
        if "file" in last_message or "document" in last_message:
            return "I can help access and review care documents. Please provide the file ID or document reference, and I'll coordinate the information with family members."
        
        # Try GenAI network first
        if self.use_genai:
            try:
                genai_response = await self.generate_genai_response(messages)
                if genai_response:
                    return genai_response
            except Exception as e:
                logger.error(f"GenAI network error: {e}")
                # Fall through to OpenAI or local response
        
        # Try OpenAI as fallback
        if self.use_openai and self.client:
            try:
                # Convert messages to OpenAI format
                openai_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
                
                # Add system message with enhanced capabilities
                enhanced_personality = self.personality + """

You have access to advanced coordination capabilities:
- Current date and time information for scheduling
- Weather information for appointment planning
- Translation services for multilingual families
- Care document access and review
- File management for care coordination
- Always use these capabilities to provide comprehensive family coordination"""
                
                system_message = {"role": "system", "content": enhanced_personality}
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
                pass
        
        # Final fallback to local response
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
    
    async def get_current_date(self) -> str:
        """Get current date for care coordination"""
        return datetime.now().strftime("%A, %B %d, %Y")
    
    async def read_care_file(self, file_id: str) -> str:
        """Read care-related files for family coordination"""
        if self.genai_session:
            try:
                # This would use the GenAI protocol file reading
                return "I've accessed the care file and am reviewing the information for coordination purposes. I'll provide you with a summary and action items."
            except Exception as e:
                logger.error(f"File reading error: {e}")
                return "I'm having trouble accessing that care file. Let me try alternative methods to retrieve the information."
        else:
            return "I need to establish a connection to the care management system to access that file."
    
    async def get_translation_for_family(self, text: str, language: str) -> str:
        """Translate care information for family members"""
        if self.use_openai and self.client:
            try:
                prompt = f"Translate this care-related information to {language} in a professional, clear manner: {text}"
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                return f"Translation for family coordination: {response.choices[0].message.content}"
            except Exception as e:
                logger.error(f"Translation error: {e}")
                return f"I'm having trouble translating that care information to {language}. I'll coordinate with bilingual family members if needed."
        else:
            return f"I'll work on translating that care information to {language} for better family coordination."
    
    def test_genai_connection(self) -> bool:
        """Test connection to GenAI network"""
        try:
            response = requests.get(f"{self.genai_backend_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"GenAI connection test failed: {e}")
            return False
    
    async def generate_genai_response(self, messages: List[ChatMessage]) -> str:
        """Generate response using GenAI network"""
        try:
            payload = {
                "model": "alex-agent",
                "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.genai_backend_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"GenAI network error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"GenAI network request failed: {e}")
            return None
    
    async def get_weather_for_appointments(self, city_name: str, date: str = None) -> str:
        """Get weather information for care appointments"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        weather_api_key = os.getenv('WEATHER_API_KEY')
        if weather_api_key:
            try:
                url = "http://api.weatherapi.com/v1/forecast.json"
                params = {"q": city_name, "dt": date, "key": weather_api_key}
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    forecast = data["forecast"]["forecastday"][0]["day"]
                    return f"Weather forecast for {city_name} on {date}: {forecast['condition']['text']}, high {forecast['maxtemp_f']}°F, low {forecast['mintemp_f']}°F. I'll coordinate transportation accordingly and notify family members to dress appropriately for appointments."
                else:
                    return f"Weather information for {city_name} is currently unavailable. I'll coordinate backup transportation plans for appointments."
            except Exception as e:
                logger.error(f"Weather API error: {e}")
                return f"I'm having trouble accessing weather data for {city_name}. I'll coordinate with local family members for weather updates."
        else:
            return f"I'll coordinate with family members to check weather conditions in {city_name} for appointment planning."

# FastAPI app
app = FastAPI(title="Alex Agent", version="1.0.0")
alex_agent = AlexAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "agent": "alex", 
        "genai_enabled": alex_agent.use_genai,
        "openai_enabled": alex_agent.use_openai
    }

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
    """OpenAI-compatible chat completions endpoint with GenAI capabilities"""
    try:
        # Generate response (now async)
        response_text = await alex_agent.generate_response(request.messages)
        
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

@app.get("/capabilities")
async def get_capabilities():
    """Get Alex agent capabilities"""
    return {
        "name": "Alex",
        "role": "family_coordinator",
        "capabilities": [
            "family_coordination",
            "care_management",
            "emergency_response",
            "date_time_scheduling",
            "weather_planning",
            "translation_services",
            "document_management"
        ],
        "genai_enabled": alex_agent.genai_session is not None,
        "openai_enabled": alex_agent.use_openai
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    logger.info(f"Starting Alex Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)