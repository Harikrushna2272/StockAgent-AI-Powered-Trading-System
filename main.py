import time
from data_fetcher import get_stock_data
from sentiment_agent import analyze_sentiment
from strategy_agent import generate_trade_signal
from execution_agent import execute_trade
from config import STOCK_LIST

def main():
    print("Starting StockAI...")
    
    while True:
        for stock in STOCK_LIST:
            print(f"Analyzing {stock}...")
            
            # Fetch Data
            stock_data = get_stock_data(stock)
            if stock_data is None:
                print(f"Failed to fetch data for {stock}")
                continue
            
            # Sentiment Analysis
            sentiment_score = analyze_sentiment(stock)
            print(f"Sentiment Score for {stock}: {sentiment_score}")
            
            # Generate Trade Signal
            trade_signal = generate_trade_signal(stock_data, sentiment_score)
            print(f"Trade Signal for {stock}: {trade_signal}")
            
            # Execute Trade
            execute_trade(stock, trade_signal)
        
        print("Waiting for next cycle...")
        time.sleep(60)  # Run every minute

if __name__ == "__main__":
    main()
