import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class FetchAgent:
    def __init__(self):
        self.news_api_key = os.getenv("NEWSAPI_KEY")
        self.congress_api_key = os.getenv("CONGRESS_API_KEY")

    def fetch_wikipedia(self, name):
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(name)}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Wikipedia fetch error: {e}")
        return {}

    def fetch_news(self, name):
        if not self.news_api_key:
            return []
        try:
            url = f"https://newsapi.org/v2/everything?q={urllib.parse.quote(name)}&sortBy=publishedAt&pageSize=5&apiKey={self.news_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("articles", [])
        except Exception as e:
            print(f"NewsAPI fetch error: {e}")
        return []

    def get_data(self, name):
        # Aggregates data from available sources
        return {
            "wikipedia": self.fetch_wikipedia(name),
            "news": self.fetch_news(name),
            # Congress API implementation omitted for MVP simplicity, can be added here
        }