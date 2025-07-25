import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from .base_agent import Agent
import openai

class ElderlyAgent(Agent):
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Elderly Agent",
            system_prompt="""You are a friendly, empathetic AI assistant designed specifically for elderly users. 
            Your role is to:
            1. Remind users about important dates and events in a warm, caring way
            2. Help them stay connected with family members
            3. Provide gentle suggestions for actions they can take
            4. Use simple, clear language that's easy to understand
            5. Be patient and supportive
            
            Always speak in a warm, conversational tone as if talking to a dear friend."""
        )
        self.openai_client = openai.OpenAI(api_key="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")
        self.master_agent = None
        self.user_responses = []
        
    def register_master_agent(self, master_agent):
        """Register the master agent for communication"""
        self.master_agent = master_agent
        print(f"Elderly Agent: Registered with Master Agent")
        
    async def remind_birthday(self, birthday_info: Dict[str, Any], master_guidance: str):
        """Remind the elderly user about a birthday using LLM-generated personalized message"""
        name = birthday_info.get("name", "someone")
        relationship = birthday_info.get("relationship", "family member")
        
        # Use LLM to generate a personalized birthday reminder
        prompt = f"""
        Generate a warm, personalized birthday reminder for an elderly user.
        
        Birthday Info: {json.dumps(birthday_info, indent=2)}
        Master Agent Guidance: {master_guidance}
        
        Create a message that:
        1. Is warm and personal
        2. Mentions the person's name and relationship
        3. Suggests ways to connect (call, message, etc.)
        4. Uses simple, clear language
        5. Feels like talking to a caring friend
        
        Format your response as a natural conversation starter.
        """
        
        reminder_message = await self.llm_call(prompt)
        print(f"Elderly Agent: {reminder_message}")
        
        # Generate follow-up suggestions
        suggestions_prompt = f"""
        Based on the birthday reminder for {name}, generate 3-4 simple suggestions for the elderly user.
        Make them actionable and easy to understand.
        Examples: "Would you like to call them?", "Should I help you send a message?"
        """
        
        suggestions_response = await self.llm_call(suggestions_prompt)
        print(f"Elderly Agent Suggestions: {suggestions_response}")
        
        # Simulate user response for demo
        await self.simulate_user_response(birthday_info, reminder_message)
        
    async def simulate_user_response(self, birthday_info: Dict[str, Any], reminder_message: str):
        """Simulate user response for demo purposes"""
        # Use LLM to generate a realistic user response
        prompt = f"""
        Generate a realistic response from an elderly user who just received this birthday reminder:
        "{reminder_message}"
        
        The response should be:
        1. Natural and conversational
        2. Show interest in connecting
        3. Maybe ask for help or clarification
        4. Feel authentic to an elderly person
        
        Generate just the user's response, nothing else.
        """
        
        user_response = await self.llm_call(prompt)
        print(f"Elderly Agent: User response: {user_response}")
        
        # Log the interaction
        self.user_responses.append({
            "timestamp": datetime.now().isoformat(),
            "birthday_info": birthday_info,
            "reminder_message": reminder_message,
            "user_response": user_response,
            "action": "birthday_reminder_interaction"
        })
        
        # Send response to master agent
        if self.master_agent:
            await self.master_agent.handle_elderly_response(user_response, {
                "birthday_info": birthday_info,
                "reminder_message": reminder_message,
                "action": "birthday_reminder_interaction"
            })
            
    async def llm_call(self, prompt: str) -> str:
        """Make a call to OpenAI GPT-4o"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content or "I'm here to help!"
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return "I'm having trouble processing that right now."
            
    def get_user_responses(self) -> list:
        """Get user response history for demo purposes"""
        return self.user_responses 