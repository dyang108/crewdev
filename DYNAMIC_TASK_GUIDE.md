# Dynamic Task Assignment Guide

This guide explains how to use the dynamic task assignment system in CrewAI, which allows agents to automatically assign tasks based on current project needs and state.

## Overview

The dynamic task assignment system enables:

1. **Automatic Task Assignment**: Agents can request the next task based on current project state
2. **Bug Tracking**: Engineers can report bugs that get automatically assigned to appropriate team members
3. **Feature Requests**: New features can be requested and assigned to the right engineers
4. **Project State Management**: The system tracks completed tasks and current project needs
5. **Intelligent Routing**: Tasks are assigned to the most appropriate agent based on their role and expertise

## How It Works

### 1. Project State Tracking

The system maintains a project state that includes:
- Completed tasks
- Pending bugs
- Pending feature requests
- Current project phase

### 2. Dynamic Task Assignment Logic

The system follows this logic for task assignment:

1. **Market Research** → Product Manager (if not completed)
2. **Technical Architecture** → Staff Engineer (if market research is done)
3. **Implementation** → Frontend/Backend/DevOps Engineers (if architecture is done)
4. **Review** → Technical Skeptic/Staff Engineer (if implementation is done)
5. **Integration** → Product Manager (if review is done)
6. **Bug Fixes** → Appropriate engineers based on component
7. **Feature Implementation** → Appropriate engineers based on component

### 3. Agent Tools

Each agent has access to these dynamic task tools:

- **DynamicTaskTool**: Request next tasks, report completion, add bugs/features
- **TaskCompletionTool**: Report task completion and get next task
- **BugReportTool**: Report bugs with automatic assignment
- **FeatureRequestTool**: Request features with automatic assignment

## Usage Examples

### Example 1: Agent Requests Next Task

```python
# An agent can use the dynamic task tool to request their next task
result = agent.use_tool("dynamic_task_tool", action="get_next_task", agent_name="senior_engineer_frontend")
print(result)
# Output: "Next task assigned: Implement the frontend components for project_name..."
```

### Example 2: Report Task Completion

```python
# An agent reports that they completed a task
result = agent.use_tool("task_completion_tool", 
                       task_name="frontend_implementation_task",
                       output="Frontend components implemented successfully",
                       agent_name="senior_engineer_frontend")
print(result)
# Output: "Task 'frontend_implementation_task' completed successfully! Next task: ..."
```

### Example 3: Report a Bug

```python
# An engineer reports a bug they found
result = agent.use_tool("bug_report_tool",
                       description="Login button not working on mobile devices",
                       priority="high",
                       component="frontend")
print(result)
# Output: "Bug reported and added to project: Login button not working... Recommended assignment: senior_engineer_frontend"
```

### Example 4: Request a Feature

```python
# Product manager requests a new feature
result = agent.use_tool("feature_request_tool",
                       description="Add user profile page with avatar upload",
                       priority="medium",
                       component="frontend")
print(result)
# Output: "Feature request added to project: Add user profile page... Recommended assignment: senior_engineer_frontend"
```

## Implementation Details

### DynamicTaskManager Class

The core of the system is the `DynamicTaskManager` class:

```python
from crewdev.dynamic_task_manager import DynamicTaskManager

# Initialize the task manager
task_manager = DynamicTaskManager()

# Update project state
task_manager.update_project_state({"phase": "implementation"})

# Add bugs or features
task_manager.add_bug("API timeout issue", "high")
task_manager.add_feature("Dark mode support", "medium")

# Get next task for an agent
next_task = task_manager.determine_next_task("senior_engineer_frontend")
```

### Task Templates

Tasks are defined as templates in `src/crewdev/config/tasks.yaml`:

```yaml
bug_fix_task:
  description: >
    Investigate and fix the reported bug: {bug_description}
    Analyze the issue, identify the root cause, and implement a proper fix.
  expected_output: >
    Bug fix implementation including:
    - Root cause analysis
    - Fix implementation
    - Test cases to prevent regression
  agent: "{assigned_agent}"
```

