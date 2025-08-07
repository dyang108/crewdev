from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from langchain_ollama import OllamaLLM

# Import all our custom tools
from crewdev.tools import (
    # File tools
    ReadFileTool, WriteFileTool, ListDirectoryTool, CreateDirectoryTool, DeleteFileTool, FileExistsTool,
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
            step_callback=lambda x: print(f"🤔 Staff Engineer thinking: {x}"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
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
            step_callback=lambda x: print(f"🎨 Frontend Engineer thinking: {x}"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
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
            step_callback=lambda x: print(f"⚙️ Backend Engineer thinking: {x}"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
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
            step_callback=lambda x: print(f"🚀 DevOps Engineer thinking: {x}"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools
                ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
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
            step_callback=lambda x: print(f"🤨 Technical Skeptic thinking: {x}"),
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
            step_callback=lambda x: print(f"📊 Product Manager thinking: {x}"),
            memory=True,
            llm=gptoss,
            tools=[
                # File management tools for documentation
                ReadFileTool(), WriteFileTool(), ListDirectoryTool(), CreateDirectoryTool(),
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
            callback=lambda x: print(f"📈 Market Research Task completed: {x}")
        )

    @task
    def technical_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_architecture_task'], # type: ignore[index]
            callback=lambda x: print(f"🏗️ Technical Architecture Task completed: {x}")
        )

    @task
    def frontend_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_implementation_task'], # type: ignore[index]
            callback=lambda x: print(f"🎨 Frontend Implementation Task completed: {x}")
        )

    @task
    def backend_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_implementation_task'], # type: ignore[index]
            callback=lambda x: print(f"⚙️ Backend Implementation Task completed: {x}")
        )

    @task
    def devops_setup_task(self) -> Task:
        return Task(
            config=self.tasks_config['devops_setup_task'], # type: ignore[index]
            callback=lambda x: print(f"🚀 DevOps Setup Task completed: {x}")
        )

    @task
    def technical_skeptic_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_skeptic_review_task'], # type: ignore[index]
            callback=lambda x: print(f"🤨 Technical Skeptic Review Task completed: {x}")
        )

    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task'], # type: ignore[index]
            callback=lambda x: print(f"🔍 Code Review Task completed: {x}")
        )

    @task
    def final_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_integration_task'], # type: ignore[index]
            callback=lambda x: print(f"🎯 Final Integration Task completed: {x}"),
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

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            llm=ollama_llm,
            temperature=0.7
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
