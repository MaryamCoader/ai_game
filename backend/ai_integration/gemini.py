import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze_code(self, code: str, language: str) -> str:
        prompt = f"""
        Analyze the following {language} code for bugs, provide an explanation,
        suggest fixes, and provide an optimized version of the code.
        Return the response as a JSON object with the following keys: 
        "bugs", "explanation", "fix_suggestions", "optimized_code".

        Code:
        ```
        {code}
        ```
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("Gemini API error:", e)
            return '{"bugs": [], "explanation": "Error connecting to Gemini API.", "fix_suggestions": [], "optimized_code": ""}'
