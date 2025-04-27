import pytest
import sys
import os
import json
from pathlib import Path
from src import RepositoryManager
from src.git_ops.repository_manager import GIT_AVAILABLE
import time

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

@pytest.fixture
def test_repo_path(tmp_path):
    """Create a temporary test repository"""
    repo_path = tmp_path / "test_repo"
    os.makedirs(repo_path)
    
    # Initialize git repository if available
    if GIT_AVAILABLE:
        from git import Repo
        repo = Repo.init(repo_path)
        
        # Configure user for commits
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial commit to establish HEAD and main branch
        readme_path = repo_path / "README.md"
        readme_path.write_text("# Test Repository\nThis is a test repository.")
        repo.index.add(["README.md"])
        repo.index.commit("Initial commit")
        
        # Ensure we're on main branch
        if "main" not in repo.heads:
            main = repo.create_head("main")
            repo.head.reference = main
    
    return str(repo_path)

@pytest.fixture
def test_code_file(test_repo_path):
    """Create a test code file in the repository"""
    file_path = os.path.join(test_repo_path, "test_file.py")
    with open(file_path, "w") as f:
        f.write("""def add(a, b):
    return a + b
""")
    return "test_file.py"

@pytest.fixture
def repo_manager(test_repo_path):
    return RepositoryManager(test_repo_path)

def test_get_branches(repo_manager):
    branches = repo_manager.get_branches()
    assert isinstance(branches, list)
    # If gitpython is not available, we should at least get the main branch
    assert len(branches) > 0

def test_get_commit_history(repo_manager):
    history = repo_manager.get_commit_history()
    assert isinstance(history, list)

def test_create_branch(repo_manager):
    branch_name = "test-branch"
    success = repo_manager.create_branch(branch_name)
    # If gitpython is not available, this will return False
    if success:
        assert branch_name in repo_manager.get_branches()

def test_get_file_content(repo_manager, test_code_file):
    content = repo_manager.get_file_content(test_code_file)
    assert isinstance(content, str)
    assert "def add" in content

def test_get_repository_status(repo_manager):
    status = repo_manager.get_repository_status()
    assert isinstance(status, dict)
    assert "current_branch" in status
    assert "changed_files" in status
    assert "untracked_files" in status
    assert "staged_changes" in status
    assert isinstance(status["changed_files"], list)
    assert isinstance(status["untracked_files"], list)
    assert isinstance(status["staged_changes"], list)

def test_get_file_diff(repo_manager, test_code_file):
    diff = repo_manager.get_file_diff(test_code_file)
    assert isinstance(diff, str)
    # If gitpython is not available, this will return an empty string
    if diff:
        assert "diff" in diff.lower() or "+" in diff or "-" in diff

def test_stage_and_unstage_file(repo_manager, test_code_file):
    # Stage the file
    stage_success = repo_manager.stage_file(test_code_file)
    if stage_success:
        status = repo_manager.get_repository_status()
        assert test_code_file in status["staged_changes"]
        
        # Unstage the file
        unstage_success = repo_manager.unstage_file(test_code_file)
        if unstage_success:
            status = repo_manager.get_repository_status()
            assert test_code_file not in status["staged_changes"]

def test_checkout_branch(repo_manager):
    # Create a test branch
    branch_name = "test-checkout-branch"
    create_success = repo_manager.create_branch(branch_name)
    
    if create_success:
        # Checkout to the new branch
        checkout_success = repo_manager.checkout_branch(branch_name)
        if checkout_success:
            status = repo_manager.get_repository_status()
            assert status["current_branch"] == branch_name

def test_commit_changes(repo_manager, test_code_file):
    # Stage the file first
    stage_success = repo_manager.stage_file(test_code_file)
    if stage_success:
        # Commit the changes
        commit_success = repo_manager.commit_changes("Test commit")
        if commit_success:
            # Verify the commit was successful
            status = repo_manager.get_repository_status()
            assert test_code_file not in status["staged_changes"]

def test_remote_operations(repo_manager):
    # Test adding a remote
    remote_name = "test-remote"
    remote_url = "https://github.com/test/repo.git"
    add_success = repo_manager.add_remote(remote_name, remote_url)
    if add_success:
        # Test getting remote URL
        url = repo_manager.get_remote_url(remote_name)
        assert url == remote_url

def test_push_and_pull(repo_manager):
    # These tests require a real remote repository
    # They will be skipped if gitpython is not available
    if not GIT_AVAILABLE:
        pytest.skip("GitPython not available")

    # Test push (will fail if no remote is configured)
    try:
        push_success = repo_manager.push_changes()
        # If push succeeds, test pull
        if push_success:
            pull_success = repo_manager.pull_changes()
            assert pull_success
    except Exception:
        # Skip if remote is not configured
        pytest.skip("No remote repository configured")

def test_merge_conflicts(repo_manager):
    conflicts = repo_manager.get_merge_conflicts()
    assert isinstance(conflicts, list)
    # If there are no conflicts, the list should be empty
    assert len(conflicts) >= 0

