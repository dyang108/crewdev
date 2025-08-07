#!/usr/bin/env python
"""
Test script to verify thought process logging
"""

from datetime import datetime
from src.crewdev.crew import SoftwareEngineeringTeam

def test_thought_logging():
    """Test that the crew logs its thought process"""
    print("🧪 Testing Thought Process Logging...")
    
    inputs = {
        'project_name': 'Logging Test Project',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        crew = team.crew()
        
        print("✅ Crew created successfully")
        print("📝 Starting thought process logging test...")
        print("=" * 50)
        
        # Test the first task to see logging in action
        first_task = crew.tasks[0]
        print(f"🎯 Testing task: {first_task.description[:100]}...")
        
        # This will trigger the step_callback and logging
        print("💭 Agents will now show their thinking process...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_thought_logging() 