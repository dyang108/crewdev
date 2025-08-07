from typing import Dict, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json

class DynamicTaskTool(BaseTool):
    """
    Tool for agents to request dynamic task assignment and report task completion.
    """
    
    name: str = "dynamic_task_tool"
    description: str = """
    Use this tool to:
    1. Request the next task based on current project state
    2. Report task completion
    3. Add bugs or feature requests to the project
    4. Get current project status
    
    Available actions:
    - get_next_task: Request the next task for the current agent
    - report_completion: Report that a task has been completed
    - add_bug: Add a new bug to the project
    - add_feature: Add a new feature request to the project
    - get_status: Get current project status
    """
    
    def __init__(self, task_manager):
        super().__init__()
        # Store task manager as a private attribute to avoid Pydantic issues
        self._task_manager = task_manager
    
    def _run(self, action: str, **kwargs) -> str:
        """
        Execute the requested action.
        
        Args:
            action: The action to perform (get_next_task, report_completion, add_bug, add_feature, get_status)
            **kwargs: Additional parameters for the action
        """
        try:
            if action == "get_next_task":
                return self._get_next_task(**kwargs)
            elif action == "report_completion":
                return self._report_completion(**kwargs)
            elif action == "add_bug":
                return self._add_bug(**kwargs)
            elif action == "add_feature":
                return self._add_feature(**kwargs)
            elif action == "get_status":
                return self._get_status()
            else:
                return f"Unknown action: {action}. Available actions: get_next_task, report_completion, add_bug, add_feature, get_status"
        except Exception as e:
            return f"Error executing action '{action}': {str(e)}"
    
    def _get_next_task(self, agent_name: str) -> str:
        """Get the next task for the specified agent."""
        task = self._task_manager.determine_next_task(agent_name)
        if task:
            return f"Next task assigned: {task.description}\nExpected output: {task.expected_output}"
        else:
            return "No specific task needed at this time. Consider reporting completion of current work or requesting next steps."
    
    def _report_completion(self, task_name: str, output: str) -> str:
        """Report that a task has been completed."""
        self._task_manager.mark_task_completed(task_name, output)
        return f"Task '{task_name}' marked as completed. Output: {output[:100]}..."
    
    def _add_bug(self, description: str, priority: str = "medium") -> str:
        """Add a new bug to the project."""
        self._task_manager.add_bug(description, priority)
        return f"Bug added to project: {description} (Priority: {priority})"
    
    def _add_feature(self, description: str, priority: str = "medium") -> str:
        """Add a new feature request to the project."""
        self._task_manager.add_feature(description, priority)
        return f"Feature request added to project: {description} (Priority: {priority})"
    
    def _get_status(self) -> str:
        """Get current project status."""
        status = self._task_manager.get_project_status()
        return json.dumps(status, indent=2)

class TaskCompletionTool(BaseTool):
    """
    Tool for agents to report task completion and request next steps.
    """
    
    name: str = "task_completion_tool"
    description: str = """
    Use this tool to report task completion and automatically request the next appropriate task.
    This helps maintain project flow and ensures tasks are assigned based on current needs.
    """
    
    def __init__(self, task_manager):
        super().__init__()
        # Store task manager as a private attribute to avoid Pydantic issues
        self._task_manager = task_manager
    
    def _run(self, task_name: str, output: str, agent_name: str) -> str:
        """
        Report task completion and get next task.
        
        Args:
            task_name: Name of the completed task
            output: Output/result of the completed task
            agent_name: Name of the agent that completed the task
        """
        try:
            # Report completion
            self._task_manager.mark_task_completed(task_name, output)
            
            # Get next task
            next_task = self._task_manager.determine_next_task(agent_name)
            
            if next_task:
                return f"Task '{task_name}' completed successfully!\n\nNext task: {next_task.description}\nExpected output: {next_task.expected_output}"
            else:
                return f"Task '{task_name}' completed successfully!\n\nNo immediate next task. Consider:\n- Reporting bugs or issues found\n- Requesting new features\n- Asking for next steps from the product manager"
        except Exception as e:
            return f"Error reporting task completion: {str(e)}"

class BugReportTool(BaseTool):
    """
    Tool for agents to report bugs and automatically assign them to appropriate engineers.
    """
    
    name: str = "bug_report_tool"
    description: str = """
    Use this tool to report bugs found during development or testing.
    The bug will be automatically added to the project and can be assigned to appropriate engineers.
    """
    
    def __init__(self, task_manager):
        super().__init__()
        # Store task manager as a private attribute to avoid Pydantic issues
        self._task_manager = task_manager
    
    def _run(self, description: str, priority: str = "medium", component: str = "unknown") -> str:
        """
        Report a bug and add it to the project.
        
        Args:
            description: Description of the bug
            priority: Priority level (low, medium, high, critical)
            component: Component where the bug was found (frontend, backend, etc.)
        """
        try:
            self._task_manager.add_bug(description, priority)
            
            # Determine which engineer should handle this bug
            if component.lower() in ['frontend', 'ui', 'react', 'typescript']:
                assigned_agent = "senior_engineer_frontend"
            elif component.lower() in ['backend', 'api', 'server', 'python', 'nodejs']:
                assigned_agent = "senior_engineer_backend"
            else:
                assigned_agent = "staff_engineer"  # Default to staff engineer for unclear cases
            
            return f"Bug reported and added to project:\nDescription: {description}\nPriority: {priority}\nComponent: {component}\nRecommended assignment: {assigned_agent}"
        except Exception as e:
            return f"Error reporting bug: {str(e)}"

class FeatureRequestTool(BaseTool):
    """
    Tool for agents to request new features and automatically assign them to appropriate engineers.
    """
    
    name: str = "feature_request_tool"
    description: str = """
    Use this tool to request new features or enhancements.
    The feature will be automatically added to the project and can be assigned to appropriate engineers.
    """
    
    def __init__(self, task_manager):
        super().__init__()
        # Store task manager as a private attribute to avoid Pydantic issues
        self._task_manager = task_manager
    
    def _run(self, description: str, priority: str = "medium", component: str = "unknown") -> str:
        """
        Request a new feature and add it to the project.
        
        Args:
            description: Description of the feature
            priority: Priority level (low, medium, high, critical)
            component: Component where the feature should be implemented (frontend, backend, etc.)
        """
        try:
            self._task_manager.add_feature(description, priority)
            
            # Determine which engineer should handle this feature
            if component.lower() in ['frontend', 'ui', 'react', 'typescript']:
                assigned_agent = "senior_engineer_frontend"
            elif component.lower() in ['backend', 'api', 'server', 'python', 'nodejs']:
                assigned_agent = "senior_engineer_backend"
            else:
                assigned_agent = "staff_engineer"  # Default to staff engineer for unclear cases
            
            return f"Feature request added to project:\nDescription: {description}\nPriority: {priority}\nComponent: {component}\nRecommended assignment: {assigned_agent}"
        except Exception as e:
            return f"Error requesting feature: {str(e)}" 