"""
Prueba del indicador ADX.
"""

from exchange.binance_client import BinanceClient
from indicators.adx import ADXIndicator
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


def main():

    client = BinanceClient()

    candles = client.get_ohlcv(
        symbol="BTC/USDT",
        timeframe=DEFAULT_TIMEFRAME,
        limit=DEFAULT_CANDLE_LIMIT,
    )

    adx = ADXIndicator.get_last(
        candles=candles,
        period=14,
    )

    assert 0 <= adx <= 100

    print("\nPRUEBA ADX")
    print("-" * 40)
    print(f"Símbolo : BTC/USDT")
    print(f"Timeframe : 15m")
    print(f"Velas : {len(candles)}")
    print(f"ADX : {adx:.2f}")

    if adx < 20:
        print("Estado : SIN TENDENCIA")

    elif adx < 25:
        print("Estado : TENDENCIA NACIENTE")

    elif adx < 40:
        print("Estado : TENDENCIA FUERTE")

    else:
        print("Estado : TENDENCIA MUY FUERTE")


if __name__ == "__main__":
    main()