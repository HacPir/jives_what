#!/usr/bin/env python3
"""
Standalone Grace Agent - Full AI Integration
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

# Grace Agent Implementation with GenAI Protocol Integration
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
            logger.info("Grace Agent initialized with OpenAI API (GenAI not available)")
        else:
            self.client = None
            self.use_openai = False
            if self.use_genai:
                logger.info("Grace Agent initialized with GenAI network")
            else:
                logger.info("Grace Agent initialized with local responses")
        
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
                logger.info("Grace Agent initialized with GenAI protocol")
            else:
                logger.info("Grace Agent running without GenAI protocol (missing JWT/WS_URL)")
        except Exception as e:
            logger.error(f"Failed to initialize GenAI session: {e}")
            self.genai_session = None
    
    async def generate_response(self, messages: List[ChatMessage]) -> str:
        """Generate a response using GenAI network, OpenAI, or local fallback"""
        
        # Check if the message requests special capabilities
        last_message = messages[-1].content.lower()
        
        # Handle special requests
        if "what day is it" in last_message or "what's the date" in last_message:
            date_info = await self.get_current_date()
            return f"Today is {date_info}, dear. I hope you're having a wonderful day!"
        
        if "weather" in last_message:
            # Extract city name if mentioned
            import re
            city_match = re.search(r"weather in (\w+)", last_message)
            city = city_match.group(1) if city_match else "your area"
            weather_info = await self.get_weather(city)
            return weather_info
        
        if "translate" in last_message:
            # Simple translation request handling
            return "I'd be happy to help you translate something, dear. What would you like me to translate and into which language?"
        
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

You also have access to helpful capabilities:
- You can check the current date and time
- You can help with weather information
- You can assist with translation
- You can read text files when needed
- Always offer these services in a gentle, caring way appropriate for elderly users"""
                
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
                "model": "grace-agent",
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
    
    async def get_current_date(self) -> str:
        """Get current date for elderly users"""
        return datetime.now().strftime("%A, %B %d, %Y")
    
    async def read_text_file(self, file_id: str) -> str:
        """Read text file for elderly users (simplified)"""
        if self.genai_session:
            try:
                # This would use the GenAI protocol file reading
                return f"I can help you read files, dear. Let me get that information for you."
            except Exception as e:
                logger.error(f"File reading error: {e}")
                return "I'm having trouble reading that file right now. Let me try another way to help you."
        else:
            return "I'd be happy to help you read files, but I need to connect to the file system first."
    
    async def get_translation(self, text: str, language: str) -> str:
        """Translate text for elderly users"""
        if self.use_openai and self.client:
            try:
                prompt = f"Translate this text to {language} in a gentle, caring way: {text}"
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=200
                )
                return f"Here's the translation for you, dear: {response.choices[0].message.content}"
            except Exception as e:
                logger.error(f"Translation error: {e}")
                return f"I'm having trouble translating that right now, but I understand you want it in {language}. Let me try to help you another way."
        else:
            return f"I'd love to help you translate that to {language}, dear. Let me see what I can do for you."
    
    async def get_weather(self, city_name: str, date: str = None) -> str:
        """Get weather information for elderly users"""
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
                    return f"The weather in {city_name} looks like it will be {forecast['condition']['text']} with a high of {forecast['maxtemp_f']}°F and a low of {forecast['mintemp_f']}°F. Please dress warmly if you're going out, dear!"
                else:
                    return f"I'm having trouble getting the weather for {city_name} right now. Maybe check your local weather app or ask a family member?"
            except Exception as e:
                logger.error(f"Weather API error: {e}")
                return f"I'd love to help you with the weather in {city_name}, but I'm having trouble connecting right now. Please dress appropriately for the season!"
        else:
            return f"I wish I could check the weather in {city_name} for you, dear. You might want to look outside or ask a family member about today's weather."

# FastAPI app
app = FastAPI(title="Grace Agent", version="1.0.0")
grace_agent = GraceAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "agent": "grace", 
        "genai_enabled": grace_agent.use_genai,
        "openai_enabled": grace_agent.use_openai
    }

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
    """OpenAI-compatible chat completions endpoint with GenAI capabilities"""
    try:
        # Generate response (now async)
        response_text = await grace_agent.generate_response(request.messages)
        
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

@app.get("/capabilities")
async def get_capabilities():
    """Get Grace agent capabilities"""
    return {
        "name": "Grace",
        "role": "elderly_companion",
        "capabilities": [
            "emotional_support",
            "health_monitoring",
            "companionship",
            "date_time_queries",
            "weather_information",
            "text_translation",
            "file_reading"
        ],
        "genai_enabled": grace_agent.genai_session is not None,
        "openai_enabled": grace_agent.use_openai
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    logger.info(f"Starting Grace Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)