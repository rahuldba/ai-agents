import requests
import logging
import json

class LlamaClient:
    """
    Client for interacting with a local Ollama Llama 3.1 server.
    Handles prompt submission and response parsing with error handling.
    """
    def __init__(self, base_url="http://localhost:11434"):
        """
        Initialize the LlamaClient.
        Args:
            base_url (str): Base URL for the local Ollama server.
        """
        self.base_url = base_url

    def query(self, prompt):
        """
        Send a prompt to the Llama 3.1 model and return the response.
        Args:
            prompt (str): The prompt to send to the model.
        Returns:
            str: The model's response or error message.
        """
        endpoint = f"{self.base_url}/api/generate"
        payload = {"model": "llama3.1", "prompt": prompt}
        try:
            response = requests.post(endpoint, json=payload, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to Llama server failed: {e}")
            return f"Error: Could not connect to Llama server. Details: {e}"

        # Handle NDJSON streaming response
        try:
            lines = response.text.strip().splitlines()
            responses = []
            for line in lines:
                try:
                    data = json.loads(line)
                    if "response" in data:
                        responses.append(data["response"])
                except Exception as e:
                    logging.warning(f"Failed to parse line as JSON: {e} | Line: {line}")
            if responses:
                return "\n".join(responses)
            else:
                return response.text
        except Exception as e:
            logging.error(f"Failed to parse NDJSON response: {e}")
            return response.text
