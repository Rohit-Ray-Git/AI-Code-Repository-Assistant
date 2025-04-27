import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_review_pull_request():
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
    response = requests.post(f"{BASE_URL}/review-pull-request", json={"changes": changes})
    print("\n=== Review Pull Request ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_generate_review_comments():
    changes = {
        "test.py": """
def add(a, b):
    return a + b
        """
    }
    response = requests.post(f"{BASE_URL}/generate-review-comments", json={"changes": changes})
    print("\n=== Generate Review Comments ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_check_code_quality():
    code = """
def add(a, b):
    return a + b
    """
    response = requests.post(f"{BASE_URL}/check-code-quality", json={"code": code})
    print("\n=== Check Code Quality ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_detect_bugs():
    code = """
def divide(a, b):
    return a / b  # Potential division by zero
    """
    response = requests.post(f"{BASE_URL}/detect-bugs", json={"code": code})
    print("\n=== Detect Bugs ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing API Endpoints...")
    test_review_pull_request()
    test_generate_review_comments()
    test_check_code_quality()
    test_detect_bugs() 