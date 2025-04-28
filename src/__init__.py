"""
AI Code Repository Assistant package.
"""

from .ai.gemini_client import GeminiClient
from .ai.code_reviewer import CodeReviewer
from .git_ops.repository_manager import RepositoryManager
from .core.config import Settings, get_settings

__version__ = "0.1.0"

__all__ = [
    "GeminiClient",
    "CodeReviewer",
    "RepositoryManager",
    "Settings",
    "get_settings",
] 