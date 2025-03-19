# execution_agent.py
import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

class ExecutionAgent:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

    def execute_trade(self, symbol, trade_signal):
        if trade_signal not in ["BUY", "SELL"]:
            print(f"No valid trade signal for {symbol}. Holding position.")
            return
        
        side = "buy" if trade_signal == "BUY" else "sell"
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=10, 
                side=side,
                type="market",
                time_in_force="gtc"
            )
            print(f"Executed {trade_signal} order for {symbol}.")
            return order
        except Exception as e:
            print(f"Trade execution failed for {symbol}: {e}")
