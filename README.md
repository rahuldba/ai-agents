# Smart Test Case Generator (AI Agents with Streamlit, CrewAI, and Ollama)

## Overview
This project provides a modern, Python-based AI agent system for generating advanced QA test cases from software requirements. It features:
- **Streamlit UI** for easy user interaction
- **CrewAI** for agent orchestration
- **Local Llama 3.1 via Ollama** for LLM-powered test case generation
- **LangChain Community** integration for robust LLM connectivity

## Features
- Paste or upload requirements documents
- Generate comprehensive test cases (positive, negative, boundary)
- Output in human-readable, standard test case format
- Download results as Markdown

## Quick Start

### 1. Clone the Repository
```sh
# Clone your repo (replace with your repo URL)
git clone <your-repo-url>
cd ai-agents
```

### 2. Set Up Python Environment
```sh
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Start Ollama and Pull Llama 3.1 Model
- [Install Ollama](https://ollama.com/download)
- Start Ollama server:
	```sh
	ollama serve
	```
- Pull the model:
	```sh
	ollama pull llama3.1
	```

### 5. Run the Streamlit App
```sh
streamlit run app/app.py
```
Visit [http://localhost:8501](http://localhost:8501) in your browser.

## Usage
1. Enter or upload your requirements document.
2. Click **Generate Smart Test Cases**.
3. Review the generated test cases in the main panel.
4. Download the results as a Markdown file.

## Folder Structure
```
app/         # Streamlit UI
agents/      # Agent logic (SmartUnitTestGenerator)
llm/         # LLM integration (Ollama, LangChain)
crewai/      # CrewAI orchestration utilities
config/      # Configuration files
tests/       # Unit/integration tests
docs/        # Documentation
```

## Advanced
- Customize agents and tasks in `agents/` and `crewai/`
- Extend LLM integration in `llm/`
- Add more test formats or output options as needed

## Troubleshooting
- Ensure Ollama is running and the Llama 3.1 model is pulled
- Activate your Python virtual environment before running
- If you see errors, check the terminal and Streamlit logs for details

## License
MIT
