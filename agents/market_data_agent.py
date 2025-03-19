# market_data.py
import websocket
import json
import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

class MarketDataAgent:
    def __init__(self, symbol):
        self.api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")
        self.symbol = symbol
        self.ws_url = "wss://stream.data.alpaca.markets/v2/iex"
        self.socket = None

    def on_message(self, ws, message):
        data = json.loads(message)
        for item in data:
            if item.get("T") == "t":  # Trade update
                print(f"Real-time price update for {self.symbol}: {item['p']}")
                # You can call further processing here if needed

    def on_open(self, ws):
        print("WebSocket connected. Subscribing to live data...")
        auth_data = {
            "action": "auth",
            "key": API_KEY,
            "secret": API_SECRET
        }
        ws.send(json.dumps(auth_data))
        subscribe_message = {
            "action": "subscribe",
            "trades": [self.symbol]
        }
        ws.send(json.dumps(subscribe_message))

    def start_stream(self):
        self.socket = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message
        )
        self.socket.run_forever()

if __name__ == "__main__":
    agent = MarketDataAgent("AAPL")
    agent.start_stream()
