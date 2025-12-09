import json
from backend.models.analysis import CodeAnalysisResponse
from backend.ai_integration.gemini import GeminiClient

class AnalysisService:
    def __init__(self):
        self.gemini_client = GeminiClient()

    def analyze_code(self, code: str, language: str) -> CodeAnalysisResponse:
        raw_response = self.gemini_client.analyze_code(code, language)

        # Clean JSON (remove any markdown)
        cleaned_json_string = raw_response.strip().replace("```json", "").replace("```", "").strip()

        try:
            analysis_data = json.loads(cleaned_json_string)
            return CodeAnalysisResponse(**analysis_data)
        except json.JSONDecodeError:
            # If AI response is invalid JSON
            return CodeAnalysisResponse(
                bugs=[],
                explanation="Error: The AI response was not valid JSON. Try again.",
                fix_suggestions=[],
                optimized_code=""
            )
