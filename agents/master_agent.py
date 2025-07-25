import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
from .base_agent import Agent
import openai

class MasterAgent(Agent):
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Master Agent",
            system_prompt="""You are a Master Agent that coordinates between specialized AI agents to help reconnect families. 
            Your role is to:
            1. Receive alerts from the Memory Agent about important dates
            2. Coordinate with the Elderly Agent to remind users about birthdays
            3. Manage the flow of information between agents
            4. Ensure smooth communication between family members
            
            Always be helpful, empathetic, and focused on fostering family connections."""
        )
        self.openai_client = openai.OpenAI(api_key="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")
        self.agents = {}
        self.conversation_log = []
        
    def register_agent(self, agent_name: str, agent_instance):
        """Register other agents with the master agent"""
        self.agents[agent_name] = agent_instance
        print(f"Master Agent: Registered {agent_name}")
        
    async def handle_birthday_alert(self, birthday_info: Dict[str, Any]):
        """Handle birthday alerts from Memory Agent using LLM reasoning"""
        print(f"Master Agent: Received birthday alert for {birthday_info['name']}")
        
        # Use LLM to generate appropriate response
        prompt = f"""
        A birthday alert has been received for {birthday_info['name']} ({birthday_info['relationship']}).
        
        Your task is to:
        1. Determine the best way to remind the elderly user
        2. Generate a warm, personalized message
        3. Suggest appropriate actions
        
        Birthday Info: {json.dumps(birthday_info, indent=2)}
        
        Generate a response that includes:
        - A warm birthday reminder message
        - Suggested actions (call, message, etc.)
        - Any additional context that might be helpful
        """
        
        response = await self.llm_call(prompt)
        print(f"Master Agent LLM Response: {response}")
        
        # Log the interaction
        self.conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "birthday_alert",
            "data": birthday_info,
            "llm_response": response
        })
        
        # Instruct Elderly Agent to remind the user
        if "elderly_agent" in self.agents:
            await self.agents["elderly_agent"].remind_birthday(birthday_info, response)
        else:
            print("Master Agent: Elderly Agent not registered")
            
    async def handle_elderly_response(self, response: str, context: Dict[str, Any]):
        """Handle responses from the elderly user using LLM analysis"""
        print(f"Master Agent: Elderly user response: {response}")
        
        # Use LLM to analyze the response and determine next steps
        prompt = f"""
        The elderly user has responded: "{response}"
        
        Context: {json.dumps(context, indent=2)}
        
        Analyze this response and determine:
        1. What action the user wants to take
        2. How to best support them
        3. What information to share with the younger relative
        4. Any follow-up actions needed
        """
        
        analysis = await self.llm_call(prompt)
        print(f"Master Agent Analysis: {analysis}")
        
        # Log the interaction
        self.conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "elderly_response",
            "response": response,
            "context": context,
            "analysis": analysis
        })
        
        # Notify Younger Relative Agent if needed
        if "younger_relative_agent" in self.agents:
            await self.agents["younger_relative_agent"].notify_interaction(response, context, analysis)
            
    async def llm_call(self, prompt: str) -> str:
        """Make a call to OpenAI GPT-4o"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content or "I'm having trouble processing that right now."
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return "I'm having trouble processing that right now."
            
    def get_conversation_log(self) -> List[Dict]:
        """Get the conversation log for demo purposes"""
        return self.conversation_log 