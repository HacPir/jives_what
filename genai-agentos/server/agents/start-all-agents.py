#!/usr/bin/env python3
"""
Start all FamilyConnect agents for full AI integration
"""

import subprocess
import sys
import os
import time
import signal
import requests
from pathlib import Path

class AgentManager:
    def __init__(self):
        self.processes = {}
        self.agents = [
            {'name': 'grace', 'script': 'grace_agent.py', 'port': 8001},
            {'name': 'alex', 'script': 'alex_agent.py', 'port': 8002},
            {'name': 'manager', 'script': 'agent_manager.py', 'port': 8000}
        ]
        
    def start_agent(self, agent):
        """Start a single agent"""
        print(f"🚀 Starting {agent['name']} agent on port {agent['port']}...")
        
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
        env['AGENT_NAME'] = agent['name']
        env['PORT'] = str(agent['port'])
        
        try:
            process = subprocess.Popen(
                [sys.executable, agent['script']],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path(__file__).parent
            )
            
            self.processes[agent['name']] = process
            
            # Save PID for cleanup
            with open(f"{agent['name']}_agent.pid", 'w') as f:
                f.write(str(process.pid))
            
            print(f"✅ {agent['name']} agent started (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start {agent['name']} agent: {e}")
            return False
    
    def check_agent_health(self, agent):
        """Check if agent is responding"""
        try:
            response = requests.get(f"http://localhost:{agent['port']}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_all_agents(self):
        """Start all agents"""
        print("🚀 Starting FamilyConnect Agent System")
        print("=" * 50)
        
        # Start individual agents first
        for agent in self.agents[:-1]:  # Skip manager for now
            if self.start_agent(agent):
                time.sleep(2)  # Brief pause between starts
        
        # Wait for agents to be ready
        print("⏳ Waiting for agents to initialize...")
        time.sleep(5)
        
        # Start manager last
        manager_agent = self.agents[-1]
        self.start_agent(manager_agent)
        
        # Wait for manager to initialize
        time.sleep(3)
        
        # Health check
        print("\n🏥 Checking agent health...")
        all_healthy = True
        
        for agent in self.agents:
            if self.check_agent_health(agent):
                print(f"✅ {agent['name']} agent healthy on port {agent['port']}")
            else:
                print(f"❌ {agent['name']} agent not responding on port {agent['port']}")
                all_healthy = False
        
        if all_healthy:
            print("\n🎉 All agents are running and healthy!")
            self.print_integration_info()
        else:
            print("\n⚠️  Some agents are not responding. Check logs for details.")
        
        return all_healthy
    
    def print_integration_info(self):
        """Print integration information"""
        print("\n🔗 Agent Integration Information:")
        print("   Grace Agent: http://localhost:8001")
        print("   Alex Agent: http://localhost:8002")
        print("   Agent Manager: http://localhost:8000")
        print("\n💡 Test Commands:")
        print("   # Test Grace Agent")
        print("   curl -X POST http://localhost:8001/v1/chat/completions \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"model\":\"grace-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello Grace!\"}]}'")
        print("\n   # Test Alex Agent")
        print("   curl -X POST http://localhost:8002/v1/chat/completions \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"model\":\"alex-agent\",\"messages\":[{\"role\":\"user\",\"content\":\"Show family status\"}]}'")
        print("\n🎯 Your GenAI dashboard can now communicate with these agents!")
        print("   The agents are running as independent processes with OpenAI compatibility")
        print("   They will auto-integrate with your FamilyConnect application")
    
    def stop_all_agents(self):
        """Stop all running agents"""
        print("🛑 Stopping all agents...")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name} agent")
            except:
                try:
                    process.kill()
                    print(f"🔪 Force killed {name} agent")
                except:
                    pass
        
        # Clean up PID files
        for agent in self.agents:
            pid_file = f"{agent['name']}_agent.pid"
            if os.path.exists(pid_file):
                os.remove(pid_file)
        
        print("✅ All agents stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n⚠️  Received shutdown signal")
        self.stop_all_agents()
        sys.exit(0)

def main():
    manager = AgentManager()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Start all agents
    success = manager.start_all_agents()
    
    if success:
        print("\n⏳ Agents running... Press Ctrl+C to stop")
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        print("\n❌ Failed to start all agents")
        sys.exit(1)

if __name__ == "__main__":
    main()