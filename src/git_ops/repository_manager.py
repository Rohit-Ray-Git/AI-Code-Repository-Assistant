import os
import shutil
import json
import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logging.warning("GitPython not available. Git operations will be limited.")

class RepositoryManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = None
        if os.path.exists(repo_path) and GIT_AVAILABLE:
            try:
                self.repo = Repo(repo_path)
            except Exception as e:
                logging.error(f"Failed to initialize repository: {str(e)}")
        elif not GIT_AVAILABLE:
            logging.warning("GitPython not available. Git operations will be limited.")

    def get_branches(self) -> List[str]:
        """
        Get all branches in the repository
        """
        if not GIT_AVAILABLE:
            return ["main"]  # Default branch
        return [branch.name for branch in self.repo.branches]

    def get_commit_history(self, branch: str = "main") -> List[Dict[str, Any]]:
        """
        Get commit history for a specific branch
        """
        if not GIT_AVAILABLE:
            return []  # Return empty list if git is not available
        commits = []
        for commit in self.repo.iter_commits(branch):
            commits.append({
                "hash": commit.hexsha,
                "author": commit.author.name,
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message
            })
        return commits

    def create_branch(self, branch_name: str) -> bool:
        """
        Create a new branch
        """
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.create_head(branch_name)
            return True
        except Exception as e:
            print(f"Error creating branch: {e}")
            return False

    def checkout_branch(self, branch_name: str) -> bool:
        """
        Checkout to a specific branch
        """
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.git.checkout(branch_name)
            return True
        except Exception as e:
            print(f"Error checking out branch: {e}")
            return False

    def get_file_content(self, file_path: str) -> str:
        """
        Get content of a specific file
        """
        try:
            with open(self.repo_path / file_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def get_changed_files(self) -> List[str]:
        """
        Get list of changed files in the working directory
        """
        if not GIT_AVAILABLE:
            return []
        return [item.a_path for item in self.repo.index.diff(None)]

    def get_repository_status(self) -> Dict[str, Any]:
        """
        Get current repository status including:
        - Current branch
        - Changed files
        - Untracked files
        - Staged changes
        """
        if not GIT_AVAILABLE:
            return {
                "current_branch": "main",
                "changed_files": [],
                "untracked_files": [],
                "staged_changes": []
            }

        try:
            current_branch = self.repo.active_branch.name
        except:
            current_branch = "detached HEAD"

        changed_files = [item.a_path for item in self.repo.index.diff(None)]
        untracked_files = [item for item in self.repo.untracked_files]
        staged_changes = [item.a_path for item in self.repo.index.diff('HEAD')]

        return {
            "current_branch": current_branch,
            "changed_files": changed_files,
            "untracked_files": untracked_files,
            "staged_changes": staged_changes
        }

    def get_file_diff(self, file_path: str) -> str:
        """
        Get diff of changes in a specific file
        """
        if not GIT_AVAILABLE:
            return ""
        try:
            return self.repo.git.diff(file_path)
        except Exception as e:
            print(f"Error getting file diff: {e}")
            return ""

    def stage_file(self, file_path: str) -> bool:
        """
        Stage a file for commit
        """
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.index.add([file_path])
            return True
        except Exception as e:
            print(f"Error staging file: {e}")
            return False

    def unstage_file(self, file_path: str) -> bool:
        """
        Unstage a file
        """
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.index.remove([file_path])
            return True
        except Exception as e:
            print(f"Error unstaging file: {e}")
            return False

    def commit_changes(self, message: str) -> bool:
        """
        Commit staged changes with a message
        """
        if not GIT_AVAILABLE:
            return False
        try:
            if not self.repo.index.diff('HEAD'):
                return False  # No changes to commit
            self.repo.index.commit(message)
            return True
        except Exception as e:
            print(f"Error committing changes: {e}")
            return False

    def push_changes(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Push changes to remote repository
        """
        if not GIT_AVAILABLE:
            return False
        try:
            if not branch:
                branch = self.repo.active_branch.name
            self.repo.remotes[remote].push(branch)
            return True
        except Exception as e:
            print(f"Error pushing changes: {e}")
            return False

    def pull_changes(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Pull changes from remote repository
        """
        if not GIT_AVAILABLE:
            return False
        try:
            if not branch:
                branch = self.repo.active_branch.name
            self.repo.remotes[remote].pull(branch)
            return True
        except Exception as e:
            print(f"Error pulling changes: {e}")
            return False

    def get_remote_url(self, remote: str = "origin") -> str:
        """
        Get the URL of a remote repository
        """
        if not GIT_AVAILABLE:
            return ""
        try:
            return self.repo.remotes[remote].url
        except Exception as e:
            print(f"Error getting remote URL: {e}")
            return ""

    def add_remote(self, name: str, url: str) -> bool:
        """
        Add a remote repository
        """
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.create_remote(name, url)
            return True
        except Exception as e:
            print(f"Error adding remote: {e}")
            return False

    def get_merge_conflicts(self) -> List[str]:
        """
        Get list of files with merge conflicts
        """
        if not GIT_AVAILABLE:
            return []
        try:
            return [item.a_path for item in self.repo.index.unmerged_blobs()]
        except Exception as e:
            print(f"Error getting merge conflicts: {e}")
            return []

    @classmethod
    def initialize_repository(cls, repo_path: str, bare: bool = False) -> bool:
        """
        Initialize a new Git repository
        """
        if not GIT_AVAILABLE:
            return False
        try:
            Repo.init(repo_path, bare=bare)
            return True
        except Exception as e:
            print(f"Error initializing repository: {e}")
            return False

    @classmethod
    def clone_repository(cls, url: str, target_path: str, branch: Optional[str] = None) -> bool:
        """
        Clone a repository from a URL
        """
        if not GIT_AVAILABLE:
            return False
        try:
            if branch:
                Repo.clone_from(url, target_path, branch=branch)
            else:
                Repo.clone_from(url, target_path)
            return True
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return False

    def configure_repository(self, config: Dict[str, str]) -> bool:
        """
        Configure repository settings
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            with self.repo.config_writer() as git_config:
                for key, value in config.items():
                    git_config.set_value(key, value)
            return True
        except Exception as e:
            print(f"Error configuring repository: {e}")
            return False

    def get_repository_config(self) -> Dict[str, str]:
        """
        Get current repository configuration
        """
        if not GIT_AVAILABLE or not self.repo:
            return {}
        try:
            config = {}
            with self.repo.config_reader() as git_config:
                for section in git_config.sections():
                    for option in git_config.options(section):
                        value = git_config.get_value(section, option)
                        config[f"{section}.{option}"] = value
            return config
        except Exception as e:
            print(f"Error getting repository configuration: {e}")
            return {}

    def create_template(self, template_name: str, description: str = "") -> bool:
        """
        Create a repository template
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            # Create a template branch
            template_branch = f"template/{template_name}"
            self.repo.create_head(template_branch)
            
            # Add template metadata
            with self.repo.config_writer() as git_config:
                git_config.set_value(f"template.{template_name}", "description", description)
            
            return True
        except Exception as e:
            print(f"Error creating template: {e}")
            return False

    def list_templates(self) -> List[Dict[str, str]]:
        """
        List available repository templates
        """
        if not GIT_AVAILABLE or not self.repo:
            return []
        try:
            templates = []
            with self.repo.config_reader() as git_config:
                for section in git_config.sections():
                    if section.startswith("template."):
                        template_name = section.split(".")[1]
                        description = git_config.get_value(section, "description", "")
                        templates.append({
                            "name": template_name,
                            "description": description
                        })
            return templates
        except Exception as e:
            print(f"Error listing templates: {e}")
            return []

    def setup_hook(self, hook_name: str, script_content: str) -> bool:
        """
        Set up a Git hook with the provided script content
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            hooks_dir = self.repo_path / ".git" / "hooks"
            hook_file = hooks_dir / hook_name
            
            # Create hooks directory if it doesn't exist
            hooks_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the hook script
            with open(hook_file, "w") as f:
                f.write(script_content)
            
            # Make the hook executable
            os.chmod(hook_file, 0o755)
            return True
        except Exception as e:
            print(f"Error setting up hook: {e}")
            return False

    def get_hooks(self) -> List[str]:
        """
        Get list of installed Git hooks
        """
        if not GIT_AVAILABLE or not self.repo:
            return []
        try:
            hooks_dir = self.repo_path / ".git" / "hooks"
            if not hooks_dir.exists():
                return []
            return [f.name for f in hooks_dir.iterdir() if f.is_file() and not f.name.endswith(".sample")]
        except Exception as e:
            print(f"Error getting hooks: {e}")
            return []

    def remove_hook(self, hook_name: str) -> bool:
        """
        Remove a Git hook
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            hook_file = self.repo_path / ".git" / "hooks" / hook_name
            if hook_file.exists():
                hook_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error removing hook: {e}")
            return False

    def setup_workflow(self, workflow_name: str, workflow_config: Dict[str, Any]) -> bool:
        """
        Set up a custom workflow configuration
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            workflows_dir = self.repo_path / ".git" / "workflows"
            workflow_file = workflows_dir / f"{workflow_name}.json"
            
            # Create workflows directory if it doesn't exist
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the workflow configuration
            with open(workflow_file, "w") as f:
                json.dump(workflow_config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error setting up workflow: {e}")
            return False

    def get_workflows(self) -> List[Dict[str, Any]]:
        """
        Get list of configured workflows
        """
        if not GIT_AVAILABLE or not self.repo:
            return []
        try:
            workflows_dir = self.repo_path / ".git" / "workflows"
            if not workflows_dir.exists():
                return []
            
            workflows = []
            for workflow_file in workflows_dir.glob("*.json"):
                with open(workflow_file, "r") as f:
                    import json
                    workflow_config = json.load(f)
                    workflows.append({
                        "name": workflow_file.stem,
                        "config": workflow_config
                    })
            return workflows
        except Exception as e:
            print(f"Error getting workflows: {e}")
            return []

    def remove_workflow(self, workflow_name: str) -> bool:
        """
        Remove a workflow configuration
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            workflow_file = self.repo_path / ".git" / "workflows" / f"{workflow_name}.json"
            if workflow_file.exists():
                workflow_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error removing workflow: {e}")
            return False

    def run_workflow(self, workflow_name: str, event: str, data: Dict[str, Any] = None) -> bool:
        """
        Run a workflow for a specific event
        """
        if not GIT_AVAILABLE or not self.repo:
            return False
        try:
            workflow_file = self.repo_path / ".git" / "workflows" / f"{workflow_name}.json"
            if not workflow_file.exists():
                return False
            
            with open(workflow_file, "r") as f:
                import json
                workflow_config = json.load(f)
            
            # Check if the event is configured in the workflow
            if event not in workflow_config.get("events", []):
                return False
            
            # Execute the workflow steps
            for step in workflow_config.get("steps", []):
                if step.get("event") == event:
                    # Execute the step's command
                    command = step.get("command")
                    if command:
                        import subprocess
                        subprocess.run(command, shell=True, check=True)
            
            return True
        except Exception as e:
            print(f"Error running workflow: {e}")
            return False

    def create_backup(self, backup_dir: str) -> bool:
        """
        Create a backup of the repository
        
        Args:
            backup_dir: Directory where backups will be stored
            
        Returns:
            bool: True if backup was successful, False otherwise
        """
        try:
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup name with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Create backup using copytree with ignore_patterns
            shutil.copytree(
                str(self.repo_path),  # Convert Path to string
                backup_path,
                symlinks=True,
                ignore=None  # Copy all files including .git
            )
            
            # Create metadata file
            metadata = {
                "timestamp": timestamp,
                "repository_path": str(self.repo_path),
                "git_version": self.repo.git.version() if self.repo and GIT_AVAILABLE else "N/A",
                "name": backup_name
            }
            
            metadata_path = os.path.join(backup_dir, f"{backup_name}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to create backup: {str(e)}")
            return False
    
    def restore_backup(self, backup_path: str, restore_path: str) -> bool:
        """
        Restore a repository from backup
        
        Args:
            backup_path: Path to the backup
            restore_path: Path where repository should be restored
            
        Returns:
            bool: True if restore was successful, False otherwise
        """
        try:
            # Check if backup exists
            if not os.path.exists(backup_path):
                raise ValueError("Backup path does not exist")
            
            # Create restore directory if it doesn't exist
            os.makedirs(restore_path, exist_ok=True)
            
            # Remove existing contents if any
            if os.path.exists(restore_path):
                for item in os.listdir(restore_path):
                    item_path = os.path.join(restore_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            
            # Restore repository with all contents including .git
            shutil.copytree(
                backup_path,
                restore_path,
                dirs_exist_ok=True,
                symlinks=True,
                ignore=None
            )
            
            # Initialize Git repository if GitPython is available
            if GIT_AVAILABLE and os.path.exists(os.path.join(restore_path, ".git")):
                try:
                    Repo(restore_path)
                except Exception as e:
                    logging.warning(f"Failed to initialize Git repository after restore: {str(e)}")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to restore backup: {str(e)}")
            return False
    
    def list_backups(self, backup_dir: str) -> List[Dict]:
        """
        List all backups in the backup directory
        
        Args:
            backup_dir: Directory containing backups
            
        Returns:
            List[Dict]: List of backup metadata
        """
        try:
            backups = []
            
            # List all metadata files
            for file in os.listdir(backup_dir):
                if file.endswith("_metadata.json"):
                    with open(os.path.join(backup_dir, file), 'r') as f:
                        metadata = json.load(f)
                        backups.append(metadata)
            
            return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
            
        except Exception as e:
            logging.error(f"Failed to list backups: {str(e)}")
            return []
    
    def delete_backup(self, backup_path: str) -> bool:
        """
        Delete a backup
        
        Args:
            backup_path: Path to the backup to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            # Delete backup directory
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            
            # Delete metadata file
            metadata_path = f"{backup_path}_metadata.json"
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            # Verify deletion
            if os.path.exists(backup_path) or os.path.exists(metadata_path):
                raise Exception("Failed to delete backup files")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to delete backup: {str(e)}")
            return False
    
    def schedule_backup(self, backup_dir: str, schedule: Dict) -> bool:
        """
        Schedule automatic backups
        
        Args:
            backup_dir: Directory where backups will be stored
            schedule: Dictionary containing schedule configuration
            
        Returns:
            bool: True if schedule was set successfully, False otherwise
        """
        try:
            # Save schedule configuration
            schedule_path = os.path.join(backup_dir, "backup_schedule.json")
            with open(schedule_path, 'w') as f:
                json.dump(schedule, f)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to set backup schedule: {str(e)}")
            return False
    
    def get_backup_schedule(self) -> Optional[Dict]:
        """
        Get current backup schedule
        
        Returns:
            Optional[Dict]: Current backup schedule or None if not set
        """
        try:
            schedule_path = os.path.join(self.repo_path, "backup_schedule.json")
            if os.path.exists(schedule_path):
                with open(schedule_path, 'r') as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            logging.error(f"Failed to get backup schedule: {str(e)}")
            return None 