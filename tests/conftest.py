import pytest
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_repo_path(tmp_path_factory):
    """
    Create a temporary git repository for testing
    """
    repo_path = tmp_path_factory.mktemp("test_repo")
    os.system(f"git init {repo_path}")
    return str(repo_path)

@pytest.fixture(scope="session")
def test_code_file(test_repo_path):
    """
    Create a test code file in the repository
    """
    file_path = Path(test_repo_path) / "test.py"
    with open(file_path, "w") as f:
        f.write("""
def add(a, b):
    return a + b
        """)
    return str(file_path)

@pytest.fixture(scope="session")
def gemini_api_key():
    """
    Get the Gemini API key from environment variable
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY environment variable not set")
    return api_key 