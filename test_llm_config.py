#!/usr/bin/env python
"""
Test different LLM configurations for Ollama in CrewAI
"""

import os
from crewai import Agent, Task, Crew

def test_llm_configs():
    """Test different LLM configuration approaches"""
    
    print("🧪 Testing LLM configurations...")
    
    # Test 1: Environment variables
    os.environ["OPENAI_API_KEY"] = "ollama"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    
    try:
        agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            verbose=True
        )
        print("✅ Test 1: Environment variables - SUCCESS")
    except Exception as e:
        print(f"❌ Test 1: Environment variables - FAILED: {e}")
    
    # Test 2: Direct LLM specification
    try:
        agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            verbose=True,
            llm="ollama/gpt-oss:20b"
        )
        print("✅ Test 2: Direct LLM specification - SUCCESS")
    except Exception as e:
        print(f"❌ Test 2: Direct LLM specification - FAILED: {e}")
    
    # Test 3: No LLM specification
    try:
        agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            verbose=True
        )
        print("✅ Test 3: No LLM specification - SUCCESS")
    except Exception as e:
        print(f"❌ Test 3: No LLM specification - FAILED: {e}")

if __name__ == "__main__":
    test_llm_configs() 