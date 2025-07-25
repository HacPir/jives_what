import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import Agent
import openai

class YoungerRelativeAgent(Agent):
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Younger Relative Agent",
            system_prompt="""You are a Younger Relative Agent that helps adult children and younger family members stay connected with their elderly relatives. 
            Your role is to:
            1. Receive notifications about elderly relative interactions
            2. Provide intelligent insights and suggestions
            3. Help coordinate family connections
            4. Suggest meaningful ways to engage with elderly family members
            5. Consider emotional and practical aspects of family relationships
            
            Always be supportive, understanding, and focused on strengthening family bonds."""
        )
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.master_agent = None
        self.notifications = []
        
    def register_master_agent(self, master_agent):
        """Register the master agent for communication"""
        self.master_agent = master_agent
        print(f"Younger Relative Agent: Registered with Master Agent")
        
    async def notify_interaction(self, response: str, context: Dict[str, Any], master_analysis: str):
        """Receive notification about elderly user interaction and provide intelligent insights"""
        print(f"Younger Relative Agent: Received notification about interaction")
        
        # Use LLM to analyze the interaction and provide insights
        prompt = f"""
        Analyze this interaction between an elderly relative and the AI system:
        
        Elderly Response: "{response}"
        Context: {json.dumps(context, indent=2)}
        Master Agent Analysis: {master_analysis}
        
        Provide insights and suggestions for the younger relative:
        1. What does this interaction reveal about the elderly person's needs/desires?
        2. What are the best ways to support this connection?
        3. What follow-up actions would be meaningful?
        4. Any emotional considerations to keep in mind?
        5. Practical suggestions for staying connected
        
        Format your response as helpful insights and actionable suggestions.
        """
        
        insights = await self.llm_call(prompt)
        print(f"Younger Relative Agent Insights: {insights}")
        
        # Log the notification
        notification = {
            "timestamp": datetime.now().isoformat(),
            "elderly_response": response,
            "context": context,
            "master_analysis": master_analysis,
            "insights": insights,
            "action_taken": "analyzed_and_insights_provided"
        }
        self.notifications.append(notification)
        
        # Generate specific suggestions based on the interaction
        await self.generate_suggestions(response, context, insights)
        
    async def generate_suggestions(self, response: str, context: Dict[str, Any], insights: str):
        """Generate specific, actionable suggestions for the younger relative"""
        birthday_info = context.get("birthday_info", {})
        
        prompt = f"""
        Based on this interaction:
        Elderly Response: "{response}"
        Birthday Info: {json.dumps(birthday_info, indent=2)}
        Insights: {insights}
        
        Generate 3-5 specific, actionable suggestions for the younger relative. 
        Make them practical and meaningful. Examples:
        - "Send a video message sharing a childhood memory"
        - "Schedule a weekly video call"
        - "Create a shared photo album"
        
        Format as a numbered list of suggestions.
        """
        
        suggestions = await self.llm_call(prompt)
        print(f"Younger Relative Agent Suggestions: {suggestions}")
        
        # Add suggestions to the notification
        if self.notifications:
            self.notifications[-1]["suggestions"] = suggestions
            
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
            return response.choices[0].message.content or "No insights available."
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return "I'm having trouble analyzing that right now."
            
    def get_notifications(self) -> List[Dict]:
        """Get notification history for demo purposes"""
        return self.notifications 