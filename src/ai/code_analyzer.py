import ast
from typing import Dict, List, Any, Tuple
import re

class CodeAnalyzer:
    def __init__(self):
        self.quality_metrics = {
            "complexity": 0,
            "maintainability": 0,
            "readability": 0,
            "test_coverage": 0
        }

    def analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """
        Analyze the structure of the code
        """
        try:
            tree = ast.parse(code)
            return {
                "functions": self._analyze_functions(tree),
                "classes": self._analyze_classes(tree),
                "imports": self._analyze_imports(tree),
                "complexity": self._calculate_complexity(tree)
            }
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {str(e)}",
                "line": e.lineno,
                "offset": e.offset
            }

    def find_code_issues(self, code: str) -> List[Dict[str, Any]]:
        """
        Find potential issues in the code
        """
        issues = []
        try:
            tree = ast.parse(code)
            issues.extend(self._check_naming_conventions(tree))
            issues.extend(self._check_function_length(tree))
            issues.extend(self._check_complexity(tree))
            issues.extend(self._check_documentation(tree))
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "line": e.lineno,
                "message": str(e),
                "severity": "high"
            })
        return issues

    def get_line_numbers(self, code: str, pattern: str) -> List[int]:
        """
        Get line numbers where a pattern appears in the code
        """
        lines = code.split('\n')
        line_numbers = []
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                line_numbers.append(i)
        return line_numbers

    def _analyze_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Analyze functions in the code
        """
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": len(node.args.args),
                    "has_docstring": ast.get_docstring(node) is not None
                })
        return functions

    def _analyze_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Analyze classes in the code
        """
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "has_docstring": ast.get_docstring(node) is not None
                })
        return classes

    def _analyze_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Analyze imports in the code
        """
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({
                        "name": name.name,
                        "line": node.lineno,
                        "type": "import"
                    })
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    imports.append({
                        "name": f"{node.module}.{name.name}",
                        "line": node.lineno,
                        "type": "from_import"
                    })
        return imports

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate code complexity
        """
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _check_naming_conventions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Check naming conventions
        """
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    issues.append({
                        "type": "naming_convention",
                        "line": node.lineno,
                        "message": f"Function name '{node.name}' should be lowercase with underscores",
                        "severity": "low"
                    })
            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append({
                        "type": "naming_convention",
                        "line": node.lineno,
                        "message": f"Class name '{node.name}' should be CamelCase",
                        "severity": "low"
                    })
        return issues

    def _check_function_length(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Check function length
        """
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:  # Arbitrary threshold
                    issues.append({
                        "type": "function_length",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too long ({len(node.body)} lines)",
                        "severity": "medium"
                    })
        return issues

    def _check_complexity(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Check code complexity
        """
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > 10:  # Arbitrary threshold
                    issues.append({
                        "type": "complexity",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too complex (complexity: {complexity})",
                        "severity": "medium"
                    })
        return issues

    def _check_documentation(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Check code documentation
        """
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    issues.append({
                        "type": "documentation",
                        "line": node.lineno,
                        "message": f"{'Function' if isinstance(node, ast.FunctionDef) else 'Class'} '{node.name}' is missing docstring",
                        "severity": "low"
                    })
        return issues 