### Integration with Crew

The dynamic task system is integrated into the crew by:

1. **Initializing the task manager** in the crew constructor
2. **Adding dynamic task tools** to all agents
3. **Using task templates** for dynamic task creation

## Agent Workflow Examples

### Product Manager Workflow

1. **Market Research**: Conduct initial market research
2. **Next Steps Planning**: Determine what should happen next
3. **Feature Requests**: Add new features to the project
4. **Integration Testing**: Oversee final integration

### Staff Engineer Workflow

1. **Technical Architecture**: Design system architecture
2. **Code Review**: Review implementations
3. **Technical Research**: Research new technologies
4. **Bug Fixes**: Handle complex technical issues

### Frontend Engineer Workflow

1. **Frontend Implementation**: Build UI components
2. **Bug Fixes**: Fix frontend-specific bugs
3. **Feature Implementation**: Add new frontend features
4. **Testing**: Test frontend functionality

### Backend Engineer Workflow

1. **Backend Implementation**: Build API and services
2. **Bug Fixes**: Fix backend-specific bugs
3. **Feature Implementation**: Add new backend features
4. **Performance Optimization**: Optimize backend performance

## Best Practices

### 1. Task Completion Reporting

Always report task completion to update project state:

```python
# Good: Report completion with detailed output
agent.use_tool("task_completion_tool",
               task_name="frontend_implementation_task",
               output="Implemented React components with TypeScript, added unit tests, and integrated with backend API",
               agent_name="senior_engineer_frontend")
```

### 2. Bug Reporting

Report bugs with specific details:

```python
# Good: Detailed bug report
agent.use_tool("bug_report_tool",
               description="User authentication fails on Safari browser - login form submits but session not created",
               priority="high",
               component="frontend")
```

### 3. Feature Requests

Request features with clear requirements:

```python
# Good: Clear feature request
agent.use_tool("feature_request_tool",
               description="Add real-time notifications for new messages using WebSocket connection",
               priority="medium",
               component="frontend")
```

### 4. Project State Updates

Keep project state updated:

```python
# Update project state when significant changes occur
task_manager.update_project_state({
    "current_phase": "implementation",
    "frontend_status": "in_progress",
    "backend_status": "completed"
})
```

## Running the Demo

To see the dynamic task system in action:

```bash
python example_dynamic_tasks.py
```

This will demonstrate:
- Initial project state
- Dynamic task assignment for different agents
- Task completion simulation
- Bug and feature assignment
- Updated task assignments after completion

## Customization

### Adding New Task Types

1. Add task template to `src/crewdev/config/tasks.yaml`:
```yaml
custom_task:
  description: >
    Custom task description with {parameters}
  expected_output: >
    Expected output description
  agent: "{assigned_agent}"
```

2. Add logic to `DynamicTaskManager.determine_next_task()`:
```python
# Check for custom task conditions
if self._needs_custom_task() and current_agent == "appropriate_agent":
    return self.create_dynamic_task('custom_task', **parameters)
```

### Modifying Assignment Logic

Update the `determine_next_task()` method in `DynamicTaskManager` to change how tasks are assigned based on your specific needs.

### Adding New Tools

Create new tools in `src/crewdev/tools/` and add them to the agents in `src/crewdev/crew.py`.

## Troubleshooting

### Common Issues

1. **Task not assigned**: Check if prerequisites are completed
2. **Wrong agent assigned**: Verify agent name matches configuration
3. **Tool not found**: Ensure tools are properly imported and added to agents

### Debugging

Use the project status tool to check current state:

```python
status = task_manager.get_project_status()
print(json.dumps(status, indent=2))
```

This will show:
- Completed tasks
- Pending bugs and features
- Current project state

## Conclusion

The dynamic task assignment system provides a flexible, intelligent way to manage task assignment in CrewAI projects. By tracking project state and using intelligent routing, agents can work more efficiently and respond to changing project needs automatically. 