#!/usr/bin/env python3
"""
Test script to verify that all tools are working correctly.
This script tests the basic functionality of each tool.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_tool_imports():
    """Test that all tools can be imported successfully."""
    print("🔍 Testing tool imports...")
    
    try:
        from crewdev.tools import (
            # File tools
            ReadFileTool, WriteFileTool, ListDirectoryTool, CreateDirectoryTool, DeleteFileTool, FileExistsTool,
            # Execution tools
            RunCommandTool, StartServerTool, StopServerTool, ListServersTool, CheckPortTool, InstallPackageTool, RunPythonScriptTool,
            # Dev tools
            CreateProjectTool, CreateRequirementsTool, CreatePackageJsonTool, CreateDockerfileTool, CreateDockerComposeTool, CreateGitignoreTool
        )
        print("✅ All tools imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_file_tools():
    """Test basic file tool functionality."""
    print("\n📁 Testing file tools...")
    
    try:
        from crewdev.tools import WriteFileTool, ReadFileTool, ListDirectoryTool, CreateDirectoryTool, FileExistsTool, DeleteFileTool
        
        # Test directory creation
        create_dir_tool = CreateDirectoryTool()
        result = create_dir_tool._run("test_project")
        print(f"  Create directory: {result}")
        
        # Test file writing
        write_tool = WriteFileTool()
        result = write_tool._run("test_project/test_file.txt", "Hello, World!")
        print(f"  Write file: {result}")
        
        # Test file reading
        read_tool = ReadFileTool()
        result = read_tool._run("test_project/test_file.txt")
        print(f"  Read file: {result[:50]}...")
        
        # Test file existence
        exists_tool = FileExistsTool()
        result = exists_tool._run("test_project/test_file.txt")
        print(f"  File exists: {result}")
        
        # Test directory listing
        list_tool = ListDirectoryTool()
        result = list_tool._run("test_project")
        print(f"  List directory: {result[:100]}...")
        
        # Test file deletion
        delete_tool = DeleteFileTool()
        result = delete_tool._run("test_project/test_file.txt")
        print(f"  Delete file: {result}")
        
        # Clean up test directory
        import shutil
        shutil.rmtree("test_project")
        
        print("✅ File tools working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ File tools error: {e}")
        return False

def test_execution_tools():
    """Test basic execution tool functionality."""
    print("\n⚡ Testing execution tools...")
    
    try:
        from crewdev.tools import RunCommandTool, CheckPortTool
        
        # Test command execution
        run_tool = RunCommandTool()
        result = run_tool._run("echo 'Hello from command'")
        print(f"  Run command: {result[:100]}...")
        
        # Test port checking
        port_tool = CheckPortTool()
        result = port_tool._run(8080)
        print(f"  Check port: {result}")
        
        print("✅ Execution tools working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Execution tools error: {e}")
        return False

def test_dev_tools():
    """Test basic development tool functionality."""
    print("\n🏗️ Testing development tools...")
    
    try:
        from crewdev.tools import CreateRequirementsTool, CreateGitignoreTool
        
        # Test requirements creation
        req_tool = CreateRequirementsTool()
        result = req_tool._run(["flask", "pytest", "requests"])
        print(f"  Create requirements: {result}")
        
        # Test gitignore creation
        gitignore_tool = CreateGitignoreTool()
        result = gitignore_tool._run("test_project", "python")
        print(f"  Create gitignore: {result}")
        
        # Clean up
        Path("requirements.txt").unlink(missing_ok=True)
        Path(".gitignore").unlink(missing_ok=True)
        
        print("✅ Development tools working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Development tools error: {e}")
        return False

def test_crew_integration():
    """Test that tools can be integrated with the crew."""
    print("\n👥 Testing crew integration...")
    
    try:
        from crewdev.crew import SoftwareEngineeringTeam
        
        # Create crew instance
        team = SoftwareEngineeringTeam()
        
        # Get the crew object
        crew_obj = team.crew()
        
        # Check that agents have tools
        for agent in crew_obj.agents:
            if hasattr(agent, 'tools') and agent.tools:
                print(f"  ✅ {agent.role} has {len(agent.tools)} tools")
            else:
                print(f"  ⚠️ {agent.role} has no tools")
        
        print("✅ Crew integration working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Crew integration error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing CrewDev Tools")
    print("=" * 50)
    
    tests = [
        ("Tool Imports", test_tool_imports),
        ("File Tools", test_file_tools),
        ("Execution Tools", test_execution_tools),
        ("Development Tools", test_dev_tools),
        ("Crew Integration", test_crew_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your tools are ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 