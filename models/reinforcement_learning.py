# rl_training.py
import gym
import numpy as np
import os
from stable_baselines3 import SAC
from stable_baselines3.common.envs import DummyVecEnv
import talib
from sentiment_agent import analyze_sentiment

class TradingEnv(gym.Env):
    def __init__(self, market_data):
        super(TradingEnv, self).__init__()
        self.market_data = market_data
        self.current_step = 0
        self.balance = 100000  # Starting cash balance
        self.position = 0      # No stock held initially
        self.last_action = 0
        
        # Discrete actions: 0 to 4 corresponding to 0%-100% investment
        self.action_space = gym.spaces.Discrete(5)
        
        # Observation space: [Close, Volume, (High-Low), Sentiment, RSI, MACD, ATR]
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)
    
    def step(self, action):
        current_price = self.market_data.iloc[self.current_step]["Close"]
        rsi = talib.RSI(self.market_data["Close"], timeperiod=14)[self.current_step]
        macd, _, _ = talib.MACD(self.market_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
        atr = talib.ATR(self.market_data["High"], self.market_data["Low"], self.market_data["Close"], timeperiod=14)[self.current_step]
        sentiment = analyze_sentiment("AAPL")  # Example, can be parameterized
        
        allocation = action / 4.0
        new_position = (self.balance * allocation) / current_price
        
        profit = (self.balance - 100000) / 1000  # Normalized profit
        sharpe = profit / (np.std([self.last_action, action]) + 1e-6)
        reward = profit + sharpe
        
        self.position = new_position
        self.last_action = action
        self.current_step += 1
        done = self.current_step >= len(self.market_data) - 1
        
        observation = np.array([
            current_price,
            self.market_data["Volume"].iloc[self.current_step],
            self.market_data["High"].iloc[self.current_step] - self.market_data["Low"].iloc[self.current_step],
            sentiment,
            rsi,
            macd[self.current_step],
            atr
        ])
        
        return observation, reward, done, {}
    
    def reset(self):
        self.current_step = 0
        self.balance = 100000
        self.position = 0
        return np.array([
            self.market_data["Close"].iloc[0],
            self.market_data["Volume"].iloc[0],
            self.market_data["High"].iloc[0] - self.market_data["Low"].iloc[0],
            analyze_sentiment("AAPL"),
            50,  # Neutral RSI
            0,   # Starting MACD
            1    # Starting ATR
        ])

def train_rl_agent(market_data, save_path="models/sac_trading_model.zip"):
    """Train the SAC model and save it to a file."""
    env = DummyVecEnv([lambda: TradingEnv(market_data)])
    model = SAC("MlpPolicy", env, verbose=1)
    
    print("Training SAC RL Model...")
    model.learn(total_timesteps=50000)

    # Ensure the models directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save the trained model
    model.save(save_path)
    print(f"Model saved successfully at {save_path}")

    return model

def load_rl_agent(model_path="models/sac_trading_model.zip"):
    """Load the trained SAC model from a file."""
    if not os.path.exists(model_path):
        print("Model file not found. Please train the model first.")
        return None
    
    model = SAC.load(model_path)
    print(f"Model loaded from {model_path}")
    return model
