import json
import asyncio
from datetime import datetime, date
from typing import Dict, List, Any
import os
from .base_agent import Agent
import openai

class MemoryAgent(Agent):
    def __init__(self, openai_api_key: str, data_file_path: str = "data/birthdays.json"):
        super().__init__(
            name="Memory Agent",
            system_prompt="""You are a Memory Agent specialized in monitoring and analyzing important dates and events. 
            Your role is to:
            1. Monitor data files for important dates (birthdays, anniversaries, appointments)
            2. Analyze the significance of dates and relationships
            3. Provide intelligent alerts with context and suggestions
            4. Help maintain family connections through timely reminders
            
            Always be thorough, accurate, and considerate of family relationships."""
        )
        self.openai_client = openai.OpenAI(api_key="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")
        self.data_file_path = data_file_path
        self.master_agent = None
        
    def register_master_agent(self, master_agent):
        """Register the master agent for communication"""
        self.master_agent = master_agent
        print(f"Memory Agent: Registered with Master Agent")
        
    def load_birthday_data(self) -> Dict[str, Any]:
        """Load birthday data from JSON file"""
        try:
            with open(self.data_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Memory Agent: Birthday file not found at {self.data_file_path}")
            return {"birthdays": [], "events": []}
        except json.JSONDecodeError:
            print(f"Memory Agent: Invalid JSON in birthday file")
            return {"birthdays": [], "events": []}
            
    async def analyze_todays_birthdays(self) -> List[Dict[str, Any]]:
        """Use LLM to analyze today's birthdays and provide context"""
        today = date.today()
        birthday_data = self.load_birthday_data()
        todays_birthdays = []
        
        # Find birthdays for today
        for birthday in birthday_data.get("birthdays", []):
            try:
                birthday_date = datetime.strptime(birthday["date"], "%Y-%m-%d").date()
                if birthday_date.month == today.month and birthday_date.day == today.day:
                    todays_birthdays.append(birthday)
            except ValueError:
                print(f"Memory Agent: Invalid date format for {birthday.get('name', 'Unknown')}")
        
        if todays_birthdays:
            # Use LLM to analyze and enhance the birthday information
            prompt = f"""
            Analyze these birthdays for today ({today.strftime('%B %d')}):
            {json.dumps(todays_birthdays, indent=2)}
            
            For each birthday, provide:
            1. The significance of the relationship
            2. Suggested ways to celebrate or connect
            3. Any special considerations (age, distance, etc.)
            4. Emotional context for the family
            
            Format your response as enhanced birthday information with additional context.
            """
            
            analysis = await self.llm_call(prompt)
            print(f"Memory Agent Analysis: {analysis}")
            
            # Enhance the birthday data with LLM analysis
            for birthday in todays_birthdays:
                birthday["llm_analysis"] = analysis
                birthday["analysis_date"] = today.isoformat()
                
        return todays_birthdays
        
    async def check_and_alert(self):
        """Check for birthdays and alert master agent with LLM-enhanced information"""
        todays_birthdays = await self.analyze_todays_birthdays()
        
        if todays_birthdays:
            print(f"Memory Agent: Found {len(todays_birthdays)} birthday(s) today!")
            
            for birthday in todays_birthdays:
                print(f"Memory Agent: Alerting Master Agent about {birthday['name']}'s birthday")
                
                if self.master_agent:
                    await self.master_agent.handle_birthday_alert(birthday)
                else:
                    print("Memory Agent: Master Agent not registered")
        else:
            print("Memory Agent: No birthdays today")
            
    async def start_monitoring(self, check_interval: int = 60):
        """Start monitoring birthdays at regular intervals"""
        print(f"Memory Agent: Starting birthday monitoring (checking every {check_interval} seconds)")
        
        while True:
            await self.check_and_alert()
            await asyncio.sleep(check_interval)
            
    async def llm_call(self, prompt: str) -> str:
        """Make a call to OpenAI GPT-4o"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.6
            )
            return response.choices[0].message.content or "No analysis available."
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return "I'm having trouble analyzing that right now." 