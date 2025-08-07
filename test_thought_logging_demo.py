#!/usr/bin/env python
"""
Demonstration of thought process logging
"""

import logging
from datetime import datetime
from src.crewdev.crew import SoftwareEngineeringTeam

def setup_demo_logging():
    """Setup logging for the demonstration"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('demo_thought_process.log'),
            logging.StreamHandler()
        ]
    )
    print("📝 Demo logging configured - thought process will be saved to 'demo_thought_process.log'")

def demo_thought_logging():
    """Demonstrate thought process logging with a simple task"""
    print("🧪 Demonstrating Thought Process Logging...")
    print("=" * 60)
    
    setup_demo_logging()
    
    inputs = {
        'project_name': 'Demo Project',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        crew = team.crew()
        
        print("✅ Team created successfully")
        print("🎯 Starting with first task to demonstrate thought process...")
        print("=" * 60)
        
        # Get the first task (market research)
        first_task = crew.tasks[0]
        print(f"📋 Task: {first_task.description}")
        print(f"👤 Assigned to: {first_task.agent.role}")
        print("=" * 60)
        
        print("💭 The agent will now show their thinking process...")
        print("📝 Check 'demo_thought_process.log' for detailed logs")
        print("=" * 60)
        
        # This would normally run the full crew, but for demo we'll just show the setup
        print("✅ Thought process logging is configured and ready!")
        print("🚀 Run 'python -m src.crewdev.main' to see it in action")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    demo_thought_logging() 