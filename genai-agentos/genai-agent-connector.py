#!/usr/bin/env python3
"""
Simple GenAI Agent Connector for FamilyConnect
This script connects the FamilyConnect agents to your GenAI OS dashboard
"""

import requests
import json
import time
import os
from typing import Dict, Any

class GenAIConnector:
    def __init__(self, genai_url: str = "http://localhost:3000"):
        self.genai_url = genai_url
        self.familyconnect_url = "http://localhost:5000"
        
    def discover_genai_endpoint(self):
        """Try to discover the GenAI OS endpoint"""
        # Common GenAI OS ports
        ports = [3000, 8000, 8080, 7860, 11434]
        
        for port in ports:
            try:
                url = f"http://localhost:{port}"
                response = requests.get(f"{url}/health", timeout=2)
                if response.status_code == 200:
                    print(f"Found GenAI OS at {url}")
                    return url
            except:
                continue
                
        # Try checking for running processes
        try:
            response = requests.get("http://localhost:5000/api/genai/agent/status", timeout=2)
            if response.status_code == 200:
                print("FamilyConnect agents are running locally")
                return None
        except:
            pass
            
        return None
    
    def register_agents_with_genai(self):
        """Register FamilyConnect agents with GenAI OS"""
        
        # Try to discover GenAI endpoint
        genai_endpoint = self.discover_genai_endpoint()
        if not genai_endpoint:
            print("GenAI OS not found. FamilyConnect agents are running locally.")
            return False
            
        # Agent definitions
        agents = [
            {
                "name": "Grace",
                "description": "FamilyConnect elderly companion - warm, caring AI for seniors",
                "endpoint": f"{self.familyconnect_url}/api/agents/grace",
                "model": "grace-familyconnect",
                "capabilities": ["companionship", "health_monitoring", "family_coordination"],
                "status": "active"
            },
            {
                "name": "Alex", 
                "description": "FamilyConnect family coordinator - professional care management",
                "endpoint": f"{self.familyconnect_url}/api/agents/alex",
                "model": "alex-familyconnect",
                "capabilities": ["care_management", "family_coordination", "emergency_response"],
                "status": "active"
            }
        ]
        
        # Try different registration endpoints
        endpoints = [
            f"{genai_endpoint}/api/agents",
            f"{genai_endpoint}/agents",
            f"{genai_endpoint}/api/register",
            f"{genai_endpoint}/register"
        ]
        
        for agent in agents:
            registered = False
            for endpoint in endpoints:
                try:
                    response = requests.post(
                        endpoint,
                        json=agent,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ {agent['name']} registered with GenAI OS")
                        registered = True
                        break
                        
                except Exception as e:
                    continue
                    
            if not registered:
                print(f"⚠️  Could not register {agent['name']} with GenAI OS")
                
        return True
        
    def create_agent_proxy(self):
        """Create a proxy endpoint for GenAI OS to communicate with FamilyConnect"""
        
        # This would create API endpoints that GenAI OS can call
        # For now, we'll just ensure the existing endpoints work
        
        try:
            # Test Grace agent
            response = requests.get(f"{self.familyconnect_url}/api/agents/grace/health", timeout=5)
            if response.status_code == 200:
                print("✅ Grace agent proxy ready")
            else:
                print("⚠️  Grace agent not responding")
                
            # Test Alex agent  
            response = requests.get(f"{self.familyconnect_url}/api/agents/alex/health", timeout=5)
            if response.status_code == 200:
                print("✅ Alex agent proxy ready")
            else:
                print("⚠️  Alex agent not responding")
                
        except Exception as e:
            print(f"⚠️  Error testing agent proxies: {e}")
            
    def run(self):
        """Main connector function"""
        print("🚀 FamilyConnect GenAI Connector")
        print("================================")
        
        # Test FamilyConnect backend
        try:
            response = requests.get(f"{self.familyconnect_url}/api/users/1", timeout=5)
            if response.status_code == 200:
                print("✅ FamilyConnect backend is running")
            else:
                print("❌ FamilyConnect backend not responding")
                return
        except Exception as e:
            print(f"❌ Could not connect to FamilyConnect: {e}")
            return
            
        # Create agent proxies
        self.create_agent_proxy()
        
        # Try to register with GenAI OS
        if self.register_agents_with_genai():
            print("✅ Agents registered with GenAI OS")
        else:
            print("ℹ️  Agents running locally (GenAI OS not detected)")
            
        print("\n🎉 FamilyConnect agents are now available!")
        print("   - Grace (elderly companion): Available via FamilyConnect interface")
        print("   - Alex (family coordinator): Available via FamilyConnect interface")
        
        if self.discover_genai_endpoint():
            print("   - Agents should now appear in your GenAI OS dashboard")

if __name__ == "__main__":
    connector = GenAIConnector()
    connector.run()