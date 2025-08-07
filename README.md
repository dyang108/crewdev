# Software Engineering Team with CrewAI

This project implements an ideal software engineering team using CrewAI, featuring specialized agents that work together to develop software projects from concept to deployment.

## Team Structure

### 🎯 **Staff Engineer** (Technical Lead)
- **Role**: Senior Staff Engineer providing technical direction and architecture
- **Responsibilities**: 
  - System design and architecture decisions
  - Code quality oversight and mentoring
  - Technical strategy and best practices
  - Code reviews and technical guidance

### 👨‍💻 **Junior Engineers** (Multiple Specializations)

#### Frontend Engineer
- **Focus**: User interfaces, React/TypeScript, UX design
- **Perspective**: Fresh UI/UX insights and modern web technologies

#### Backend Engineer  
- **Focus**: APIs, services, database design, performance
- **Perspective**: Data modeling, microservices, cloud technologies

#### DevOps Engineer
- **Focus**: CI/CD, infrastructure, deployment, monitoring
- **Perspective**: Operational excellence, reliability, automation

### 📊 **Product Manager** (Market Research & Requirements)
- **Role**: Product Manager & Market Researcher
- **Responsibilities**:
  - Market analysis and user research
  - Requirements gathering and prioritization
  - Business value alignment
  - User acceptance testing

## Technology Stack

All agents use **local Ollama** with the **gpt-oss:20b** model for:
- Privacy and data security
- No external API dependencies
- Consistent performance
- Cost-effective operation

## Workflow

The team follows a comprehensive software development workflow:

1. **Market Research** → Product Manager analyzes user needs and market opportunities
2. **Technical Architecture** → Staff Engineer designs system architecture
3. **Implementation** → Junior Engineers build frontend, backend, and DevOps components
4. **Code Review** → Staff Engineer reviews all implementations
5. **Integration** → Product Manager ensures end-to-end functionality

## Getting Started

### Prerequisites

1. Install Ollama and pull the gpt-oss:20b model:
```bash
ollama pull gpt-oss:20b
```

2. Install project dependencies:
```bash
pip install -e .
```

### Running the Team

```bash
# Run the complete software engineering workflow
python -m src.crewdev.main

# Train the team (for optimization)
python -m src.crewdev.main train <iterations> <filename>

# Test the team performance
python -m src.crewdev.main test <iterations> <eval_llm>
```

### Configuration

The team is configured through YAML files:

- `src/crewdev/config/agents.yaml` - Agent definitions and personalities
- `src/crewdev/config/tasks.yaml` - Task descriptions and workflows

### Customization

To work on different projects, modify the inputs in `src/crewdev/main.py`:

```python
inputs = {
    'project_name': 'Your Project Name',
    'current_year': str(datetime.now().year)
}
```

## Output

The team produces comprehensive deliverables including:
- Market research reports
- Technical architecture documents
- Frontend and backend implementations
- DevOps infrastructure setup
- Code review reports
- Integration and testing results

All outputs are saved to `project_deliverables.md` for easy review.

## Benefits

- **Diverse Perspectives**: Multiple junior engineers bring different viewpoints
- **Technical Leadership**: Staff engineer ensures quality and consistency
- **Market Focus**: Product manager ensures business value
- **Complete Workflow**: From research to deployment
- **Local Operation**: Privacy and cost benefits of local LLM

## Contributing

Feel free to extend the team by:
- Adding new agent specializations
- Creating additional task workflows
- Customizing agent personalities
- Adding new tools and capabilities
