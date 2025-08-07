#!/usr/bin/env python3
"""
Example demonstrating how the crew can use tools to build a complete application.
This example shows the crew creating a simple Flask API with a React frontend.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_example():
    """Run a complete example of the crew using tools to build an application."""
    
    print("🚀 CrewDev Tools Example")
    print("=" * 60)
    print("This example demonstrates how your crew can use tools to:")
    print("1. Create a complete project structure")
    print("2. Write code files")
    print("3. Set up dependencies")
    print("4. Start development servers")
    print("5. Test the application")
    print("=" * 60)
    
    # Import the crew
    from crewdev.crew import SoftwareEngineeringTeam
    
    # Create the team
    team = SoftwareEngineeringTeam()
    
    # Define the project inputs
    inputs = {
        'project_name': 'Todo App',
        'project_description': 'A simple todo application with Flask backend and React frontend',
        'target_users': 'individuals who want to manage their daily tasks',
        'key_features': 'add todos, mark as complete, delete todos, persistent storage',
        'tech_preferences': 'Flask backend, React frontend, SQLite database',
        'current_year': '2024'
    }
    
    print(f"\n🎯 Building: {inputs['project_name']}")
    print(f"📝 Description: {inputs['project_description']}")
    print(f"👥 Target Users: {inputs['target_users']}")
    print(f"✨ Features: {inputs['key_features']}")
    print(f"🔧 Tech Stack: {inputs['tech_preferences']}")
    
    # Confirm with user
    confirm = input("\n🤔 Ready to start building? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '']:
        print("❌ Example cancelled. Goodbye!")
        return
    
    print("\n🚀 Starting the crew...")
    print("The crew will now:")
    print("1. Create project structure")
    print("2. Write backend API code")
    print("3. Write frontend React code")
    print("4. Set up dependencies")
    print("5. Create Docker configuration")
    print("6. Test the application")
    print("\n📝 Check 'crew_thought_process.log' for detailed thought process")
    print("=" * 60)
    
    try:
        # Run the crew
        result = team.crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 60)
        print("✅ Crew work completed!")
        print("📄 Check 'project_deliverables.md' for final deliverables")
        print("📄 Check 'crew_thought_process.log' for detailed thought process")
        
        # Show what was created
        print("\n📁 Project Structure Created:")
        if Path("todo_app").exists():
            print("  📁 todo_app/ - Main project directory")
            if Path("todo_app/backend").exists():
                print("    📁 backend/ - Flask API")
            if Path("todo_app/frontend").exists():
                print("    📁 frontend/ - React app")
            if Path("todo_app/docker-compose.yml").exists():
                print("    📄 docker-compose.yml - Multi-service setup")
        
        print("\n🎉 Your crew has successfully created a complete application!")
        print("You can now:")
        print("  - Navigate to the project directory")
        print("  - Start the development servers")
        print("  - Test the application")
        print("  - Deploy using Docker")
        
        return result
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        raise

def show_tool_capabilities():
    """Show what tools are available to each agent."""
    print("\n🛠️ Tool Capabilities by Role:")
    print("=" * 60)
    
    capabilities = {
        "Staff Engineer": [
            "📁 File management (read/write/list/create directories)",
            "🏗️ Project creation and structure setup",
            "🐳 Docker and Docker Compose configuration",
            "⚡ Command execution and port checking"
        ],
        "Frontend Engineer": [
            "📁 File management for frontend code",
            "📦 Package.json creation for Node.js/React",
            "🚀 Server management (start/stop dev servers)",
            "📦 npm package installation"
        ],
        "Backend Engineer": [
            "📁 File management for backend code",
            "🐍 Requirements.txt creation for Python",
            "🚀 API server management",
            "🐍 Python script execution and pip package installation",
            "🐳 Dockerfile creation for backend services"
        ],
        "DevOps Engineer": [
            "📁 File management for infrastructure",
            "🐳 Docker and Docker Compose setup",
            "🚀 Full server lifecycle management",
            "📦 System and Python package installation"
        ],
        "Technical Skeptic": [
            "📁 Code review tools (read files, check existence)",
            "🧪 Testing tools (run commands and scripts)",
            "🔍 Analysis tools (port checking, system status)"
        ],
        "Product Manager": [
            "📁 Documentation tools (read/write files)",
            "🏗️ Project setup and structure creation",
            "⚡ Basic command execution for project management"
        ]
    }
    
    for role, tools in capabilities.items():
        print(f"\n👤 {role}:")
        for tool in tools:
            print(f"  {tool}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tools":
        show_tool_capabilities()
    else:
        run_example() 