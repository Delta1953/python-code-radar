"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : binance_client.py
Autor    : Roberto Günther
Versión  : 0.3
=========================================================

OBJETIVO
--------
Centralizar toda la comunicación con Binance utilizando
la biblioteca CCXT.

RESPONSABILIDADES
-----------------
- Conectarse al exchange.
- Obtener precios.
- Obtener información de mercados.
- Obtener tickers.
- Aislar el resto de la aplicación de la API del exchange.

=========================================================
"""
import ccxt

class BinanceClient:
    def __init__(self):
        self.exchange = ccxt.binance()

    def get_ticker(self, symbol: str):
        return self.exchange.fetch_ticker(symbol)
    
    def get_tickers(self):
        return self.exchange.fetch_tickers()
    
    def get_ohlcv(self, symbol: str, timeframe: str='1m', limit: int = 100,):
        return self.exchange.fetch_ohlcv(
            symbol=symbol, 
            timeframe=timeframe, 
            limit=limit)
    
    def get_ohlcv(self, symbol, timeframe="5m", limit=10):
        return self.exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )