# AI Code Repository Assistant

An intelligent AI-powered coding assistant that integrates with code repositories to automate code reviews, streamline repository management, and support debugging.

## Features

- 🤖 AI-powered code review automation
- 📦 Repository management automation
- 🔍 Intelligent debugging support
- 🔄 Seamless integration with GitHub and GitLab
- 📝 Documentation generation and management

## Tech Stack

- Python 3.9+
- Google Gemini AI
- FastAPI for API endpoints
- SQLite for local storage
- GitPython for repository operations
- Pydantic for data validation

## Project Structure

```
ai-code-repo-assistant/
├── src/
│   ├── core/           # Core functionality
│   ├── ai/             # AI integration
│   ├── git/            # Git operations
│   ├── api/            # API endpoints
│   └── utils/          # Utility functions
├── tests/              # Test files
├── docs/               # Documentation
└── config/             # Configuration files
```

## Setup

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Set up environment variables
5. Run the application

## Development Status

🚧 Under Development

## License

MIT License 

# Git Repository Manager

A Python library for managing Git repositories with advanced features including workflow automation and backup/restore capabilities.

## Features

- Basic Git operations (branches, commits, status)
- Repository configuration management
- Git hooks management
- Workflow automation
- Repository backup and restore
- Template management

## Installation

```bash
pip install git-repository-manager
```

## Usage

### Basic Repository Operations

```python
from git_ops import RepositoryManager

# Initialize repository manager
repo_manager = RepositoryManager("/path/to/repo")

# Get repository status
status = repo_manager.get_repository_status()
print(f"Current branch: {status['current_branch']}")
print(f"Changed files: {status['changed_files']}")
```

### Workflow Automation

Set up and manage automated workflows:

```python
# Define a workflow
workflow = {
    "name": "test-workflow",
    "description": "Run tests on push",
    "events": ["push", "pull_request"],
    "steps": [
        {
            "name": "run-tests",
            "event": "push",
            "command": "pytest tests/"
        },
        {
            "name": "lint-check",
            "event": "pull_request",
            "command": "flake8 src/"
        }
    ]
}

# Set up the workflow
repo_manager.setup_workflow("test-workflow", workflow)

# Run workflow for a specific event
workflow_id = repo_manager.run_workflow("test-workflow", "push")

# Check workflow status
status = repo_manager.get_workflow_status(workflow_id)
print(f"Workflow status: {status['status']}")
```

### Repository Backup and Restore

Backup and restore your repository:

```python
# Create a backup
backup_dir = "/path/to/backups"
repo_manager.create_backup(backup_dir)

# List available backups
backups = repo_manager.list_backups(backup_dir)
for backup in backups:
    print(f"Backup: {backup['name']} from {backup['timestamp']}")

# Restore from a backup
repo_manager.restore_backup(
    "/path/to/backups/backup_20240101_120000",
    "/path/to/restore"
)

# Set up automated backups
schedule = {
    "frequency": "daily",
    "time": "00:00",
    "retention_days": 7,
    "backup_path": backup_dir
}
repo_manager.schedule_backup(backup_dir, schedule)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 