import os
from groq import Groq
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            print("Warning: GROQ_API_KEY not found or not configured in environment variables.")
            print("Please set your Groq API key in the .env file.")
            print("Get a free key from: https://console.groq.com/")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
                print("✓ Groq client initialized successfully")
            except Exception as e:
                print(f"Error initializing Groq client: {e}")
                self.client = None

    def get_client(self):
        return self.client