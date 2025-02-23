import requests
from textblob import TextBlob
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
            return 0  # Neutral sentiment if no news found
        
        sentiment_scores = [TextBlob(article["title"]).sentiment.polarity for article in articles]
        return np.mean(sentiment_scores)

# Optional: Fetch Twitter sentiment (You can integrate Twitter API if needed)
