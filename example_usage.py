#!/usr/bin/env python
"""
Example usage of the Software Engineering Team with CrewAI

This script demonstrates how to use the team for different types of projects.
"""

import os
from datetime import datetime
from src.crewdev.crew import SoftwareEngineeringTeam

# Configure Ollama for this script
# For Ollama with CrewAI, use only OpenAI-compatible environment variables
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Dummy key for Ollama
# Remove OLLAMA_BASE_URL - CrewAI uses Langchain which expects OpenAI-style APIs
os.environ["LLM_MODEL"] = "gpt-oss:20b"
os.environ["DEFAULT_MODEL"] = "gpt-oss:20b"
os.environ["MODEL_NAME"] = "gpt-oss:20b"

def run_ecommerce_project():
    """Run the team on an e-commerce project"""
    print("🚀 Starting E-commerce Project Development...")
    
    inputs = {
        'project_name': 'E-commerce Platform',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        result = team.crew().kickoff(inputs=inputs)
        print("✅ E-commerce project completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Error in e-commerce project: {e}")
        return None

def run_mobile_app_project():
    """Run the team on a mobile app project"""
    print("📱 Starting Mobile App Development...")
    
    inputs = {
        'project_name': 'Task Management Mobile App',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        result = team.crew().kickoff(inputs=inputs)
        print("✅ Mobile app project completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Error in mobile app project: {e}")
        return None

def run_saas_project():
    """Run the team on a SaaS project"""
    print("☁️ Starting SaaS Platform Development...")
    
    inputs = {
        'project_name': 'Project Management SaaS',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        result = team.crew().kickoff(inputs=inputs)
        print("✅ SaaS project completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Error in SaaS project: {e}")
        return None

if __name__ == "__main__":
    print("🏗️  Software Engineering Team Examples")
    print("=" * 50)
    
    # Choose which project to run
    print("\nAvailable projects:")
    print("1. E-commerce Platform")
    print("2. Mobile App")
    print("3. SaaS Platform")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        run_ecommerce_project()
    elif choice == "2":
        run_mobile_app_project()
    elif choice == "3":
        run_saas_project()
    else:
        print("❌ Invalid choice. Running default task management project...")
        # Run the default project from main.py
        from src.crewdev.main import run
        run() 