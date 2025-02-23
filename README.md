# StockAgent: AI-Powered Trading System

## Overview
StockAgent is a fully agentic AI-based trading system that leverages Reinforcement Learning (RL), LangChain, and real-time WebSockets to analyze stock market data, generate trade signals, and execute trades automatically. It integrates multiple AI agents, including market data analysis, sentiment analysis, strategy generation, and trade execution, ensuring a comprehensive automated trading workflow.

## Features
- **Real-time Market Data Streaming**: Uses WebSockets for low-latency stock price updates.
- **Reinforcement Learning (RL)**: Implements PPO & SAC models for decision-making.
- **Technical Analysis**: Computes EMA, RSI, and ATR indicators.
- **Sentiment Analysis**: Evaluates news sentiment for enhanced trading signals.
- **Automated Trade Execution**: Places buy/sell orders via Alpaca API.
- **Configurable Strategy**: Customizable risk parameters, stop-loss, and take-profit settings.

## Technologies Used
- **Python** (Primary Language)
- **LangChain** (Agentic AI)
- **Stable-Baselines3** (RL Algorithms)
- **Alpaca Trade API** (Execution)
- **Yahoo Finance & WebSockets** (Market Data)
- **TA-Lib** (Technical Indicators)
- **NewsAPI** (Sentiment Analysis)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/StockAgent.git
   cd StockAgent
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up API keys in `config.py`:
   ```python
   ALPACA_API_KEY = "your_alpaca_api_key"
   ALPACA_API_SECRET = "your_alpaca_api_secret"
   NEWS_API_KEY = "your_news_api_key"
   ```

## Running the Project
1. **Start WebSocket Market Data Streaming:**
   ```sh
   python market_data_agent.py
   ```
2. **Train RL Model:**
   ```sh
   python model.py
   ```
3. **Run Trading System:**
   ```sh
   python main.py
   ```

## File Structure

StockAgent/
│── agents/
│   ├── market_data_agent.py
│   ├── sentiment_agent.py
│   ├── strategy_agent.py
│   ├── execution_agent.py
│── models/
│   ├── reinforcement_learning.py
│── data/
│   ├── historical_data.py
│── utils/
│   ├── config.py
│── main.py
│── requirements.txt
│── README.md

## How It Works
1. **Market Data Collection:** Fetches real-time stock prices via WebSockets.
2. **Sentiment Analysis:** Scores recent news articles for trading insights.
3. **Trade Signal Generation:** Uses RL model & technical indicators to determine Buy/Sell signals.
4. **Trade Execution:** Places orders automatically via Alpaca API.
5. **Reinforcement Learning:** Continuously improves strategy through training.

## Future Enhancements
- Add more RL models like DDPG and A2C.
- Implement portfolio optimization.
- Enhance risk management features.
- Integrate multi-asset trading (crypto, forex).

## Contributing
Feel free to fork this repository, improve the strategy, and submit pull requests!



# StockAgent-AI-Powered-Trading-System
