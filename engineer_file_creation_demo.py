#!/usr/bin/env python3
"""
Engineer File Creation Demo Script

This script demonstrates using only an engineer agent to create files and ensure
they are actually created in the filesystem. It focuses on practical file creation
tasks that can be verified.
"""

import os
import sys
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM

# Add the src directory to the path so we can import our tools
sys.path.append(str(Path(__file__).parent / "src"))

from crewdev.tools import (
    ReadFileTool, WriteFileTool, ListDirectoryTool, CreateDirectoryTool,
    CreateProjectTool, CreateRequirementsTool, CreatePackageJsonTool,
    CreateDockerfileTool, CreateDockerComposeTool, CreateGitignoreTool,
    RunCommandTool, CheckPortTool, InstallPackageTool
)

def setup_environment():
    """Set up environment variables for Ollama"""
    os.environ["LITELLM_PROVIDER"] = "ollama"
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"  # Dummy key for Ollama
    os.environ["LLM_MODEL"] = "ollama/gpt-oss:20b"  # Using Mistral with ollama/ prefix
    # Additional environment variables to ensure correct model usage
    os.environ["DEFAULT_MODEL"] = "ollama/gpt-oss:20b"
    os.environ["MODEL_NAME"] = "ollama/gpt-oss:20b"

def create_engineer_agent():
    """Create an engineer agent with file creation tools"""
    llm = OllamaLLM(
        model="ollama/gpt-oss:20b",
        url="http://localhost:11434",
        provider="ollama",
    )
    
    return Agent(
        role="Senior Software Engineer",
        goal="Create and manage files effectively, ensuring they are actually created in the filesystem",
        backstory="""You are a senior software engineer with 8+ years of experience in software development.
        You are highly skilled at creating files, managing projects, and ensuring code quality.
        You always verify that files are actually created and contain the expected content.
        You follow best practices and create well-structured, maintainable code.""",
        verbose=True,
        allow_delegation=False,
        step_callback=lambda x: print(f"🔧 Engineer thinking: {x}"),
        memory=True,
        llm=llm,
        tools=[
            # File management tools
            ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
            # Project creation tools
            CreateProjectTool(), CreateRequirementsTool(), CreatePackageJsonTool(),
            CreateDockerfileTool(), CreateDockerComposeTool(), CreateGitignoreTool(),
            # Execution tools
            RunCommandTool(), CheckPortTool(), InstallPackageTool(),
        ]
    )

def create_file_creation_task():
    """Create a task for file creation"""
    return Task(
        description="""
        Create a complete Python project structure with the following requirements:
        
        1. Create a new directory called 'demo_project' in the current working directory
        2. Create a main.py file with a simple "Hello, World!" application
        3. Create a requirements.txt file with basic dependencies (requests, flask)
        4. Create a README.md file with project documentation
        5. Create a .gitignore file with Python-specific ignores
        6. Create a simple test file (test_main.py) with basic unit tests
        7. Create a Dockerfile for containerization
        8. Create a docker-compose.yml file for easy deployment
        
        IMPORTANT: After creating each file, verify that it actually exists in the filesystem
        and contains the expected content. Use the file tools to read back the files and
        confirm they were created successfully.
        
        Expected output: A complete project structure with all files created and verified.
        """,
        expected_output="""
        A complete Python project structure including:
        - demo_project/ directory
        - main.py with Hello World application
        - requirements.txt with dependencies
        - README.md with documentation
        - .gitignore with Python ignores
        - test_main.py with unit tests
        - Dockerfile for containerization
        - docker-compose.yml for deployment
        
        Verification report showing all files were created successfully.
        """,
        agent=create_engineer_agent(),
        output_file="file_creation_report.md"
    )

def create_verification_task():
    """Create a task to verify all files were created"""
    return Task(
        description="""
        Verify that all files in the demo_project directory were created successfully:
        
        1. List all files in the demo_project directory
        2. Read each file and verify it contains the expected content
        3. Check that the file sizes are reasonable (not empty)
        4. Verify the project structure is correct
        5. Test that the main.py file can be executed without errors
        
        Create a detailed verification report showing the status of each file.
        """,
        expected_output="""
        A verification report including:
        - List of all created files
        - Content verification for each file
        - File size information
        - Project structure validation
        - Execution test results
        - Overall success/failure status
        """,
        agent=create_engineer_agent(),
        output_file="verification_report.md"
    )

def main():
    """Main function to run the engineer file creation demo"""
    print("🚀 Starting Engineer File Creation Demo")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Create the engineer agent
    engineer = create_engineer_agent()
    
    # Create tasks
    file_creation_task = create_file_creation_task()
    verification_task = create_verification_task()
    
    # Create the crew with only the engineer
    # Create Ollama LLM instance directly
    ollama_llm = OllamaLLM(
        model="ollama/gpt-oss:20b",
        url="http://localhost:11434",
        verbose=True
    )
    
    crew = Crew(
        agents=[engineer],
        tasks=[file_creation_task, verification_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
        llm=ollama_llm,
        temperature=0.7
    )
    
    # Run the crew
    print("🔧 Starting file creation process...")
    result = crew.kickoff()
    
    print("\n" + "=" * 50)
    print("✅ File Creation Demo Completed!")
    print("=" * 50)
    print(f"Result: {result}")
    
    # Check if demo_project was actually created
    demo_project_path = Path("demo_project")
    if demo_project_path.exists():
        print(f"\n📁 Demo project created successfully at: {demo_project_path.absolute()}")
        print("📋 Project contents:")
        for item in demo_project_path.rglob("*"):
            if item.is_file():
                print(f"  📄 {item.relative_to(demo_project_path)}")
            elif item.is_dir():
                print(f"  📁 {item.relative_to(demo_project_path)}/")
    else:
        print("\n❌ Demo project was not created!")
    
    return result

if __name__ == "__main__":
    main() 