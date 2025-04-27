import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze code using Gemini AI
        
        """
        prompt = f"""
        Analyze the following code and provide:
        1. Code quality assessment
        2. Potential bugs or issues
        3. Improvement suggestions
        4. Best practices recommendations

        Code:
        {code}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "analysis": response.text,
                "raw_response": response
            }
        except Exception as e:
            print(f"Error analyzing code: {e}")
            return {
                "analysis": "Error analyzing code. Please check your API key and model configuration.",
                "error": str(e)
            }

    def generate_documentation(self, code: str) -> str:
        """
        Generate documentation for the given code
        """
        prompt = f"""
        Generate comprehensive documentation for the following code:
        {code}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating documentation: {e}")
            return f"Error generating documentation: {str(e)}"

    def suggest_improvements(self, code: str) -> List[str]:
        """
        Suggest improvements for the given code
        """
        prompt = f"""
        Suggest specific improvements for the following code:
        {code}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.split('\n')
        except Exception as e:
            print(f"Error suggesting improvements: {e}")
            return [f"Error suggesting improvements: {str(e)}"] 