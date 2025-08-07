from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Set environment variable to use Ollama
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

@CrewBase
class SoftwareEngineeringTeam():
    """Software Engineering Team Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

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
            memory=True
        )

    @agent
    def senior_engineer_frontend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_frontend'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=lambda x: print(f"🎨 Frontend Engineer thinking: {x}"),
            memory=True
        )

    @agent
    def senior_engineer_backend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_backend'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=lambda x: print(f"⚙️ Backend Engineer thinking: {x}"),
            memory=True
        )

    @agent
    def senior_engineer_devops(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_devops'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=lambda x: print(f"🚀 DevOps Engineer thinking: {x}"),
            memory=True
        )

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['product_manager'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            step_callback=lambda x: print(f"📊 Product Manager thinking: {x}"),
            memory=True
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

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
