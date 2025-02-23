import websocket
import json
import alpaca_trade_api as tradeapi

class MarketDataAgent:
    def __init__(self, api_key, api_secret, base_url, symbol):
        self.api = tradeapi.REST(api_key, api_secret, base_url, api_version="v2")
        self.symbol = symbol
        self.ws_url = "wss://stream.data.alpaca.markets/v2/iex"
        self.socket = None

    def on_message(self, ws, message):
        data = json.loads(message)
        for item in data:
            if item.get("T") == "t":  # Trade update
                print(f"Real-time price update for {self.symbol}: {item['p']}")
                # Call strategy agent for real-time decision-making
                # Example: self.process_trade_signal(item['p'])

    def on_open(self, ws):
        print("WebSocket connected, subscribing to live data...")
        auth_data = {
            "action": "auth",
            "key": "YOUR_ALPACA_API_KEY",
            "secret": "YOUR_ALPACA_API_SECRET"
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
    agent = MarketDataAgent("YOUR_ALPACA_API_KEY", "YOUR_ALPACA_API_SECRET", "https://paper-api.alpaca.markets", "AAPL")
    agent.start_stream()
