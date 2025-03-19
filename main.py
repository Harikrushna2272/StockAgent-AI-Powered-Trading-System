# main.py
import time
from data_fetcher import get_stock_data  
from sentiment_agent import analyze_sentiment
from strategy_agent import generate_trade_signal
from execution_agent import ExecutionAgent
from config import STOCK_LIST

def main():
    print("Starting StockAgent...")
    exec_agent = ExecutionAgent()

    while True:
        for stock in STOCK_LIST:
            print(f"\nAnalyzing {stock}...")
            # Fetch historical/real-time stock data
            stock_data = get_stock_data(stock)
            if stock_data is None:
                print(f"Failed to fetch data for {stock}")
                continue
            
            # Perform sentiment analysis
            sentiment_score = analyze_sentiment(stock)
            print(f"Sentiment Score for {stock}: {sentiment_score}")
            
            # Generate a trade signal based on data and sentiment
            trade_signal = generate_trade_signal(stock_data, sentiment_score)
            print(f"Trade Signal for {stock}: {trade_signal}")
            
            # Execute trade based on the generated signal
            exec_agent.execute_trade(stock, trade_signal)
        
        print("Waiting for next cycle...")
        time.sleep(60)  # Delay between cycles (60 seconds)

if __name__ == "__main__":
    main()
