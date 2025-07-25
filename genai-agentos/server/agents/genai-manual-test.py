#!/usr/bin/env python3
"""
Manual test for GenAI AgentOS integration
"""

import json

def create_agent_configs():
    """Create agent configurations for manual deployment"""
    
    grace_config = {
        "name": "Grace",
        "description": "Warm, patient elderly companion AI agent designed for senior users",
        "type": "elderly_companion",
        "personality": {
            "traits": ["warm", "patient", "caring", "gentle", "empathetic"],
            "voice": "grandmother-like",
            "communication_style": "slow and clear"
        },
        "capabilities": [
            "emotional_support",
            "health_monitoring", 
            "family_coordination",
            "memory_assistance",
            "companionship"
        ],
        "system_prompt": "You are Grace, a warm, patient, and caring AI companion designed specifically for elderly users. Speak slowly and clearly with a gentle, grandmother-like tone. Always be patient and understanding, never rush conversations. Show genuine care and empathy for their feelings and concerns.",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    }
    
    alex_config = {
        "name": "Alex",
        "description": "Professional family coordinator AI agent for caregivers and family management",
        "type": "family_coordinator",
        "personality": {
            "traits": ["professional", "organized", "proactive", "efficient"],
            "voice": "professional",
            "communication_style": "clear and action-oriented"
        },
        "capabilities": [
            "family_coordination",
            "care_management",
            "appointment_scheduling",
            "health_monitoring",
            "emergency_response"
        ],
        "system_prompt": "You are Alex, a professional and efficient family coordinator AI agent designed to help caregivers and family members manage elderly care. Coordinate care activities, monitor health status, and facilitate family communication.",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    }
    
    return grace_config, alex_config

def main():
    print("🤖 GenAI AgentOS Manual Configuration")
    print("=" * 50)
    
    grace_config, alex_config = create_agent_configs()
    
    print("\n📋 Grace Agent Configuration:")
    print(json.dumps(grace_config, indent=2))
    
    print("\n📋 Alex Agent Configuration:")
    print(json.dumps(alex_config, indent=2))
    
    print("\n💡 Manual Deployment Instructions:")
    print("   1. Copy the JSON configurations above")
    print("   2. In your GenAI AgentOS dashboard, click 'Generate token' or 'New Agent'")
    print("   3. Paste each configuration as a new agent")
    print("   4. The agents will be available for testing through FamilyConnect")
    
    print("\n🚀 Testing the Integration:")
    print("   1. Start your FamilyConnect application")
    print("   2. Go to Alex Dashboard > GenAI Protocol Agent Dashboard")
    print("   3. Click 'Deploy to GenAI' button")
    print("   4. Test agent communication through the interface")
    
    # Save configs to files for easy copying
    with open('grace_config.json', 'w') as f:
        json.dump(grace_config, f, indent=2)
    
    with open('alex_config.json', 'w') as f:
        json.dump(alex_config, f, indent=2)
    
    print("\n📁 Configuration files saved:")
    print("   - grace_config.json")
    print("   - alex_config.json")

if __name__ == "__main__":
    main()