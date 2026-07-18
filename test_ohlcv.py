"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_ohlcv.py
Autor    : Roberto Günther
Versión  : 0.3
=========================================================

OBJETIVO
--------
Verificar que BinanceClient pueda obtener múltiples velas
OHLCV desde Binance.

Cada vela contiene:
- timestamp
- apertura
- máximo
- mínimo
- cierre
- volumen
=========================================================
"""
from datetime import datetime
from exchange.binance_client import BinanceClient

def main() -> None:
    client = BinanceClient()
    symbol = 'BTC/USDT'
    timeframe = '5m'
    limit = 10
    candles = client.get_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    ##
    # O = Open
    # H   High
    # L   Low
    # C   Close
    # V   Volume
    ##

    print()
    print("================================================")
    print(f"OHLCV - {symbol} - Marco Temporal: {timeframe}")
    print("================================================")   
    print(f"{'Fecha y hora':<20}"
          f"{'Apertura':>14}"
          f"{'Máximo':>14}"
          f"{'Mínimo':>14}"
          f"{'Cierre':>14}"
          f"{'Volumen':>16}"
                 )
    print("-" * 92)
    print(f"Cantidad de velas recibidas: {len(candles)}")

    for candle in candles:
            timestamp, open_price, high, low, close, volume = candle

            date_time = datetime.fromtimestamp(timestamp / 1000)

            print(
                f"{date_time:%Y-%m-%d %H:%M:%S} | "
                f"Apertura: {open_price} | "
                f"Máximo: {high} | "
                f"Mínimo: {low} | "
                f"Cierre: {close} | "
                f"Volumen: {volume}"
            )

        
if __name__ == "__main__":
    main()