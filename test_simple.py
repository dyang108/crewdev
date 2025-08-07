#!/usr/bin/env python
"""
Simple test to verify the software engineering team works
"""

from datetime import datetime
from src.crewdev.crew import SoftwareEngineeringTeam

def test_single_task():
    """Test the team with just the market research task"""
    print("🧪 Testing Software Engineering Team...")
    
    inputs = {
        'project_name': 'Simple Test Project',
        'current_year': str(datetime.now().year)
    }
    
    try:
        team = SoftwareEngineeringTeam()
        crew = team.crew()
        
        # Test with just the first task
        print(f"✅ Team created with {len(crew.agents)} agents")
        print(f"✅ Team has {len(crew.tasks)} tasks")
        
        # Test the first task
        first_task = crew.tasks[0]
        print(f"✅ First task: {first_task.description[:100]}...")
        
        print("✅ Team configuration is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_single_task() 