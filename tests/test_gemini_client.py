import pytest
from src import GeminiClient

pytestmark = pytest.mark.asyncio

@pytest.fixture
def gemini_client():
    return GeminiClient()

async def test_analyze_code(gemini_client):
    test_code = """
    def add(a, b):
        return a + b
    """
    result = await gemini_client.analyze_code(test_code)
    assert "analysis" in result
    assert isinstance(result["analysis"], str)

async def test_generate_documentation(gemini_client):
    test_code = """
    def add(a, b):
        return a + b
    """
    result = await gemini_client.generate_documentation(test_code)
    assert isinstance(result, str)
    assert len(result) > 0

async def test_suggest_improvements(gemini_client):
    test_code = """
    def add(a, b):
        return a + b
    """
    result = await gemini_client.suggest_improvements(test_code)
    assert isinstance(result, list)
    assert len(result) > 0 