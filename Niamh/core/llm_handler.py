import requests
import json
import logging

class LLMHandler:
    def __init__(self, model="llama3.1:latest"):
        """Initialize the LLM Handler with the specified model."""
        logging.info(f"Initializing LLM Handler with model: {model}")
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def generate_response(self, prompt):
        """Send a request to Ollama's API and return the generated response."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False  # We want the full response at once
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an error if the request fails
            response_data = response.json()
            return response_data.get("response", "No response received from LLM.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error communicating with Ollama API: {e}")
            return "Error: Unable to communicate with the LLM."
