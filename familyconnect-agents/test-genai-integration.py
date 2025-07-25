#!/usr/bin/env python3
"""
Test GenAI network integration for FamilyConnect agents
"""

import os
import json
import requests
import time
from typing import Dict, Any

def test_genai_backend():
    """Test GenAI backend connection"""
    genai_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{genai_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ GenAI backend is accessible")
            return True
        else:
            print(f"❌ GenAI backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GenAI backend connection failed: {e}")
        return False

def test_agent_connection(agent_name: str, port: int):
    """Test individual agent connection"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {agent_name} agent is healthy")
            print(f"   GenAI enabled: {data.get('genai_enabled', False)}")
            print(f"   OpenAI enabled: {data.get('openai_enabled', False)}")
            return True
        else:
            print(f"❌ {agent_name} agent returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {agent_name} agent connection failed: {e}")
        return False

def test_agent_chat(agent_name: str, port: int):
    """Test agent chat functionality"""
    try:
        payload = {
            "model": f"{agent_name.lower()}-agent",
            "messages": [
                {"role": "user", "content": "Hello! Can you introduce yourself?"}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        response = requests.post(
            f"http://localhost:{port}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data["choices"][0]["message"]["content"]
            print(f"✅ {agent_name} chat test successful")
            print(f"   Response: {message[:100]}...")
            return True
        else:
            print(f"❌ {agent_name} chat test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {agent_name} chat test error: {e}")
        return False

def test_genai_network_connectivity():
    """Test if agents can connect to GenAI network"""
    # Test Grace agent GenAI connectivity
    try:
        grace_payload = {
            "model": "grace-agent",
            "messages": [{"role": "user", "content": "Test GenAI network connection"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        # Try to connect to GenAI backend through Grace agent
        response = requests.post(
            "http://localhost:8001/v1/chat/completions",
            json=grace_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Grace agent GenAI network connection test passed")
        else:
            print(f"⚠️ Grace agent GenAI network connection test failed: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Grace agent GenAI network test error: {e}")
    
    # Test Alex agent GenAI connectivity
    try:
        alex_payload = {
            "model": "alex-agent",
            "messages": [{"role": "user", "content": "Test GenAI network connection"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = requests.post(
            "http://localhost:8002/v1/chat/completions",
            json=alex_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Alex agent GenAI network connection test passed")
        else:
            print(f"⚠️ Alex agent GenAI network connection test failed: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Alex agent GenAI network test error: {e}")

def main():
    """Main test function"""
    print("🔍 Testing FamilyConnect GenAI Network Integration...")
    print("=" * 60)
    
    # Test GenAI backend
    print("\n1. Testing GenAI Backend Connection:")
    genai_ok = test_genai_backend()
    
    # Test individual agents
    print("\n2. Testing Agent Health:")
    grace_ok = test_agent_connection("Grace", 8001)
    alex_ok = test_agent_connection("Alex", 8002)
    
    # Test agent chat functionality
    print("\n3. Testing Agent Chat Functionality:")
    grace_chat_ok = test_agent_chat("Grace", 8001)
    alex_chat_ok = test_agent_chat("Alex", 8002)
    
    # Test GenAI network connectivity
    print("\n4. Testing GenAI Network Connectivity:")
    test_genai_network_connectivity()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"GenAI Backend:     {'✅ PASS' if genai_ok else '❌ FAIL'}")
    print(f"Grace Agent:       {'✅ PASS' if grace_ok else '❌ FAIL'}")
    print(f"Alex Agent:        {'✅ PASS' if alex_ok else '❌ FAIL'}")
    print(f"Grace Chat:        {'✅ PASS' if grace_chat_ok else '❌ FAIL'}")
    print(f"Alex Chat:         {'✅ PASS' if alex_chat_ok else '❌ FAIL'}")
    
    if all([genai_ok, grace_ok, alex_ok, grace_chat_ok, alex_chat_ok]):
        print("\n🎉 All tests passed! FamilyConnect agents are properly integrated with GenAI network.")
    else:
        print("\n⚠️ Some tests failed. Check the logs for details.")
        print("Common issues:")
        print("- GenAI OS not running (start with docker-compose up)")
        print("- Agents not connecting to GenAI network (check GENAI_BACKEND_URL)")
        print("- Network connectivity issues (check Docker networking)")

if __name__ == "__main__":
    main()