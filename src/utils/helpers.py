import os
from typing import List, Dict, Any
from pathlib import Path

def validate_repo_path(repo_path: str) -> bool:
    """
    Validate if the given path is a valid git repository
    """
    try:
        path = Path(repo_path)
        return path.exists() and (path / ".git").exists()
    except Exception:
        return False

def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path
    """
    return os.path.splitext(file_path)[1].lower()

def is_code_file(file_path: str) -> bool:
    """
    Check if the file is a code file based on its extension
    """
    code_extensions = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
        '.cs', '.go', '.rb', '.php', '.swift', '.kt', '.rs'
    }
    return get_file_extension(file_path) in code_extensions

def format_error_message(error: Exception) -> Dict[str, Any]:
    """
    Format error message for API response
    """
    return {
        "error": str(error),
        "type": error.__class__.__name__
    } 