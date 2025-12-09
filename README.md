# AI Bug Exterminator

This project is a tool for detecting bugs in Python, JavaScript, C++, and Java code using an AI-powered backend. It provides both a web interface and a command-line tool.

## Folder Structure

```
.
├── backend
│   ├── ai_integration
│   │   └── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── analysis.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── analysis.py
│   ├── services
│   │   ├── __init__.py
│   │   └── analysis.py
│   ├── utils
│   │   └── __init__.py
│   └── main.py
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── cli.py
└── requirements.txt
```

## Setup

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage the project's dependencies.

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS and Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set up Gemini API Key

This project uses the Gemini API for code analysis. You need to get an API key from Google AI Studio.

Create a `.env` file in the `backend` directory and add your API key:

```
GEMINI_API_KEY=your_api_key
```

## How to Run

### 1. Run the FastAPI Server

Navigate to the project's root directory and run the following command:

```bash
uvicorn backend.main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

### 2. Open the Web UI

Open the `frontend/index.html` file in your web browser.

### 3. Use the CLI Tool

You can use the CLI tool to analyze a code file from the command line.

**Example:**

```bash
python cli.py path/to/your/code.py -l python
```

Replace `path/to/your/code.py` with the actual path to your code file and `python` with the appropriate language.

## Example Workflow

1.  **Start the backend server.**
2.  **Open the web UI or use the CLI tool.**
3.  **Select the programming language.**
4.  **Enter or upload your code.**
5.  **Click "Analyze Code" or run the CLI command.**
6.  **View the analysis results, including bugs, explanations, fix suggestions, and optimized code.**
