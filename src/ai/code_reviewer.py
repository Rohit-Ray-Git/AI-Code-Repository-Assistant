from typing import Dict, List, Any
from .gemini_client import GeminiClient
from .code_analyzer import CodeAnalyzer

class CodeReviewer:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.code_analyzer = CodeAnalyzer()

    def review_pull_request(self, changes: Dict[str, str]) -> Dict[str, Any]:
        """
        Review a pull request by analyzing the changes
        """
        review_results = {}
        for file_path, code in changes.items():
            # Get AI analysis
            ai_analysis = self.gemini_client.analyze_code(code)
            
            # Get code structure analysis
            structure_analysis = self.code_analyzer.analyze_code_structure(code)
            
            # Get code issues
            issues = self.code_analyzer.find_code_issues(code)
            
            review_results[file_path] = {
                "ai_analysis": ai_analysis["analysis"],
                "suggestions": self.gemini_client.suggest_improvements(code),
                "structure": structure_analysis,
                "issues": issues
            }
        return review_results

    def generate_review_comments(self, changes: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Generate review comments for the changes
        """
        comments = []
        for file_path, code in changes.items():
            # Get AI analysis
            ai_analysis = self.gemini_client.analyze_code(code)
            
            # Get code issues with line numbers
            issues = self.code_analyzer.find_code_issues(code)
            
            # Add AI analysis comment
            comments.append({
                "file": file_path,
                "line": 1,
                "comment": ai_analysis["analysis"],
                "type": "suggestion"
            })
            
            # Add issue comments
            for issue in issues:
                comments.append({
                    "file": file_path,
                    "line": issue["line"],
                    "comment": issue["message"],
                    "type": issue["type"],
                    "severity": issue["severity"]
                })
        return comments

    def check_code_quality(self, code: str) -> Dict[str, Any]:
        """
        Check code quality and return metrics
        """
        # Get AI analysis
        ai_analysis = self.gemini_client.analyze_code(code)
        
        # Get code structure analysis
        structure_analysis = self.code_analyzer.analyze_code_structure(code)
        
        # Get code issues
        issues = self.code_analyzer.find_code_issues(code)
        
        # Calculate quality score based on issues
        quality_score = self._calculate_quality_score(issues)
        
        return {
            "quality_score": quality_score,
            "issues": issues,
            "suggestions": self.gemini_client.suggest_improvements(code),
            "structure": structure_analysis
        }

    def detect_potential_bugs(self, code: str) -> List[Dict[str, Any]]:
        """
        Detect potential bugs in the code
        """
        # Get AI analysis
        ai_analysis = self.gemini_client.analyze_code(code)
        
        # Get code issues
        issues = self.code_analyzer.find_code_issues(code)
        
        # Combine AI analysis with code issues
        bugs = []
        for issue in issues:
            if issue["severity"] in ["high", "medium"]:
                bugs.append({
                    "type": "potential_bug",
                    "description": issue["message"],
                    "severity": issue["severity"],
                    "line": issue["line"]
                })
        
        # Add AI-detected issues
        bugs.append({
            "type": "ai_analysis",
            "description": ai_analysis["analysis"],
            "severity": "medium",
            "line": 1
        })
        
        return bugs

    def _calculate_quality_score(self, issues: List[Dict[str, Any]]) -> float:
        """
        Calculate quality score based on issues
        """
        if not issues:
            return 1.0
        
        severity_weights = {
            "high": 0.5,
            "medium": 0.3,
            "low": 0.1
        }
        
        total_weight = sum(severity_weights[issue["severity"]] for issue in issues)
        max_possible_weight = len(issues) * max(severity_weights.values())
        
        return max(0.0, 1.0 - (total_weight / max_possible_weight)) 