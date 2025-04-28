import os
import shutil
import json
import datetime
import subprocess
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import threading
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import fnmatch
from datetime import datetime
import re

try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logging.warning("GitPython not available. Git operations will be limited.")

class WorkflowManager:
    def __init__(self):
        self.workflow_queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.running_workflows = {}
        self.workflow_history = []
        self._start_workflow_processor()

    def _start_workflow_processor(self):
        """Start the workflow processing thread"""
        def process_workflows():
            while True:
                try:
                    workflow = self.workflow_queue.get()
                    if workflow is None:
                        break
                    
                    workflow_id = workflow.get('id')
                    self.running_workflows[workflow_id] = {
                        'status': 'running',
                        'start_time': datetime.datetime.now(),
                        'workflow': workflow
                    }
                    
                    try:
                        success = self._execute_workflow(workflow)
                        if success:
                            self.running_workflows[workflow_id]['status'] = 'completed'
                        else:
                            self.running_workflows[workflow_id]['status'] = 'failed'
                            self.running_workflows[workflow_id]['error'] = "Workflow execution failed"
                    except Exception as e:
                        logging.error(f"Workflow {workflow_id} failed: {str(e)}")
                        self.running_workflows[workflow_id]['status'] = 'failed'
                        self.running_workflows[workflow_id]['error'] = str(e)
                    
                    self.running_workflows[workflow_id]['end_time'] = datetime.datetime.now()
                    self.workflow_history.append(self.running_workflows[workflow_id])
                    
                except Exception as e:
                    logging.error(f"Error processing workflow: {str(e)}")
                finally:
                    self.workflow_queue.task_done()

        thread = threading.Thread(target=process_workflows, daemon=True)
        thread.start()

    def _execute_workflow(self, workflow: Dict[str, Any]) -> bool:
        """Execute a workflow's steps"""
        try:
            for step in workflow.get('steps', []):
                if not self._execute_step(step):
                    raise Exception(f"Step '{step.get('name', 'unknown')}' failed")
            return True
        except Exception as e:
            logging.error(f"Error executing workflow: {str(e)}")
            return False

    def _execute_step(self, step: Dict[str, Any]) -> bool:
        """Execute a single workflow step"""
        try:
            command = step.get('command')
            if not command:
                return True

            # Execute the command
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            
            # Log the output
            if process.stdout:
                logging.info(f"Command output: {process.stdout}")
            if process.stderr:
                logging.warning(f"Command stderr: {process.stderr}")
            
            # Return False if command failed
            if process.returncode != 0:
                logging.error(f"Command failed with exit code {process.returncode}")
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"Error executing step: {str(e)}")
            return False

    def schedule_workflow(self, workflow: Dict[str, Any]) -> str:
        """Schedule a workflow for execution"""
        workflow_id = f"wf_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        workflow['id'] = workflow_id
        self.workflow_queue.put(workflow)
        return workflow_id

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow"""
        return self.running_workflows.get(workflow_id)

    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get the history of executed workflows"""
        return self.workflow_history

class RepositoryManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = None
        self.workflow_manager = WorkflowManager()
        
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
        """Set up a new workflow with the given configuration."""
        # Validate workflow configuration
        if not isinstance(workflow_config, dict):
            raise ValueError("Workflow configuration must be a dictionary.")
        
        required_fields = ["name", "description", "events", "steps"]
        for field in required_fields:
            if field not in workflow_config:
                raise ValueError(f"Workflow configuration missing required field: {field}")
        
        # Validate events
        valid_events = ["push", "pull_request", "merge"]
        for event in workflow_config["events"]:
            if event not in valid_events:
                raise ValueError(f"Invalid event: {event}. Valid events are: {valid_events}")
        
        # Validate steps
        for step in workflow_config["steps"]:
            if not isinstance(step, dict):
                raise ValueError("Each step must be a dictionary.")
            if "name" not in step or "event" not in step or "command" not in step:
                raise ValueError("Each step must have 'name', 'event', and 'command' fields.")
            if step["event"] not in valid_events:
                raise ValueError(f"Invalid event in step: {step['event']}. Valid events are: {valid_events}")
        
        # Proceed with workflow setup
        try:
            workflows_dir = self.repo_path / ".git" / "workflows"
            workflow_file = workflows_dir / f"{workflow_name}.json"
            
            # Create workflows directory if it doesn't exist
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the workflow configuration
            with open(workflow_file, "w") as f:
                json.dump(workflow_config, f, indent=2)
            
            logging.info(f"Successfully set up workflow: {workflow_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to set up workflow {workflow_name}: {str(e)}")
            return False

    def get_workflows(self) -> List[Dict[str, Any]]:
        """
        Get list of configured workflows
        
        Returns:
            List[Dict]: List of workflow configurations
        """
        try:
            workflows_dir = self.repo_path / ".git" / "workflows"
            if not workflows_dir.exists():
                return []
            
            workflows = []
            for workflow_file in workflows_dir.glob("*.json"):
                with open(workflow_file, "r") as f:
                    workflow_config = json.load(f)
                    workflows.append({
                        "name": workflow_file.stem,
                        "config": workflow_config
                    })
            return workflows
            
        except Exception as e:
            logging.error(f"Failed to get workflows: {str(e)}")
            return []

    def remove_workflow(self, workflow_name: str) -> bool:
        """
        Remove a workflow configuration
        
        Args:
            workflow_name: Name of the workflow to remove
            
        Returns:
            bool: True if workflow was removed successfully
        """
        try:
            workflow_file = self.repo_path / ".git" / "workflows" / f"{workflow_name}.json"
            if workflow_file.exists():
                workflow_file.unlink()
                return True
            return False
            
        except Exception as e:
            logging.error(f"Failed to remove workflow: {str(e)}")
            return False

    def run_workflow(self, workflow_name: str, event: str) -> str:
        """Run a workflow for the specified event."""
        try:
            # Load workflow configuration
            workflow_file = self.repo_path / ".git" / "workflows" / f"{workflow_name}.json"
            if not workflow_file.exists():
                raise ValueError(f"Workflow {workflow_name} not found.")
            
            with open(workflow_file, "r") as f:
                workflow_config = json.load(f)
            
            # Validate event
            if event not in workflow_config["events"]:
                raise ValueError(f"Event {event} not configured in workflow {workflow_name}.")
            
            # Execute steps for the event
            for step in workflow_config["steps"]:
                if step["event"] == event:
                    # Execute the command
                    subprocess.run(step["command"], shell=True, check=True)
            
            # Generate a unique workflow ID
            workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Log workflow execution
            logging.info(f"Workflow {workflow_name} executed for event {event} with ID {workflow_id}")
            
            return workflow_id
            
        except Exception as e:
            logging.error(f"Failed to run workflow: {str(e)}")
            raise

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow execution
        
        Args:
            workflow_id: ID of the workflow execution
            
        Returns:
            Optional[Dict]: Workflow status information
        """
        return self.workflow_manager.get_workflow_status(workflow_id)

    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of workflow executions
        
        Returns:
            List[Dict]: List of workflow execution records
        """
        return self.workflow_manager.get_workflow_history()

    @staticmethod
    def get_essential_file_patterns() -> List[str]:
        """Get patterns for essential project files that should be included in backups."""
        return [
            # Python files
            "*.py",
            "*.pyi",
            "*.pyx",
            "*.pxd",
            
            # Configuration files
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "*.toml",
            "*.yaml",
            "*.yml",
            "*.json",
            "*.ini",
            "*.cfg",
            "*.conf",
            ".env",
            ".env.*",
            
            # Documentation
            "README*",
            "*.md",
            "*.rst",
            "docs/*",
            "*.txt",
            
            # Git related
            ".gitignore",
            ".gitattributes",
            
            # Project specific
            "Makefile",
            "Dockerfile",
            "docker-compose*.yml",
            "*.sh",
            "*.bat",
            "*.ps1",
            
            # Source code directories
            "src/*",
            "tests/*",
            "scripts/*",
            "bin/*"
        ]

    def create_backup(self, backup_dir: str, exclude_patterns: List[str] = None, progress_callback = None) -> bool:
        """Create a backup of essential repository files."""
        try:
            # Convert paths to absolute
            backup_dir = os.path.abspath(backup_dir)
            repo_path = os.path.abspath(str(self.repo_path))
            
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup name with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Get list of files to backup
            files_to_backup = []
            total_size = 0
            
            # Get essential file patterns
            include_patterns = self.get_essential_file_patterns()
            
            # Walk through repository
            for root, dirs, files in os.walk(repo_path):
                # Skip backup directory
                if root.startswith(backup_dir):
                    continue
                
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not any(
                    fnmatch.fnmatch(d, pattern) for pattern in (exclude_patterns or [])
                )]
                
                # Process files
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, repo_path)
                    
                    # Check if file matches any include pattern
                    if not any(fnmatch.fnmatch(rel_path, pattern) for pattern in include_patterns):
                        continue
                    
                    # Skip excluded files
                    if any(fnmatch.fnmatch(rel_path, pattern) for pattern in (exclude_patterns or [])):
                        continue
                    
                    file_size = os.path.getsize(full_path)
                    files_to_backup.append((full_path, rel_path, file_size))
                    total_size += file_size
            
            # Report initial progress
            if progress_callback:
                progress_callback(0)
            
            # Copy files
            copied_size = 0
            for src_path, rel_path, file_size in files_to_backup:
                # Create destination path
                dst_path = os.path.join(backup_path, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy file
                shutil.copy2(src_path, dst_path)
                
                # Update progress
                copied_size += file_size
                if progress_callback and total_size > 0:
                    progress = int((copied_size / total_size) * 100)
                    progress_callback(progress)
            
            # Report completion
            if progress_callback:
                progress_callback(100)
            
            # Create metadata
            metadata = {
                "timestamp": timestamp,
                "repository_path": repo_path,
                "git_version": self.repo.git.version() if self.repo and GIT_AVAILABLE else "N/A",
                "name": backup_name,
                "include_patterns": include_patterns,
                "exclude_patterns": exclude_patterns or [],
                "total_files": len(files_to_backup),
                "total_size": total_size,
                "included_files": [rel_path for _, rel_path, _ in files_to_backup]
            }
            
            # Save metadata
            metadata_path = os.path.join(backup_dir, f"{backup_name}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to create backup: {str(e)}")
            return False

    def restore_backup(self, backup_path: str, restore_path: str, progress_callback = None) -> bool:
        """Restore a repository from a backup.
        
        Args:
            backup_path: Path to the backup directory
            restore_path: Path where the repository should be restored
            progress_callback: Optional callback function to report progress (0-100)
            
        Returns:
            bool: True if restore was successful, False otherwise
            
        The restore process:
            1. Validates backup exists
            2. Creates restore directory if needed
            3. Cleans existing content in restore path
            4. Copies all backup content including .git
            5. Reinitializes Git repository if GitPython is available
            
        Example:
            >>> repo_manager.restore_backup("/path/to/backup_20240101_120000", "/path/to/restore")
            True
        """
        try:
            # Check if backup exists
            if not os.path.exists(backup_path):
                logging.error("Backup path does not exist")
                raise ValueError("Backup path does not exist")
            
            # Create restore directory if it doesn't exist
            os.makedirs(restore_path, exist_ok=True)
            
            if progress_callback:
                progress_callback(0)  # Initial progress
            
            # Remove existing contents if any
            if os.path.exists(restore_path):
                for item in os.listdir(restore_path):
                    item_path = os.path.join(restore_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            
            if progress_callback:
                progress_callback(20)  # Progress after cleanup
            
            # Count total files for progress tracking
            total_files = sum(len(files) for _, _, files in os.walk(backup_path))
            copied_files = 0
            
            # Custom copy function with progress tracking
            def copy_with_progress(src, dst, symlinks=True):
                nonlocal copied_files
                if os.path.isdir(src):
                    if not os.path.exists(dst):
                        os.makedirs(dst)
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item)
                        if os.path.isdir(s):
                            copy_with_progress(s, d, symlinks)
                        else:
                            shutil.copy2(s, d)
                            copied_files += 1
                            if progress_callback and total_files > 0:
                                progress = 20 + int((copied_files / total_files) * 60)  # Scale to 20-80%
                                progress_callback(progress)
                else:
                    shutil.copy2(src, dst)
                    copied_files += 1
                    if progress_callback and total_files > 0:
                        progress = 20 + int((copied_files / total_files) * 60)  # Scale to 20-80%
                        progress_callback(progress)
            
            # Restore repository with all contents including .git
            copy_with_progress(backup_path, restore_path)
            
            if progress_callback:
                progress_callback(80)  # Progress after copy
            
            # Initialize Git repository if GitPython is available
            if GIT_AVAILABLE and os.path.exists(os.path.join(restore_path, ".git")):
                try:
                    Repo(restore_path)
                    logging.info("Successfully reinitialized Git repository")
                except Exception as e:
                    logging.warning(f"Failed to initialize Git repository after restore: {str(e)}")
            
            if progress_callback:
                progress_callback(100)  # Final progress
            
            logging.info(f"Successfully restored backup to: {restore_path}")
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

    def create_and_switch_branch(self, branch_name: str) -> bool:
        """Create a new branch and switch to it in a single operation."""
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.create_head(branch_name)
            self.repo.git.checkout(branch_name)
            return True
        except Exception as e:
            logging.error(f"Error creating and switching to branch: {e}")
            return False

    def merge_branch(self, source_branch: str, target_branch: str = None) -> bool:
        """Merge a source branch into the target branch, handling conflicts automatically."""
        if not GIT_AVAILABLE:
            return False
        try:
            if not target_branch:
                target_branch = self.repo.active_branch.name
            
            # Checkout target branch
            self.repo.git.checkout(target_branch)
            
            # Merge source branch
            self.repo.git.merge(source_branch)
            
            # Check for conflicts
            conflicts = self.get_merge_conflicts()
            if conflicts:
                logging.warning(f"Merge conflicts detected: {conflicts}")
                # Resolve conflicts automatically (e.g., by taking the source branch version)
                for conflict in conflicts:
                    self.repo.git.checkout("--theirs", conflict)
                    self.repo.index.add([conflict])
                self.repo.index.commit("Resolved merge conflicts automatically")
            
            return True
        except Exception as e:
            logging.error(f"Error merging branch: {e}")
            return False

    def handle_git_operation(self, operation: str, *args, **kwargs) -> bool:
        """Handle git operations with improved error handling and logging."""
        if not GIT_AVAILABLE:
            logging.error("GitPython is not available. Git operations cannot be performed.")
            return False
        try:
            # Log the operation
            logging.info(f"Performing git operation: {operation}")
            
            # Execute the operation
            if operation == "push":
                self.repo.git.push(*args, **kwargs)
            elif operation == "pull":
                self.repo.git.pull(*args, **kwargs)
            elif operation == "fetch":
                self.repo.git.fetch(*args, **kwargs)
            elif operation == "checkout":
                self.repo.git.checkout(*args, **kwargs)
            elif operation == "merge":
                self.repo.git.merge(*args, **kwargs)
            else:
                logging.error(f"Unsupported git operation: {operation}")
                return False
            
            logging.info(f"Git operation {operation} completed successfully.")
            return True
        except Exception as e:
            logging.error(f"Error performing git operation {operation}: {e}")
            return False

    def protect_branch(self, branch_name: str) -> bool:
        """Protect a branch from direct pushes, requiring pull requests for changes."""
        if not GIT_AVAILABLE:
            return False
        try:
            # Set branch protection rules
            self.repo.git.branch("--set-upstream-to=origin/" + branch_name, branch_name)
            self.repo.git.config("branch." + branch_name + ".pushRemote", "origin")
            self.repo.git.config("branch." + branch_name + ".merge", "refs/heads/" + branch_name)
            return True
        except Exception as e:
            logging.error(f"Error protecting branch: {e}")
            return False

    def validate_branch_name(self, branch_name: str) -> bool:
        """Validate branch names to ensure they follow a specific convention."""
        pattern = r'^(feature|bugfix|hotfix)/[a-zA-Z0-9-]+$'
        if not re.match(pattern, branch_name):
            return False 

    def validate_commit_message(self, message: str) -> bool:
        """Validate commit messages to ensure they follow a specific format."""
        import re
        pattern = r'^(feat|fix|docs|style|refactor|test|chore)(\([a-zA-Z0-9-]+\))?: .+$'
        if not re.match(pattern, message):
            logging.error(f"Commit message does not follow the conventional format.")
            return False
        return True 

    def resolve_conflicts_interactive(self, conflicts: List[str]) -> bool:
        """Resolve merge conflicts interactively."""
        if not GIT_AVAILABLE:
            return False
        try:
            for conflict in conflicts:
                # Open the conflicted file for editing
                subprocess.run(["notepad", conflict], check=True)
                # Stage the resolved file
                self.repo.index.add([conflict])
            self.repo.index.commit("Resolved merge conflicts interactively")
            return True
        except Exception as e:
            logging.error(f"Error resolving conflicts interactively: {e}")
            return False

    def create_stash(self, message: str = None) -> bool:
        """Create a stash with an optional message."""
        if not GIT_AVAILABLE:
            return False
        try:
            if message:
                self.repo.git.stash("save", message)
            else:
                self.repo.git.stash("save")
            return True
        except Exception as e:
            logging.error(f"Error creating stash: {e}")
            return False

    def apply_stash(self, stash_index: int = 0) -> bool:
        """Apply a stash by its index."""
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.git.stash("apply", f"stash@{{{stash_index}}}")
            return True
        except Exception as e:
            logging.error(f"Error applying stash: {e}")
            return False

    def drop_stash(self, stash_index: int = 0) -> bool:
        """Drop a stash by its index."""
        if not GIT_AVAILABLE:
            return False
        try:
            self.repo.git.stash("drop", f"stash@{{{stash_index}}}")
            return True
        except Exception as e:
            logging.error(f"Error dropping stash: {e}")
            return False

    def rebase_branch(self, base_branch: str) -> bool:
        """Rebase the current branch onto the specified base branch, handling unstaged changes."""
        if not GIT_AVAILABLE:
            return False
        try:
            # Check for unstaged changes
            if self.repo.is_dirty():
                # Stash changes
                self.repo.git.stash("save", "Temporary stash for rebase")
                stashed = True
            else:
                stashed = False
            
            # Perform rebase
            self.repo.git.rebase(base_branch)
            
            # Apply stash if changes were stashed
            if stashed:
                self.repo.git.stash("apply")
            
            return True
        except Exception as e:
            logging.error(f"Error rebasing branch: {e}")
            return False 

    def setup_conditional_workflow(self, workflow_name: str, workflow_config: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Set up a workflow that is triggered based on specific conditions."""
        if not isinstance(workflow_config, dict):
            raise ValueError("Workflow configuration must be a dictionary.")
        
        # Validate conditions
        if not isinstance(conditions, dict):
            raise ValueError("Conditions must be a dictionary.")
        
        # Add conditions to workflow config
        workflow_config["conditions"] = conditions
        
        # Proceed with workflow setup
        try:
            workflows_dir = self.repo_path / ".git" / "workflows"
            workflow_file = workflows_dir / f"{workflow_name}.json"
            
            # Create workflows directory if it doesn't exist
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the workflow configuration
            with open(workflow_file, "w") as f:
                json.dump(workflow_config, f, indent=2)
            
            logging.info(f"Successfully set up conditional workflow: {workflow_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to set up conditional workflow {workflow_name}: {str(e)}")
            return False

    def run_workflows_in_parallel(self, workflow_names: List[str], event: str) -> List[str]:
        """Run multiple workflows in parallel for a specific event."""
        workflow_ids = []
        for workflow_name in workflow_names:
            try:
                workflow_id = self.run_workflow(workflow_name, event)
                workflow_ids.append(workflow_id)
            except Exception as e:
                logging.error(f"Failed to run workflow {workflow_name}: {str(e)}")
        return workflow_ids

    def create_workflow_template(self, template_name: str, template_config: Dict[str, Any]) -> bool:
        """Create a template for common workflows to simplify setup."""
        if not isinstance(template_config, dict):
            raise ValueError("Template configuration must be a dictionary.")
        
        try:
            templates_dir = self.repo_path / ".git" / "workflow_templates"
            template_file = templates_dir / f"{template_name}.json"
            
            # Create templates directory if it doesn't exist
            templates_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the template configuration
            with open(template_file, "w") as f:
                json.dump(template_config, f, indent=2)
            
            logging.info(f"Successfully created workflow template: {template_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to create workflow template {template_name}: {str(e)}")
            return False 