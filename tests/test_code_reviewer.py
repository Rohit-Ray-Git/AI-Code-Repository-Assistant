import pytest
from src.ai.code_reviewer import CodeReviewer

pytestmark = pytest.mark.asyncio

@pytest.fixture
def code_reviewer():
    return CodeReviewer()

@pytest.fixture
def sample_changes():
    return {
        "test.py": """
def add(a, b):
    return a + b
        """,
        "test2.py": """
def multiply(a, b):
    return a * b
        """
    }

async def test_review_pull_request(code_reviewer, sample_changes):
    results = await code_reviewer.review_pull_request(sample_changes)
    assert isinstance(results, dict)
    assert "test.py" in results
    assert "test2.py" in results
    assert "analysis" in results["test.py"]
    assert "suggestions" in results["test.py"]

async def test_generate_review_comments(code_reviewer, sample_changes):
    comments = await code_reviewer.generate_review_comments(sample_changes)
    assert isinstance(comments, list)
    assert len(comments) == 2
    assert all("file" in comment for comment in comments)
    assert all("comment" in comment for comment in comments)

async def test_check_code_quality(code_reviewer):
    code = """
def add(a, b):
    return a + b
    """
    quality = await code_reviewer.check_code_quality(code)
    assert isinstance(quality, dict)
    assert "quality_score" in quality
    assert "issues" in quality
    assert "suggestions" in quality

async def test_detect_potential_bugs(code_reviewer):
    code = """
def divide(a, b):
    return a / b  # Potential division by zero
    """
    bugs = await code_reviewer.detect_potential_bugs(code)
    assert isinstance(bugs, list)
    assert len(bugs) > 0
    assert all("type" in bug for bug in bugs)
    assert all("description" in bug for bug in bugs)
    assert all("severity" in bug for bug in bugs) 