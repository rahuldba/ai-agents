# --- Smart System Log Analyzer: Dashboard, Charts, OLAMA LLM ---


from llm.llama_client import LlamaClient
import logging

# --- CrewAI System Log Analyzer Agent ---

class SystemLogAnalyzer:

    """
    CrewAI agent for system log analysis and actionable insights using Llama 3.1.

    Goal:
        To provide deep, actionable, and context-rich insights from system logs, enabling teams to proactively address reliability, performance, and security issues.

    Backstory:
        You are a world-class System Health Analyst and SRE. You have spent years building, monitoring, and troubleshooting distributed systems at scale. You are trusted by engineering and leadership alike for your ability to spot patterns, root causes, and emerging risks in massive log datasets. You combine expert knowledge of log semantics, incident response, and modern observability with advanced LLM-powered reasoning. Your reports are clear, actionable, and always anticipate what the team needs to know next.
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

    def analyze(self, log_text):
        """
        Send the raw log text directly to the LLM for analysis. No DataFrame or preprocessing.
        """
        prompt = (
            "You are a world-class System Health Analyst, SRE, and AI log analysis expert. Your job is to analyze the following system logs and provide a professional, actionable dashboard summary for engineering and leadership.\n"
            "Instructions:\n"
            "- Identify and summarize the most critical recurring issues, error spikes, and performance risks.\n"
            "- Highlight the top affected components, error types, and time windows.\n"
            "- Detect and describe any anomalies, outliers, or unusual patterns (e.g., bursts, rare errors, new modules, security warnings).\n"
            "- Prioritize risks by severity and potential impact.\n"
            "- For each major issue, provide a root cause hypothesis and suggest concrete next steps or mitigations.\n"
            "- Recommend monitoring, escalation, or automation actions if appropriate.\n"
            "- If possible, identify modules or teams that should be notified.\n"
            "- Format your output as a Markdown report with these sections: Executive Summary, Key Findings (with tables/bullets), Root Cause Analysis, Actionable Recommendations, and Next Steps.\n"
            "- Use tables for error/warning breakdowns, and bullet points for recommendations.\n"
            "- Be concise but thorough.\n"
            "\nSystem Logs:\n"
            f"{log_text.strip()}"
            "\n---\nDashboard Report:"
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
    agent = SystemLogAnalyzer()
    insights = agent.analyze(requirements)
    print("\nGenerated Insights:\n", insights)
