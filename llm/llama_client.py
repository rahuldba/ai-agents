import requests
import logging

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
            response = requests.post(endpoint, json=payload, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to Llama server failed: {e}")
            return f"Error: Could not connect to Llama server. Details: {e}"

        # Try to parse JSON response
        try:
            data = response.json()
            if "response" in data:
                return data["response"]
            else:
                logging.warning(f"Unexpected JSON structure: {data}")
                return str(data)
        except Exception as e:
            logging.error(f"Failed to parse JSON response: {e}")
            # Return raw text if JSON parsing fails
            return response.text
