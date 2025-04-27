from setuptools import setup, find_packages
import os

# Read README.md if it exists
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="ai-code-repo-assistant",
    version="1.0.0",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "python-dotenv>=1.0.0",
        "gitpython>=3.1.40",
        "pydantic>=2.4.2",
        "google-generativeai>=0.3.1",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "pytest>=7.4.3",
        "black>=23.11.0",
        "isort>=5.12.0",
        "flake8>=6.1.0",
        "pydantic-settings>=2.0.0",
    ],
    python_requires=">=3.9",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered coding assistant for repository management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-code-repo-assistant",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 