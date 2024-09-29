import json
import os
import requests
import logging
from dotenv import load_dotenv
from typing import List, Dict, Any
from utils.console import pretty_print, MessageType

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPT:
    def __init__(self):
        self.url = os.environ.get('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HF_INFERENCE_TOKEN')}"
        }
        self.payload = {
            "inputs": "",
            "parameters": {
                "return_full_text": False, # strip 'Bot:' from the response
                "use_cache": True, # toggle to disable caching
                "max_new_tokens": 25
            }
        }

        # Check if environment variables are set
        if not self.url or not self.headers["Authorization"]:
            pretty_print("Environment variables MODEL_URL or HF_INFERENCE_TOKEN are not set. Hugging Face inference token starts with 'hf_'..", MessageType.FATAL)
            raise ValueError("Missing environment variables")

    def query(self, input: str) -> str:
        self.payload["inputs"] = f"Human: {input} Bot:" # this input format turns the GPT-J6B into a conversational model
        data = json.dumps(self.payload)
        try:
            response = requests.post(self.url, headers=self.headers, data=data)
            response.raise_for_status()
            data = json.loads(response.content.decode("utf-8"))
            text = data[0]['generated_text']
            res = str(text.split("Human:")[0]).strip("\n").strip()
            pretty_print("Query successful", MessageType.INFO)
            return res
        except requests.exceptions.RequestException as e:
            pretty_print(f"HTTP request failed: {e}", MessageType.FATAL)
            raise

# Example usage
# PYTHONPATH=/Users/x/git/pythuto-chan python3 /Users/x/git/pythuto-chan/worker/src/model/gptj.py
if __name__ == "__main__":
    try:
        gpt = GPT()
        result = gpt.query("Hello, world!")
        pretty_print(f"Result: {result}", MessageType.INFO)
    except Exception as e:
        pretty_print(f"An error occurred: {e}", MessageType.FATAL)