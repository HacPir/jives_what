#!/usr/bin/env python3
"""
Register FamilyConnect agents with GenAI OS
"""

import os
import json
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_agents():
    """Wait for agents to be ready"""
    agents = [
        ("Grace", "http://grace-agent:8001"),
        ("Alex", "http://alex-agent:8002")
    ]
    
    for name, url in agents:
        logger.info(f"Waiting for {name} agent to be ready...")
        for attempt in range(30):  # 30 attempts, 10 seconds each = 5 minutes
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {name} agent is ready")
                    break
            except Exception as e:
                if attempt == 29:
                    logger.error(f"❌ {name} agent failed to start: {e}")
                    return False
                time.sleep(10)
        else:
            logger.error(f"❌ {name} agent not ready after 5 minutes")
            return False
    
    return True

def register_agent(genai_url, agent_name, agent_url, agent_config):
    """Register a single agent with GenAI OS"""
    try:
        # Register via API
        response = requests.post(
            f"{genai_url}/api/agents/register",
            json={
                "name": agent_name,
                "url": agent_url,
                "config": agent_config
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ {agent_name} registered successfully")
            return True
        else:
            logger.error(f"❌ Failed to register {agent_name}: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error registering {agent_name}: {e}")
        return False

def main():
    """Main registration function"""
    genai_url = os.getenv("GENAI_BACKEND_URL", "http://genai-backend:8000")
    
    # Wait for GenAI OS to be ready
    logger.info("Waiting for GenAI OS to be ready...")
    for attempt in range(30):
        try:
            response = requests.get(f"{genai_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ GenAI OS is ready")
                break
        except Exception as e:
            if attempt == 29:
                logger.error(f"❌ GenAI OS not ready: {e}")
                exit(1)
            time.sleep(10)
    
    # Wait for agents to be ready
    if not wait_for_agents():
        logger.error("❌ Agents not ready, exiting")
        exit(1)
    
    # Register Grace agent
    grace_config = {
        "name": "Grace",
        "description": "Warm, patient elderly companion AI agent",
        "capabilities": ["conversation", "memory_assistance", "emotional_support"],
        "personality": "elderly_companion",
        "port": 8001
    }
    
    grace_success = register_agent(
        genai_url,
        "Grace",
        "http://grace-agent:8001",
        grace_config
    )
    
    # Register Alex agent
    alex_config = {
        "name": "Alex",
        "description": "Professional family coordinator AI agent",
        "capabilities": ["family_coordination", "care_management", "scheduling"],
        "personality": "professional_coordinator",
        "port": 8002
    }
    
    alex_success = register_agent(
        genai_url,
        "Alex",
        "http://alex-agent:8002", 
        alex_config
    )
    
    if grace_success and alex_success:
        logger.info("🎉 All FamilyConnect agents registered successfully!")
        logger.info("Visit your GenAI OS dashboard to see the agents")
    else:
        logger.error("❌ Some agents failed to register")
        exit(1)

if __name__ == "__main__":
    main()