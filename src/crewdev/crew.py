from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
import sys
import logging
from langchain_ollama import OllamaLLM

# Import all our custom tools
from crewdev.tools import (
    # File tools
    ReadFileTool, WriteFileTool, FileWriterTool, ListDirectoryTool, CreateDirectoryTool, DeleteFileTool, FileExistsTool,
    # Execution tools
    RunCommandTool, StartServerTool, StopServerTool, ListServersTool, CheckPortTool, InstallPackageTool, RunPythonScriptTool,
    # Dev tools
    CreateProjectTool, CreateRequirementsTool, CreatePackageJsonTool, CreateDockerfileTool, CreateDockerComposeTool, CreateGitignoreTool,
    # Dynamic task tools
    DynamicTaskTool, TaskCompletionTool, BugReportTool, FeatureRequestTool
)

# Import dynamic task manager
from crewdev.dynamic_task_manager import DynamicTaskManager
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
os.environ["LITELLM_PROVIDER"] = "ollama"

# Set environment variables to use Ollama
# For Ollama with CrewAI, use only OpenAI-compatible environment variables
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Dummy key for Ollama
# Remove OLLAMA_BASE_URL - CrewAI uses Langchain which expects OpenAI-style APIs
os.environ["LLM_MODEL"] = "ollama/gpt-oss:20b"  # Using Mistral with ollama/ prefix
# Additional environment variables to ensure correct model usage
os.environ["DEFAULT_MODEL"] = "ollama/gpt-oss:20b"
os.environ["MODEL_NAME"] = "ollama/gpt-oss:20b"

gptoss = OllamaLLM(
    model="ollama/gpt-oss:20b",
    url="http://localhost:11434",
    provider="ollama",
)


