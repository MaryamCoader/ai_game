import requests
import argparse

def analyze_code(code, language, url="http://127.0.0.1:8000/api/analyze"):
    """
    Sends code to the backend for analysis and prints the results.
    """
    try:
        response = requests.post(url, json={"code": code, "language": language})
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        print("Analysis Results:")
        print("=" * 20)
        print("Bugs:")
        for bug in data.get("bugs", []):
            print(f"- Line {bug['line']}: {bug['description']}")
        print("\nExplanation:")
        print(data.get("explanation"))
        print("\nFix Suggestions:")
        for fix in data.get("fix_suggestions", []):
            print(f"- {fix['description']}:\n```\n{fix['code']}\n```")
        print("\nOptimized Code:")
        print(data.get("optimized_code"))
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the analysis server: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Bug Exterminator CLI")
    parser.add_argument("file", help="Path to the code file to analyze")
    parser.add_argument(
        "-l", "--language",
        required=True,
        choices=["python", "javascript", "c++", "java"],
        help="Programming language of the code"
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            code_to_analyze = f.read()
        analyze_code(code_to_analyze, args.language)
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
