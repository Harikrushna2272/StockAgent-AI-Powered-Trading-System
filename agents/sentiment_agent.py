# sentiment_agent.py
import requests
from textblob import TextBlob # to calculate a sentiment polarity score
import numpy as np
from config import NEWS_API_KEY

class SentimentAgent:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_news(self):
        url = f"https://newsapi.org/v2/everything?q={self.ticker}&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()
        articles = response.get("articles", [])[:5]
        return articles

    def analyze_sentiment(self):
        articles = self.fetch_news()
        if not articles:
            return 0  # Neutral sentiment if no news
        scores = [TextBlob(article["title"]).sentiment.polarity for article in articles]
        return np.mean(scores)

# Helper function for easier integration
def analyze_sentiment(ticker):
    agent = SentimentAgent(ticker)
    return agent.analyze_sentiment()
