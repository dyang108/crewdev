import subprocess
import threading
import time
import signal
import os
import psutil
from typing import Dict, List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class RunCommandInput(BaseModel):
    """Input schema for RunCommandTool."""
    command: str = Field(..., description="Command to execute")
    working_directory: str = Field(default=".", description="Working directory for the command")
    timeout: int = Field(default=300, description="Timeout in seconds")


class StartServerInput(BaseModel):
    """Input schema for StartServerTool."""
    command: str = Field(..., description="Command to start the server")
    working_directory: str = Field(default=".", description="Working directory for the server")
    port: Optional[int] = Field(default=None, description="Port the server will run on")
    server_name: str = Field(default="server", description="Name to identify this server")


class StopServerInput(BaseModel):
    """Input schema for StopServerTool."""
    server_name: str = Field(..., description="Name of the server to stop")


class ListServersInput(BaseModel):
    """Input schema for ListServersTool."""
    pass


class CheckPortInput(BaseModel):
    """Input schema for CheckPortTool."""
    port: int = Field(..., description="Port number to check")


class RunCommandTool(BaseTool):
    name: str = "run_command"
    description: str = "Execute a shell command and return the output"
    args_schema: type[BaseModel] = RunCommandInput

    def _run(self, command: str, working_directory: str = ".", timeout: int = 300) -> str:
        try:
            # Change to working directory
            original_dir = os.getcwd()
            os.chdir(working_directory)
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Return to original directory
            os.chdir(original_dir)
            
            output = f"Command: {command}\n"
            output += f"Working Directory: {working_directory}\n"
            output += f"Return Code: {result.returncode}\n"
            
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
            
            return output
        except subprocess.TimeoutExpired:
            return f"Error: Command '{command}' timed out after {timeout} seconds"
        except Exception as e:
            return f"Error executing command '{command}': {str(e)}"


class StartServerTool(BaseTool):
    name: str = "start_server"
    description: str = "Start a server process in the background"
    args_schema: type[BaseModel] = StartServerInput
    
    # Class variable to track running servers
    _servers: Dict[str, subprocess.Popen] = {}

    def _run(self, command: str, working_directory: str = ".", port: Optional[int] = None, server_name: str = "server") -> str:
        try:
            # Check if server is already running
            if server_name in self._servers:
                return f"Error: Server '{server_name}' is already running"
            
            # Change to working directory
            original_dir = os.getcwd()
            os.chdir(working_directory)
            
            # Start server process
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid  # Create new process group
            )
            
            # Return to original directory
            os.chdir(original_dir)
            
            # Store server process
            self._servers[server_name] = process
            
            output = f"Started server '{server_name}' with PID {process.pid}\n"
            output += f"Command: {command}\n"
            output += f"Working Directory: {working_directory}\n"
            
            if port:
                output += f"Port: {port}\n"
            
            # Wait a moment to check if server started successfully
            time.sleep(2)
            if process.poll() is None:
                output += "✅ Server is running"
            else:
                output += "❌ Server failed to start"
            
            return output
        except Exception as e:
            return f"Error starting server '{server_name}': {str(e)}"


class StopServerTool(BaseTool):
    name: str = "stop_server"
    description: str = "Stop a running server process"
    args_schema: type[BaseModel] = StopServerInput

    def _run(self, server_name: str) -> str:
        try:
            if server_name not in StartServerTool._servers:
                return f"Error: Server '{server_name}' is not running"
            
            process = StartServerTool._servers[server_name]
            
            # Try graceful shutdown first
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait(timeout=10)
                output = f"✅ Server '{server_name}' stopped gracefully"
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                output = f"⚠️ Server '{server_name}' force stopped"
            except Exception:
                # Fallback to process.kill()
                process.kill()
                output = f"⚠️ Server '{server_name}' killed"
            
            # Remove from tracking
            del StartServerTool._servers[server_name]
            
            return output
        except Exception as e:
            return f"Error stopping server '{server_name}': {str(e)}"


class ListServersTool(BaseTool):
    name: str = "list_servers"
    description: str = "List all running servers"
    args_schema: type[BaseModel] = ListServersInput

    def _run(self) -> str:
        try:
            if not StartServerTool._servers:
                return "No servers are currently running"
            
            output = "Running servers:\n"
            for name, process in StartServerTool._servers.items():
                status = "🟢 Running" if process.poll() is None else "🔴 Stopped"
                output += f"  {name}: PID {process.pid} - {status}\n"
            
            return output
        except Exception as e:
            return f"Error listing servers: {str(e)}"


class CheckPortTool(BaseTool):
    name: str = "check_port"
    description: str = "Check if a port is in use"
    args_schema: type[BaseModel] = CheckPortInput

    def _run(self, port: int) -> str:
        try:
            import socket
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    return f"Port {port} is in use"
                else:
                    return f"Port {port} is available"
        except Exception as e:
            return f"Error checking port {port}: {str(e)}"


class InstallPackageTool(BaseTool):
    name: str = "install_package"
    description: str = "Install a Python package using pip"
    args_schema: type[BaseModel] = RunCommandInput

    def _run(self, command: str, working_directory: str = ".", timeout: int = 300) -> str:
        # Override command to ensure it's a pip install command
        if not command.startswith("pip install"):
            return "Error: This tool is for pip install commands only"
        
        return RunCommandTool()._run(command, working_directory, timeout)


class RunPythonScriptTool(BaseTool):
    name: str = "run_python_script"
    description: str = "Run a Python script"
    args_schema: type[BaseModel] = RunCommandInput

    def _run(self, command: str, working_directory: str = ".", timeout: int = 300) -> str:
        # Ensure it's a Python command
        if not command.startswith("python") and not command.startswith("python3"):
            command = f"python {command}"
        
        return RunCommandTool()._run(command, working_directory, timeout) 