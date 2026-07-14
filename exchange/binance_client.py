import ccxt

class BinanceClient:
    def __init__(self):
        self.exchange = ccxt.binance()

    def get_ticker(self, symbol):
        return self.exchange.fetch_ticker(symbol)