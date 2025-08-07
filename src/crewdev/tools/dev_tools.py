import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class CreateProjectInput(BaseModel):
    """Input schema for CreateProjectTool."""
    project_name: str = Field(..., description="Name of the project to create")
    project_type: str = Field(default="python", description="Type of project (python, node, react, etc.)")
    template: Optional[str] = Field(default=None, description="Template to use for project creation")


class CreateRequirementsInput(BaseModel):
    """Input schema for CreateRequirementsTool."""
    packages: List[str] = Field(..., description="List of Python packages to include")
    filename: str = Field(default="requirements.txt", description="Name of requirements file")


class CreatePackageJsonInput(BaseModel):
    """Input schema for CreatePackageJsonTool."""
    project_name: str = Field(..., description="Name of the project")
    version: str = Field(default="1.0.0", description="Project version")
    description: str = Field(default="", description="Project description")
    dependencies: List[str] = Field(default=[], description="List of dependencies")
    dev_dependencies: List[str] = Field(default=[], description="List of dev dependencies")


class CreateDockerfileInput(BaseModel):
    """Input schema for CreateDockerfileTool."""
    base_image: str = Field(default="python:3.11-slim", description="Base Docker image")
    working_dir: str = Field(default="/app", description="Working directory in container")
    requirements_file: str = Field(default="requirements.txt", description="Requirements file path")
    entry_point: str = Field(default="app.py", description="Entry point script")


class CreateDockerComposeInput(BaseModel):
    """Input schema for CreateDockerComposeTool."""
    services: List[str] = Field(..., description="List of services to include")
    ports: Dict[str, str] = Field(default={}, description="Port mappings")


