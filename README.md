# StockAgent: AI-Driven Trading System

**StockAgent** is an AI-driven trading system that processes real-time stock data via WebSockets, performs sentiment analysis, generates trade signals using a Reinforcement Learning (SAC) model enhanced with technical indicators, and executes trades using the Alpaca API.

## Features

- **Real-Time Data Streaming:**  
  Continuously fetch live trade data using WebSockets.

- **Sentiment Analysis:**  
  Analyze news headlines via the News API and TextBlob to gauge market sentiment.

- **Reinforcement Learning:**  
  Use a custom Gym environment to train a Soft Actor-Critic (SAC) model for generating trading signals.

- **Technical Indicators:**  
  Incorporate conditions like the 200-day moving average to refine buy decisions.

- **Automated Trade Execution:**  
  Execute trades automatically using the Alpaca Trade API.

## Project Structure

- **config.py:**  
  Contains API credentials, model file paths, and the list of stock symbols.

- **main.py:**  
  Orchestrates the overall workflow by fetching data, performing sentiment analysis, generating trade signals, and executing trades.

- **data_fetcher.py:**  
  Uses a continuously running WebSocket connection to receive real-time trade data and makes the latest data available on demand.

- **sentiment_agent.py:**  
  Fetches news articles and analyzes sentiment using TextBlob.

- **strategy_agent.py:**  
  Generates trade signals by combining RL model predictions with technical indicator conditions (e.g., MA200 increasing and current candle low touching MA200).

- **execution_agent.py:**  
  Executes trades via the Alpaca API.

- **rl_training.py:**  
  Defines a custom Gym environment for trading and provides functions to train, save, and load the SAC RL model.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/StockAgent.git
   cd StockAgent
