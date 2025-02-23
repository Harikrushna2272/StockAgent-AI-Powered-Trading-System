import gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.envs import DummyVecEnv
import talib
from sentiment_agent import analyze_sentiment

class TradingEnv(gym.Env):
    def __init__(self, market_data):
        super(TradingEnv, self).__init__()
        self.market_data = market_data
        self.current_step = 0
        self.balance = 100000  # Starting cash
        self.position = 0  # No stock held
        self.last_action = 0
        
        # Action space: [0-4] (Cash, 25%, 50%, 75%, 100% invested)
        self.action_space = gym.spaces.Discrete(5)
        
        # Observation space includes: Close Price, Volume, High-Low, Sentiment, RSI, MACD, ATR
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)
    
    def step(self, action):
        current_price = self.market_data.iloc[self.current_step]["Close"]
        rsi = talib.RSI(self.market_data["Close"], timeperiod=14)[self.current_step]
        macd, _, _ = talib.MACD(self.market_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
        atr = talib.ATR(self.market_data["High"], self.market_data["Low"], self.market_data["Close"], timeperiod=14)[self.current_step]
        sentiment = analyze_sentiment("AAPL")  # Example stock
        
        # Position sizing based on action
        allocation = action / 4.0  # Convert action [0-4] to [0-100%] capital allocation
        new_position = (self.balance * allocation) / current_price
        
        # Reward function: Profit + Sharpe Ratio
        reward = (self.balance - 100000) / 1000  # Normalized profit
        sharpe_ratio = reward / (np.std([self.last_action, action]) + 1e-6)
        reward += sharpe_ratio
        
        self.position = new_position
        self.current_step += 1
        done = self.current_step >= len(self.market_data) - 1
        
        return np.array([current_price, self.market_data["Volume"][self.current_step],
                         self.market_data["High"][self.current_step] - self.market_data["Low"][self.current_step],
                         sentiment, rsi, macd[self.current_step], atr]), reward, done, {}
    
    def reset(self):
        self.current_step = 0
        self.balance = 100000
        self.position = 0
        return np.array([self.market_data["Close"][0], self.market_data["Volume"][0],
                         self.market_data["High"][0] - self.market_data["Low"][0],
                         analyze_sentiment("AAPL"), 50, 0, 1])

def train_rl_agent(market_data):
    env = DummyVecEnv([lambda: TradingEnv(market_data)])
    model = SAC("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=50000)
    return model
