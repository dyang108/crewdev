#!/usr/bin/env python
import sys
import warnings
import logging
import yaml
from datetime import datetime

from crewdev.crew import SoftwareEngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def setup_logging():
    """Setup detailed logging for the crew's thought process"""
    try:
        with open('src/crewdev/config/logging_config.yaml', 'r') as f:
            log_config = yaml.safe_load(f)
        
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('crew_thought_process.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        print("📝 Logging configured - thought process will be saved to 'crew_thought_process.log'")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not load logging config: {e}")
        # Fallback to basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the software engineering team crew.
    """
    setup_logging()
    
    # Prompt user for project details
    print("🚀 Welcome to the Software Engineering Team!")
    print("=" * 60)
    
    # Get project name
    project_name = input("📋 What project would you like to build? (e.g., 'E-commerce Platform', 'Task Management App', 'Social Media App'): ").strip()
    if not project_name:
        project_name = "Custom Software Project"
    
    # Get additional project context
    print("\n💡 Tell us more about your project:")
    project_description = input("📝 Project description (optional): ").strip()
    
    # Get target users
    target_users = input("👥 Who are the target users? (e.g., 'busy professionals', 'students', 'small businesses'): ").strip()
    if not target_users:
        target_users = "general users"
    
    # Get key features
    key_features = input("✨ What are the key features you want? (e.g., 'user authentication, real-time chat, payment processing'): ").strip()
    if not key_features:
        key_features = "standard features"
    
    # Get technology preferences
    tech_preferences = input("🔧 Any technology preferences? (e.g., 'React frontend, Python backend, AWS hosting'): ").strip()
    if not tech_preferences:
        tech_preferences = "modern best practices"
    
    # Build inputs dictionary
    inputs = {
        'project_name': project_name,
        'project_description': project_description,
        'target_users': target_users,
        'key_features': key_features,
        'tech_preferences': tech_preferences,
        'current_year': str(datetime.now().year)
    }
    
    print("\n" + "=" * 60)
    print("📋 Project Summary:")
    print(f"   🎯 Project: {project_name}")
    if project_description:
        print(f"   📝 Description: {project_description}")
    print(f"   👥 Target Users: {target_users}")
    print(f"   ✨ Key Features: {key_features}")
    print(f"   🔧 Tech Preferences: {tech_preferences}")
    print("=" * 60)
    
    # Confirm with user
    confirm = input("\n🤔 Ready to start building? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '']:
        print("❌ Project cancelled. Goodbye!")
        return None
    
    print("\n🚀 Starting Software Engineering Team...")
    print("📝 Thought process will be logged to 'crew_thought_process.log'")
    print("=" * 60)
    
    try:
        result = SoftwareEngineeringTeam().crew().kickoff(inputs=inputs)
        print("=" * 60)
        print("✅ Team work completed successfully!")
        print("📄 Check 'crew_thought_process.log' for detailed thought process")
        print("📄 Check 'project_deliverables.md' for final deliverables")
        return result
    except Exception as e:
        print(f"❌ Error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    setup_logging()
    
    # Prompt user for project details
    print("🚀 Training the Software Engineering Team!")
    print("=" * 60)
    
    # Get project name
    project_name = input("📋 What project should the team train on? (e.g., 'E-commerce Platform', 'Task Management App'): ").strip()
    if not project_name:
        project_name = "Custom Software Project"
    
    # Get additional context
    project_description = input("📝 Project description (optional): ").strip()
    target_users = input("👥 Target users (optional): ").strip()
    if not target_users:
        target_users = "general users"
    
    inputs = {
        "project_name": project_name,
        "project_description": project_description,
        "target_users": target_users,
        'current_year': str(datetime.now().year)
    }
    
    print(f"\n🎯 Training on: {project_name}")
    
    try:
        result = SoftwareEngineeringTeam().crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)
        print("✅ Training completed successfully!")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    setup_logging()
    
    try:
        result = SoftwareEngineeringTeam().crew().replay(task_id=sys.argv[2])
        print("✅ Replay completed successfully!")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    setup_logging()
    
    # Prompt user for project details
    print("🧪 Testing the Software Engineering Team!")
    print("=" * 60)
    
    # Get project name
    project_name = input("📋 What project should the team test on? (e.g., 'E-commerce Platform', 'Task Management App'): ").strip()
    if not project_name:
        project_name = "Custom Software Project"
    
    # Get additional context
    project_description = input("📝 Project description (optional): ").strip()
    target_users = input("👥 Target users (optional): ").strip()
    if not target_users:
        target_users = "general users"
    
    inputs = {
        "project_name": project_name,
        "project_description": project_description,
        "target_users": target_users,
        "current_year": str(datetime.now().year)
    }
    
    print(f"\n🧪 Testing on: {project_name}")
    
    try:
        result = SoftwareEngineeringTeam().crew().test(n_iterations=int(sys.argv[2]), eval_llm=sys.argv[3], inputs=inputs)
        print("✅ Testing completed successfully!")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

# Add the missing entry point
if __name__ == "__main__":
    # Check command line arguments to determine which function to run
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "train" and len(sys.argv) >= 4:
            train()
        elif command == "replay" and len(sys.argv) >= 3:
            replay()
        elif command == "test" and len(sys.argv) >= 4:
            test()
        else:
            print("Usage:")
            print("  python -m src.crewdev.main                    # Run the crew")
            print("  python -m src.crewdev.main train <iterations> <filename>")
            print("  python -m src.crewdev.main replay <task_id>")
            print("  python -m src.crewdev.main test <iterations> <eval_llm>")
    else:
        # Default: run the crew
        run()
