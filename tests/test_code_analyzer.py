import pytest
from src.ai.code_analyzer import CodeAnalyzer

@pytest.fixture
def code_analyzer():
    return CodeAnalyzer()

def test_analyze_code_structure(code_analyzer):
    code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
    """
    structure = code_analyzer.analyze_code_structure(code)
    assert "functions" in structure
    assert "classes" in structure
    assert "imports" in structure
    assert "complexity" in structure
    assert len(structure["functions"]) == 1
    assert len(structure["classes"]) == 1

def test_find_code_issues(code_analyzer):
    code = """
def BadFunctionName():
    pass

class badClassName:
    def __init__(self):
        pass
    """
    issues = code_analyzer.find_code_issues(code)
    assert len(issues) > 0
    assert any(issue["type"] == "naming_convention" for issue in issues)

def test_get_line_numbers(code_analyzer):
    code = """
def function1():
    pass

def function2():
    pass
    """
    line_numbers = code_analyzer.get_line_numbers(code, r"def \w+")
    assert len(line_numbers) == 2
    assert line_numbers[0] == 2
    assert line_numbers[1] == 5

def test_check_function_length(code_analyzer):
    code = """
def long_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u
    """
    issues = code_analyzer.find_code_issues(code)
    assert any(issue["type"] == "function_length" for issue in issues)

def test_check_complexity(code_analyzer):
    code = """
def complex_function():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    if True:
                                        if True:
                                            return True
    """
    issues = code_analyzer.find_code_issues(code)
    assert any(issue["type"] == "complexity" for issue in issues)

def test_check_documentation(code_analyzer):
    code = """
def undocumented_function():
    pass

class UndocumentedClass:
    def __init__(self):
        pass
    """
    issues = code_analyzer.find_code_issues(code)
    assert any(issue["type"] == "documentation" for issue in issues) 