import numpy as np
import joblib
from config import RL_MODEL_PATH

def load_rl_model():
    try:
        model = joblib.load(RL_MODEL_PATH)
        return model
    except Exception as e:
        print(f"Error loading RL model: {e}")
        return None

def generate_trade_signal(stock_data, sentiment_score):
    if stock_data is None or stock_data.empty:
        return "HOLD"
    
    model = load_rl_model()
    if model is None:
        return "HOLD"
    
    features = extract_features(stock_data, sentiment_score)
    prediction = model.predict([features])[0]

    return "BUY" if prediction == 1 else "SELL" if prediction == -1 else "HOLD"

def extract_features(stock_data, sentiment_score):
    latest_data = stock_data.iloc[-1]
    return [
        latest_data['Close'],
        latest_data['Volume'],
        latest_data['High'] - latest_data['Low'],
        latest_data.get('RSI', 50),  # Default to neutral RSI if missing
        sentiment_score
    ]
