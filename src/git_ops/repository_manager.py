import os
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from gitpython import Repo, Git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    print("Warning: gitpython not available. Git operations will be limited.")

class RepositoryManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        if GIT_AVAILABLE:
            try:
                self.repo = Repo(repo_path)
            except:
                self.repo = None
        else:
            self.repo = None

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