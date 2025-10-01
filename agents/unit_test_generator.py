from llm.llama_client import LlamaClient
import logging

class SmartUnitTestGenerator:
    """
    CrewAI agent for generating detailed unit test cases from requirements documents using Llama 3.1.
    """
    def __init__(self):
        """
        Initialize the SmartUnitTestGenerator agent as a CrewAI Agent with LiteLLM Ollama provider integration.
        """
        try:
            from langchain_ollama import OllamaLLM
            self.ollama_llm = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")
        except ImportError:
            self.ollama_llm = None
            self.llm_client = LlamaClient()

    def generate_test_cases(self, requirements_text):
        """
        Generate high-level QA test cases in a standard, human-readable format from requirements text using CrewAI Agent persona and Llama 3.1.
        Args:
            requirements_text (str): The requirements document as text.
        Returns:
            str: Generated test cases or error message.
        """
        if not requirements_text or not requirements_text.strip():
            logging.warning("No requirements text provided.")
            return "Error: No requirements text provided."
        prompt = (
            "You are an expert QA Test Case Writer and Senior Automation Engineer. Your job is to create a comprehensive, actionable, and human-readable set of test cases for the provided requirements."
            "\n\nInstructions:"
            "\n- Analyze the requirements and identify all core functionalities, edge cases, and user stories."
            "\n- For each functionality, generate positive, negative, and boundary test cases."
            "\n- Use a standard test case format with the following fields:"
            "\n  - Test Case ID (unique and descriptive)"
            "\n  - Title (short, clear description)"
            "\n  - Preconditions (any setup or state required)"
            "\n  - Test Steps (step-by-step actions)"
            "\n  - Input Data (specific values or files)"
            "\n  - Expected Results (precise, measurable outcomes)"
            "\n  - Actual Result (leave blank)"
            "\n- Format the output as a Markdown table."
            "\n- Make sure the test cases are clear, actionable, and cover all relevant scenarios."
            "\n\nRequirements:\n" + requirements_text
        )
        try:
            if self.ollama_llm:
                return self.ollama_llm.invoke(prompt)
            elif hasattr(self, 'llm_client') and self.llm_client:
                return self.llm_client.query(prompt)
            else:
                return "Error: No LLM provider available."
        except Exception as e:
            logging.error(f"Failed to generate test cases: {e}")
            return f"Error: Failed to generate test cases. Details: {e}"

# Example usage for CLI
if __name__ == "__main__":
    import sys
    import os
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)
        with open(file_path, 'r', encoding='utf-8') as f:
            requirements = f.read()
    else:
        requirements = input("Enter requirements text: ")
    agent = SmartUnitTestGenerator()
    test_cases = agent.generate_test_cases(requirements)
    print("\nGenerated Test Cases:\n", test_cases)
