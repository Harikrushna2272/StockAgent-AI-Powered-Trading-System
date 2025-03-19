# strategy_agent.py
import numpy as np
import joblib
import pandas as pd
from config import RL_MODEL_PATH

def load_rl_model():
    """Load the pre-trained RL model."""
    try:
        model = joblib.load(RL_MODEL_PATH)
        return model
    except Exception as e:
        print(f"Error loading RL model: {e}")
        return None

def calculate_ma200(stock_data):
    """Calculate the 200-day moving average (MA200)."""
    if len(stock_data) < 200:
        return None  # Not enough data

    stock_data["MA200"] = stock_data["Close"].rolling(window=200).mean()
    return stock_data

def generate_trade_signal(stock_data, sentiment_score):
    """Generate trade signal using RL model and technical indicators."""
    
    if stock_data is None or stock_data.empty:
        return "HOLD"
    
    model = load_rl_model()
    if model is None:
        return "HOLD"
    
    # Compute the moving average
    stock_data = calculate_ma200(stock_data)
    
    # If MA200 calculation failed due to insufficient data, use RL agent only
    if stock_data is None:
        features = extract_features(stock_data, sentiment_score)
        prediction = model.predict([features])[0]
        return "BUY" if prediction == 1 else "SELL" if prediction == -1 else "HOLD"
    
    latest_data = stock_data.iloc[-1]
    
    # Check BUY condition: MA200 is increasing and price touches MA200
    if (
        stock_data["MA200"].iloc[-1] > stock_data["MA200"].iloc[-2]  # MA200 increasing
        and latest_data["Low"] <= stock_data["MA200"].iloc[-1]  # Low touches MA200
    ):
        return "BUY"
    
    # SELL condition remains controlled by RL agent
    features = extract_features(stock_data, sentiment_score)
    prediction = model.predict([features])[0]

    return "SELL" if prediction == -1 else "HOLD"

def extract_features(stock_data, sentiment_score):
    """Extract features for RL model."""
    latest_data = stock_data.iloc[-1]
    return [
        latest_data['Close'],
        latest_data['Volume'],
        latest_data['High'] - latest_data['Low'],
        latest_data.get('RSI', 50),  # Default RSI to 50 if missing
        sentiment_score
    ]
