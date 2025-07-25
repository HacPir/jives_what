"""
Base agent functionality shared between Grace and Alex agents
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from genai_protocol.schemas import ChatRequest, ChatMessage, ChatResponse, ChatChoice
from genai_protocol.handlers import BaseHandler
import openai

class BaseAgent(BaseHandler, ABC):
    """Base class for all FamilyConnect agents"""
    
    def __init__(self, agent_name: str, agent_role: str):
        super().__init__()
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.openai_client = None
        
        # Initialize OpenAI client if API key is available
        if os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.conversation_history: List[Dict[str, Any]] = []
        self.memory: Dict[str, Any] = {
            "short_term": [],
            "long_term": [],
            "context": {}
        }
    
    def add_to_memory(self, user_message: str, agent_response: str, context: Dict[str, Any]):
        """Add interaction to agent memory"""
        memory_entry = {
            "timestamp": asyncio.get_event_loop().time(),
            "user_message": user_message,
            "agent_response": agent_response,
            "context": context
        }
        
        self.memory["short_term"].append(memory_entry)
        
        # Keep only last 20 short-term memories
        if len(self.memory["short_term"]) > 20:
            self.memory["short_term"] = self.memory["short_term"][-20:]
    
    def get_memory_context(self) -> str:
        """Get relevant memory context for prompting"""
        recent_memories = self.memory["short_term"][-5:]
        context = f"Recent conversation history for {self.agent_name}:\n"
        
        for memory in recent_memories:
            context += f"User: {memory['user_message']}\n"
            context += f"{self.agent_name}: {memory['agent_response']}\n\n"
        
        return context
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get agent-specific system prompt"""
        pass
    
    @abstractmethod
    def get_fallback_response(self, user_message: str) -> str:
        """Get fallback response when OpenAI is not available"""
        pass
    
    async def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate response using OpenAI or fallback"""
        if self.openai_client:
            try:
                return await self._generate_openai_response(user_message, context)
            except Exception as e:
                print(f"OpenAI error for {self.agent_name}: {e}")
        
        # Fallback to local response
        return self.get_fallback_response(user_message)
    
    async def _generate_openai_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate response using OpenAI"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "system", "content": self.get_memory_context()}
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"Additional context: {json.dumps(context)}"
            })
        
        messages.append({"role": "user", "content": user_message})
        
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
    
    async def handle_chat_request(self, chat_request: ChatRequest) -> ChatResponse:
        """Handle incoming chat requests"""
        try:
            # Extract user message
            user_message = ""
            context = {}
            
            for msg in chat_request.messages:
                if msg.role == "user":
                    user_message = msg.content
                elif msg.role == "system" and "context" in msg.content.lower():
                    try:
                        context = json.loads(msg.content.split(":", 1)[1].strip())
                    except:
                        context = {"raw": msg.content}
            
            if not user_message:
                user_message = f"Hello, {self.agent_name}!"
            
            # Generate response
            response_content = await self.generate_response(user_message, context)
            
            # Add to memory
            self.add_to_memory(user_message, response_content, context)
            
            # Create response
            response_message = ChatMessage(
                role="assistant",
                content=response_content
            )
            
            choice = ChatChoice(
                index=0,
                message=response_message,
                finish_reason="stop"
            )
            
            return ChatResponse(
                id=f"{self.agent_name}-{int(asyncio.get_event_loop().time())}",
                object="chat.completion",
                created=int(asyncio.get_event_loop().time()),
                model=f"{self.agent_name}-agent",
                choices=[choice],
                usage={
                    "prompt_tokens": len(user_message.split()),
                    "completion_tokens": len(response_content.split()),
                    "total_tokens": len(user_message.split()) + len(response_content.split())
                }
            )
            
        except Exception as e:
            print(f"Error in {self.agent_name} chat request: {e}")
            
            # Fallback response
            fallback_content = self.get_fallback_response(user_message or "Hello")
            
            fallback_message = ChatMessage(
                role="assistant",
                content=fallback_content
            )
            
            choice = ChatChoice(
                index=0,
                message=fallback_message,
                finish_reason="stop"
            )
            
            return ChatResponse(
                id=f"{self.agent_name}-error-{int(asyncio.get_event_loop().time())}",
                object="chat.completion",
                created=int(asyncio.get_event_loop().time()),
                model=f"{self.agent_name}-agent",
                choices=[choice]
            )