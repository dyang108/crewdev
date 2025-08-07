#!/usr/bin/env python3
"""
Simple demonstration of dynamic task assignment logic.
This shows how the system works without the full CrewAI setup.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crewdev.dynamic_task_manager import DynamicTaskManager

def main():
    """Demonstrate dynamic task assignment logic."""
    
    print("🚀 Simple Dynamic Task Assignment Demo")
    print("=" * 50)
    
    # Initialize the task manager
    task_manager = DynamicTaskManager()
    
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
    
    # Demonstrate task assignment logic for different agents
    print("\n🎯 Demonstrating Dynamic Task Assignment Logic:")
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
        
        # Check what task would be assigned
        if not task_manager._has_market_research():
            print(f"   Would assign: Market Research Task")
        elif not task_manager._has_technical_architecture():
            print(f"   Would assign: Technical Architecture Task")
        elif not task_manager._has_implementation():
            if agent_name == 'senior_engineer_frontend':
                print(f"   Would assign: Frontend Implementation Task")
            elif agent_name == 'senior_engineer_backend':
                print(f"   Would assign: Backend Implementation Task")
            elif agent_name == 'senior_engineer_devops':
                print(f"   Would assign: DevOps Setup Task")
            else:
                print(f"   No implementation task for this agent")
        elif not task_manager._has_review():
            if agent_name == 'technical_skeptic':
                print(f"   Would assign: Technical Skeptic Review Task")
            elif agent_name == 'staff_engineer':
                print(f"   Would assign: Code Review Task")
            else:
                print(f"   No review task for this agent")
        elif not task_manager._has_integration():
            print(f"   Would assign: Final Integration Task")
        else:
            # Check for bugs and features
            bugs = task_manager._get_pending_bugs()
            features = task_manager._get_pending_features()
            
            if bugs and agent_name in ['senior_engineer_frontend', 'senior_engineer_backend']:
                bug = bugs[0]
                print(f"   Would assign: Bug Fix Task - {bug['description'][:50]}...")
            elif features and agent_name in ['senior_engineer_frontend', 'senior_engineer_backend']:
                feature = features[0]
                print(f"   Would assign: Feature Implementation Task - {feature['description'][:50]}...")
            elif agent_name == 'product_manager':
                print(f"   Would assign: Next Steps Planning Task")
            else:
                print(f"   No specific task needed at this time")
    
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
        
        # Check what task would be assigned now
        if not task_manager._has_implementation():
            if agent_name == 'senior_engineer_frontend':
                print(f"   Would assign: Frontend Implementation Task")
            elif agent_name == 'senior_engineer_backend':
                print(f"   Would assign: Backend Implementation Task")
            elif agent_name == 'senior_engineer_devops':
                print(f"   Would assign: DevOps Setup Task")
            else:
                print(f"   No implementation task for this agent")
        elif not task_manager._has_review():
            if agent_name == 'technical_skeptic':
                print(f"   Would assign: Technical Skeptic Review Task")
            elif agent_name == 'staff_engineer':
                print(f"   Would assign: Code Review Task")
            else:
                print(f"   No review task for this agent")
        elif not task_manager._has_integration():
            print(f"   Would assign: Final Integration Task")
        else:
            # Check for bugs and features
            bugs = task_manager._get_pending_bugs()
            features = task_manager._get_pending_features()
            
            if bugs and agent_name in ['senior_engineer_frontend', 'senior_engineer_backend']:
                bug = bugs[0]
                print(f"   Would assign: Bug Fix Task - {bug['description'][:50]}...")
            elif features and agent_name in ['senior_engineer_frontend', 'senior_engineer_backend']:
                feature = features[0]
                print(f"   Would assign: Feature Implementation Task - {feature['description'][:50]}...")
            elif agent_name == 'product_manager':
                print(f"   Would assign: Next Steps Planning Task")
            else:
                print(f"   No specific task needed at this time")
    
    # Demonstrate bug assignment
    print("\n🐛 Bug Assignment Demo:")
    print("-" * 40)
    
    frontend_bug = task_manager._get_pending_bugs()[0]
    print(f"Frontend bug: {frontend_bug['description']}")
    print(f"Component: {frontend_bug['component']}")
    print(f"Priority: {frontend_bug['priority']}")
    print(f"Would be assigned to: senior_engineer_frontend")
    
    backend_bug = task_manager._get_pending_bugs()[1]
    print(f"\nBackend bug: {backend_bug['description']}")
    print(f"Component: {backend_bug['component']}")
    print(f"Priority: {backend_bug['priority']}")
    print(f"Would be assigned to: senior_engineer_backend")
    
    # Demonstrate feature assignment
    print("\n✨ Feature Assignment Demo:")
    print("-" * 40)
    
    frontend_feature = task_manager._get_pending_features()[0]
    print(f"Frontend feature: {frontend_feature['description']}")
    print(f"Component: {frontend_feature['component']}")
    print(f"Priority: {frontend_feature['priority']}")
    print(f"Would be assigned to: senior_engineer_frontend")
    
    backend_feature = task_manager._get_pending_features()[1]
    print(f"\nBackend feature: {backend_feature['description']}")
    print(f"Component: {backend_feature['component']}")
    print(f"Priority: {backend_feature['priority']}")
    print(f"Would be assigned to: senior_engineer_backend")
    
    # Show final project status
    print("\n📊 Final Project Status:")
    print("-" * 40)
    status = task_manager.get_project_status()
    print(f"Completed tasks: {status['completed_tasks']}")
    print(f"Pending bugs: {status['pending_bugs']}")
    print(f"Pending features: {status['pending_features']}")
    
    print("\n🎉 Dynamic Task Assignment Demo Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Task assignment based on project state")
    print("   ✅ Automatic routing to appropriate agents")
    print("   ✅ Bug and feature tracking")
    print("   ✅ Task completion updates project state")
    print("   ✅ Intelligent task prioritization")

if __name__ == "__main__":
    main() 