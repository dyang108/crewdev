#!/usr/bin/env python3
"""
Example demonstrating dynamic task assignment in CrewAI.

This script shows how agents can:
1. Request the next task based on project state
2. Report task completion
3. Add bugs and feature requests
4. Automatically assign tasks to appropriate agents
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crewdev.crew import SoftwareEngineeringTeam
from crewdev.dynamic_task_manager import DynamicTaskManager

def main():
    """Demonstrate dynamic task assignment."""
    
    print("🚀 Starting Dynamic Task Assignment Demo")
    print("=" * 50)
    
    # Initialize the crew with dynamic task management
    crew = SoftwareEngineeringTeam()
    
    # Get the task manager for demonstration
    task_manager = crew.task_manager
    
    print("\n📋 Initial Project State:")
    print(f"Completed tasks: {len(task_manager.completed_tasks)}")
    print(f"Pending bugs: {len(task_manager._get_pending_bugs())}")
    print(f"Pending features: {len(task_manager._get_pending_features())}")
    
    # Simulate some project state
    print("\n🔧 Simulating project state...")
    
    # Add some bugs
    task_manager.add_bug("Frontend login button not working", "high", "frontend")
    task_manager.add_bug("API endpoint returning 500 error", "critical", "backend")
    task_manager.add_feature("Add user profile page", "medium", "frontend")
    task_manager.add_feature("Implement search functionality", "high", "backend")
    
    print("✅ Added bugs and feature requests to project state")
    
    # Demonstrate task assignment for different agents
    print("\n🎯 Demonstrating Dynamic Task Assignment:")
    print("-" * 40)
    
    agents = [
        "product_manager",
        "staff_engineer", 
        "senior_engineer_frontend",
        "senior_engineer_backend",
        "technical_skeptic"
    ]
    
    for agent_name in agents:
        print(f"\n🤖 {agent_name.upper()}:")
        next_task = task_manager.determine_next_task(agent_name)
        
        if next_task:
            print(f"   Next task: {next_task.description[:100]}...")
            print(f"   Expected output: {next_task.expected_output[:100]}...")
        else:
            print("   No specific task needed at this time")
    
    # Simulate task completion
    print("\n✅ Simulating task completion...")
    task_manager.mark_task_completed("market_research_task", "Market research completed with user personas and requirements")
    task_manager.mark_task_completed("technical_architecture_task", "Technical architecture designed with React frontend and Python backend")
    
    print("✅ Marked market research and technical architecture as completed")
    
    # Show updated task assignments
    print("\n🔄 Updated Task Assignments After Completion:")
    print("-" * 40)
    
    for agent_name in agents:
        print(f"\n🤖 {agent_name.upper()}:")
        next_task = task_manager.determine_next_task(agent_name)
        
        if next_task:
            print(f"   Next task: {next_task.description[:100]}...")
        else:
            print("   No specific task needed at this time")
    
    # Demonstrate bug assignment
    print("\n🐛 Bug Assignment Demo:")
    print("-" * 40)
    
    frontend_bug_task = task_manager.create_bug_fix_task(
        "Frontend login button not working", 
        "senior_engineer_frontend"
    )
    print(f"Frontend bug task: {frontend_bug_task.description}")
    
    backend_bug_task = task_manager.create_bug_fix_task(
        "API endpoint returning 500 error", 
        "senior_engineer_backend"
    )
    print(f"Backend bug task: {backend_bug_task.description}")
    
    # Demonstrate feature assignment
    print("\n✨ Feature Assignment Demo:")
    print("-" * 40)
    
    frontend_feature_task = task_manager.create_feature_task(
        "Add user profile page", 
        "senior_engineer_frontend"
    )
    print(f"Frontend feature task: {frontend_feature_task.description}")
    
    backend_feature_task = task_manager.create_feature_task(
        "Implement search functionality", 
        "senior_engineer_backend"
    )
    print(f"Backend feature task: {backend_feature_task.description}")
    
    # Show final project status
    print("\n📊 Final Project Status:")
    print("-" * 40)
    status = task_manager.get_project_status()
    print(f"Completed tasks: {status['completed_tasks']}")
    print(f"Pending bugs: {status['pending_bugs']}")
    print(f"Pending features: {status['pending_features']}")
    
    print("\n🎉 Dynamic Task Assignment Demo Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Agents can request next tasks based on project state")
    print("   ✅ Tasks are automatically assigned to appropriate agents")
    print("   ✅ Bugs and features are tracked and assigned")
    print("   ✅ Task completion updates project state")
    print("   ✅ Dynamic task creation based on current needs")

if __name__ == "__main__":
    main() 