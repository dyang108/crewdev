import os
import json
from pathlib import Path
from typing import List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    """Input schema for ReadFileTool."""
    file_path: str = Field(..., description="Path to the file to read")


class WriteFileInput(BaseModel):
    """Input schema for WriteFileTool."""
    file_path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write to the file")
    overwrite: bool = Field(default=True, description="Whether to overwrite existing file")


class ListDirectoryInput(BaseModel):
    """Input schema for ListDirectoryTool."""
    directory_path: str = Field(default=".", description="Path to the directory to list")


class CreateDirectoryInput(BaseModel):
    """Input schema for CreateDirectoryTool."""
    directory_path: str = Field(..., description="Path to the directory to create")


class DeleteFileInput(BaseModel):
    """Input schema for DeleteFileTool."""
    file_path: str = Field(..., description="Path to the file to delete")


class FileExistsInput(BaseModel):
    """Input schema for FileExistsTool."""
    file_path: str = Field(..., description="Path to the file to check")


class ReadFileTool(BaseTool):
    name: str = "read_file"
    description: str = "Read the contents of a file from the local filesystem"
    args_schema: type[BaseModel] = ReadFileInput

    def _run(self, file_path: str) -> str:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return f"Error: File '{file_path}' does not exist"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"File '{file_path}' contents:\n{content}"
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"


class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Write content to a file on the local filesystem. Creates directories if needed."
    args_schema: type[BaseModel] = WriteFileInput

    def _run(self, file_path: str, content: str, overwrite: bool = True) -> str:
        try:
            file_path = Path(file_path)
            
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and overwrite flag
            if file_path.exists() and not overwrite:
                return f"Error: File '{file_path}' already exists and overwrite=False"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote {len(content)} characters to '{file_path}'"
        except Exception as e:
            return f"Error writing file '{file_path}': {str(e)}"


class ListDirectoryTool(BaseTool):
    name: str = "list_directory"
    description: str = "List the contents of a directory on the local filesystem"
    args_schema: type[BaseModel] = ListDirectoryInput

    def _run(self, directory_path: str = ".") -> str:
        try:
            directory_path = Path(directory_path)
            if not directory_path.exists():
                return f"Error: Directory '{directory_path}' does not exist"
            
            if not directory_path.is_dir():
                return f"Error: '{directory_path}' is not a directory"
            
            items = []
            for item in directory_path.iterdir():
                item_type = "📁" if item.is_dir() else "📄"
                items.append(f"{item_type} {item.name}")
            
            if not items:
                return f"Directory '{directory_path}' is empty"
            
            return f"Contents of '{directory_path}':\n" + "\n".join(sorted(items))
        except Exception as e:
            return f"Error listing directory '{directory_path}': {str(e)}"


class CreateDirectoryTool(BaseTool):
    name: str = "create_directory"
    description: str = "Create a directory on the local filesystem"
    args_schema: type[BaseModel] = CreateDirectoryInput

    def _run(self, directory_path: str) -> str:
        try:
            directory_path = Path(directory_path)
            directory_path.mkdir(parents=True, exist_ok=True)
            return f"Successfully created directory '{directory_path}'"
        except Exception as e:
            return f"Error creating directory '{directory_path}': {str(e)}"


class DeleteFileTool(BaseTool):
    name: str = "delete_file"
    description: str = "Delete a file from the local filesystem"
    args_schema: type[BaseModel] = DeleteFileInput

    def _run(self, file_path: str) -> str:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return f"Error: File '{file_path}' does not exist"
            
            file_path.unlink()
            return f"Successfully deleted file '{file_path}'"
        except Exception as e:
            return f"Error deleting file '{file_path}': {str(e)}"


class FileExistsTool(BaseTool):
    name: str = "file_exists"
    description: str = "Check if a file exists on the local filesystem"
    args_schema: type[BaseModel] = FileExistsInput

    def _run(self, file_path: str) -> str:
        try:
            file_path = Path(file_path)
            exists = file_path.exists()
            return f"File '{file_path}' {'exists' if exists else 'does not exist'}"
        except Exception as e:
            return f"Error checking file '{file_path}': {str(e)}" 