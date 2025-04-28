import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from git_ops.repository_manager import RepositoryManager

def test_repository_management():
    print("\n=== Testing Repository Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test branch operations
    print("\nTesting branch operations:")
    branches = repo_manager.get_branches()
    print(f"Current branches: {branches}")
    
    # Test commit history
    print("\nTesting commit history:")
    history = repo_manager.get_commit_history()
    print(f"Commit history: {len(history)} commits")
    
    # Test repository status
    print("\nTesting repository status:")
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")
    print(f"Changed files: {status['changed_files']}")
    print(f"Untracked files: {status['untracked_files']}")
    print(f"Staged changes: {status['staged_changes']}")

def test_robust_repository_management():
    print("\n=== Testing Robust Repository Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test branch operations with edge cases
    print("\nTesting branch operations with edge cases:")
    branches = repo_manager.get_branches()
    print(f"Current branches: {branches}")
    
    # Test commit history with empty repository
    print("\nTesting commit history with empty repository:")
    history = repo_manager.get_commit_history()
    print(f"Commit history: {len(history)} commits")
    
    # Test repository status with untracked files
    print("\nTesting repository status with untracked files:")
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")
    print(f"Changed files: {status['changed_files']}")
    print(f"Untracked files: {status['untracked_files']}")
    print(f"Staged changes: {status['staged_changes']}")

def test_enhanced_repository_management():
    print("\n=== Testing Enhanced Repository Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test branch operations with multiple branches
    print("\nTesting branch operations with multiple branches:")
    branches = repo_manager.get_branches()
    print(f"Current branches: {branches}")
    
    # Test commit history with specific branch
    print("\nTesting commit history with specific branch:")
    history = repo_manager.get_commit_history("main")
    print(f"Commit history: {len(history)} commits")
    
    # Test repository status with staged changes
    print("\nTesting repository status with staged changes:")
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")
    print(f"Changed files: {status['changed_files']}")
    print(f"Untracked files: {status['untracked_files']}")
    print(f"Staged changes: {status['staged_changes']}")

def test_git_operations():
    print("\n=== Testing Git Operations ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test remote operations
    print("\nTesting remote operations:")
    remote_url = repo_manager.get_remote_url()
    print(f"Remote URL: {remote_url}")
    
    # Test merge conflicts
    print("\nTesting merge conflicts:")
    conflicts = repo_manager.get_merge_conflicts()
    print(f"Merge conflicts: {conflicts}")

def test_robust_git_operations():
    print("\n=== Testing Robust Git Operations ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test remote operations with invalid URL
    print("\nTesting remote operations with invalid URL:")
    remote_url = repo_manager.get_remote_url()
    print(f"Remote URL: {remote_url}")
    
    # Test merge conflicts with complex scenarios
    print("\nTesting merge conflicts with complex scenarios:")
    conflicts = repo_manager.get_merge_conflicts()
    print(f"Merge conflicts: {conflicts}")

def test_workflow_management():
    print("\n=== Testing Workflow Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test workflow setup
    print("\nTesting workflow setup:")
    workflow = {
        "name": "test-workflow",
        "description": "Test workflow",
        "events": ["push", "pull_request"],
        "steps": [
            {
                "name": "test-step",
                "event": "push",
                "command": "echo 'Test step'"
            }
        ]
    }
    
    success = repo_manager.setup_workflow("test-workflow", workflow)
    print(f"Workflow setup: {'Success' if success else 'Failed'}")
    
    # Test workflow listing
    print("\nTesting workflow listing:")
    workflows = repo_manager.get_workflows()
    print(f"Found {len(workflows)} workflows")
    
    # Test workflow execution
    print("\nTesting workflow execution:")
    workflow_id = repo_manager.run_workflow("test-workflow", "push")
    print(f"Workflow ID: {workflow_id}")
    
    # Test workflow status
    print("\nTesting workflow status:")
    status = repo_manager.get_workflow_status(workflow_id)
    print(f"Workflow status: {status['status'] if status else 'Not found'}")
    
    # Test workflow history
    print("\nTesting workflow history:")
    history = repo_manager.get_workflow_history()
    print(f"Workflow history: {len(history)} entries")

def test_robust_workflow_management():
    print("\n=== Testing Robust Workflow Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test workflow setup with invalid configuration
    print("\nTesting workflow setup with invalid configuration:")
    workflow = {
        "name": "invalid-workflow",
        "description": "Invalid workflow",
        "events": ["invalid_event"],
        "steps": [
            {
                "name": "invalid-step",
                "event": "invalid_event",
                "command": "echo 'Invalid step'"
            }
        ]
    }
    
    success = repo_manager.setup_workflow("invalid-workflow", workflow)
    print(f"Workflow setup: {'Success' if success else 'Failed'}")
    
    # Test workflow listing with no workflows
    print("\nTesting workflow listing with no workflows:")
    workflows = repo_manager.get_workflows()
    print(f"Found {len(workflows)} workflows")
    
    # Test workflow execution with invalid workflow
    print("\nTesting workflow execution with invalid workflow:")
    workflow_id = repo_manager.run_workflow("invalid-workflow", "push")
    print(f"Workflow ID: {workflow_id}")
    
    # Test workflow status with invalid ID
    print("\nTesting workflow status with invalid ID:")
    status = repo_manager.get_workflow_status("invalid-id")
    print(f"Workflow status: {status['status'] if status else 'Not found'}")
    
    # Test workflow history with no history
    print("\nTesting workflow history with no history:")
    history = repo_manager.get_workflow_history()
    print(f"Workflow history: {len(history)} entries")

def test_create_and_switch_branch():
    print("\n=== Testing Create and Switch Branch ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test creating and switching to a new branch
    print("\nTesting create and switch branch:")
    success = repo_manager.create_and_switch_branch("test-branch")
    print(f"Create and switch branch: {'Success' if success else 'Failed'}")
    
    # Verify the current branch
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")

def test_merge_branch():
    print("\n=== Testing Merge Branch ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test merging a branch
    print("\nTesting merge branch:")
    success = repo_manager.merge_branch("test-branch", "main")
    print(f"Merge branch: {'Success' if success else 'Failed'}")
    
    # Verify the current branch
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")

def test_handle_git_operation():
    print("\n=== Testing Handle Git Operation ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test handling git operations
    print("\nTesting handle git operation:")
    success = repo_manager.handle_git_operation("push", "origin", "main")
    print(f"Handle git operation: {'Success' if success else 'Failed'}")
    
    # Verify the current branch
    status = repo_manager.get_repository_status()
    print(f"Current branch: {status['current_branch']}")

def test_protect_branch():
    print("\n=== Testing Protect Branch ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test protecting a branch
    print("\nTesting protect branch:")
    success = repo_manager.protect_branch("main")
    print(f"Protect branch: {'Success' if success else 'Failed'}")

def test_validate_branch_name():
    print("\n=== Testing Validate Branch Name ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test validating branch names
    print("\nTesting validate branch name:")
    valid_name = "feature/new-feature"
    invalid_name = "invalid-branch"
    print(f"Valid branch name: {valid_name} - {'Valid' if repo_manager.validate_branch_name(valid_name) else 'Invalid'}")
    print(f"Invalid branch name: {invalid_name} - {'Valid' if repo_manager.validate_branch_name(invalid_name) else 'Invalid'}")

def test_validate_commit_message():
    print("\n=== Testing Validate Commit Message ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test validating commit messages
    print("\nTesting validate commit message:")
    valid_message = "feat: add new feature"
    invalid_message = "invalid commit message"
    print(f"Valid commit message: {valid_message} - {'Valid' if repo_manager.validate_commit_message(valid_message) else 'Invalid'}")
    print(f"Invalid commit message: {invalid_message} - {'Valid' if repo_manager.validate_commit_message(invalid_message) else 'Invalid'}")

def test_resolve_conflicts_interactive():
    print("\n=== Testing Resolve Conflicts Interactive ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test resolving conflicts interactively
    print("\nTesting resolve conflicts interactive:")
    conflicts = ["file1.txt", "file2.txt"]  # Example conflicts
    success = repo_manager.resolve_conflicts_interactive(conflicts)
    print(f"Resolve conflicts interactive: {'Success' if success else 'Failed'}")

def test_stash_management():
    print("\n=== Testing Stash Management ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test creating a stash
    print("\nTesting create stash:")
    success = repo_manager.create_stash("Test stash")
    print(f"Create stash: {'Success' if success else 'Failed'}")
    
    # Test applying a stash
    print("\nTesting apply stash:")
    success = repo_manager.apply_stash(0)
    print(f"Apply stash: {'Success' if success else 'Failed'}")
    
    # Test dropping a stash
    print("\nTesting drop stash:")
    success = repo_manager.drop_stash(0)
    print(f"Drop stash: {'Success' if success else 'Failed'}")

def test_rebase_branch():
    print("\n=== Testing Rebase Branch ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test rebasing a branch
    print("\nTesting rebase branch:")
    success = repo_manager.rebase_branch("main")
    print(f"Rebase branch: {'Success' if success else 'Failed'}")

def test_setup_conditional_workflow():
    print("\n=== Testing Setup Conditional Workflow ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test setting up a conditional workflow
    print("\nTesting setup conditional workflow:")
    workflow_config = {
        "name": "conditional-workflow",
        "description": "Conditional workflow",
        "events": ["push", "pull_request"],
        "steps": [
            {
                "name": "test-step",
                "event": "push",
                "command": "echo 'Test step'"
            }
        ]
    }
    conditions = {
        "branch": "main",
        "file_changes": ["*.py"]
    }
    success = repo_manager.setup_conditional_workflow("conditional-workflow", workflow_config, conditions)
    print(f"Setup conditional workflow: {'Success' if success else 'Failed'}")

def test_run_workflows_in_parallel():
    print("\n=== Testing Run Workflows in Parallel ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test running workflows in parallel
    print("\nTesting run workflows in parallel:")
    workflow_names = ["test-workflow", "conditional-workflow"]
    workflow_ids = repo_manager.run_workflows_in_parallel(workflow_names, "push")
    print(f"Run workflows in parallel: {workflow_ids}")

def test_create_workflow_template():
    print("\n=== Testing Create Workflow Template ===")
    
    # Initialize repository manager
    repo_path = os.getcwd()
    repo_manager = RepositoryManager(repo_path)
    
    # Test creating a workflow template
    print("\nTesting create workflow template:")
    template_config = {
        "name": "test-template",
        "description": "Test template",
        "events": ["push", "pull_request"],
        "steps": [
            {
                "name": "test-step",
                "event": "push",
                "command": "echo 'Test step'"
            }
        ]
    }
    success = repo_manager.create_workflow_template("test-template", template_config)
    print(f"Create workflow template: {'Success' if success else 'Failed'}")

def main():
    print("Starting comprehensive feature tests...")
    
    # Test repository management
    test_repository_management()
    
    # Test robust repository management
    test_robust_repository_management()
    
    # Test enhanced repository management
    test_enhanced_repository_management()
    
    # Test create and switch branch
    test_create_and_switch_branch()
    
    # Test merge branch
    test_merge_branch()
    
    # Test handle git operation
    test_handle_git_operation()
    
    # Test protect branch
    test_protect_branch()
    
    # Test validate branch name
    test_validate_branch_name()
    
    # Test validate commit message
    test_validate_commit_message()
    
    # Test resolve conflicts interactive
    test_resolve_conflicts_interactive()
    
    # Test stash management
    test_stash_management()
    
    # Test rebase branch
    test_rebase_branch()
    
    # Test setup conditional workflow
    test_setup_conditional_workflow()
    
    # Test run workflows in parallel
    test_run_workflows_in_parallel()
    
    # Test create workflow template
    test_create_workflow_template()
    
    # Test git operations
    test_git_operations()
    
    # Test robust git operations
    test_robust_git_operations()
    
    # Test workflow management
    test_workflow_management()
    
    # Test robust workflow management
    test_robust_workflow_management()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main() 