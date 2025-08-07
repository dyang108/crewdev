#!/usr/bin/env python
"""
Comprehensive verification script for the Software Engineering Team
"""

import subprocess
import sys
import os
from datetime import datetime

def check_ollama():
    """Check if Ollama is installed and the model is available"""
    print("🔍 Checking Ollama setup...")
    
    try:
        # Check if ollama is installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not found")
            return False
        
        # Check if the model is available
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'gpt-oss:20b' in result.stdout:
            print("✅ gpt-oss:20b model is available")
            return True
        else:
            print("❌ gpt-oss:20b model not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    print("🔍 Checking Python dependencies...")
    
    try:
        import crewai
        print(f"✅ CrewAI installed: {crewai.__version__}")
        
        from src.crewdev.crew import SoftwareEngineeringTeam
        print("✅ SoftwareEngineeringTeam class imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_team_creation():
    """Test team creation and configuration"""
    print("🔍 Testing team creation...")
    
    try:
        from src.crewdev.crew import SoftwareEngineeringTeam
        
        team = SoftwareEngineeringTeam()
        crew = team.crew()
        
        print(f"✅ Team created with {len(crew.agents)} agents:")
        for i, agent in enumerate(crew.agents, 1):
            print(f"   {i}. {agent.role}")
        
        print(f"✅ Team has {len(crew.tasks)} tasks:")
        for i, task in enumerate(crew.tasks, 1):
            print(f"   {i}. {task.description[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating team: {e}")
        return False

def test_configuration_files():
    """Test configuration file loading"""
    print("🔍 Testing configuration files...")
    
    try:
        import yaml
        
        # Test agents config
        with open('src/crewdev/config/agents.yaml', 'r') as f:
            agents_config = yaml.safe_load(f)
            print(f"✅ Agents config loaded: {len(agents_config)} agents")
        
        # Test tasks config
        with open('src/crewdev/config/tasks.yaml', 'r') as f:
            tasks_config = yaml.safe_load(f)
            print(f"✅ Tasks config loaded: {len(tasks_config)} tasks")
        
        # Test logging config
        with open('src/crewdev/config/logging_config.yaml', 'r') as f:
            logging_config = yaml.safe_load(f)
            print(f"✅ Logging config loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading config files: {e}")
        return False

def test_logging_setup():
    """Test logging configuration and thought process tracking"""
    print("🔍 Testing logging setup...")
    
    try:
        import logging
        import yaml
        
        # Test logging config loading
        with open('src/crewdev/config/logging_config.yaml', 'r') as f:
            log_config = yaml.safe_load(f)
            print("✅ Logging configuration loaded")
        
        # Test that log file can be created
        test_log_file = "test_thought_process.log"
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[logging.FileHandler(test_log_file)]
        )
        
        logger = logging.getLogger("test")
        logger.info("Test log message")
        
        if os.path.exists(test_log_file):
            print("✅ Log file creation works")
            os.remove(test_log_file)  # Clean up
        else:
            print("❌ Log file creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing logging: {e}")
        return False

def test_example_usage():
    """Test example usage script"""
    print("🔍 Testing example usage...")
    
    try:
        from example_usage import run_ecommerce_project, run_mobile_app_project, run_saas_project
        print("✅ Example usage functions imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error importing example usage: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🏗️  Software Engineering Team Verification")
    print("=" * 50)
    
    tests = [
        ("Ollama Setup", check_ollama),
        ("Python Dependencies", check_python_dependencies),
        ("Configuration Files", test_configuration_files),
        ("Team Creation", test_team_creation),
        ("Logging Setup", test_logging_setup),
        ("Example Usage", test_example_usage),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The software engineering team is ready to use.")
        print("\n🚀 To run the team with thought process logging:")
        print("   python -m src.crewdev.main")
        print("\n📖 To see examples:")
        print("   python example_usage.py")
        print("\n📝 Thought process will be logged to:")
        print("   crew_thought_process.log")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 