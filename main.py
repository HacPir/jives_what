import asyncio
import os
import json
from datetime import datetime, date
from agents.master_agent import MasterAgent
from agents.memory_agent import MemoryAgent
from agents.elderly_agent import ElderlyAgent
from agents.younger_relative_agent import YoungerRelativeAgent

class FamilyConnectionOrchestrator:
    def __init__(self, openai_api_key: str):
<<<<<<< HEAD
        self.openai_api_key = "TOKEN_API_OPENAI"
=======
        self.openai_api_key = "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"
>>>>>>> 105f2ca28f2c8d5cc20dc1224055068bb84f1d54
        self.agents = {}
        self.setup_agents()
        
    def setup_agents(self):
        """Initialize all agents with AGNO and register them"""
        print("Setting up Family Connection Agents...")
        
        # Create agents
        self.agents["master"] = MasterAgent(self.openai_api_key)
        self.agents["memory"] = MemoryAgent(self.openai_api_key)
        self.agents["elderly"] = ElderlyAgent(self.openai_api_key)
        self.agents["younger_relative"] = YoungerRelativeAgent(self.openai_api_key)
        
        # Register agents with master
        self.agents["master"].register_agent("memory_agent", self.agents["memory"])
        self.agents["master"].register_agent("elderly_agent", self.agents["elderly"])
        self.agents["master"].register_agent("younger_relative_agent", self.agents["younger_relative"])
        
        # Register master with other agents
        self.agents["memory"].register_master_agent(self.agents["master"])
        self.agents["elderly"].register_master_agent(self.agents["master"])
        self.agents["younger_relative"].register_master_agent(self.agents["master"])
        
        print("All agents registered and ready!")
        
    async def run_demo(self):
        """Run a demo scenario for the hackathon"""
        print("\n" + "="*60)
        print("FAMILY CONNECTION AI AGENTS DEMO")
        print("="*60)
        
        # Check if there are any birthdays today
        today = date.today()
        print(f"\nChecking for birthdays on {today.strftime('%B %d, %Y')}...")
        
        # Trigger the birthday check
        await self.agents["memory"].check_and_alert()
        
        # Wait a moment for all interactions to complete
        await asyncio.sleep(2)
        
        # Display results
        print("\n" + "="*60)
        print("DEMO RESULTS")
        print("="*60)
        
        # Show conversation log
        master_log = self.agents["master"].get_conversation_log()
        print(f"\nMaster Agent processed {len(master_log)} interactions")
        
        # Show elderly agent responses
        elderly_responses = self.agents["elderly"].get_user_responses()
        print(f"Elderly Agent had {len(elderly_responses)} interactions")
        
        # Show younger relative notifications
        younger_notifications = self.agents["younger_relative"].get_notifications()
        print(f"Younger Relative Agent received {len(younger_notifications)} notifications")
        
        # Display detailed interaction if any occurred
        if elderly_responses:
            print("\nSample Interaction:")
            response = elderly_responses[0]
            print(f"Birthday: {response['birthday_info']['name']}")
            print(f"Reminder: {response['reminder_message']}")
            print(f"User Response: {response['user_response']}")
            
        if younger_notifications:
            print("\nYounger Relative Insights:")
            notification = younger_notifications[0]
            print(f"Insights: {notification['insights']}")
            if 'suggestions' in notification:
                print(f"Suggestions: {notification['suggestions']}")
                
    async def run_continuous_monitoring(self, check_interval: int = 60):
        """Run continuous monitoring for real-time birthday checks"""
        print(f"Starting continuous monitoring (checking every {check_interval} seconds)...")
        await self.agents["memory"].start_monitoring(check_interval)

async def main():
    """Main function to run the family connection system"""
    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        return
        
    # Create orchestrator
    orchestrator = FamilyConnectionOrchestrator(openai_api_key)
    
    # Run demo
    await orchestrator.run_demo()
    
    # Optionally run continuous monitoring
    # await orchestrator.run_continuous_monitoring(check_interval=30)

if __name__ == "__main__":
    asyncio.run(main())