#!/usr/bin/env python3
"""
Simple Engineer Demo - File Creation Verification (CrewAI without custom tools)

This version uses CrewAI Agents/Tasks/Crew but avoids any custom tools
to bypass the known issue with custom tools possibly returning None
responses. It asks the agent to produce a JSON manifest of files, then
the host program writes those files using standard Python I/O.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM


def ensure_directory(directory_path: Path) -> None:
    directory_path.mkdir(parents=True, exist_ok=True)


def write_text_file(file_path: Path, content: str) -> None:
    file_path.write_text(content, encoding="utf-8")


def write_json_file(file_path: Path, content: dict) -> None:
    file_path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def create_test_files(base_dir: Path) -> str:
    ensure_directory(base_dir)

    # 1) hello.txt
    hello_path = base_dir / "hello.txt"
    write_text_file(hello_path, "Hello, World!\n")

    # 2) test.py
    test_py_path = base_dir / "test.py"
    test_py_content = (
        """
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("CrewDev"))
"""
    ).lstrip()
    write_text_file(test_py_path, test_py_content)

    # 3) data.json
    data_json_path = base_dir / "data.json"
    data_json = {"project": "CrewDev", "items": [1, 2, 3], "ok": True}
    write_json_file(data_json_path, data_json)

    # Create verification summary
    created = [hello_path, test_py_path, data_json_path]
    lines = ["# File Creation Results", "", f"Base directory: {base_dir.resolve()}", ""]
    for path in created:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        preview: str
        try:
            if path.suffix == ".json":
                preview = path.read_text(encoding="utf-8").strip()[:120]
            else:
                preview = path.read_text(encoding="utf-8").strip()[:120]
        except Exception:
            preview = "<unreadable>"
        lines.append(f"- {path.name} — exists={exists}, size={size} bytes")
        lines.append(f"  Preview: {preview}")
    lines.append("")

    summary = "\n".join(lines)
    (base_dir / "file_creation_results.md").write_text(summary + "\n", encoding="utf-8")
    return summary


def main() -> None:
    print("🚀 Simple Engineer File Creation Demo (CrewAI, no custom tools)")
    print("=" * 40)

    # Configure an OpenAI-compatible client (e.g., Ollama /v1)
    os.environ.setdefault("OPENAI_API_BASE", "http://localhost:11434/v1")
    os.environ.setdefault("OPENAI_API_KEY", "ollama")
    model_name = os.getenv("LLM_MODEL", "gpt-oss:20b")

    llm = OllamaLLM(
        model="ollama/gpt-oss:20b",
        url="http://localhost:11434",
        provider="ollama",
    )
    

    # Make local tools available
    import sys as _sys
    _sys.path.append(str(Path(__file__).parent / "src"))
    from crewdev.tools import FileWriterTool, CreateDirectoryTool, ListDirectoryTool, ReadFileTool

    engineer = Agent(
        role="Software Engineer",
        goal="Use available tools to create and verify files in a local directory",
        backstory="You create files using FileWriterTool and verify them with the provided tools.",
        verbose=True,
        allow_delegation=False,
        memory=False,
        llm=llm,
        tools=[
            CreateDirectoryTool(),
            FileWriterTool(),
            ListDirectoryTool(),
            ReadFileTool(),
        ],
    )

    manifest_task = Task(
        description=(
            """
Create a directory named 'test_files' and then create the following files using the available tools:
1) hello.txt (text): content = "Hello, World!\n"
2) test.py (text):
   def greet(name: str) -> str:
       return f"Hello, {name}!"

   if __name__ == "__main__":
       print(greet("CrewDev"))
3) data.json (json): {"project": "CrewDev", "items": [1,2,3], "ok": true}

After creating files, list the directory and read each file to verify content.
Only use the available tools; keep output concise.
"""
        ),
        expected_output="A concise summary confirming file creation and verification using tools.",
        agent=engineer,
        output_file="file_creation_results.md",
    )

    crew_obj = Crew(
        agents=[engineer],
        tasks=[manifest_task],
        process=Process.sequential,
        verbose=True,
        memory=False,
        llm=llm,
        # Do not set function_calling_llm to avoid the custom tools bug path
    )

    print("🔧 Asking agent to create files using tools...")
    result = crew_obj.kickoff()
    base_dir = Path("test_files")
    print("🔧 Verifying created files...")
    summary = create_test_files(base_dir)

    print("\n" + "=" * 40)
    print("✅ Demo completed!")
    print("=" * 40)

    if base_dir.exists():
        print(f"\n📁 Test files created at: {base_dir.absolute()}")
        print("📋 Files created:")
        for file_path in base_dir.iterdir():
            if file_path.is_file():
                print(f"  📄 {file_path.name}")
                try:
                    content = file_path.read_text(encoding="utf-8").strip()
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"     Content: {preview}")
                except Exception as e:
                    print(f"     Error reading file: {e}")
    else:
        print("\n❌ Test files directory was not created!")

    # Also print a brief summary path
    results_md = base_dir / "file_creation_results.md"
    if results_md.exists():
        print(f"\n📝 Summary written to: {results_md.resolve()}")


if __name__ == "__main__":
    main()