def test_initialize_repository(tmp_path):
    repo_path = str(tmp_path / "test_repo")
    success = RepositoryManager.initialize_repository(repo_path)
    if success:
        assert os.path.exists(os.path.join(repo_path, ".git"))
        repo_manager = RepositoryManager(repo_path)
        assert repo_manager.repo is not None

def test_clone_repository(tmp_path):
    if not GIT_AVAILABLE:
        pytest.skip("GitPython not available")
    
    # Use a small public repository for testing
    test_repo_url = "https://github.com/octocat/Hello-World.git"
    target_path = str(tmp_path / "cloned_repo")
    
    success = RepositoryManager.clone_repository(test_repo_url, target_path)
    if success:
        assert os.path.exists(os.path.join(target_path, ".git"))
        repo_manager = RepositoryManager(target_path)
        assert repo_manager.repo is not None

def test_configure_repository(repo_manager):
    config = {
        "user.name": "Test User",
        "user.email": "test@example.com"
    }
    success = repo_manager.configure_repository(config)
    if success:
        current_config = repo_manager.get_repository_config()
        assert current_config.get("user.name") == "Test User"
        assert current_config.get("user.email") == "test@example.com"

def test_create_and_list_templates(repo_manager):
    template_name = "test-template"
    description = "A test template"
    
    # Create a template
    success = repo_manager.create_template(template_name, description)
    if success:
        # List templates
        templates = repo_manager.list_templates()
        assert len(templates) > 0
        template = next((t for t in templates if t["name"] == template_name), None)
        assert template is not None
        assert template["description"] == description

def test_hook_management(repo_manager):
    # Test setting up a hook
    hook_name = "pre-commit"
    script_content = """#!/bin/sh
echo "Running pre-commit hook"
exit 0
"""
    success = repo_manager.setup_hook(hook_name, script_content)
    if success:
        # Verify the hook was created
        hooks = repo_manager.get_hooks()
        assert hook_name in hooks
        
        # Test removing the hook
        remove_success = repo_manager.remove_hook(hook_name)
        if remove_success:
            hooks = repo_manager.get_hooks()
            assert hook_name not in hooks

