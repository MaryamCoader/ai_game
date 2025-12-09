from pydantic import BaseModel
from typing import List, Dict

class Bug(BaseModel):
    line: int
    description: str

class FixSuggestion(BaseModel):
    description: str
    code: str

class CodeAnalysisResponse(BaseModel):
    bugs: List[Bug]
    explanation: str
    fix_suggestions: List[FixSuggestion]
    optimized_code: str
