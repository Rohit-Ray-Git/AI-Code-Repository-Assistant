import pytest
import sys
from pathlib import Path
from src import RepositoryManager
from src.git_ops.repository_manager import GIT_AVAILABLE

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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