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
    
    inputs = {
        'project_name': 'Task Management Application',
        'current_year': str(datetime.now().year)
    }
    
    print("🚀 Starting Software Engineering Team...")
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
    
    inputs = {
        "project_name": "Task Management Application",
        'current_year': str(datetime.now().year)
    }
    try:
        result = SoftwareEngineeringTeam().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
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
        result = SoftwareEngineeringTeam().crew().replay(task_id=sys.argv[1])
        print("✅ Replay completed successfully!")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    setup_logging()
    
    inputs = {
        "project_name": "Task Management Application",
        "current_year": str(datetime.now().year)
    }
    
    try:
        result = SoftwareEngineeringTeam().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        print("✅ Testing completed successfully!")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
