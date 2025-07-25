#!/usr/bin/env python3
"""
Deploy FamilyConnect agents to GenAI AgentOS
"""

import requests
import json
import os
import time
from typing import Dict, Any

class GenAIDeployer:
    def __init__(self, genai_url: str = "http://localhost:3000"):
        self.genai_url = genai_url.rstrip('/')
        self.session = requests.Session()
        
    def deploy_agent(self, agent_config: Dict[str, Any]) -> bool:
        """Deploy an agent to GenAI AgentOS"""
        try:
            # Register agent with GenAI AgentOS
            deploy_url = f"{self.genai_url}/api/agents/deploy"
            
            response = self.session.post(
                deploy_url,
                json=agent_config,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully deployed {agent_config['name']} agent")
                print(f"   Agent ID: {result.get('agent_id', 'N/A')}")
                print(f"   Status: {result.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to deploy {agent_config['name']} agent")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error deploying {agent_config['name']} agent: {e}")
            return False
    
    def get_agent_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get agent configurations for deployment"""
        return {
            "grace": {
                "name": "Grace",
                "description": "Warm, patient elderly companion AI agent designed for senior users",
                "personality": {
                    "role": "elderly_companion",
                    "traits": ["warm", "patient", "caring", "gentle", "empathetic", "understanding"],
                    "voice": {"tone": "grandmother-like", "pace": "slow and clear", "warmth": "very high"}
                },
                "capabilities": [
                    "emotional_support",
                    "health_monitoring", 
                    "family_coordination",
                    "memory_assistance",
                    "companionship",
                    "voice_interaction"
                ],
                "endpoints": {
                    "chat": "/v1/chat/completions",
                    "health": "/health",
                    "info": "/agent/info"
                },
                "port": 8001,
                "system_prompt": """You are Grace, a warm, patient, and caring AI companion designed specifically for elderly users. 

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

When health concerns arise, gently suggest contacting family or medical professionals. Always prioritize their safety and wellbeing while maintaining your warm, caring demeanor.""",
                "model": "grace-agent",
                "temperature": 0.7,
                "max_tokens": 400
            },
            "alex": {
                "name": "Alex",
                "description": "Professional family coordinator AI agent for caregivers and family management",
                "personality": {
                    "role": "family_coordinator",
                    "traits": ["professional", "organized", "proactive", "efficient", "compassionate", "reliable"],
                    "voice": {"tone": "professional", "pace": "normal", "warmth": "moderate"}
                },
                "capabilities": [
                    "family_coordination",
                    "care_management",
                    "appointment_scheduling",
                    "health_monitoring",
                    "emergency_response",
                    "communication_facilitation"
                ],
                "endpoints": {
                    "chat": "/v1/chat/completions",
                    "health": "/health", 
                    "info": "/agent/info"
                },
                "port": 8002,
                "system_prompt": """You are Alex, a professional and efficient family coordinator AI agent designed to help caregivers and family members manage elderly care.

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

When coordinating care, always prioritize safety and wellbeing while keeping family members informed and involved in care decisions.""",
                "model": "alex-agent",
                "temperature": 0.7,
                "max_tokens": 400
            }
        }
    
    def deploy_all_agents(self) -> bool:
        """Deploy all FamilyConnect agents"""
        print("🚀 Deploying FamilyConnect agents to GenAI AgentOS...")
        print(f"   Target: {self.genai_url}")
        
        configs = self.get_agent_configs()
        success_count = 0
        
        for agent_id, config in configs.items():
            print(f"\n📦 Deploying {config['name']} agent...")
            
            if self.deploy_agent(config):
                success_count += 1
                time.sleep(1)  # Brief pause between deployments
        
        print(f"\n🎯 Deployment Summary:")
        print(f"   Total agents: {len(configs)}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {len(configs) - success_count}")
        
        return success_count == len(configs)
    
    def check_genai_status(self) -> bool:
        """Check if GenAI AgentOS is accessible"""
        try:
            response = self.session.get(f"{self.genai_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False

def main():
    # Configuration
    genai_url = os.getenv("GENAI_URL", "http://localhost:3000")
    
    print("🔧 FamilyConnect Agent Deployer")
    print("=" * 50)
    
    deployer = GenAIDeployer(genai_url)
    
    # Check GenAI AgentOS availability
    print(f"🔍 Checking GenAI AgentOS at {genai_url}...")
    if not deployer.check_genai_status():
        print(f"❌ GenAI AgentOS not accessible at {genai_url}")
        print("   Please ensure GenAI AgentOS is running")
        return False
    
    print("✅ GenAI AgentOS is accessible")
    
    # Deploy agents
    success = deployer.deploy_all_agents()
    
    if success:
        print("\n🎉 All agents deployed successfully!")
        print("\n📋 Next steps:")
        print("   1. Check agent status in GenAI AgentOS dashboard")
        print("   2. Test agent communication through FamilyConnect")
        print("   3. Monitor agent performance and health")
    else:
        print("\n⚠️  Some agents failed to deploy")
        print("   Check the logs above for details")
    
    return success

if __name__ == "__main__":
    main()