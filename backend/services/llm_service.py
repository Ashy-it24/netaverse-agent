import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found in environment variables.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

    def get_client(self):
        return self.client