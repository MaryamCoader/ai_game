from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import tempfile
import os

router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    language: str

# -------------------
# Fix suggestion templates
# -------------------
PYTHON_FIXES = {
    "division by zero": "if y != 0:\n    print(x/y)",
    "nameerror": "# Define the variable before using it",
    "syntaxerror": "# Check your syntax (colons, parentheses, indentation)"
}

JS_FIXES = {
    "referenceerror": "# Check if all variables are defined",
    "typeerror": "# Ensure you are accessing valid properties or calling functions correctly",
    "syntaxerror": "# Check your JS syntax, missing brackets or parentheses"
}

CPP_FIXES = {
    "division by zero": "if (y != 0) { cout << x / y; }",
    "undeclared": "// Declare the variable before using it",
    "type": "// Correct type assignment",
    "syntax": "// Check syntax, missing semicolon/brackets",
    "out of bounds": "// Ensure array index is within bounds"
}

JAVA_FIXES = {
    "division by zero": "if (y != 0) { System.out.println(x / y); }",
    "cannot find symbol": "// Declare variable before use",
    "type": "// Correct type assignment",
    "syntax": "// Check syntax, missing semicolon/brackets",
    "array index out of bounds": "// Ensure array index is within bounds"
}

def generate_suggestions(error_msg, language):
    suggestions = []
    error_msg_lower = error_msg.lower()
    fixes = {}
    if language == "python":
        fixes = PYTHON_FIXES
    elif language == "javascript":
        fixes = JS_FIXES
    elif language == "java":
        fixes = JAVA_FIXES
    elif language == "c++":
        fixes = CPP_FIXES

    for key, fix in fixes.items():
        if key.lower() in error_msg_lower:
            suggestions.append({"description": f"Suggestion for {key}", "code": fix})
    return suggestions

# -------------------
# Main Analyze Endpoint
# -------------------
@router.post("/analyze")
async def analyze_code(request: CodeRequest):
    code = request.code
    lang = request.language.lower()

    # -------------------
    # Python
    # -------------------
    if lang == "python":
        try:
            exec(code)
            return {"bugs": [], "explanation": "No runtime errors", "fix_suggestions": [], "optimized_code": code}
        except Exception as e:
            error_msg = str(e)
            suggestions = generate_suggestions(error_msg, "python")
            return {
                "bugs": [{"line": 1, "description": error_msg}],
                "explanation": error_msg,
                "fix_suggestions": suggestions,
                "optimized_code": code
            }

    # -------------------
    # JavaScript
    # -------------------
    elif lang in ["javascript", "js"]:
        try:
            result = subprocess.run(['node', '-e', code], capture_output=True, text=True)
            stderr = result.stderr.strip()
            if stderr:
                suggestions = generate_suggestions(stderr, "javascript")
                return {
                    "bugs": [{"line": 1, "description": stderr}],
                    "explanation": stderr,
                    "fix_suggestions": suggestions,
                    "optimized_code": code
                }
            return {"bugs": [], "explanation": "No runtime errors", "fix_suggestions": [], "optimized_code": code}
        except Exception as e:
            suggestions = generate_suggestions(str(e), "javascript")
            return {
                "bugs": [{"line": 1, "description": str(e)}],
                "explanation": str(e),
                "fix_suggestions": suggestions,
                "optimized_code": code
            }

    # -------------------
    # Java
    # -------------------
    elif lang == "java":
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "Temp.java")
            with open(file_path, "w") as f:
                f.write(code)
            try:
                compile_result = subprocess.run(["javac", file_path], capture_output=True, text=True)
                if compile_result.stderr:
                    suggestions = generate_suggestions(compile_result.stderr, "java")
                    return {
                        "bugs": [{"line": 1, "description": compile_result.stderr.strip()}],
                        "explanation": compile_result.stderr.strip(),
                        "fix_suggestions": suggestions,
                        "optimized_code": code
                    }
                run_result = subprocess.run(["java", "-cp", tmpdir, "Temp"], capture_output=True, text=True)
                if run_result.stderr:
                    suggestions = generate_suggestions(run_result.stderr, "java")
                    return {
                        "bugs": [{"line": 1, "description": run_result.stderr.strip()}],
                        "explanation": run_result.stderr.strip(),
                        "fix_suggestions": suggestions,
                        "optimized_code": code
                    }
                return {"bugs": [], "explanation": "No runtime errors", "fix_suggestions": [], "optimized_code": code}
            except Exception as e:
                suggestions = generate_suggestions(str(e), "java")
                return {
                    "bugs": [{"line": 1, "description": str(e)}],
                    "explanation": str(e),
                    "fix_suggestions": suggestions,
                    "optimized_code": code
                }

    # -------------------
    # C++
    # -------------------
    elif lang in ["c++", "cpp"]:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "temp.cpp")
            exe_path = os.path.join(tmpdir, "temp.exe")
            with open(file_path, "w") as f:
                f.write(code)
            try:
                compile_result = subprocess.run(["g++", file_path, "-o", exe_path], capture_output=True, text=True)
                if compile_result.stderr:
                    suggestions = generate_suggestions(compile_result.stderr, "c++")
                    return {
                        "bugs": [{"line": 1, "description": compile_result.stderr.strip()}],
                        "explanation": compile_result.stderr.strip(),
                        "fix_suggestions": suggestions,
                        "optimized_code": code
                    }
                run_result = subprocess.run([exe_path], capture_output=True, text=True)
                if run_result.stderr:
                    suggestions = generate_suggestions(run_result.stderr, "c++")
                    return {
                        "bugs": [{"line": 1, "description": run_result.stderr.strip()}],
                        "explanation": run_result.stderr.strip(),
                        "fix_suggestions": suggestions,
                        "optimized_code": code
                    }
                return {"bugs": [], "explanation": "No runtime errors", "fix_suggestions": [], "optimized_code": code}
            except Exception as e:
                suggestions = generate_suggestions(str(e), "c++")
                return {
                    "bugs": [{"line": 1, "description": str(e)}],
                    "explanation": str(e),
                    "fix_suggestions": suggestions,
                    "optimized_code": code
                }

    # -------------------
    # Unsupported language
    # -------------------
    else:
        return {
            "bugs": [{"line": 1, "description": "Unsupported language"}],
            "explanation": "Unsupported language",
            "fix_suggestions": [],
            "optimized_code": code
        }