class CreateProjectTool(BaseTool):
    name: str = "create_project"
    description: str = "Create a new project with basic structure and files"
    args_schema: type[BaseModel] = CreateProjectInput

    def _run(self, project_name: str, project_type: str = "python", template: Optional[str] = None) -> str:
        try:
            project_path = Path(project_name)
            
            if project_path.exists():
                return f"Error: Project directory '{project_name}' already exists"
            
            # Create project directory
            project_path.mkdir(parents=True)
            
            # Create basic project structure based on type
            if project_type.lower() == "python":
                self._create_python_project(project_path)
            elif project_type.lower() == "node":
                self._create_node_project(project_path)
            elif project_type.lower() == "react":
                self._create_react_project(project_path)
            else:
                self._create_generic_project(project_path)
            
            return f"✅ Created {project_type} project '{project_name}' successfully"
        except Exception as e:
            return f"Error creating project '{project_name}': {str(e)}"
    
    def _create_python_project(self, project_path: Path):
        """Create a Python project structure"""
        # Create directories
        (project_path / "src").mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()
        
        # Create basic files
        (project_path / "README.md").write_text(f"# {project_path.name}\n\nA Python project.")
        (project_path / "requirements.txt").write_text("# Add your dependencies here\n")
        (project_path / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\n.venv/\n")
        (project_path / "main.py").write_text('print("Hello, World!")\n')
    
    def _create_node_project(self, project_path: Path):
        """Create a Node.js project structure"""
        # Create directories
        (project_path / "src").mkdir()
        (project_path / "tests").mkdir()
        
        # Create package.json
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }
        (project_path / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Create other files
        (project_path / "README.md").write_text(f"# {project_path.name}\n\nA Node.js project.")
        (project_path / ".gitignore").write_text("node_modules/\n.env\n")
        (project_path / "src" / "index.js").write_text('console.log("Hello, World!");\n')
    
    def _create_react_project(self, project_path: Path):
        """Create a React project structure"""
        # Create directories
        (project_path / "src").mkdir()
        (project_path / "public").mkdir()
        (project_path / "src" / "components").mkdir()
        
        # Create package.json
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.0.0",
                "react-dom": "^18.0.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            }
        }
        (project_path / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Create basic React files
        (project_path / "public" / "index.html").write_text("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>""")
        
        (project_path / "src" / "App.js").write_text("""import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Hello, World!</h1>
    </div>
  );
}

export default App;""")
        
        (project_path / "src" / "index.js").write_text("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""")
    
    def _create_generic_project(self, project_path: Path):
        """Create a generic project structure"""
        (project_path / "README.md").write_text(f"# {project_path.name}\n\nA new project.")


class CreateRequirementsTool(BaseTool):
    name: str = "create_requirements"
    description: str = "Create a Python requirements.txt file with specified packages"
    args_schema: type[BaseModel] = CreateRequirementsInput

    def _run(self, packages: List[str], filename: str = "requirements.txt") -> str:
        try:
            content = "\n".join(packages)
            Path(filename).write_text(content)
            return f"✅ Created requirements file '{filename}' with {len(packages)} packages"
        except Exception as e:
            return f"Error creating requirements file: {str(e)}"


class CreatePackageJsonTool(BaseTool):
    name: str = "create_package_json"
    description: str = "Create a Node.js package.json file"
    args_schema: type[BaseModel] = CreatePackageJsonInput

    def _run(self, project_name: str, version: str = "1.0.0", description: str = "", 
             dependencies: List[str] = [], dev_dependencies: List[str] = []) -> str:
        try:
            package_json = {
                "name": project_name,
                "version": version,
                "description": description,
                "main": "src/index.js",
                "scripts": {
                    "start": "node src/index.js",
                    "test": "echo \"Error: no test specified\" && exit 1"
                },
                "keywords": [],
                "author": "",
                "license": "ISC",
                "dependencies": {dep: "latest" for dep in dependencies},
                "devDependencies": {dep: "latest" for dep in dev_dependencies}
            }
            
            Path("package.json").write_text(json.dumps(package_json, indent=2))
            return f"✅ Created package.json for '{project_name}'"
        except Exception as e:
            return f"Error creating package.json: {str(e)}"


class CreateDockerfileTool(BaseTool):
    name: str = "create_dockerfile"
    description: str = "Create a Dockerfile for Python applications"
    args_schema: type[BaseModel] = CreateDockerfileInput

    def _run(self, base_image: str = "python:3.11-slim", working_dir: str = "/app", 
             requirements_file: str = "requirements.txt", entry_point: str = "app.py") -> str:
        try:
            dockerfile_content = f"""FROM {base_image}

WORKDIR {working_dir}

COPY {requirements_file} .
RUN pip install --no-cache-dir -r {requirements_file}

COPY . .

EXPOSE 8000

CMD ["python", "{entry_point}"]
"""
            
            Path("Dockerfile").write_text(dockerfile_content)
            return f"✅ Created Dockerfile with base image {base_image}"
        except Exception as e:
            return f"Error creating Dockerfile: {str(e)}"


class CreateDockerComposeTool(BaseTool):
    name: str = "create_docker_compose"
    description: str = "Create a docker-compose.yml file"
    args_schema: type[BaseModel] = CreateDockerComposeInput

    def _run(self, services: List[str], ports: Dict[str, str] = {}) -> str:
        try:
            compose_config = {
                "version": "3.8",
                "services": {}
            }
            
            for service in services:
                compose_config["services"][service] = {
                    "build": ".",
                    "ports": [ports.get(service, "8000:8000")] if service in ports else [],
                    "volumes": [".:/app"],
                    "environment": ["PYTHONUNBUFFERED=1"]
                }
            
            Path("docker-compose.yml").write_text(yaml.dump(compose_config, default_flow_style=False))
            return f"✅ Created docker-compose.yml with {len(services)} services"
        except Exception as e:
            return f"Error creating docker-compose.yml: {str(e)}"


class CreateGitignoreTool(BaseTool):
    name: str = "create_gitignore"
    description: str = "Create a .gitignore file for common project types"
    args_schema: type[BaseModel] = CreateProjectInput

    def _run(self, project_name: str, project_type: str = "python", template: Optional[str] = None) -> str:
        try:
            gitignore_content = ""
            
            if project_type.lower() == "python":
                gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
"""
            elif project_type.lower() == "node":
                gitignore_content = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
node_modules/
jspm_packages/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test

# parcel-bundler cache
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/
"""
            elif project_type.lower() == "react":
                gitignore_content = """# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
            else:
                gitignore_content = """# General
.DS_Store
.env
*.log
"""
            
            Path(".gitignore").write_text(gitignore_content)
            return f"✅ Created .gitignore for {project_type} project"
        except Exception as e:
            return f"Error creating .gitignore: {str(e)}" 