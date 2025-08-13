# Engineer File Creation Demo Scripts

This directory contains scripts that demonstrate using only an engineer agent to create files and verify they are actually created in the filesystem.

## Scripts Overview

### 1. `direct_file_creation_demo.py` - Direct Tool Usage (Recommended)
A script that directly uses the file creation tools without LLM dependency to demonstrate file creation capabilities.

**What it does:**
- Creates a `direct_demo` directory with basic files
- Creates a `demo_project` directory with complete Python project structure
- Uses file creation tools directly (no LLM required)
- Verifies all files exist and contain expected content
- Demonstrates that file creation tools work independently

**Usage:**
```bash
python direct_file_creation_demo.py
```

### 2. `simple_engineer_demo.py` - Simple File Creation (LLM-based)
A basic script that creates a few test files using an engineer agent with LLM.

**What it does:**
- Creates a `test_files` directory
- Creates `hello.txt` with "Hello, World!" content
- Creates `test.py` with a simple Python function
- Creates `data.json` with sample JSON data
- Verifies all files exist and contain expected content

**Usage:**
```bash
python simple_engineer_demo.py
```

### 3. `engineer_file_creation_demo.py` - Complete Project Creation (LLM-based)
A comprehensive script that creates a complete Python project structure using an engineer agent.

**What it does:**
- Creates a `demo_project` directory with full project structure
- Creates `main.py` with a Hello World application
- Creates `requirements.txt` with dependencies
- Creates `README.md` with documentation
- Creates `.gitignore` with Python ignores
- Creates `test_main.py` with unit tests
- Creates `Dockerfile` for containerization
- Creates `docker-compose.yml` for deployment
- Verifies all files were created successfully

**Usage:**
```bash
python engineer_file_creation_demo.py
```

## Prerequisites

1. **Ollama Setup**: Make sure Ollama is running with the required model:
   ```bash
   # Install and start Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama serve
   
   # Pull the required model
   ollama pull gpt-oss:20b
   ```

2. **Python Dependencies**: Install the required packages:
   ```bash
   pip install crewai langchain-ollama
   ```

3. **Project Structure**: Make sure you're in the root directory of the crewdev project so the tools can be imported correctly.

## Key Features

### File Creation Verification
Both scripts include built-in verification to ensure files are actually created:
- Uses file tools to read back created files
- Lists directory contents to confirm file existence
- Checks file content matches expectations
- Provides detailed reports of what was created

### Engineer-Only Approach
These scripts use only engineer agents (no product managers, designers, etc.) to focus specifically on:
- File creation and management
- Code generation
- Project structure setup
- File verification and testing

### Tool Integration
The scripts use the custom tools from the crewdev project:
- `ReadFileTool` - Read file contents
- `WriteFileTool` - Write content to files
- `ListDirectoryTool` - List directory contents
- `CreateDirectoryTool` - Create directories
- `CreateProjectTool` - Create project structures
- And more...

## Expected Output

### Direct Demo (Recommended)
After running `direct_file_creation_demo.py`, you should see:
```
✅ All demos completed successfully!
📁 Check the created directories:
   - direct_demo/ (basic files)
   - demo_project/ (complete project structure)
```

The script will create:
- `direct_demo/` with `hello.txt`, `test.py`, and `data.json`
- `demo_project/` with complete Python project structure including `requirements.txt`, `Dockerfile`, etc.

### LLM-based Demos
After running `simple_engineer_demo.py` or `engineer_file_creation_demo.py`, you should see:
```
📁 Test files created at: /path/to/test_files
📋 Files created:
  📄 hello.txt
     Content: Hello, World!
  📄 test.py
     Content: def greet(name):...
  📄 data.json
     Content: {"name": "test", "value": 42}...
```

**Note:** The LLM-based demos require Ollama to be running and may fail if there are connection issues.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the project root directory
2. **Ollama Connection**: Ensure Ollama is running on `http://localhost:11434`
3. **Model Not Found**: Make sure you've pulled the `gpt-oss:20b` model
4. **Permission Errors**: Ensure you have write permissions in the current directory

### Debug Mode
Both scripts run in verbose mode by default, so you'll see detailed output of what the engineer agent is thinking and doing.

## Customization

You can easily modify these scripts to:
- Create different types of files
- Use different project structures
- Add more verification steps
- Change the engineer agent's behavior

The scripts are designed to be modular and easy to understand, making them good starting points for your own file creation workflows. 