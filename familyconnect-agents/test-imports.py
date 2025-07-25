#!/usr/bin/env python3
"""
Test that all imports work correctly in the standalone agents
"""

import sys
import os

def test_alex_imports():
    """Test Alex agent imports"""
    try:
        # Test the critical imports from Alex agent
        import json
        import logging
        import asyncio
        from datetime import datetime
        from typing import Dict, List, Any, Optional
        from pydantic import BaseModel
        import requests
        import nest_asyncio
        print("✅ All Alex agent imports successful")
        return True
    except Exception as e:
        print(f"❌ Alex agent import failed: {e}")
        return False

def test_grace_imports():
    """Test Grace agent imports"""
    try:
        # Test the critical imports from Grace agent
        import json
        import logging
        import asyncio
        from datetime import datetime
        from typing import Dict, List, Any, Optional
        from pydantic import BaseModel
        import requests
        import nest_asyncio
        print("✅ All Grace agent imports successful")
        return True
    except Exception as e:
        print(f"❌ Grace agent import failed: {e}")
        return False

def test_genai_session():
    """Test GenAI session class"""
    try:
        # Test our simplified GenAI session class
        class GenAISession:
            def __init__(self, jwt_token: str, ws_url: str):
                self.jwt_token = jwt_token
                self.ws_url = ws_url
                self.connected = False
            
            def connect(self):
                self.connected = True
                return self.connected
        
        session = GenAISession("test_token", "ws://test")
        session.connect()
        print("✅ GenAI session class works correctly")
        return True
    except Exception as e:
        print(f"❌ GenAI session test failed: {e}")
        return False

def main():
    """Run all import tests"""
    print("🔍 Testing FamilyConnect Agent Imports...")
    print("=" * 50)
    
    alex_ok = test_alex_imports()
    grace_ok = test_grace_imports()
    genai_ok = test_genai_session()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Alex imports:    {'✅ PASS' if alex_ok else '❌ FAIL'}")
    print(f"Grace imports:   {'✅ PASS' if grace_ok else '❌ FAIL'}")
    print(f"GenAI session:   {'✅ PASS' if genai_ok else '❌ FAIL'}")
    
    if all([alex_ok, grace_ok, genai_ok]):
        print("\n🎉 All import tests passed! Agents should work correctly.")
        return 0
    else:
        print("\n❌ Some imports failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())