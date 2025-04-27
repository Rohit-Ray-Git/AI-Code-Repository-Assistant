import pytest
from src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_review_pull_request(client):
    changes = {
        "test.py": """
def add(a, b):
    return a + b
        """,
        "test2.py": """
def multiply(a, b):
    return a * b
        """
    }
    response = client.post("/api/v1/review-pull-request", json={"changes": changes})
    assert response.status_code == 200
    data = response.json
    assert "test.py" in data
    assert "test2.py" in data
    assert "analysis" in data["test.py"]
    assert "suggestions" in data["test.py"]

def test_generate_review_comments(client):
    changes = {
        "test.py": """
def add(a, b):
    return a + b
        """
    }
    response = client.post("/api/v1/generate-review-comments", json={"changes": changes})
    assert response.status_code == 200
    data = response.json
    assert "comments" in data
    assert len(data["comments"]) > 0
    assert all("file" in comment for comment in data["comments"])
    assert all("comment" in comment for comment in data["comments"])

def test_check_code_quality(client):
    code = """
def add(a, b):
    return a + b
    """
    response = client.post("/api/v1/check-code-quality", json={"code": code})
    assert response.status_code == 200
    data = response.json
    assert "quality_score" in data
    assert "issues" in data
    assert "suggestions" in data

def test_detect_bugs(client):
    code = """
def divide(a, b):
    return a / b  # Potential division by zero
    """
    response = client.post("/api/v1/detect-bugs", json={"code": code})
    assert response.status_code == 200
    data = response.json
    assert "bugs" in data
    assert len(data["bugs"]) > 0
    assert all("type" in bug for bug in data["bugs"])
    assert all("description" in bug for bug in data["bugs"])
    assert all("severity" in bug for bug in data["bugs"]) 