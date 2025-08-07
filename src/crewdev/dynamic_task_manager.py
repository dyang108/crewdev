from typing import Dict, List, Optional, Any
from crewai import Task, Agent
import yaml
import os
from pathlib import Path

class DynamicTaskManager:
    """
    Manages dynamic task creation and assignment based on project state and needs.
    """
    
    def __init__(self, tasks_config_path: str = "src/crewdev/config/tasks.yaml"):
        self.tasks_config_path = tasks_config_path
        self.tasks_config = self._load_tasks_config()
        self.project_state = {}
        self.completed_tasks = []
        
    def _load_tasks_config(self) -> Dict:
        """Load task configurations from YAML file."""
        with open(self.tasks_config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def update_project_state(self, state: Dict[str, Any]):
        """Update the current project state."""
        self.project_state.update(state)
    
    def mark_task_completed(self, task_name: str, output: str):
        """Mark a task as completed with its output."""
        self.completed_tasks.append({
            'name': task_name,
            'output': output,
            'state': self.project_state.copy()
        })
    
    def create_dynamic_task(self, task_template: str, **kwargs) -> Task:
        """Create a dynamic task based on a template with specific parameters."""
        if task_template not in self.tasks_config:
            raise ValueError(f"Task template '{task_template}' not found in configuration")
        
        template = self.tasks_config[task_template]
        
        # Add default values for common template variables
        default_params = {
            'project_name': 'the project',
            'bug_description': 'the reported issue',
            'feature_description': 'the requested feature',
            'research_topic': 'the technical topic',
            'assigned_agent': 'staff_engineer'
        }
        
        # Merge default params with provided kwargs
        format_params = {**default_params, **kwargs}
        
        # Format the description and expected_output with provided kwargs
        description = template['description'].format(**format_params)
        expected_output = template['expected_output'].format(**format_params)
        
        # Determine the agent based on the template or kwargs
        agent_name = kwargs.get('agent', template.get('agent', 'product_manager'))
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent_name,
            context=f"Project State: {self.project_state}\nCompleted Tasks: {len(self.completed_tasks)}"
        )
    
    def determine_next_task(self, current_agent: str) -> Optional[Task]:
        """
        Determine what task should be done next based on current project state.
        This is the core logic for dynamic task assignment.
        """
        
        # Check if market research is needed
        if not self._has_market_research():
            return self.create_dynamic_task('market_research_task')
        
        # Check if technical architecture is needed
        if not self._has_technical_architecture():
            return self.create_dynamic_task('technical_architecture_task')
        
        # Check if implementation is needed
        if self._has_technical_architecture() and not self._has_implementation():
            if current_agent == 'senior_engineer_frontend':
                return self.create_dynamic_task('frontend_implementation_task')
            elif current_agent == 'senior_engineer_backend':
                return self.create_dynamic_task('backend_implementation_task')
            elif current_agent == 'senior_engineer_devops':
                return self.create_dynamic_task('devops_setup_task')
        
        # Check if review is needed
        if self._has_implementation() and not self._has_review():
            if current_agent == 'technical_skeptic':
                return self.create_dynamic_task('technical_skeptic_review_task')
            elif current_agent == 'staff_engineer':
                return self.create_dynamic_task('code_review_task')
        
        # Check if integration is needed
        if self._has_implementation() and self._has_review() and not self._has_integration():
            return self.create_dynamic_task('final_integration_task')
        
        # Check for bugs that need fixing
        bugs = self._get_pending_bugs()
        if bugs and current_agent in ['senior_engineer_frontend', 'senior_engineer_backend']:
            bug = bugs[0]  # Get the first pending bug
            return self.create_dynamic_task(
                'bug_fix_task',
                bug_description=bug['description'],
                assigned_agent=current_agent
            )
        
        # Check for features that need implementation
        features = self._get_pending_features()
        if features and current_agent in ['senior_engineer_frontend', 'senior_engineer_backend']:
            feature = features[0]  # Get the first pending feature
            return self.create_dynamic_task(
                'feature_implementation_task',
                feature_description=feature['description'],
                assigned_agent=current_agent
            )
        
        # If no specific task is needed, ask for next steps
        if current_agent == 'product_manager':
            return self.create_dynamic_task('next_steps_planning_task')
        
        return None
    
    def create_bug_fix_task(self, bug_description: str, assigned_agent: str) -> Task:
        """Create a specific bug fix task."""
        return self.create_dynamic_task(
            'bug_fix_task',
            bug_description=bug_description,
            agent=assigned_agent
        )
    
    def create_feature_task(self, feature_description: str, assigned_agent: str) -> Task:
        """Create a specific feature implementation task."""
        return self.create_dynamic_task(
            'feature_implementation_task',
            feature_description=feature_description,
            agent=assigned_agent
        )
    
    def create_research_task(self, research_topic: str) -> Task:
        """Create a technical research task."""
        return self.create_dynamic_task(
            'technical_research_task',
            research_topic=research_topic
        )
    
    # Helper methods to check project state
    def _has_market_research(self) -> bool:
        return any(task['name'] == 'market_research_task' for task in self.completed_tasks)
    
    def _has_technical_architecture(self) -> bool:
        return any(task['name'] == 'technical_architecture_task' for task in self.completed_tasks)
    
    def _has_implementation(self) -> bool:
        implementation_tasks = ['frontend_implementation_task', 'backend_implementation_task', 'devops_setup_task']
        return any(task['name'] in implementation_tasks for task in self.completed_tasks)
    
    def _has_review(self) -> bool:
        review_tasks = ['technical_skeptic_review_task', 'code_review_task']
        return any(task['name'] in review_tasks for task in self.completed_tasks)
    
    def _has_integration(self) -> bool:
        return any(task['name'] == 'final_integration_task' for task in self.completed_tasks)
    
    def _get_pending_bugs(self) -> List[Dict]:
        """Get list of pending bugs from project state."""
        return self.project_state.get('pending_bugs', [])
    
    def _get_pending_features(self) -> List[Dict]:
        """Get list of pending features from project state."""
        return self.project_state.get('pending_features', [])
    
    def add_bug(self, bug_description: str, priority: str = "medium", component: str = "unknown"):
        """Add a new bug to the project state."""
        if 'pending_bugs' not in self.project_state:
            self.project_state['pending_bugs'] = []
        
        self.project_state['pending_bugs'].append({
            'description': bug_description,
            'priority': priority,
            'component': component,
            'status': 'pending'
        })
    
    def add_feature(self, feature_description: str, priority: str = "medium", component: str = "unknown"):
        """Add a new feature request to the project state."""
        if 'pending_features' not in self.project_state:
            self.project_state['pending_features'] = []
        
        self.project_state['pending_features'].append({
            'description': feature_description,
            'priority': priority,
            'component': component,
            'status': 'pending'
        })
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status for agents to understand context."""
        return {
            'completed_tasks': [task['name'] for task in self.completed_tasks],
            'pending_bugs': len(self._get_pending_bugs()),
            'pending_features': len(self._get_pending_features()),
            'project_state': self.project_state
        } 