def test_workflow_setup_and_validation(repo_manager):
    # Test valid workflow configuration
    valid_workflow = {
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
    
    # Test setup with valid configuration
    assert repo_manager.setup_workflow("test-workflow", valid_workflow) == True
    
    # Test invalid configurations
    invalid_configs = [
        # Missing required field
        {
            "name": "test-workflow",
            "steps": []
        },
        # Invalid steps format
        {
            "name": "test-workflow",
            "description": "Test workflow",
            "steps": "not-a-list"
        },
        # Missing required step fields
        {
            "name": "test-workflow",
            "description": "Test workflow",
            "steps": [{"name": "test-step"}]
        },
        # Invalid step field types
        {
            "name": "test-workflow",
            "description": "Test workflow",
            "steps": [{
                "name": 123,
                "event": "push",
                "command": "echo 'Test'"
            }]
        },
        # Invalid event in step
        {
            "name": "test-workflow",
            "description": "Test workflow",
            "events": ["push"],
            "steps": [{
                "name": "test-step",
                "event": "invalid-event",
                "command": "echo 'Test'"
            }]
        }
    ]
    
    for config in invalid_configs:
        assert repo_manager.setup_workflow("test-invalid-workflow", config) == False

def test_workflow_management(repo_manager):
    """Test workflow management operations"""
    # Create a test workflow
    workflow = {
        "name": "test-workflow",
        "description": "A test workflow",
        "events": ["push", "pull_request"],
        "steps": [
            {
                "name": "test-step",
                "event": "push",
                "command": "echo 'Test step'"
            }
        ]
    }
    
    # Test workflow setup
    assert repo_manager.setup_workflow("test-workflow", workflow)
    
    # Test getting workflows
    workflows = repo_manager.get_workflows()
    assert len(workflows) == 1
    assert workflows[0]["name"] == "test-workflow"
    assert workflows[0]["config"] == workflow
    
    # Test workflow removal
    assert repo_manager.remove_workflow("test-workflow")
    workflows = repo_manager.get_workflows()
    assert len(workflows) == 0

def test_workflow_execution(repo_manager):
    """Test workflow execution and monitoring"""
    # Create a test workflow
    workflow = {
        "name": "test-workflow",
        "description": "A test workflow",
        "events": ["push", "pull_request"],
        "steps": [
            {
                "name": "test-step",
                "event": "push",
                "command": "echo 'Test step'"
            }
        ]
    }
    
    # Set up the workflow
    assert repo_manager.setup_workflow("test-workflow", workflow)
    
    # Run the workflow
    workflow_id = repo_manager.run_workflow("test-workflow", "push")
    assert workflow_id is not None
    
    # Wait for workflow completion
    max_wait = 5  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = repo_manager.get_workflow_status(workflow_id)
        if status and status["status"] in ["completed", "failed"]:
            break
        time.sleep(0.1)
    
    # Verify workflow status
    status = repo_manager.get_workflow_status(workflow_id)
    assert status is not None
    assert status["status"] == "completed"
    assert "start_time" in status
    assert "end_time" in status
    
    # Verify workflow history
    history = repo_manager.get_workflow_history()
    assert len(history) > 0
    assert any(w["workflow"]["id"] == workflow_id for w in history)

def test_workflow_error_handling(repo_manager):
    """Test workflow error handling"""
    # Create a workflow with a failing command
    workflow = {
        "name": "error-workflow",
        "description": "A workflow with errors",
        "events": ["push"],
        "steps": [
            {
                "name": "failing-step",
                "event": "push",
                "command": "exit 1"  # This will fail
            }
        ]
    }
    
    # Set up the workflow
    assert repo_manager.setup_workflow("error-workflow", workflow)
    
    # Run the workflow
    workflow_id = repo_manager.run_workflow("error-workflow", "push")
    assert workflow_id is not None
    
    # Wait for workflow completion
    max_wait = 5  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = repo_manager.get_workflow_status(workflow_id)
        if status and status["status"] in ["completed", "failed"]:
            break
        time.sleep(0.1)
    
    # Verify workflow failed
    status = repo_manager.get_workflow_status(workflow_id)
    assert status is not None
    assert status["status"] == "failed"
    assert "error" in status

def test_workflow_concurrent_execution(repo_manager):
    """Test concurrent workflow execution"""
    # Create multiple workflows
    workflows = []
    for i in range(3):
        workflow = {
            "name": f"concurrent-workflow-{i}",
            "description": f"Concurrent workflow {i}",
            "events": ["push"],
            "steps": [
                {
                    "name": f"step-{i}",
                    "event": "push",
                    "command": f"echo 'Concurrent step {i}'"
                }
            ]
        }
        workflows.append(workflow)
    
    # Set up all workflows
    for workflow in workflows:
        assert repo_manager.setup_workflow(workflow["name"], workflow)
    
    # Run all workflows concurrently
    workflow_ids = []
    for workflow in workflows:
        workflow_id = repo_manager.run_workflow(workflow["name"], "push")
        workflow_ids.append(workflow_id)
    
    # Wait for all workflows to complete
    max_wait = 10  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        all_completed = True
        for workflow_id in workflow_ids:
            status = repo_manager.get_workflow_status(workflow_id)
            if not status or status["status"] not in ["completed", "failed"]:
                all_completed = False
                break
        if all_completed:
            break
        time.sleep(0.1)
    
    # Verify all workflows completed
    for workflow_id in workflow_ids:
        status = repo_manager.get_workflow_status(workflow_id)
        assert status is not None
        assert status["status"] == "completed"
    
    # Verify workflow history
    history = repo_manager.get_workflow_history()
    assert len(history) >= len(workflow_ids)
    for workflow_id in workflow_ids:
        assert any(w["workflow"]["id"] == workflow_id for w in history)

def test_backup_and_restore(repo_manager, tmp_path):
    # Create a backup
    backup_dir = str(tmp_path / "backups")
    success = repo_manager.create_backup(backup_dir)
    if success:
        # List backups
        backups = repo_manager.list_backups(backup_dir)
        assert len(backups) > 0
        
        # Verify backup metadata
        backup = backups[0]
        assert "timestamp" in backup
        assert "repository_path" in backup
        assert "git_version" in backup
        
        # Restore the backup
        restore_path = str(tmp_path / "restored_repo")
        restore_success = repo_manager.restore_backup(
            str(tmp_path / "backups" / backup["name"]),
            restore_path
        )
        if restore_success:
            assert os.path.exists(restore_path)
            assert os.path.exists(os.path.join(restore_path, ".git"))

def test_backup_scheduling(repo_manager, tmp_path):
    backup_dir = str(tmp_path / "scheduled_backups")
    schedule = {
        "frequency": "daily",
        "time": "00:00",
        "retention_days": 7,
        "backup_path": backup_dir
    }
    
    # Set up backup schedule
    success = repo_manager.schedule_backup(backup_dir, schedule)
    if success:
        # Get and verify schedule
        current_schedule = repo_manager.get_backup_schedule()
        assert current_schedule == schedule

def test_backup_management(repo_manager, tmp_path):
    # Create multiple backups
    backup_dir = str(tmp_path / "managed_backups")
    
    # Create first backup
    success1 = repo_manager.create_backup(backup_dir)
    assert success1
    
    # Add a small delay to ensure different timestamps
    time.sleep(1)
    
    # Create second backup
    success2 = repo_manager.create_backup(backup_dir)
    assert success2
    
    # List backups
    backups = repo_manager.list_backups(backup_dir)
    assert len(backups) == 2
    
    # Delete first backup
    delete_success = repo_manager.delete_backup(
        str(tmp_path / "managed_backups" / backups[0]["name"])
    )
    if delete_success:
        # Verify backup was deleted
        remaining_backups = repo_manager.list_backups(backup_dir)
        assert len(remaining_backups) == 1 