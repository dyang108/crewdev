# CrewDev Tools Guide

Your software engineering team now has access to powerful tools for local development, code writing, and server management. This guide explains all available tools and how they work.

## 🛠️ Available Tools

### 📁 File System Tools

#### `read_file`
- **Purpose**: Read the contents of any file from the local filesystem
- **Use Case**: Review existing code, read configuration files, check documentation
- **Example**: Read a Python file to understand its structure

#### `write_file`
- **Purpose**: Write content to files, creating directories if needed
- **Use Case**: Create new code files, write documentation, generate configuration files
- **Example**: Create a new Python module or update existing files

#### `list_directory`
- **Purpose**: List contents of directories to understand project structure
- **Use Case**: Explore project layout, find specific files, understand organization
- **Example**: List files in a project directory to see what's already there

#### `create_directory`
- **Purpose**: Create new directories for organizing code
- **Use Case**: Set up project structure, create subdirectories for modules
- **Example**: Create `src/`, `tests/`, `docs/` directories

#### `delete_file`
- **Purpose**: Remove files from the filesystem
- **Use Case**: Clean up temporary files, remove outdated code
- **Example**: Delete test files or temporary artifacts

#### `file_exists`
- **Purpose**: Check if a file exists before attempting operations
- **Use Case**: Validate file presence, avoid overwriting important files
- **Example**: Check if a configuration file exists before creating it

### ⚡ Execution & Server Management Tools

#### `run_command`
- **Purpose**: Execute shell commands and return output
- **Use Case**: Run build scripts, execute tests, run package managers
- **Example**: Run `npm install` or `python -m pytest`

#### `start_server`
- **Purpose**: Start server processes in the background
- **Use Case**: Launch development servers, start API servers, run web applications
- **Example**: Start a Flask app on port 5000 or a React dev server

#### `stop_server`
- **Purpose**: Gracefully stop running server processes
- **Use Case**: Shutdown development servers, clean up processes
- **Example**: Stop a running API server before restarting it

#### `list_servers`
- **Purpose**: Show all currently running servers
- **Use Case**: Monitor active processes, check server status
- **Example**: See which development servers are currently active

#### `check_port`
- **Purpose**: Check if a port is available or in use
- **Use Case**: Avoid port conflicts, verify server status
- **Example**: Check if port 3000 is available before starting a React app

#### `install_package`
- **Purpose**: Install Python packages using pip
- **Use Case**: Add dependencies to Python projects
- **Example**: Install Flask, Django, or other Python packages

#### `run_python_script`
- **Purpose**: Execute Python scripts with proper environment
- **Use Case**: Run Python applications, execute scripts
- **Example**: Run a Flask application or test suite

### 🏗️ Development Environment Tools

#### `create_project`
- **Purpose**: Create new projects with proper structure
- **Use Case**: Initialize new Python, Node.js, or React projects
- **Example**: Create a new Flask API project with proper directory structure

#### `create_requirements`
- **Purpose**: Generate Python requirements.txt files
- **Use Case**: Define Python project dependencies
- **Example**: Create requirements.txt with Flask, SQLAlchemy, pytest

#### `create_package_json`
- **Purpose**: Generate Node.js package.json files
- **Use Case**: Set up Node.js/React projects with dependencies
- **Example**: Create package.json for a React frontend with necessary packages

#### `create_dockerfile`
- **Purpose**: Generate Dockerfiles for containerization
- **Use Case**: Containerize applications for deployment
- **Example**: Create a Dockerfile for a Python Flask application

#### `create_docker_compose`
- **Purpose**: Generate docker-compose.yml for multi-service applications
- **Use Case**: Set up development environments with multiple services
- **Example**: Create docker-compose.yml for a full-stack app with frontend, backend, and database

#### `create_gitignore`
- **Purpose**: Generate appropriate .gitignore files
- **Use Case**: Exclude unnecessary files from version control
- **Example**: Create .gitignore for Python projects with virtual environments

## 🎯 Tool Assignment by Role

### Staff Engineer
- **File Management**: Full access to read/write files and directories
- **Project Creation**: Can create new projects and set up basic structure
- **Architecture Tools**: Docker and Docker Compose creation
- **Execution**: Basic command execution and port checking

### Frontend Engineer
- **File Management**: Full access to read/write files
- **Frontend Tools**: Package.json creation, Node.js project setup
- **Server Management**: Can start/stop development servers
- **Package Management**: Install npm packages

### Backend Engineer
- **File Management**: Full access to read/write files
- **Backend Tools**: Requirements.txt creation, Python project setup
- **Server Management**: Can start/stop API servers
- **Python Tools**: Run Python scripts, install pip packages
- **Containerization**: Create Dockerfiles for backend services

### DevOps Engineer
- **File Management**: Full access to read/write files
- **DevOps Tools**: Docker, Docker Compose, gitignore creation
- **Server Management**: Full server lifecycle management
- **Package Management**: Install system and Python packages

### Technical Skeptic
- **Code Review Tools**: Read files, check file existence, list directories
- **Testing Tools**: Run commands and Python scripts for testing
- **Analysis Tools**: Check ports and system status

### Product Manager
- **Documentation Tools**: Read/write files for documentation
- **Project Setup**: Create basic project structure
- **Basic Execution**: Run commands for project management

## 🚀 Example Workflows

### Creating a Full-Stack Application

1. **Product Manager** uses `create_project` to set up project structure
2. **Staff Engineer** uses `create_docker_compose` for multi-service setup
3. **Backend Engineer** uses `write_file` to create API code and `create_requirements` for dependencies
4. **Frontend Engineer** uses `create_package_json` and `write_file` for React components
5. **DevOps Engineer** uses `create_dockerfile` for each service
6. **Technical Skeptic** uses `read_file` to review code and `run_command` to test

### Starting a Development Environment

1. **Backend Engineer** uses `start_server` to launch API server
2. **Frontend Engineer** uses `start_server` to launch React dev server
3. **DevOps Engineer** uses `list_servers` to monitor running services
4. **Technical Skeptic** uses `check_port` to verify server availability

### Code Review Process

1. **Technical Skeptic** uses `list_directory` to explore project structure
2. Uses `read_file` to examine specific code files
3. Uses `run_command` to execute tests
4. Uses `write_file` to suggest improvements

## ⚠️ Safety Considerations

- **File Operations**: Tools can read and write any file on the system
- **Command Execution**: Commands run with the same permissions as the user
- **Server Management**: Servers run in the background and need to be properly stopped
- **Port Conflicts**: Always check port availability before starting servers

## 🔧 Installation

The tools are automatically available to your crew. Make sure you have the required dependencies:

```bash
pip install -e .
```

## 📝 Usage Tips

1. **Always check file existence** before writing to avoid overwriting important files
2. **Use descriptive server names** when starting servers for easy management
3. **Check port availability** before starting servers to avoid conflicts
4. **Stop servers properly** using the stop_server tool to avoid orphaned processes
5. **Use the right tool for the job** - each tool is optimized for specific tasks

## 🎉 Getting Started

Your crew can now:
- ✅ Write and read code files locally
- ✅ Create complete project structures
- ✅ Start and manage development servers
- ✅ Install and manage dependencies
- ✅ Containerize applications with Docker
- ✅ Execute commands and run tests
- ✅ Review and analyze code

The tools are designed to work together seamlessly, allowing your crew to build complete applications from scratch and manage the entire development lifecycle! 