@CrewBase
class SoftwareEngineeringTeam():
    """Software Engineering Team Crew with Dynamic Task Assignment"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()
        # Initialize dynamic task manager
        self.task_manager = DynamicTaskManager()
        
        # Create dynamic task tools
        self.dynamic_task_tool = DynamicTaskTool(self.task_manager)
        self.task_completion_tool = TaskCompletionTool(self.task_manager)
        self.bug_report_tool = BugReportTool(self.task_manager)
        self.feature_request_tool = FeatureRequestTool(self.task_manager)

        # Track task start/end to log clearly at boundaries
        self._task_order = [
            ("📈 Market Research Task", "product_manager"),
            ("🏗️ Technical Architecture Task", "staff_engineer"),
            ("🎨 Frontend Implementation Task", "senior_engineer_frontend"),
            ("⚙️ Backend Implementation Task", "senior_engineer_backend"),
            ("🚀 DevOps Setup Task", "senior_engineer_devops"),
            ("🤨 Technical Skeptic Review Task", "technical_skeptic"),
            ("🔍 Code Review Task", "staff_engineer"),
            ("🎯 Final Integration Task", "product_manager"),
        ]
        self._started_task_count = 0
        self._completed_task_count = 0

    def _pause_prompt(self, task_name: str) -> None:
        """Offer a short window to pause after a task; continue automatically if no input."""
        try:
            should_pause = os.environ.get("CREWDEV_PAUSE_BETWEEN_TASKS", "0").strip() in ("1", "true", "True")
            if not should_pause:
                return

            project_name = os.environ.get("CREWDEV_PROJECT_NAME", "<unknown>")
            project_path = f"projects/{project_name}" if project_name else "projects/<unknown>"
            print("\n---")
            print(f"After {task_name}.")
            print(f"Type anything and press Enter within 10s to PAUSE, otherwise it will continue.")
            print(f"Inspect path: {project_path}")
            timeout_secs = 10
            try:
                timeout_env = os.environ.get("CREWDEV_PAUSE_WINDOW_SECS")
                if timeout_env:
                    timeout_secs = max(1, int(timeout_env))
            except Exception:
                pass

            user_line = self._timed_input(f"pause?> ", timeout_secs)
            if user_line is not None:
                print("\nPaused. When ready, press Enter to continue...")
                try:
                    input()
                except Exception:
                    pass
            else:
                print("Continuing...")
            print("---\n")
        except Exception:
            # Never block the run if pause prompt fails
            pass

    def _make_task_callback(self, label: str):
        """Create a task callback that logs completion and optionally pauses."""
        def _callback(result: str) -> None:
            print(f"{label} completed: {result}")
            try:
                logging.info(f"{label} completed")
            except Exception:
                pass
            # Mark completion so the next agent step can announce the next task start
            try:
                self._completed_task_count += 1
                # Immediately announce and mark the start of the next task for visibility
                if self._completed_task_count < len(self._task_order):
                    next_label, _ = self._task_order[self._completed_task_count]
                    print(f"▶️ Starting {next_label} …")
                    try:
                        logging.info(f"Starting {next_label}")
                    except Exception:
                        pass
                    # Keep counters aligned so step callbacks don't duplicate
                    if self._started_task_count < self._completed_task_count + 1:
                        self._started_task_count = self._completed_task_count + 1
            except Exception:
                pass
            self._pause_prompt(label)
        return _callback

    def _make_step_callback(self, agent_key: str, prefix: str):
        """Create an agent step callback that logs task start once per task."""
        def _callback(message: str) -> None:
            try:
                if self._started_task_count == self._completed_task_count and self._started_task_count < len(self._task_order):
                    next_label, _ = self._task_order[self._started_task_count]
                    print(f"▶️ Starting {next_label} …")
                    try:
                        logging.info(f"Starting {next_label}")
                    except Exception:
                        pass
                    self._started_task_count += 1
            except Exception:
                pass
            print(f"{prefix} {message}")
        return _callback

    def _timed_input(self, prompt: str, timeout_secs: int):
        """Read a line from stdin with timeout. Returns the line or None on timeout."""
        try:
            print(prompt, end='', flush=True)
            try:
                import select
            except Exception:
                return None
            rlist, _, _ = select.select([sys.stdin], [], [], float(timeout_secs))
            if rlist:
                return sys.stdin.readline().rstrip('\n')
            print("")
            return None
        except Exception:
            return None

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def staff_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['staff_engineer'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("staff_engineer", "🤔 Staff Engineer thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), FileWriterTool(), ListDirectoryTool(), CreateDirectoryTool(), DeleteFileTool(), FileExistsTool(),
                # Project creation tools
                CreateProjectTool(), CreateRequirementsTool(), CreateGitignoreTool(),
                # Execution tools
                RunCommandTool(), CheckPortTool(),
                # Development tools
                CreateDockerfileTool(), CreateDockerComposeTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    @agent
    def senior_engineer_frontend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_frontend'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("senior_engineer_frontend", "🎨 Frontend Engineer thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), FileWriterTool(), ListDirectoryTool(), CreateDirectoryTool(), DeleteFileTool(), FileExistsTool(),
                # Frontend-specific tools
                CreatePackageJsonTool(), CreateGitignoreTool(),
                # Execution tools
                RunCommandTool(), StartServerTool(), StopServerTool(), ListServersTool(), CheckPortTool(),
                # Package management
                InstallPackageTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    @agent
    def senior_engineer_backend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_backend'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("senior_engineer_backend", "⚙️ Backend Engineer thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), FileWriterTool(), ListDirectoryTool(), CreateDirectoryTool(), DeleteFileTool(), FileExistsTool(),
                # Backend-specific tools
                CreateRequirementsTool(), CreateGitignoreTool(),
                # Execution tools
                RunCommandTool(), StartServerTool(), StopServerTool(), ListServersTool(), CheckPortTool(),
                # Python-specific tools
                RunPythonScriptTool(), InstallPackageTool(),
                # Development tools
                CreateDockerfileTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    @agent
    def senior_engineer_devops(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_devops'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("senior_engineer_devops", "🚀 DevOps Engineer thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), FileWriterTool(), ListDirectoryTool(), CreateDirectoryTool(), DeleteFileTool(), FileExistsTool(),
                # DevOps-specific tools
                CreateDockerfileTool(), CreateDockerComposeTool(), CreateGitignoreTool(),
                # Execution tools
                RunCommandTool(), StartServerTool(), StopServerTool(), ListServersTool(), CheckPortTool(),
                # Package management
                InstallPackageTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    @agent
    def technical_skeptic(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_skeptic'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("technical_skeptic", "🤨 Technical Skeptic thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools for code review
                ReadFileTool(), ListDirectoryTool(), FileExistsTool(),
                # Execution tools for testing
                RunCommandTool(), RunPythonScriptTool(),
                # Development tools for analysis
                CheckPortTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['product_manager'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=self._make_step_callback("product_manager", "📊 Product Manager thinking:"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools for documentation
                ReadFileTool(), WriteFileTool(), FileWriterTool(), ListDirectoryTool(), CreateDirectoryTool(),
                # Project creation tools
                CreateProjectTool(), CreateGitignoreTool(),
                # Basic execution tools
                RunCommandTool(),
                # Dynamic task tools
                self.dynamic_task_tool, self.task_completion_tool, self.bug_report_tool, self.feature_request_tool
            ]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_task'], # type: ignore[index]
            callback=self._make_task_callback("📈 Market Research Task")
        )

    @task
    def technical_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_architecture_task'], # type: ignore[index]
            callback=self._make_task_callback("🏗️ Technical Architecture Task")
        )

    @task
    def frontend_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_implementation_task'], # type: ignore[index]
            callback=self._make_task_callback("🎨 Frontend Implementation Task")
        )

    @task
    def backend_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_implementation_task'], # type: ignore[index]
            callback=self._make_task_callback("⚙️ Backend Implementation Task")
        )

    @task
    def devops_setup_task(self) -> Task:
        return Task(
            config=self.tasks_config['devops_setup_task'], # type: ignore[index]
            callback=self._make_task_callback("🚀 DevOps Setup Task")
        )

    @task
    def technical_skeptic_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_skeptic_review_task'], # type: ignore[index]
            callback=self._make_task_callback("🤨 Technical Skeptic Review Task")
        )

    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task'], # type: ignore[index]
            callback=self._make_task_callback("🔍 Code Review Task")
        )

    @task
    def final_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_integration_task'], # type: ignore[index]
            callback=self._make_task_callback("🎯 Final Integration Task"),
            output_file='project_deliverables.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Software Engineering Team crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # Create Ollama LLM instance directly
        ollama_llm = OllamaLLM(
            model="ollama/gpt-oss:20b",
            url="http://localhost:11434",
            verbose=True
        )

        # Optionally limit number of tasks for faster debug iterations
        try:
            import os
            limit_env = os.environ.get("CREWDEV_TASK_LIMIT")
            if limit_env is not None:
                limit = max(1, int(limit_env))
                limited_tasks = self.tasks[:limit]
            else:
                limited_tasks = self.tasks
        except Exception:
            limited_tasks = self.tasks

        print("Planned tasks:")
        for t in limited_tasks:
            try:
                print(f" - {t.description.splitlines()[0][:100]}")
            except Exception:
                pass

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=limited_tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            llm=ollama_llm,
            temperature=0.7
        )
