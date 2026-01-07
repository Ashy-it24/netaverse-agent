import os
import requests
import urllib.parse
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class FetchAgent:
    def __init__(self):
        self.news_api_key = os.getenv("NEWSAPI_KEY")
        self.congress_api_key = os.getenv("CONGRESS_API_KEY")

    def fetch_wikipedia(self, name):
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(name)}"
            headers = {
                'User-Agent': 'PoliticianAnalyzer/1.0 (https://github.com/user/politician-analyzer)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Wikipedia data fetched for {name}")
                return data
            else:
                print(f"Wikipedia API returned status {response.status_code}")
        except Exception as e:
            print(f"Wikipedia fetch error: {e}")
        return {}

    def fetch_news(self, name):
        if not self.news_api_key or self.news_api_key == "your_newsapi_key_here":
            print("NewsAPI key not configured, skipping news fetch")
            return []
        try:
            url = f"https://newsapi.org/v2/everything?q={urllib.parse.quote(name)}&sortBy=publishedAt&pageSize=5&apiKey={self.news_api_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                print(f"✓ {len(articles)} news articles fetched for {name}")
                return articles
            else:
                print(f"NewsAPI returned status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"NewsAPI fetch error: {e}")
        return []

    def get_fallback_data(self, name):
        """Provide fallback data when APIs are not available"""
        name_lower = name.lower()
        
        # Basic politician data for common names
        fallback_politicians = {
            "joe biden": {
                "extract": "Joseph Robinette Biden Jr. is an American politician who is the 46th and current president of the United States. A member of the Democratic Party, he previously served as the 47th vice president from 2009 to 2017 under Barack Obama.",
                "title": "Joe Biden"
            },
            "donald trump": {
                "extract": "Donald John Trump is an American politician, media personality, and businessman who served as the 45th president of the United States from 2017 to 2021.",
                "title": "Donald Trump"
            },
            "kamala harris": {
                "extract": "Kamala Devi Harris is an American politician and attorney who is the 49th and current vice president of the United States.",
                "title": "Kamala Harris"
            }
        }
        
        return fallback_politicians.get(name_lower, {
            "extract": f"Political figure: {name}. Please configure API keys for detailed information.",
            "title": name
        })

    def get_data(self, name):
        print(f"\n=== Fetching data for: {name} ===")
        
        # Try to fetch real data
        wikipedia_data = self.fetch_wikipedia(name)
        news_data = self.fetch_news(name)
        
        # If no Wikipedia data, use fallback
        if not wikipedia_data or not wikipedia_data.get('extract'):
            print("Using fallback Wikipedia data")
            wikipedia_data = self.get_fallback_data(name)
        
        result = {
            "wikipedia": wikipedia_data,
            "news": news_data,
        }
        
        print(f"Data summary: Wikipedia={'✓' if wikipedia_data.get('extract') else '✗'}, News={len(news_data)} articles")
        return result