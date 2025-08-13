#!/usr/bin/env python3
"""
Direct File Creation Demo

This script directly uses the file creation tools to demonstrate that files
are actually created in the filesystem, without relying on the LLM.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our tools
sys.path.append(str(Path(__file__).parent / "src"))

from crewdev.tools import (
    ReadFileTool, WriteFileTool, ListDirectoryTool, CreateDirectoryTool,
    CreateProjectTool, CreateRequirementsTool, CreatePackageJsonTool,
    CreateDockerfileTool, CreateDockerComposeTool, CreateGitignoreTool
)

def demo_basic_file_creation():
    """Demonstrate basic file creation using tools directly"""
    print("🔧 Direct File Creation Demo")
    print("=" * 50)
    
    # Initialize tools
    write_tool = WriteFileTool()
    read_tool = ReadFileTool()
    list_tool = ListDirectoryTool()
    create_dir_tool = CreateDirectoryTool()
    
    # Create a test directory
    print("1. Creating test directory...")
    create_dir_tool.run("direct_demo")
    
    # Create a simple text file
    print("2. Creating hello.txt...")
    write_tool.run("direct_demo/hello.txt", "Hello, World! This file was created by the file creation tools.")
    
    # Create a Python file
    print("3. Creating test.py...")
    python_content = '''def greet(name):
    """Simple greeting function"""
    return f"Hello, {name}!"

def main():
    print(greet("World"))
    print("This Python file was created by the file creation tools!")

if __name__ == "__main__":
    main()
'''
    write_tool.run("direct_demo/test.py", python_content)
    
    # Create a JSON file
    print("4. Creating data.json...")
    json_content = '''{
    "name": "test_project",
    "version": "1.0.0",
    "description": "A test project created by file creation tools",
    "files": [
        "hello.txt",
        "test.py",
        "data.json"
    ],
    "created_by": "crewdev_tools"
}
'''
    write_tool.run("direct_demo/data.json", json_content)
    
    # Verify files were created
    print("5. Verifying files were created...")
    list_result = list_tool.run("direct_demo")
    print(f"Directory contents: {list_result}")
    
    # Read back the files to verify content
    print("6. Reading back files to verify content...")
    
    hello_content = read_tool.run("direct_demo/hello.txt")
    print(f"hello.txt content: {hello_content[:50]}...")
    
    python_content_read = read_tool.run("direct_demo/test.py")
    print(f"test.py content: {python_content_read[:50]}...")
    
    json_content_read = read_tool.run("direct_demo/data.json")
    print(f"data.json content: {json_content_read[:50]}...")
    
    return True

def demo_project_creation():
    """Demonstrate project creation using project tools"""
    print("\n🏗️ Project Creation Demo")
    print("=" * 50)
    
    # Initialize project tools
    create_project_tool = CreateProjectTool()
    create_requirements_tool = CreateRequirementsTool()
    create_gitignore_tool = CreateGitignoreTool()
    create_dockerfile_tool = CreateDockerfileTool()
    create_docker_compose_tool = CreateDockerComposeTool()
    
    # Create a Python project
    print("1. Creating Python project structure...")
    project_result = create_project_tool.run("demo_project", "python")
    print(f"Project creation result: {project_result}")
    
    # Create requirements.txt
    print("2. Creating requirements.txt...")
    requirements_result = create_requirements_tool.run(["flask", "requests", "pytest"], "demo_project/requirements.txt")
    print(f"Requirements creation result: {requirements_result}")
    
    # Create .gitignore
    print("3. Creating .gitignore...")
    gitignore_result = create_gitignore_tool.run("demo_project", "python")
    print(f"Gitignore creation result: {gitignore_result}")
    
    # Create Dockerfile
    print("4. Creating Dockerfile...")
    dockerfile_result = create_dockerfile_tool.run("python:3.9-slim", "/app", "requirements.txt", "app.py")
    write_tool = WriteFileTool()
    write_tool.run("demo_project/Dockerfile", dockerfile_result)
    print(f"Dockerfile creation result: {dockerfile_result}")
    
    # Create docker-compose.yml
    print("5. Creating docker-compose.yml...")
    compose_result = create_docker_compose_tool.run(["demo-app"], {"demo-app": "5000"})
    write_tool.run("demo_project/docker-compose.yml", compose_result)
    print(f"Docker compose creation result: {compose_result}")
    
    # Verify project structure
    print("6. Verifying project structure...")
    list_tool = ListDirectoryTool()
    project_contents = list_tool.run("demo_project")
    print(f"Project contents: {project_contents}")
    
    return True

def demo_file_verification():
    """Demonstrate file verification capabilities"""
    print("\n✅ File Verification Demo")
    print("=" * 50)
    
    read_tool = ReadFileTool()
    list_tool = ListDirectoryTool()
    
    # Check if our demo directories exist
    print("1. Checking if demo directories exist...")
    
    if Path("direct_demo").exists():
        print("✅ direct_demo directory exists")
        direct_contents = list_tool.run("direct_demo")
        print(f"   Contents: {direct_contents}")
    else:
        print("❌ direct_demo directory does not exist")
    
    if Path("demo_project").exists():
        print("✅ demo_project directory exists")
        project_contents = list_tool.run("demo_project")
        print(f"   Contents: {project_contents}")
    else:
        print("❌ demo_project directory does not exist")
    
    # Read some files to verify they contain expected content
    print("\n2. Verifying file contents...")
    
    try:
        hello_content = read_tool.run("direct_demo/hello.txt")
        if "Hello, World!" in hello_content:
            print("✅ hello.txt contains expected content")
        else:
            print("❌ hello.txt does not contain expected content")
    except Exception as e:
        print(f"❌ Error reading hello.txt: {e}")
    
    try:
        requirements_content = read_tool.run("demo_project/requirements.txt")
        if "flask" in requirements_content and "requests" in requirements_content:
            print("✅ requirements.txt contains expected dependencies")
        else:
            print("❌ requirements.txt does not contain expected dependencies")
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
    
    return True

def main():
    """Main function to run all demos"""
    print("🚀 Starting Direct File Creation Demos")
    print("This demo shows that file creation tools work without LLM dependency")
    print("=" * 60)
    
    try:
        # Run basic file creation demo
        demo_basic_file_creation()
        
        # Run project creation demo
        demo_project_creation()
        
        # Run file verification demo
        demo_file_verification()
        
        print("\n" + "=" * 60)
        print("✅ All demos completed successfully!")
        print("📁 Check the created directories:")
        print("   - direct_demo/ (basic files)")
        print("   - demo_project/ (complete project structure)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 